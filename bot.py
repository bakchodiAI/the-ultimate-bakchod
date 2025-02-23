import os
import logging
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ✅ Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Debug: Check if keys are loading correctly
print(f"DEBUG: Loaded API Key -> {OPENAI_API_KEY}")
print(f"DEBUG: Loaded Telegram Bot Token -> {TELEGRAM_BOT_TOKEN}")

# ✅ Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# ✅ Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ✅ Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Oye! Main hoon Bakchodi Bot. Jo marzi bol, mazak udane ke liye ready hoon!")

# ✅ OpenAI API function with debugging
async def generate_response(user_message):
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu ek sarcastic, funny aur witty AI hai. Har jawab thoda mazak aur masti bhara ho."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response["choices"][0]["message"]["content"].strip()
        logger.info(f"DEBUG: OpenAI Response -> {reply}")  # ✅ API response log karega
        return reply
    except Exception as e:
        logger.error(f"DEBUG: OpenAI Error -> {e}")
        return f"Error: {e}"  # ✅ Actual error dikhayega

# ✅ Handle user messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"DEBUG: User Message -> {user_message}")  # ✅ User ka message log karega
    response = await generate_response(user_message)
    await update.message.reply_text(response)

# ✅ Main function to run the bot
def main():
    # ✅ Webhook conflict solve karne ke liye check
    import requests
    webhook_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/deleteWebhook"
    requests.get(webhook_url)
    logger.info("DEBUG: Webhook deleted (if exists)")

    # ✅ Telegram bot setup
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # ✅ Command handlers
    app.add_handler(CommandHandler("start", start))

    # ✅ Message handler for text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ✅ Start the bot
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
