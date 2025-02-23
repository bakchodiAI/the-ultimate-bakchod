import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import random

# 🔹 Replace Your API Keys Here
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

# 🔹 Fun, Sarcastic, and Abusive Replies
sarcastic_responses = [
    "Wah bhai, kya bekaar baat boli hai! 🤦‍♂️",
    "Aapko Nobel Prize kab mil raha hai is bakwaas ke liye? 😂",
    "Tere jaisa smart banda toh Google bhi search nahi kar sakta! 🤣",
    "Itni bakwaas sunne se accha toh main sojaun 😴",
    "Mujhe laga koi intelligent baat hogi, lekin ye toh comedy show nikla! 🤡",
    "Tera dimaag Windows 95 jaisa slow lag raha hai! 🖥️",
]

abusive_responses = [
    "Oye, chal nikal idhar se! 🖕😂",
    "Tere jaise logon ki wajah se duniya slow chal rahi hai! 😆",
    "Dimag hai ya WiFi signal, kabhi full strength nahi hota! 🤡",
    "Abe chup be, tere words se zyada toh meri battery chalti hai 🔋😂",
    "Tere jokes sunne se accha toh raat ko bina pankhe so jau! 🫠",
]

# 🔹 OpenRouter AI API Function
def chat_with_ai(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    data = {
        "model": "mistral",  # Free & Fast Model
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(url, headers=headers, json=data)
    ai_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

    # 🔥 30% Chance AI Reply + 70% Chance Random Savage Reply
    if random.random() < 0.7:
        return random.choice(sarcastic_responses + abusive_responses)
    return ai_response if ai_response else "Bakwaas mat kar! 😆"

# 🔹 Telegram Bot Functions
def start(update, context):
    update.message.reply_text("Aye! Chal bol kya bakwaas hai? 😆")

def handle_message(update, context):
    user_message = update.message.text
    bot_response = chat_with_ai(user_message)
    update.message.reply_text(bot_response)

# 🔹 Run the Telegram Bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
