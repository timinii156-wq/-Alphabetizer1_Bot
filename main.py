import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Setup basic logging to see exactly what's happening in Railway logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sorting Logic
def sort_list(text, reverse=False):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    sorted_lines = sorted(lines, key=str.lower, reverse=reverse)
    return "\n".join(sorted_lines)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a list (one item per line), and I'll give you sorting buttons!")

# Handler for incoming lists
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    context.user_data['last_list'] = user_text
    
    keyboard = [
        [InlineKeyboardButton("Sort A-Z", callback_data='az'),
         InlineKeyboardButton("Sort Z-A", callback_data='za')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("List received! How would you like to sort it?", reply_markup=reply_markup)

# Handler for button clicks
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_list = context.user_data.get('last_list')
    if not user_list:
        await query.edit_message_text("List expired. Please send it again.")
        return

    reverse_sort = (query.data == 'za')
    result = sort_list(user_list, reverse=reverse_sort)
    await query.edit_message_text(f"Sorted Result:\n\n{result}")

# Error Handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("ERROR: TELEGRAM_TOKEN not set!")
    else:
        # Correct way to build the application and set drop_pending_updates
        app = ApplicationBuilder().token(token).updater_settings(dict(drop_pending_updates=True)).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(CallbackQueryHandler(button_click))
        app.add_error_handler(error_handler)
        
        print("Bot is running...")
        app.run_polling()
