# Add this function to your main.py
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a list of words or names separated by new lines, and I will sort them for you! Use /sort_az or /sort_za.")

# Add this line in your 'if __name__ == '__main__':' section
app.add_handler(CommandHandler("start", start))
