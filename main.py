from telegram.ext import *
from Interactions import datetime_command, start_command, help_command, text_response, get_quote, movies_command, API_KEY

if __name__ == "__main__":

    print("Starting the bot")
    # here I need to load the model one time model = get_llm_model()
    app = Application.builder().token(API_KEY).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('time', datetime_command))
    app.add_handler(CommandHandler('quote', get_quote))
    app.add_handler(CommandHandler('movies', movies_command))
    app.add_handler(MessageHandler(filters.TEXT, text_response))


    print("Polling...")
    app.run_polling(poll_interval=1)


