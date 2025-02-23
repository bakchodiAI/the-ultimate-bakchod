import os
import logging
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Oye! Main hoon Bakchodi Bot. Jo marzi bol, mazak udane ke liye ready hoon!")

# Async function to generate response
async def generate_response(user_message):
    try:
        response = await openai.ChatCompletion.acreate(
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

# Handle user messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = await generate_response(user_message)
    await update.message.reply_text(response)

# Main function to run the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # Message handler for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
