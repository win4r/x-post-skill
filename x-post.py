#!/usr/bin/env python3
"""X (Twitter) Post CLI - Post to X directly from Claude Code."""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SCRIPT_DIR = Path(__file__).parent.resolve()
HISTORY_FILE = SCRIPT_DIR / "post-history.json"
SCREENSHOTS_DIR = SCRIPT_DIR / "screenshots"


def load_history():
    """Load or initialize history."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tweets": [], "threads": {}}


def save_history(history):
    """Save history to file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def record_tweet(tweet_id, text, thread_name=None, parent_id=None):
    """Record a tweet to history."""
    history = load_history()
    entry = {
        "id": tweet_id,
        "text": text[:100] + ("..." if len(text) > 100 else ""),
        "timestamp": datetime.now().isoformat(),
        "threadName": thread_name,
        "parentId": parent_id,
    }
    history["tweets"].insert(0, entry)  # Most recent first
    history["tweets"] = history["tweets"][:100]  # Keep last 100

    # Track thread's latest tweet for easy continuation
    if thread_name:
        first_tweet_id = history["threads"].get(thread_name, {}).get("firstTweetId", tweet_id)
        history["threads"][thread_name] = {
            "latestTweetId": tweet_id,
            "firstTweetId": first_tweet_id,
            "updatedAt": datetime.now().isoformat(),
        }

    save_history(history)


def get_client():
    """Create and return Twitter API client."""
    client = tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_KEY_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
    )
    return client


def get_api_v1():
    """Create and return Twitter API v1.1 client for media upload."""
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY"),
        os.getenv("X_API_KEY_SECRET"),
        os.getenv("X_ACCESS_TOKEN"),
        os.getenv("X_ACCESS_TOKEN_SECRET"),
    )
    return tweepy.API(auth)


def post_tweet(text, thread_name=None):
    """Post a text tweet."""
    try:
        client = get_client()
        response = client.create_tweet(text=text)
        tweet_id = response.data["id"]
        print("Tweet posted successfully!")
        print(f"Tweet ID: {tweet_id}")
        print(f"URL: https://x.com/i/status/{tweet_id}")
        record_tweet(tweet_id, text, thread_name)
        return response
    except Exception as error:
        print(f"Error posting tweet: {error}", file=sys.stderr)
        sys.exit(1)


def post_with_media(text, media_path, thread_name=None):
    """Post a tweet with media."""
    try:
        client = get_client()
        api_v1 = get_api_v1()

        absolute_path = Path(media_path).resolve()
        media = api_v1.media_upload(str(absolute_path))

        response = client.create_tweet(text=text, media_ids=[media.media_id])
        tweet_id = response.data["id"]
        print("Tweet with media posted successfully!")
        print(f"Tweet ID: {tweet_id}")
        print(f"URL: https://x.com/i/status/{tweet_id}")
        record_tweet(tweet_id, text, thread_name)
        return response
    except Exception as error:
        print(f"Error posting tweet with media: {error}", file=sys.stderr)
        sys.exit(1)


def reply_to_tweet(reply_to_id, text, thread_name=None):
    """Reply to a tweet."""
    try:
        client = get_client()
        response = client.create_tweet(text=text, in_reply_to_tweet_id=reply_to_id)
        tweet_id = response.data["id"]
        print("Reply posted successfully!")
        print(f"Tweet ID: {tweet_id}")
        print(f"URL: https://x.com/i/status/{tweet_id}")
        record_tweet(tweet_id, text, thread_name, reply_to_id)
        return response
    except Exception as error:
        print(f"Error posting reply: {error}", file=sys.stderr)
        sys.exit(1)


def reply_with_media(reply_to_id, text, media_path, thread_name=None):
    """Reply to a tweet with media."""
    try:
        client = get_client()
        api_v1 = get_api_v1()

        absolute_path = Path(media_path).resolve()
        media = api_v1.media_upload(str(absolute_path))

        response = client.create_tweet(
            text=text,
            media_ids=[media.media_id],
            in_reply_to_tweet_id=reply_to_id,
        )
        tweet_id = response.data["id"]
        print("Reply with media posted successfully!")
        print(f"Tweet ID: {tweet_id}")
        print(f"URL: https://x.com/i/status/{tweet_id}")
        record_tweet(tweet_id, text, thread_name, reply_to_id)
        return response
    except Exception as error:
        print(f"Error posting reply with media: {error}", file=sys.stderr)
        sys.exit(1)


