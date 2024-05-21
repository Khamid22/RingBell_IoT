import asyncio
import aiohttp
import logging
import telebot
from db_users import save_message
from config import BOT_TOKEN

AUTHORIZED_USERS = [1081721793, 1114820537, 1270439555]
logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)


def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return
    bot.reply_to(message, "Hi! Send /ring to ring the bell.")
    # save_message(message.from_user.id, message.from_user.username, message.text)


@bot.message_handler(commands=['ring'])
def ring_bell(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return

    async def ring():
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f'http://{ESP32_IP}/ring') as resp:
                    if resp.status == 200:
                        bot.reply_to(message, "Bell is ringing!")
                    else:
                        bot.reply_to(message, "Failed to ring the bell.")
            except aiohttp.ClientError as e:
                bot.reply_to(message, f"Error: {e}")

    asyncio.run(ring())
    save_message(message.from_user.id, message.from_user.username, message.text)


if __name__ == "__main__":
    bot.polling()