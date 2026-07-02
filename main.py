import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Sorting Logic
def sort_list(text, reverse=False):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    sorted_lines = sorted(lines, key=str.lower, reverse=reverse)
    return "\n".join(sorted_lines)

# Command: /start - Shows instructions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a list (one item per line), and I'll give you sorting buttons!")

# Handle plain text messages (the list)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Save the text in user_data so we can sort it when they click a button
    context.user_data['last_list'] = user_text
    
    keyboard = [
        [InlineKeyboardButton("Sort A-Z", callback_data='az'),
         InlineKeyboardButton("Sort Z-A", callback_data='za')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("List received! How would you like to sort it?", reply_markup=reply_markup)

# Handle button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_list = context.user_data.get('last_list')
    if not user_list:
        await query.edit_message_text("List expired. Please send it again.")
        return

    if query.data == 'az':
        result = sort_list(user_list, reverse=False)
        await query.edit_message_text(f"Sorted (A-Z):\n\n{result}")
    elif query.data == 'za':
        result = sort_list(user_list, reverse=True)
        await query.edit_message_text(f"Sorted (Z-A):\n\n{result}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is running...")
    app.run_polling()
