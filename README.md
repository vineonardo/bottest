
# 🛰️ Luna Monitor

**Luna Monitor** is a stealth-mode analytics bot framework for Telegram and Discord. It ingests group/channel messages, scores them using custom signal logic, and logs high-signal content for downstream processing or summary dispatch.

---

## 🚀 Features

- Telegram + Discord bot observers (passive/stealth mode by default)
- Keyword and emoji scoring using `signal_score.py`
- Rotating Bloom filter to prevent duplicate ingestion
- FastAPI service with webhook endpoint
- SQLite logging for all ingested messages
- Deploy-ready in GitHub Codespaces or Docker

---

## ⚙️ Setup Guide

One command autonomous run
```bash
python init_launchpad.py
```

###  Create a `.env` File if needed

```env
TELEGRAM_TOKEN=your_telegram_token
DISCORD_TOKEN=your_discord_token
WEBHOOK_URL=http://localhost:8000/webhook
```

---

## 🧪 Run and Test

### 🟢 Start the App

```bash
python init_launchpad.py
```

This will:
- Launch the FastAPI service on port 8000
- Start Telegram and Discord observers
- Enable webhook summary dispatch

### 🔍 Test API

- `GET /ping` → `{ "status": "pong" }`
- `GET /status` → `{ "service": "running" }`
- `POST /webhook` → Accepts summary JSON payloads

### 🧾 Check Logs

```bash
sqlite3 log_matrix.db
SELECT * FROM logs ORDER BY id DESC LIMIT 5;
```

---

## 📡 Add Bots to Telegram and Discord

### 🤖 Telegram Bot

1. Go to [@BotFather](https://t.me/BotFather)
2. Create your bot: `/newbot`
3. Copy the token into `.env`
4. Add the bot to a **public group**
5. (Optional) Disable Privacy Mode:
   - `/mybots` → Bot → Group Privacy → **Turn off**

### 💬 Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers)
2. Select your app → OAuth2 → URL Generator
3. Scopes: `bot`
4. Permissions:
   - `Read Messages/View Channels`
   - `Send Messages`
   - `Read Message History`
   - `Message Content`
5. Copy the generated URL and open it in browser to invite bot to server

---

## 🔎 Scoring and Filtering (`signal_score.py`)

The message scoring system works by evaluating content against **weighted keywords, emojis, and phrases**:

```python
SCORING_RULES = {
    "words": { "alpha": 1, "drop": 1, ... },
    "emojis": { "🚀": 1.5, "🔥": 1.2, ... },
    "phrases": { "airdrop incoming": 2, ... }
}
```

The score is normalized (0 to 1). 
---

## 🧼 Duplicate Filtering

To prevent re-ingesting the same messages:
- Each observer uses a **rotating Bloom filter**
- It resets every 5 minutes
- If a message ID is already seen, it is skipped

---

## 📦 Deployment (Codespaces Ready)

This project includes:
- `.devcontainer/devcontainer.json`
- `.devcontainer/Dockerfile`

Open it in GitHub Codespaces and it auto-runs:
- Environment setup
- Server launch
- Observer startup

---# bottest
