# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code skill for posting to X (Twitter). It's designed to be installed in `~/.claude/skills/x-post/` and enables natural language posting to X directly from Claude Code sessions.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Post a tweet
python x-post.py tweet "Your text"

# Post with media
python x-post.py media /path/to/image.jpg "Your text"

# Post a thread from JSON file
python x-post.py thread /path/to/thread.json --name "thread-name"

# Continue a named thread
python x-post.py continue "thread-name" "Next tweet"
python x-post.py continue-media "thread-name" /path/to/image.jpg "Next tweet"

# Reply to a tweet
python x-post.py reply <tweet_id> "Reply text"
python x-post.py reply-media <tweet_id> /path/to/image.jpg "Reply text"

# Screenshot and tweet (macOS only)
python x-post.py snap "caption"

# View history
python x-post.py history
python x-post.py threads
```

## Architecture

**Single-file CLI** (`x-post.py`): Python script using `tweepy` for X API interaction.

**Key patterns:**
- All commands run via `python x-post.py <command> [args]`
- Thread tracking via `--name "name"` flag stores latest tweet ID in `post-history.json`
- Screenshots use macOS `screencapture -wo` (window capture mode)
- Optional `silicon` CLI for code rendering (Dracula theme, shadows)

**Data files (generated at runtime):**
- `post-history.json` - Tweet history and thread tracking
- `screenshots/` - Temporary screenshot/render storage

## Configuration

Requires `.env` file with X API credentials:
```
X_API_KEY=
X_API_KEY_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
```

## Skill Integration

`SKILL.md` defines how Claude Code invokes this skill. Commands should always be run from the skill directory (`cd ~/.claude/skills/x-post && python x-post.py ...`).
