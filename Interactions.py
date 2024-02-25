from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
from Constants import TMDB_API_KEY, text_for_user_start, list_of_commands, system_promt, TMDB_LINK, start_help_message
import requests
import replicate
import time
#model = [1,2,3] here load the model

# The start function
async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text(text_for_user_start)

# The help function
async def help_command(update, context):
    # A dictionary with commands and their descriptions
    commands_with_descriptions = list_of_commands
    # Constructing the help message with command descriptions
    help_message = start_help_message
    for command, description in commands_with_descriptions.items():
        help_message += f'{command}: {description}\n'
    # Sending the help message to the user
    await update.message.reply_text(help_message)

# The text function
async def text_response(update, context)->str:
    text : str = update.message.text.lower()
    if text == 'ping':
        await update.message.reply_text("pong")
    elif text == 'meow':
        await update.message.reply_text('meow')
    elif text == 'start':
        await start_command(update, context)
    else:
        await llama2(update, context, text)

#The datetime now function
async def datetime_command(update: Update, context: CallbackContext) -> None:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"The current time is: {current_time}")


# Function to fetch a motivational quote from ZenQuotes API
def get_motivational_quote():
    api_url = "https://zenquotes.io/api/random"
    response = requests.get(api_url)
    data = response.json()
    quote = data[0]['q'] + " - " + data[0]['a']
    return quote

async def get_quote(update, context):
    user_message = update.message.text

    # Check if the message sender is the bot itself
    if update.message.from_user.id == context.bot.id:
        return

    # Retrieve chat history from user
    user_id = update.message.from_user.id
    chat_history_key = f"chat_history_{user_id}"
    chat_history = context.user_data.get(chat_history_key, "")

    # Check if the user's message is a request for a quote
    if user_message.lower() == "/quote":
        # Fetch a motivational quote
        quote = get_motivational_quote()
        bot_response = f"Here's a motivational quote for you:\n\n{quote}"
    else:
        # Append user's message to existing chat history
        if chat_history:
            chat_history += f" {user_message}"
        else:
            chat_history = user_message

        # Generate response using DialoGPT
        bot_response = generate_response(chat_history)

    # Update chat history in user_data
    context.user_data[chat_history_key] = chat_history

    # Send the bot's response back to the user using send_message
    await context.bot.send_message(chat_id=update.message.chat_id, text=bot_response)

#TMDB functionality
# Function to get the latest movie releases from TMDb
def get_latest_movies():
    base_url = TMDB_LINK
    params = {'api_key': TMDB_API_KEY, 'language': 'en-US', 'page': 1}

    response = requests.get(base_url, params=params)
    data = response.json()

    # Extract movie information
    movies = data.get('results', [])
    return movies

async def movies_command(update, context):
    # Fetch the latest movies
    latest_movies = get_latest_movies()

    # Construct a message with movie details
    if latest_movies:
        movie_message = "Latest movie releases:\n\n"
        for movie in latest_movies:
            title = movie.get('title', 'N/A')
            release_date = movie.get('release_date', 'N/A')
            overview = movie.get('overview', 'No overview available')
            movie_message += f"{title} ({release_date})\n{overview}\n\n"

        # Split the message into chunks of 4096 characters (Telegram's maximum message length)
        message_chunks = [movie_message[i:i + 4096] for i in range(0, len(movie_message), 4096)]

        # Send each chunk as a separate message
        for chunk in message_chunks:
            await update.message.reply_text(chunk)
    else:
        movie_message = "Sorry, unable to fetch the latest movies at the moment."

        # Send the error message to the user
        await update.message.reply_text(movie_message)

async def llama2(update, context, text)->str:
    output = replicate.run(
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": text,
            "system_promt": system_promt,
            "max_new_tokens": 800,

        }
    )
    output_text = ""
    for item in output:
        output_text += str(item)
    await update.message.reply_text(output_text)
    # for char in output_text:
    #     print(char, end='', flush=True)
    #     time.sleep(0.05)
    # print()

def get_llm_model():
    return [1,2,3]