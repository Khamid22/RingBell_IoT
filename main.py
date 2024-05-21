import logging
import aiohttp
import telebot
import asyncio
import mysql.connector
from datetime import datetime

TELEGRAM_TOKEN = '7061775503:AAEgn5_Q-BBuRxHjIg1F27FUD1QbxGPEhP8'
ESP32_IP = '192.168.181.217'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'devuser'
MYSQL_PASSWORD = '4467996m'
MYSQL_DATABASE = 'telegram_bot_db'

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
db_cursor = db_connection.cursor()

# List of authorized user IDs
AUTHORIZED_USERS = [1081721793, 1114820537]

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS


def save_message(user_id, username, message_text):
    timestamp = datetime.now()
    query = "INSERT INTO user_messages (user_id,username, message_text, message_time) VALUES (%s,%s , %s, %s)"
    values = (user_id, username, message_text, timestamp)
    db_cursor.execute(query, values)
    db_connection.commit()


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


if name == "main":
    bot.polling()
