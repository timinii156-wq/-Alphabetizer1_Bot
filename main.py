import logging
from telegram.ext import ApplicationBuilder

# Enable logging to see errors in Railway logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("CRITICAL: TELEGRAM_TOKEN environment variable is missing!")
    else:
        app = ApplicationBuilder().token(token).build()
        
        # Add your handlers here...
        
        print("Starting polling...")
        app.run_polling()
