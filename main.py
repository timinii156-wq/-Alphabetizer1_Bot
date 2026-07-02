if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    # Use drop_pending_updates=True to clear out old "conflicting" sessions
    app = ApplicationBuilder().token(token).drop_pending_updates(True).build()

    # ... your other code ...
    app.run_polling()
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# ... (rest of your code)
