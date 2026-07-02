import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Sorting Logic
def sort_list(text, reverse=False):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    sorted_lines = sorted(lines, key=str.lower, reverse=reverse)
    return "\n".join(sorted_lines)

# Command: /sort_az
async def sort_az(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = sort_list(update.message.text.replace('/sort_az', ''), reverse=False)
    await update.message.reply_text(f"Sorted (A-Z):\n\n{result}")

# Command: /sort_za
async def sort_za(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = sort_list(update.message.text.replace('/sort_za', ''), reverse=True)
    await update.message.reply_text(f"Sorted (Z-A):\n\n{result}")

if __name__ == '__main__':
    # Get token from Railway environment variable
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("sort_az", sort_az))
    app.add_handler(CommandHandler("sort_za", sort_za))
    
    print("Bot is running...")
    app.run_polling()
