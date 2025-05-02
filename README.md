# 🤖 Hamudnik Telegram Bot

Welcome to **Hamudnik Bot**, a fun and friendly Telegram bot built with `python-telegram-bot` that offers:

- Motivational quotes 💬  
- Current time ⏰  
- Latest movie releases 🍿  
- Chat powered by LLaMA 2 (Replicate) 🧠  
- A little sass and a whole lot of vibes 😎

---

## 📁 Project Structure

```
📂 Hamudnik_Bot/
├── main.py               # Bot entry point and handler setup
├── Interactions.py       # Command and message logic
├── Constants.py          # API keys and user text constants
└── README.md             # This file
```

---

## 💡 Features

### `/start`
Greets the user with a warm welcome in Hebrew-English style 🇮🇱✨  
> “Shalom aleichem ✡︎, bruchim habaim!”

### `/help`
Shows available commands and descriptions.

### `/time`
Replies with the current date and time.

### `/quote`
Fetches a motivational quote from the [ZenQuotes API](https://zenquotes.io/).

### `/movies`
Returns the latest movie releases using [The Movie Database (TMDb)](https://www.themoviedb.org/) API.

### 🧠 Free text chat
Users can send any message (e.g., questions), and the bot will respond using **Meta’s LLaMA 2-70B Chat model** hosted on Replicate.


## 📦 Dependencies

- `python-telegram-bot`
- `requests`
- `replicate`

---

## 📜 Sample Conversation

**User:** `/quote`  
**Bot:**  
> “The only way to do great work is to love what you do.” – Steve Jobs

**User:** `what is the capital of France?`  
**Bot (via LLaMA 2):**  
> The capital of France is Paris 🇫🇷

---

## 👤 Author

**Aleksandr Tanskii**
---

Want to extend this bot? Add weather, jokes, images, or even integrate it with your data pipelines! Let the bot evolve ✨