def post_thread(tweets, thread_name=None):
    """Post a thread (multiple tweets)."""
    try:
        client = get_client()
        previous_tweet_id = None
        posted_tweets = []

        for i, tweet_text in enumerate(tweets):
            if previous_tweet_id:
                response = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_tweet_id)
            else:
                response = client.create_tweet(text=tweet_text)

            tweet_id = response.data["id"]
            previous_tweet_id = tweet_id
            posted_tweets.append({"id": tweet_id})
            print(f"Tweet {i + 1}/{len(tweets)} posted: https://x.com/i/status/{tweet_id}")

            parent_id = posted_tweets[i - 1]["id"] if i > 0 else None
            record_tweet(tweet_id, tweet_text, thread_name, parent_id)

        print(f"\nThread posted successfully! {len(tweets)} tweets.")
        print(f"Thread URL: https://x.com/i/status/{posted_tweets[0]['id']}")
        if thread_name:
            print(f'Thread saved as: "{thread_name}" - use this name to continue the thread later')
        return posted_tweets
    except Exception as error:
        print(f"Error posting thread: {error}", file=sys.stderr)
        sys.exit(1)


def show_history(count=10):
    """Show recent tweet history."""
    history = load_history()
    print(f"\nRecent tweets (last {count}):\n")
    for i, t in enumerate(history["tweets"][:count]):
        thread_info = f" [{t['threadName']}]" if t.get("threadName") else ""
        print(f"{i + 1}. {t['id']}{thread_info}")
        print(f'   "{t["text"]}"')
        print(f"   {t['timestamp']}\n")


def show_threads():
    """Show saved threads."""
    history = load_history()
    threads = history.get("threads", {})
    if not threads:
        print('\nNo named threads yet. Use --name "thread-name" when posting to track threads.\n')
        return
    print("\nSaved threads:\n")
    for name, data in threads.items():
        print(f'  "{name}"')
        print(f"    Latest tweet ID: {data['latestTweetId']}")
        print(f"    Thread URL: https://x.com/i/status/{data['firstTweetId']}")
        print(f"    Updated: {data['updatedAt']}\n")


def get_thread_latest_id(thread_name):
    """Get the latest tweet ID from a named thread."""
    history = load_history()
    thread = history.get("threads", {}).get(thread_name)
    if not thread:
        print(f'Thread "{thread_name}" not found. Use \'threads\' command to see available threads.', file=sys.stderr)
        sys.exit(1)
    return thread["latestTweetId"]


def ensure_screenshots_dir():
    """Ensure screenshots directory exists."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def capture_window():
    """Capture a window screenshot (macOS only)."""
    ensure_screenshots_dir()
    filename = f"screenshot-{int(datetime.now().timestamp() * 1000)}.png"
    filepath = SCREENSHOTS_DIR / filename

    print("Click on the window you want to capture...")
    try:
        subprocess.run(["screencapture", "-wo", str(filepath)], check=True)
    except subprocess.CalledProcessError:
        return None

    if filepath.exists():
        print(f"Screenshot saved: {filepath}")
        return str(filepath)
    return None


def render_with_silicon(input_file, output_file=None):
    """Render a file with silicon for aesthetic code screenshots."""
    ensure_screenshots_dir()
    output = output_file or str(SCREENSHOTS_DIR / f"render-{int(datetime.now().timestamp() * 1000)}.png")

    try:
        subprocess.run([
            "silicon", str(input_file), "-o", output,
            "--theme", "Dracula",
            "--shadow-color", "#555555",
            "--shadow-blur-radius", "30",
            "--pad-horiz", "40",
            "--pad-vert", "40",
            "--background", "#00000000",
        ], check=True)
        print(f"Rendered: {output}")
        return output
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"Silicon render failed: {error}", file=sys.stderr)
        return None


def render_text_with_silicon(text):
    """Render inline text with silicon."""
    ensure_screenshots_dir()
    temp_file = SCREENSHOTS_DIR / f"temp-{int(datetime.now().timestamp() * 1000)}.txt"
    output_file = str(SCREENSHOTS_DIR / f"render-{int(datetime.now().timestamp() * 1000)}.png")

    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(text)

    try:
        subprocess.run([
            "silicon", str(temp_file), "-o", output_file,
            "--theme", "Dracula",
            "--shadow-color", "#555555",
            "--shadow-blur-radius", "30",
            "--pad-horiz", "40",
            "--pad-vert", "40",
            "--no-window-controls",
        ], check=True)
        temp_file.unlink()  # Clean up temp file
        print(f"Rendered: {output_file}")
        return output_file
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"Silicon render failed: {error}", file=sys.stderr)
        temp_file.unlink()
        return None


def parse_args(args):
    """Parse --name flag from args."""
    thread_name = None
    clean_args = list(args)

    if "--name" in clean_args:
        name_index = clean_args.index("--name")
        if name_index + 1 < len(clean_args):
            thread_name = clean_args[name_index + 1]
            del clean_args[name_index:name_index + 2]

    return thread_name, clean_args


def print_usage():
    """Print usage information."""
    print("""
X Post CLI - Post to X (Twitter)

Usage:
  python x-post.py tweet "Your tweet text" [--name "thread-name"]
  python x-post.py media /path/to/image.jpg "Your tweet text" [--name "thread-name"]
  python x-post.py thread /path/to/thread.json [--name "thread-name"]
  python x-post.py reply <tweet_id> "Your reply text" [--name "thread-name"]
  python x-post.py reply-media <tweet_id> /path/to/image.jpg "Your reply text"

