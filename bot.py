import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# OpenRouter AI API Key
OPENROUTER_API_KEY = "your_openrouter_api_key"  # <-- Yaha apni API key daalo

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"  # <-- Apna Telegram bot token daalo

# OpenRouter AI ke liye function
async def chat_with_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_data = await response.json()
            return response_data.get("choices", [{}])[0].get("message", {}).get("content", "Kuch gadbad ho gayi!")

# Start command
async def start(update: Update, context):
    await update.message.reply_text("Bhai! Mai ek sarcastic aur thoda abusive AI bot hoon. Kuch bol na!")

# Message handling function
async def handle_message(update: Update, context):
    user_message = update.message.text
    logging.info(f"User: {user_message}")
    
    # AI se reply lo
    response = await chat_with_ai(user_message)
    
    # Reply karo
    await update.message.reply_text(response)

# Main function
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot chal raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
