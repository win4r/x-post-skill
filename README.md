# Claude X Post Skill

A Claude Code skill for posting to X (Twitter) directly from your Claude Code session. Just ask Claude naturally.

## What You Can Do

```
"Post this to X: Just shipped a new feature!"

"Tweet: Working on something cool with Claude Code"

"Take a screenshot of this terminal and tweet it"

"Start a thread called 'launch-day' with: We're launching today!"

"Continue my launch-day thread with: The response has been incredible..."
```

That's it. Claude handles the rest.

## Features

- **Natural posting** - Just say "post to X" or "tweet this"
- **Threads** - Start and continue threads by name
- **Media** - Attach images, GIFs, videos
- **Screenshots** - Capture your terminal and tweet it
- **History** - Claude remembers your threads

## Installation

### 1. Create the skills directory (if it doesn't exist)

```bash
mkdir -p ~/.claude/skills
```

### 2. Clone this repository

```bash
cd ~/.claude/skills
git clone https://github.com/pravj/claude-x-post-skill.git x-post
```

### 3. Install dependencies

```bash
cd ~/.claude/skills/x-post
pip install -r requirements.txt
```

### 4. Configure X API credentials

```bash
cp .env.example .env
```

Edit `.env` with your X API credentials:
```
X_API_KEY=your_api_key
X_API_KEY_SECRET=your_api_key_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### 5. Restart Claude Code

The skill will be automatically detected on the next conversation.

## Verify Installation

Your directory structure should look like:

```
~/.claude/
└── skills/
    └── x-post/
        ├── SKILL.md          # Required - skill definition
        ├── x-post.py         # Main script
        ├── requirements.txt
        ├── .env              # Your credentials (you create this)
        └── .env.example
```

## Example Conversations

**Simple tweet:**
> You: "Post to X: Building in public with Claude Code"
> Claude: Done! https://x.com/i/status/123...

**Starting a thread:**
> You: "Start a thread called 'launch-day' with: We're launching today!"
> Claude: Thread started! I'll remember 'launch-day' so you can continue it later.

**Continuing later:**
> You: "Add to my launch-day thread: The response has been incredible..."
> Claude: Added to thread! https://x.com/i/status/456...

**With screenshot:**
> You: "Screenshot this and tweet: Check out what Claude just built"
> Claude: *captures terminal* Posted! https://x.com/i/status/789...

## CLI Reference

For direct usage or scripting:

```bash
# Tweets
python x-post.py tweet "text"
python x-post.py media /path/to/file "text"

# Threads
python x-post.py thread thread.json --name "thread-name"
python x-post.py continue "thread-name" "text"
python x-post.py continue-media "thread-name" /path/to/file "text"

# Replies
python x-post.py reply <tweet_id> "text"
python x-post.py reply-media <tweet_id> /path/to/file "text"

# Screenshots
python x-post.py snap "caption"

# History
python x-post.py history
python x-post.py threads
```

## License

MIT

## Author

Pravendra Singh