Continue a named thread:
  python x-post.py continue "thread-name" "Your reply text"
  python x-post.py continue-media "thread-name" /path/to/image.jpg "Your reply text"

Screenshot & Render:
  python x-post.py snap "caption"                    Capture window + tweet
  python x-post.py render file.js "caption"          Render code file (aesthetic) + tweet
  python x-post.py render-text "code here" "caption" Render inline text + tweet

View history:
  python x-post.py history [count]
  python x-post.py threads

Thread file format (JSON array):
  ["First tweet", "Second tweet", "Third tweet"]

The --name flag saves tweets to a named thread for easy continuation later.
""")


def main():
    """Main entry point."""
    args = sys.argv[1:]

    if not args:
        print_usage()
        return

    command = args[0]
    thread_name, rest_args = parse_args(args[1:])

    if command == "tweet":
        text = " ".join(rest_args)
        if not text:
            print('Usage: python x-post.py tweet "Your tweet text" [--name "thread-name"]', file=sys.stderr)
            sys.exit(1)
        post_tweet(text, thread_name)

    elif command == "media":
        if len(rest_args) < 2:
            print('Usage: python x-post.py media /path/to/image.jpg "Your tweet text" [--name "thread-name"]', file=sys.stderr)
            sys.exit(1)
        media_path = rest_args[0]
        text = " ".join(rest_args[1:])
        post_with_media(text, media_path, thread_name)

    elif command == "thread":
        if not rest_args:
            print('Usage: python x-post.py thread /path/to/thread.json [--name "thread-name"]', file=sys.stderr)
            print('Thread file should be a JSON array of strings: ["Tweet 1", "Tweet 2", ...]', file=sys.stderr)
            sys.exit(1)
        input_file = Path(rest_args[0]).resolve()
        with open(input_file, "r", encoding="utf-8") as f:
            tweets = json.load(f)
        post_thread(tweets, thread_name)

    elif command == "reply":
        if len(rest_args) < 2:
            print('Usage: python x-post.py reply <tweet_id> "Your reply text" [--name "thread-name"]', file=sys.stderr)
            sys.exit(1)
        reply_to_id = rest_args[0]
        text = " ".join(rest_args[1:])
        reply_to_tweet(reply_to_id, text, thread_name)

    elif command == "reply-media":
        if len(rest_args) < 3:
            print('Usage: python x-post.py reply-media <tweet_id> /path/to/image.jpg "Your reply text" [--name "thread-name"]', file=sys.stderr)
            sys.exit(1)
        reply_to_id = rest_args[0]
        media_path = rest_args[1]
        text = " ".join(rest_args[2:])
        reply_with_media(reply_to_id, text, media_path, thread_name)

    elif command == "continue":
        if len(rest_args) < 2:
            print('Usage: python x-post.py continue "thread-name" "Your reply text"', file=sys.stderr)
            sys.exit(1)
        name = rest_args[0]
        text = " ".join(rest_args[1:])
        latest_id = get_thread_latest_id(name)
        reply_to_tweet(latest_id, text, name)

    elif command == "continue-media":
        if len(rest_args) < 3:
            print('Usage: python x-post.py continue-media "thread-name" /path/to/image.jpg "Your reply text"', file=sys.stderr)
            sys.exit(1)
        name = rest_args[0]
        media_path = rest_args[1]
        text = " ".join(rest_args[2:])
        latest_id = get_thread_latest_id(name)
        reply_with_media(latest_id, text, media_path, name)

    elif command == "history":
        count = int(rest_args[0]) if rest_args else 10
        show_history(count)

    elif command == "threads":
        show_threads()

    elif command == "snap":
        text = " ".join(rest_args) if rest_args else "Screenshot from terminal"
        screenshot = capture_window()
        if screenshot:
            post_with_media(text, screenshot, thread_name)
        else:
            print("Screenshot cancelled or failed.", file=sys.stderr)
            sys.exit(1)

    elif command == "render":
        if not rest_args:
            print('Usage: python x-post.py render <file> "Your caption"', file=sys.stderr)
            print('Example: python x-post.py render script.js "Check out this code!"', file=sys.stderr)
            sys.exit(1)
        input_file = Path(rest_args[0]).resolve()
        text = " ".join(rest_args[1:]) if len(rest_args) > 1 else "Code snippet"
        rendered = render_with_silicon(input_file)
        if rendered:
            post_with_media(text, rendered, thread_name)
        else:
            print("Render failed.", file=sys.stderr)
            sys.exit(1)

    elif command == "render-text":
        if not rest_args:
            print('Usage: python x-post.py render-text "code or text to render" "Your caption"', file=sys.stderr)
            sys.exit(1)
        text = rest_args[0]
        caption = " ".join(rest_args[1:]) if len(rest_args) > 1 else "From terminal"
        rendered = render_text_with_silicon(text)
        if rendered:
            post_with_media(caption, rendered, thread_name)
        else:
            print("Render failed.", file=sys.stderr)
            sys.exit(1)

    else:
        print_usage()


if __name__ == "__main__":
    main()
