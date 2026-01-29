---
name: x-post
description: Post to X (Twitter) - tweets, media, threads with history tracking. Use when the user wants to post, tweet, or share something on X/Twitter.
---

# X (Twitter) Posting Skill

Post content to X (formerly Twitter) including text tweets, media posts, and threads.

## Setup Check

If credentials are not configured, guide the user:
```bash
cd ~/.claude/skills/x-post && cp .env.example .env
# User must edit .env with their X API credentials
cd ~/.claude/skills/x-post && pip install -r requirements.txt
```

## Commands

All commands run from the skill directory.

### Post a text tweet
```bash
cd ~/.claude/skills/x-post && python x-post.py tweet "Your tweet text here"
```

### Post with media (image/video)
```bash
cd ~/.claude/skills/x-post && python x-post.py media /absolute/path/to/image.jpg "Your tweet text"
```

### Post a thread (multiple tweets)
Create a temp JSON file with array of tweets, then:
```bash
cd ~/.claude/skills/x-post && python x-post.py thread /path/to/thread.json --name "thread-name"
```

Thread JSON format: `["First tweet", "Second tweet", "Third tweet"]`

### Reply to a tweet by ID
```bash
cd ~/.claude/skills/x-post && python x-post.py reply <tweet_id> "Your reply"
cd ~/.claude/skills/x-post && python x-post.py reply-media <tweet_id> /path/to/image.jpg "Your reply"
```

### Reply with screenshot
  1. Capture: screencapture -w ~/.claude/skills/x-post/screenshots/temp.png
  2. Reply: python x-post.py reply-media <tweet_id> <screenshot> "caption"


### Continue a named thread
```bash
cd ~/.claude/skills/x-post && python x-post.py continue "thread-name" "Next tweet"
cd ~/.claude/skills/x-post && python x-post.py continue-media "thread-name" /path/to/image.jpg "Next tweet"
```

### Screenshot terminal and tweet
```bash
cd ~/.claude/skills/x-post && python x-post.py snap "Your caption"
```
User will be prompted to click the window to capture.

### View history
```bash
cd ~/.claude/skills/x-post && python x-post.py history
cd ~/.claude/skills/x-post && python x-post.py threads
```

## Guidelines

- **Character limit**: 280 chars (Premium users may have extended limits)
- **Media**: JPG, PNG, GIF, MP4 supported
- **Thread naming**: Use `--name "name"` to track threads for later continuation
- **Tweet IDs**: From `https://x.com/user/status/1234567890` the ID is `1234567890`

## When User Asks to Post

1. Help craft content within character limits
2. Run the appropriate command from the skill directory
3. Share the resulting tweet URL with them
4. If starting a thread they may want to continue later, use `--name` to track it
