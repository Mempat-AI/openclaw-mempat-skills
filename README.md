# Watchie OpenClaw Skills

**Language:** English | [中文](./README.zh-CN.md) | [Bahasa Melayu](./README.ms.md)

Reusable OpenClaw skills for Watchie workflows.

## Included skills

- `gen-music`: generate songs through an ACE-Step-compatible API backend, save stable output files, and optionally play results on Watchie.
- `youtube-music`: experimental personal-use helper that downloads YouTube or YouTube Music audio into stable local files, with optional Watchie playback.
- `story-teller`: writing-focused storytelling skill for vivid, voice-friendly stories.

## Quick start

### 1. Install skills

Copy the skills you want into your OpenClaw skills directory:

```bash
git clone https://github.com/Mempat-AI/openclaw-watchie-skills.git
mkdir -p ~/.openclaw/skills

# Install all three:
cp -R openclaw-watchie-skills/skills/story-teller ~/.openclaw/skills/
cp -R openclaw-watchie-skills/skills/gen-music ~/.openclaw/skills/
cp -R openclaw-watchie-skills/skills/youtube-music ~/.openclaw/skills/
```

Or pick only what you need — each skill is independent.

### 2. Assign skills to your Watchie agent

After installing the skill files, tell OpenClaw which skills the Watchie agent should use.

First, find the Watchie agent's position in your agent list:

```bash
openclaw config get agents.list
```

Look for the entry with `"id": "watchie"` and note its index (0-based). Then assign skills:

```bash
# If watchie is at index 1 (the second agent):
openclaw config set 'agents.list[1].skills' '["story-teller", "gen-music", "youtube-music"]'
```

You can assign any subset:

```bash
# Story-teller only:
openclaw config set 'agents.list[1].skills' '["story-teller"]'

# Story-teller + gen-music:
openclaw config set 'agents.list[1].skills' '["story-teller", "gen-music"]'
```

### 3. Restart the gateway

```bash
openclaw gateway restart
```

### 4. Verify

```bash
# Check skills are detected:
openclaw skills list

# Check skills are assigned to watchie:
openclaw config get 'agents.list[1].skills'
```

Skills show as "ready" when the skill files are installed and all requirements are met.

## Removing a skill

Remove the skill from the agent config and delete the files:

```bash
# Update the skills list (omit the skill you want to remove):
openclaw config set 'agents.list[1].skills' '["gen-music", "youtube-music"]'

# Optionally delete the skill files:
rm -rf ~/.openclaw/skills/story-teller

openclaw gateway restart
```

## Watchie setup (if not already done)

1. Install the Watchie plugin: `openclaw plugins install @mempat-ai/watchie`
2. Sign in and pair:
   ```bash
   openclaw watchie login <countryCode> <phoneNumber>
   openclaw watchie pair <imei>
   openclaw watchie bind
   ```
3. Install and assign skills (steps above).

## Example requests

- `Tell me a bedtime story about a brave rabbit.`
- `Generate a playful one-minute beach pop song and save the audio.`
- `Generate a happy song and play it on my watch.`
- `Download this YouTube Music link as mp3.`
- `Find this song on YouTube Music, save it locally, then play it on my watch.`

## Requirements

- Python 3
- `ffmpeg` and `yt-dlp` for `youtube-music`
- An ACE-Step-compatible backend for `gen-music`
- Watchie plugin for watch playback

## Notes

- `gen-music` does not bundle ACE-Step model weights or service binaries.
- You can use either a local ACE-Step server or a remote compatible endpoint.
- Skills are opt-in. Install only what you need.
- Each skill works independently — no cross-dependencies.
