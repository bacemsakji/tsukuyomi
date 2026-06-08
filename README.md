# Tsukuyomi - Instagram DM Bot

An intelligent, automated conversational agent designed to manage, process, and respond to Instagram Direct Messages (DMs) in real-time using AI-powered personalization.

## Overview

Tsukuyomi is an Instagram DM bot that:
- **Auto-replies** to incoming messages with AI-generated contextual responses
- **Schedules broadcasts** to send messages at specific times
- **Maintains conversation memory** with persistent session management
- **Adapts tone dynamically** based on user sentiment (friendly, rude, flirty, etc.)
- **Mimics human behavior** with random delays to avoid rate limits

## Tech Stack

- **Language:** Python 3.12
- **AI Model:** OpenRouter DeepSeek API
- **Key Libraries:**
  - `instagrapi` - Instagram private API client
  - `schedule` - Task scheduling
  - `requests` - HTTP requests
  - `flask` - Web health check endpoint
  - `python-dotenv` - Environment configuration

## Features

### Intelligent Responses
- Persona-based AI replies (Tsukuyoma - Japanese moon god)
- Multilingual support (English, French, Tunisian Arabic)
- Context-aware tone matching
- Short, engaging responses (1-3 sentences)

### Session Management
- Session-based authentication (no password stored)
- Automatic session expiry detection
- Track processed messages to avoid duplicate replies

### Scheduled Broadcasting
- Send broadcasts at configurable times (default: 11:00, 17:00, 21:00)
- Variable delays between messages for human-like behavior

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with:
```env
OPENROUTER_API_KEY=your_api_key_here
```

### Bot Settings (in `insta.py`)

| Setting | Default | Purpose |
|---------|---------|---------|
| `CHECK_EVERY` | 20s | DM scan interval |
| `MAX_REPLY_LEN` | 150 | Max response length |
| `SCHEDULED_TIMES` | 11:00, 17:00, 21:00 | Broadcast times |
| `SEND_DELAY_MIN/MAX` | 10-40s | Random delays between actions |

## Running the Bot

```bash
python insta.py
```

The bot will:
1. Load the Instagram session from `ig_session.json`
2. Start a Flask health check server on port 10000
3. Begin scanning for new DMs every 20 seconds
4. Reply using AI and send scheduled broadcasts

## Project Structure

```
tsukuyomi/
├── insta.py              # Main bot script
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Project metadata
├── .env.example         # Environment variables template
├── ig_session.json      # Instagram session data (auto-created)
└── seen_dms.json        # Processed message IDs (auto-created)
```

## Session Setup

To set up a new Instagram session:

```python
from instagrapi import Client

cl = Client()
cl.login("username", "password")
session = cl.get_settings()
# Save session to ig_session.json
```

**Note:** Session files should be kept private and not committed to version control.

## How It Works

### Message Processing Loop
1. Scan for new DMs every 20 seconds
2. Check against `seen_dms.json` to skip already-processed messages
3. Use OpenRouter API to generate personalized AI response
4. Send reply with human-like delays

### Persona System
The bot adapts its responses based on user tone:
- **Friendly/Kind** → Warm, charming, mysterious
- **Rude** → Sarcastic, sharp wit (calibrated intensity)
- **Flirty** → Engaging, playful banter
- **Question** → Helpful, factual answer

### Thread Management
- Main thread: DM scanning and replies
- Background thread: Scheduled broadcasts

## Anti-Rate Limiting

- Random delays between actions (10-40 seconds)
- Configurable scan intervals
- Respects Instagram rate limits
- Auto-stops on session expiry to prevent bans

## Important Notes

- **Security:** Never commit `ig_session.json` or `.env` to version control
- **TOS:** This tool is for educational purposes. Ensure compliance with Instagram's Terms of Service
- **API Keys:** Keep `OPENROUTER_API_KEY` private and secure
- **Session Expiry:** Bot automatically stops if session expires to prevent Instagram bans

## License

MIT

## Author

Created by [Bacem Sakji](https://www.instagram.com/tsukuy_01/)
