import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sorting Logic
def sort_list(text, reverse=False):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    sorted_lines = sorted(lines, key=str.lower, reverse=reverse)
    return "\n".join(sorted_lines)

# Start command
async def start(update, context):
    await update.message.reply_text("Hello! Send me a list, and I'll sort it.")

# Handle messages
async def handle_message(update, context):
    context.user_data['last_list'] = update.message.text
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = [[InlineKeyboardButton("Sort A-Z", callback_data='az'), InlineKeyboardButton("Sort Z-A", callback_data='za')]]
    await update.message.reply_text("List received! Choose sorting order:", reply_markup=InlineKeyboardMarkup(keyboard))

# Handle clicks
async def button_click(update, context):
    query = update.callback_query
    await query.answer()
    user_list = context.user_data.get('last_list')
    if user_list:
        reverse = (query.data == 'za')
        await query.edit_message_text(f"Result:\n{sort_list(user_list, reverse)}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    
    # Standard builder
    app = ApplicationBuilder().token(token).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is running...")
    
    # This is the correct way to clear old updates in newer versions
    app.run_polling(drop_pending_updates=True)
