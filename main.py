import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Sorting Logic ---
def sort_list(text, reverse=False, unique=False):
    # Split text into lines and remove empty ones
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Remove duplicates if requested
    if unique:
        lines = list(set(lines))
        
    # Sort the list
    sorted_lines = sorted(lines, key=str.lower, reverse=reverse)
    return "\n".join(sorted_lines)

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a list, and I'll give you sorting buttons.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save the text in user_data
    context.user_data['last_list'] = update.message.text
    
    # Create the 3 buttons
    keyboard = [
        [InlineKeyboardButton("Sort A-Z", callback_data='az'),
         InlineKeyboardButton("Sort Z-A", callback_data='za')],
        [InlineKeyboardButton("Sort & Remove Duplicates", callback_data='unique')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("List received! How should I sort it?", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_list = context.user_data.get('last_list')
    if not user_list:
        await query.edit_message_text("List expired. Please send it again.")
        return

    # Process based on which button was clicked
    if query.data == 'az':
        result = sort_list(user_list, reverse=False, unique=False)
        await query.edit_message_text(f"Sorted (A-Z):\n\n{result}")
    elif query.data == 'za':
        result = sort_list(user_list, reverse=True, unique=False)
        await query.edit_message_text(f"Sorted (Z-A):\n\n{result}")
    elif query.data == 'unique':
        result = sort_list(user_list, reverse=False, unique=True)
        await query.edit_message_text(f"Sorted & Unique:\n\n{result}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")

# --- Main Setup ---
if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("ERROR: TELEGRAM_TOKEN not set!")
    else:
        # Build the application
        app = ApplicationBuilder().token(token).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(CallbackQueryHandler(button_click))
        app.add_error_handler(error_handler)
        
        print("Bot is running...")
        # Start polling and clear old updates
        app.run_polling(drop_pending_updates=True)
