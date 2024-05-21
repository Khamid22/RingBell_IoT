import asyncio
import aiohttp
import logging
import telebot
from db_users import save_message
from config import BOT_TOKEN

AUTHORIZED_USERS = [1081721793, 1114820537, 1270439555]
logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)
ESP32_IP = None


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
                async with session.get(f'https://{ESP32_IP}/ring') as resp:
                    if resp.status == 200:
                        bot.reply_to(message, "Bell is ringing!")
                    else:
                        bot.reply_to(message, "Failed to ring the bell.")
            except aiohttp.ClientError as e:
                bot.reply_to(message, f"Error: {e}")

    asyncio.run(ring())
    save_message(message.from_user.id, message.from_user.username, message.text)


@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return

    file_info = bot.get_file(message.audio.file_id)
    file_size = message.audio.file_size  # Size in bytes
    duration = message.audio.duration  # Duration in seconds

    if file_size > 2 * 1024 * 1024:  # 2 MB in bytes
        bot.reply_to(message, "Audio size must not exceed 2MB.")
    elif duration > 180:  # 3 minutes in seconds
        bot.reply_to(message, "Audio duration must not exceed 3 minutes.")
    else:
        downloaded_file = bot.download_file(file_info.file_path)
        bot.reply_to(message, "Audio received successfully.")
        # Handle the audio file as needed

    save_message(message.from_user.id, message.from_user.username, message.text)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    file_size = file_info.file_size
    duration = message.voice.duration

    if file_size > 2 * 1024 * 1024:  # 2 MB in bytes
        bot.reply_to(message, "Audio size must not exceed 2MB.")
    elif duration > 180:  # 3 minutes in seconds
        bot.reply_to(message, "Audio duration must not exceed 3 minutes.")
    else:
        downloaded_file = bot.download_file(file_info.file_path)
        bot.reply_to(message, "Audio received successfully.")


if __name__ == "__main__":
    bot.polling()
