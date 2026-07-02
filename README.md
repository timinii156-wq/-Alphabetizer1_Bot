# Telegram List Sorter Bot

A simple, fast, and free Telegram bot designed to instantly sort words, names, and lists alphabetically (A–Z or Z–A).

## Features
- **A-Z Sorting:** Quickly organize your lists in ascending order.
- **Z-A Sorting:** Reverse your lists with a single command.
- **Instant Response:** Built for speed and simplicity.

## How to Use
Add your list to the bot using the following commands:

### Sort A-Z
Send the command followed by your list:
`/sort_az`
`Banana`
`Apple`
`Cherry`

**Result:**
Apple
Banana
Cherry

### Sort Z-A
Send the command followed by your list:
`/sort_za`
`Banana`
`Apple`
`Cherry`

**Result:**
Cherry
Banana
Apple

## Deployment
This bot is deployed using [Python](https://www.python.org/) and the [python-telegram-bot](https://python-telegram-bot.org/) library, hosted on [Railway](https://railway.app/).

### Prerequisites
- Python 3.10+
- A Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Setup
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your environment variable: `TELEGRAM_TOKEN=your_token_here`
4. Run the bot: `python main.py`

## License
[MIT](https://choosealicense.com/licenses/mit/)
