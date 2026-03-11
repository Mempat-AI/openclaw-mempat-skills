# Mempat AI OpenClaw Skills

Reusable OpenClaw skills for Mempat AI workflows.

## Included skills

- `gen-music`: generate songs through an ACE-Step-compatible API backend, save stable output files, and optionally hand the result to Clawatch playback.
- `youtube-music`: experimental personal-use helper that downloads YouTube or YouTube Music audio into a stable local file, optionally to hand off to Clawatch playback.
- `story-teller`: writing-focused storytelling skill for vivid, catchy, voice-friendly stories with stronger hooks, sharper images, and less generic AI prose.

## Install

```bash
git clone https://github.com/Mempat-AI/openclaw-mempat-skills.git
mkdir -p ~/.openclaw/skills
cp -R openclaw-mempat-skills/skills/gen-music ~/.openclaw/skills/
cp -R openclaw-mempat-skills/skills/youtube-music ~/.openclaw/skills/
cp -R openclaw-mempat-skills/skills/story-teller ~/.openclaw/skills/
```

Restart OpenClaw Gateway or start a new session after copying the skill.

## Recommended Clawatch setup

1. Install the `@mempat-ai/clawatch` plugin.
2. Install `gen-music` if you want the text-to-music workflow.
3. Install `youtube-music` if you want an experimental YouTube/YouTube Music downloader.
4. Sign in and pair the watch:
   - `openclaw clawatch login <countryCode> <phoneNumber>`
   - `openclaw clawatch pair <imei>`
5. Point `gen-music` at an ACE-Step-compatible backend. This can be a local server on `http://127.0.0.1:8001` or a remote compatible endpoint.

## Example requests

- `Generate a playful one-minute beach pop song and save the audio.`
- `Generate a happy song about rising waves and play it on watch 860000019579324.`
- `Write a short summer pop song from these lyrics, then send it to my watch.`
- `Download this YouTube Music link as mp3.`
- `Find this song on YouTube Music, save it locally, then play it on my watch.`
- `Tell me a bedtime story about a brave rabbit that does not sound AI-generated.`
- `Write a funny, fast-moving story for a seven-year-old about a lost mooncake.`

## Requirements

- Python 3
- An ACE-Step-compatible API backend, local or remote
- `ffmpeg` plus local `yt-dlp` for `youtube-music`
- The Clawatch plugin if you want watch playback

## Backend choice

`gen-music` does not install or bundle ACE-Step. Users can connect it to:

- a local ACE-Step server they already run themselves, or
- a remote ACE-Step-compatible endpoint by setting `baseUrl`.

If you want community-hosted guidance for ACE-Step music generation, see the upstream OpenClaw community skills such as `ace-music`.
