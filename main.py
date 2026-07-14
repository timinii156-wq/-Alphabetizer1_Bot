import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

# ----------------------------
# Logging
# ----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ----------------------------
# Sorting Function
# ----------------------------
def sort_list(text, reverse=False, unique=False):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if unique:
        seen = set()
        unique_lines = []
        for line in lines:
            key = line.lower()
            if key not in seen:
                seen.add(key)
                unique_lines.append(line)
        lines = unique_lines

    return "\n".join(sorted(lines, key=str.lower, reverse=reverse))


# ----------------------------
# /start
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome = (
        "👋 *Welcome to Alphabetizer!*\n\n"
        "I can organize your lists alphabetically.\n\n"
        "*How to use me:*\n"
        "• Send a list with one item per line.\n"
        "• Choose how you'd like it sorted.\n\n"
        "*Example:*\n"
        "Orange\n"
        "Apple\n"
        "Banana\n"
        "Mango"
    )

    await update.message.reply_text(
        welcome,
        parse_mode="Markdown"
    )


# ----------------------------
# /help
# ----------------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "📖 *How to Use Alphabetizer*\n\n"
        "1. Send your list.\n"
        "2. Put each item on its own line.\n"
        "3. Choose one of the sorting options.\n\n"
        "Available options:\n"
        "✅ A-Z\n"
        "✅ Z-A\n"
        "✅ Remove Duplicates + A-Z"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )


# ----------------------------
# /about
# ----------------------------
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "ℹ️ *About Alphabetizer*\n\n"
        "Alphabetizer is a simple Telegram bot that sorts "
        "names, words, and text lists alphabetically.\n\n"
        "Fast • Simple • Free"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )


# ----------------------------
# /example
# ----------------------------
async def example(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "*Example Input*\n\n"
        "Orange\n"
        "Apple\n"
        "Banana\n"
        "Mango\n\n"
        "*Example Output*\n\n"
        "Apple\n"
        "Banana\n"
        "Mango\n"
        "Orange"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )


# ----------------------------
# Handle List
# ----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["last_list"] = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("🔤 Sort A–Z", callback_data="az"),
            InlineKeyboardButton("🔠 Sort Z–A", callback_data="za")
        ],
        [
            InlineKeyboardButton(
                "✨ Remove Duplicates",
                callback_data="unique"
            )
        ]
    ]

    await update.message.reply_text(
        "✅ *List received!*\n\nChoose how you'd like to sort it.",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ----------------------------
# Buttons
# ----------------------------
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_list = context.user_data.get("last_list")

    if not user_list:
        await query.edit_message_text(
            "⚠️ Your previous list has expired.\n\nPlease send it again."
        )
        return

    if query.data == "az":

        result = sort_list(user_list)

        await query.edit_message_text(
            f"🔤 *Sorted A–Z*\n\n{result}",
            parse_mode="Markdown"
        )

    elif query.data == "za":

        result = sort_list(user_list, reverse=True)

        await query.edit_message_text(
            f"🔠 *Sorted Z–A*\n\n{result}",
            parse_mode="Markdown"
        )

    elif query.data == "unique":

        result = sort_list(user_list, unique=True)

        await query.edit_message_text(
            f"✨ *Duplicates Removed*\n\n{result}",
            parse_mode="Markdown"
        )


# ----------------------------
# Error Handler
# ----------------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling update:", exc_info=context.error)


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":

    token = os.getenv("TELEGRAM_TOKEN")

    app = (
        ApplicationBuilder()
        .token(token)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("example", example))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_handler(CallbackQueryHandler(button_click))

    app.add_error_handler(error_handler)

    print("Alphabetizer Bot is running...")

    app.run_polling(drop_pending_updates=True)
