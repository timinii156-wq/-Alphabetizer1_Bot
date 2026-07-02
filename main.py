import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Sorting Logic
def sort_list(text, reverse=False):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    sorted_lines = sorted(lines, key=str.lower, reverse=reverse)
    return "\n".join(sorted_lines)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a list (one item per line) and use /sort_az or /sort_za to sort them.")

# Command: /sort_az
async def sort_az(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This removes the command part from the message and sorts the rest
    text_to_sort = update.message.text.replace('/sort_az', '').strip()
    if text_to_sort:
        result = sort_list(text_to_sort, reverse=False)
        await update.message.reply_text(f"Sorted (A-Z):\n\n{result}")
    else:
        await update.message.reply_text("Please provide a list to sort after the command.")

# Command: /sort_za
async def sort_za(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_sort = update.message.text.replace('/sort_za', '').strip()
    if text_to_sort:
        result = sort_list(text_to_sort, reverse=True)
        await update.message.reply_text(f"Sorted (Z-A):\n\n{result}")
    else:
        await update.message.reply_text("Please provide a list to sort after the command.")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sort_az", sort_az))
    app.add_handler(CommandHandler("sort_za", sort_za))
    
    print("Bot is running...")
    app.run_polling()
