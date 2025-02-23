import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Badtameez Bot Online Hai! Bol kya chahiye?")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text

    # Send request to OpenRouter AI
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
        json={"model": "mistralai/mistral-saba", "messages": [{"role": "user", "content": user_message}]}
    )

    reply_text = "Kuch garbar hai, OpenRouter ka response nahi mila!"  
    if response.status_code == 200:
        reply_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Samajh nahi aaya!")

    await update.message.reply_text(reply_text)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logging.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
