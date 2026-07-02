if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    # ... add your handlers here ...
    
    print("Bot is starting polling...")
    app.run_polling() 
    # This function is blocking, which is exactly what we want.
