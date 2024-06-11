import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Read the token from the environment variable
TOKEN = os.environ["TELEGRAM_TOKEN"]

def get_meme():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    data = response.json()
    if data['success']:
        memes = data['data']['memes']
        return memes[0]['url']  # Return the URL of the first meme
    return None

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send /meme to get a meme.')

def send_meme(update: Update, context: CallbackContext) -> None:
    meme_url = get_meme()
    if meme_url:
        update.message.reply_text(meme_url)
    else:
        update.message.reply_text("Sorry, I couldn't fetch a meme at the moment.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("meme", send_meme))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
