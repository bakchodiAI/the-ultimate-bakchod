import openai
import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables
load_dotenv()

# Fetch API keys from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_response(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tum ek sarcastic, funny aur witty AI ho. Har jawab mazak aur thodi masti ke sath do."},
                {"role": "user", "content": user_message}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "Bhai, abhi dimaag kaam nahi kar raha. Thoda break lele!"

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Oye! Main hoon Bakchodi Bot. Jo marzi bol, mazak udane ke liye ready hoon!")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = generate_response(user_message)
    update.message.reply_text(response)

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updat

