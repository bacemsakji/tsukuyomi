# Tsukuyomi - AI-Powered Instagram DM Bot

An intelligent Instagram Direct Message bot that leverages Large Language Models to deliver adaptive, context-aware responses with a unique personality. The bot features scheduled messaging, spam filtering, and session-based authentication.

## 🚀 Features

- **AI-Powered Responses**: Uses OpenRouter API with DeepSeek model for intelligent, context-aware replies
- **Adaptive Personality**: Dynamically adjusts tone based on conversation context (sarcastic, flirty, warm, or helpful)
- **Scheduled Messaging**: Automatically sends mysterious messages at configurable times
- **Spam Filtering**: Automatically filters out promotional and spam messages
- **Session-Based Auth**: Secure authentication using Instagram session files (no password storage)
- **Conversation Memory**: Maintains conversation history for contextual responses
- **Rate Limiting**: Built-in retry logic with exponential backoff for API rate limits
- **Multi-threading**: Concurrent message processing and scheduled task execution
- **Health Check Endpoint**: Flask web server for deployment monitoring

## 🛠 Tech Stack

- **Python 3.12+**
- **instagrapi**: Instagram API client
- **OpenRouter API**: LLM integration (DeepSeek model)
- **Flask**: Web server for health checks
- **schedule**: Task scheduling
- **python-dotenv**: Environment variable management
- **threading**: Concurrent execution

## 📋 Architecture

### Core Components

1. **Session Management**: Loads and validates Instagram session from `ig_session.json`
2. **Message Scanner**: Continuously polls for new DMs every 20 seconds
3. **LLM Integration**: Generates responses using OpenRouter API with retry logic
4. **Scheduler**: Manages scheduled broadcasts at specific times
5. **Spam Filter**: Identifies and ignores promotional messages
6. **Conversation Memory**: Tracks seen messages to prevent duplicate responses

### Design Decisions

- **Session-based auth**: Avoids storing credentials, uses Instagram session files for security
- **Thread-safe operations**: Uses locks to prevent race conditions in API calls
- **Graceful degradation**: Continues operation even if individual API calls fail
- **Rate limit handling**: Implements exponential backoff for API rate limits
- **Message deduplication**: Tracks seen messages in JSON file for persistence

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- Instagram session file (`ig_session.json`)
- OpenRouter API key

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd tsukuyomi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

4. Add your Instagram session file:
- Place `ig_session.json` in the project root
- This file should contain your Instagram session data

## 🎯 Usage

Run the bot:
```bash
python insta.py
```

The bot will:
- Start a Flask web server on port 10000 for health checks
- Begin scanning for new DMs every 20 seconds
- Send scheduled messages at configured times (default: 11:00, 17:00, 21:00)
- Respond to messages with AI-generated replies

### Configuration

Key configuration options in `insta.py`:

- `CHECK_EVERY`: Scan interval in seconds (default: 20)
- `MAX_REPLY_LEN`: Maximum response length (default: 150)
- `SCHEDULED_TIMES`: List of times for scheduled messages
- `MAX_HISTORY`: Number of messages to keep in context (default: 30)
- `MY_PERSONA`: Bot personality and behavior rules

## 🔒 Security

- Session files are gitignored to prevent credential exposure
- Environment variables for API keys
- No password storage - uses Instagram session files only
- Input validation to prevent prompt injection attacks

## 🧪 Testing

The bot includes error handling and logging for:
- API rate limits
- Session expiration
- Network failures
- Invalid responses

## 🚀 Deployment

The bot is designed for deployment on platforms like:
- Replit
- Railway
- Render
- Any VPS with Python support

Ensure the following environment variables are set:
- `OPENROUTER_API_KEY`

The Flask health check endpoint responds at `/` with "Bot alive ✅"

## 📈 Future Improvements

- [ ] Add unit tests
- [ ] Implement database for conversation history
- [ ] Add web dashboard for monitoring
- [ ] Support for multiple Instagram accounts
- [ ] Custom personality templates
- [ ] Analytics dashboard
- [ ] Docker containerization

## 📝 License

This project is for educational and personal use.

## 👤 Author

Built with Python, Instagram API, and AI.

---

**Note**: This bot is intended for personal use and educational purposes. Always comply with Instagram's Terms of Service and API usage guidelines.
