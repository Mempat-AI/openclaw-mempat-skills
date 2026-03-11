#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SKILL_NAME = "youtube-music"
DEFAULT_FORMAT = "mp3"


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def default_out_dir() -> Path:
    base = Path.home() / "Projects" / "tmp" / "youtube-music"
    return base / dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download YouTube or YouTube Music audio into a stable local file.")
    parser.add_argument("--url", default="", help="YouTube or YouTube Music URL.")
    parser.add_argument("--query", default="", help="Simple search query; downloads the first result by default.")
    parser.add_argument("--format", choices=["mp3", "m4a"], default=DEFAULT_FORMAT, help="Final audio format.")
    parser.add_argument("--out-dir", default="", help="Directory to store output files.")
    parser.add_argument("--max-results", type=int, default=1, help="Number of search results to resolve in query mode.")
    return parser.parse_args()


def resolve_source(args: argparse.Namespace) -> str:
    has_url = bool(args.url.strip())
    has_query = bool(args.query.strip())
    if has_url == has_query:
        raise RuntimeError("Provide exactly one of --url or --query.")
    if has_url:
        return args.url.strip()
    limit = max(1, min(int(args.max_results), 5))
    return f"ytsearch{limit}:{args.query.strip()}"


def ensure_runtime() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg is required but not found in PATH.")
    try:
        import yt_dlp  # noqa: F401
    except Exception as exc:
        raise RuntimeError("yt-dlp Python package is required. Install it with: python3 -m pip install --user yt-dlp") from exc


def detect_js_runtime() -> list[str]:
    for candidate in ("node", "deno", "bun"):
        path = shutil.which(candidate)
        if path:
            return ["--js-runtimes", f"{candidate}:{path}"]
    return []


def run_yt_dlp(source: str, out_dir: Path, audio_format: str) -> tuple[list[Path], list[dict[str, Any]]]:
    out_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(out_dir / "%(playlist_index|1)02d.%(ext)s")
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        *detect_js_runtime(),
        "--no-playlist",
        "--extract-audio",
        "--audio-format",
        audio_format,
        "--audio-quality",
        "0",
        "--output",
        output_template,
        "--print-json",
        source,
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip()
        raise RuntimeError(f"yt-dlp failed: {detail}")

    metadata: list[dict[str, Any]] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("{"):
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict):
                metadata.append(item)

    suffix = f".{audio_format}"
    saved = sorted(path for path in out_dir.glob(f"*{suffix}") if path.is_file())
    if not saved:
        saved = sorted(path for path in out_dir.iterdir() if path.is_file() and path.suffix in {".mp3", ".m4a", ".webm", ".opus"})
    if not saved:
        raise RuntimeError("Download completed but no audio file was saved.")
    normalized: list[Path] = []
    for index, path in enumerate(saved, start=1):
        destination = out_dir / f"{index:02d}{path.suffix.lower()}"
        if path != destination:
            if destination.exists():
                destination.unlink()
            path.rename(destination)
        normalized.append(destination)
    return normalized, metadata


def write_manifest(out_dir: Path, source: str, saved_files: list[Path], metadata: list[dict[str, Any]]) -> None:
    manifest = {
        "source": source,
        "saved_files": [str(path) for path in saved_files],
        "entries": [
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "uploader": item.get("uploader"),
                "webpage_url": item.get("webpage_url"),
                "duration": item.get("duration"),
            }
            for item in metadata
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    args = parse_args()
    ensure_runtime()
    source = resolve_source(args)
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir()
    saved_files, metadata = run_yt_dlp(source=source, out_dir=out_dir, audio_format=args.format)
    write_manifest(out_dir, source, saved_files, metadata)
    print(f"out_dir={out_dir}")
    for path in saved_files:
        print(path)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        eprint("Interrupted.")
        raise SystemExit(130)
    except Exception as exc:
        eprint(str(exc))
        raise SystemExit(1)
