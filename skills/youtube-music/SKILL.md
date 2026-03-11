---
name: youtube-music
description: Experimental helper that downloads audio from YouTube or YouTube Music URLs, or from simple YouTube search queries, into stable local files. Use when the user wants a personal-use, best-effort way to turn a YouTube or YouTube Music source into a local audio file, optionally to play it on Clawatch.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎧",
        "requires": { "bins": ["python3", "ffmpeg"] },
      },
  }
---

# YouTube Music To Audio

Use this skill for experimental, personal-use downloading of audio from YouTube or YouTube Music into stable local files.

This skill is intentionally best-effort. It depends on community tooling and may break when upstream sites change.

## Quick start

```bash
python3 {baseDir}/scripts/fetch.py --url "https://www.youtube.com/watch?v=BaW_jenozKc"
python3 {baseDir}/scripts/fetch.py --query "lofi study beats"
```

## When to use

- The user wants a YouTube or YouTube Music URL turned into a local audio file.
- The user wants a simple search query resolved to one downloadable result.
- The user wants the resulting audio later played on Clawatch.

## Inputs

Use exactly one of:

- `--url <youtube-or-ytmusic-url>`
- `--query <search text>`

Useful flags:

- `--format mp3|m4a` default `mp3`
- `--out-dir /path/to/output`
- `--max-results 1..5` for search mode

## Run

```bash
# Direct URL
python3 {baseDir}/scripts/fetch.py --url "https://music.youtube.com/watch?v=..."

# Search and download first result
python3 {baseDir}/scripts/fetch.py --query "city pop mix"

# Keep m4a instead of mp3
python3 {baseDir}/scripts/fetch.py --query "jazz piano" --format m4a
```

## Output

The script writes:

- a stable audio file such as `01.mp3`
- `manifest.json`
- `out_dir=...` on stdout
- one saved file path per line

## Delivery behavior

- In a `clawatch` conversation, do not ask whether to send the file or play it. After download completes, call `clawatch_play_audio` immediately with the saved `filePath`. Do not pass a different watch IMEI in the same clawatch session; use the current watch only.
- In a Telegram conversation, prefer sending the downloaded file back as media instead of asking follow-up questions.
- Outside those channels, return the saved local file path unless the user explicitly asks for Clawatch playback.

## Notes

- This is experimental and best-effort.
- It relies on `yt-dlp` plus `ffmpeg` locally.
- Prefer explicit URLs when possible; search results are less deterministic.
- Do not describe this as an official streaming integration.
