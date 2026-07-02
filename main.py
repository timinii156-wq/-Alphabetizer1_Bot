import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Sorting Logic
def sort_list(text, reverse=False, unique=False):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if unique:
        lines = list(set(lines))
    sorted_lines = sorted(lines, key=str.lower, reverse=reverse)
    return "\n".join(sorted_lines)

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a list, and I'll give you sorting buttons!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['last_list'] = update.message.text
    keyboard = [
        [InlineKeyboardButton("Sort A-Z", callback_data='az'),
         InlineKeyboardButton("Sort Z-A", callback_data='za')],
        [InlineKeyboardButton("Sort & Remove Duplicates", callback_data='unique')]
    ]
    await update.message.reply_text("List received! Choose an option:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_list = context.user_data.get('last_list')
    if not user_list:
        await query.edit_message_text("List expired. Please send it again.")
        return
    
    # Sorting logic execution
    if query.data == 'az':
        result = sort_list(user_list, reverse=False, unique=False)
        await query.edit_message_text(f"Sorted (A-Z):\n\n{result}")
    elif query.data == 'za':
        result = sort_list(user_list, reverse=True, unique=False)
        await query.edit_message_text(f"Sorted (Z-A):\n\n{result}")
    elif query.data == 'unique':
        result = sort_list(user_list, reverse=False, unique=True)
        await query.edit_message_text(f"Sorted & Unique:\n\n{result}")

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("Bot is running...")
    # This correctly clears old updates without causing AttributeErrors
    app.run_polling(drop_pending_updates=True)
