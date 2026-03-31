# Instagram DM Bot

## Overview
An Instagram DM bot that auto-replies to messages and sends scheduled broadcasts using a session-based login. Uses the DeepSeek AI API to generate contextual replies as the "Tsukuyoma" persona (a Japanese moon god).

## Tech Stack
- **Language:** Python 3.12
- **Key Libraries:**
  - `instagrapi` - Unofficial Instagram private API client
  - `schedule` - Periodic task scheduling
  - `requests` - HTTP calls to DeepSeek API

## Project Structure
- `insta.py` - Main bot script (login, DM scanning, AI replies, scheduled broadcasts)
- `ig_session.json` - Instagram session/auth data (used instead of password login)
- `seen_dms.json` - Tracks processed message IDs to avoid duplicate replies (auto-created)
- `requirements.txt` - Python dependencies

## Running
The bot runs as a persistent background process:
```
python insta.py
```

## Configuration
Key settings in `insta.py`:
- `DEEPSEEK_API_KEY` - DeepSeek API key for AI responses
- `CHECK_EVERY` - How often to scan for new DMs (default: 20 seconds)
- `SCHEDULED_TIMES` - Times to send broadcast messages (default: 11:00, 17:00, 21:00)
- `MY_PERSONA` - The AI persona/system prompt

## Session Management
- Authentication uses `ig_session.json` (session-based, no password required)
- If the session expires, the bot stops automatically to avoid Instagram bans
- To refresh: generate a new session file using instagrapi's login flow

## Notes
- The bot uses threading: one thread for scheduled broadcasts, main thread for DM scanning
- Spam filtering skips messages containing keywords like "f4f", "promote", etc.
- Random delays between actions to mimic human behavior and avoid rate limits
