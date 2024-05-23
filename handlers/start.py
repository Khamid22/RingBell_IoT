import asyncio
import json

import aiohttp
import logging
import telebot
import random
import paho.mqtt.client as mqtt
from db_users import save_message
from config import BOT_TOKEN
import os

AUTHORIZED_USERS = [1081721793, 1114820537, 1270439555]
logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)
# MQTT configuration
MQTT_BROKER = "mqtt.iotserver.uz"
MQTT_PORT = 1883
MQTT_TOPIC = "ttpu/User"
USERNAME = "userTTPU"
PASSWORD = "mqttpass"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# Initialize the MQTT client
mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)
mqtt_client.username_pw_set(USERNAME, PASSWORD)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker", flush=True)
    else:
        print(f"Failed to connect to MQTT broker with result code {rc}", flush=True)


mqtt_client.on_connect = on_connect
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()


def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return
    bot.reply_to(message, "Hi! Send /ring to ring the bell.")
    save_message(message.from_user.id, message.from_user.username, message.text)


@bot.message_handler(commands=['ring'])
def ring_bell(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return

    # JSON message to send to MQTT
    json_message = json.dumps({"ring": "on"})
    mqtt_client.publish(MQTT_TOPIC, json_message)

    bot.reply_to(message, "Bell is ringing!")
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
        file_path = file_info.file_path
        file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
        file_name = "ringbell_audio_1"
        mqtt_message = f'{file_name}: {file_url}'
        mqtt_client.publish(MQTT_TOPIC, mqtt_message)
        bot.reply_to(message, "Audio received and URL sent to MQTT broker.")
        save_message(message.from_user.id, message.from_user.username, "Audio", file_url)


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "You are not authorized to use this bot.")
        return

    file_info = bot.get_file(message.voice.file_id)
    file_size = message.voice.file_size
    duration = message.voice.duration

    if file_size > 2 * 1024 * 1024:  # 2 MB in bytes
        bot.reply_to(message, "Voice message size must not exceed 2MB.")
    elif duration > 180:  # 3 minutes in seconds
        bot.reply_to(message, "Voice message duration must not exceed 3 minutes.")
    else:
        file_path = file_info.file_path
        file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
        file_name = "ringbell_audio_1"
        mqtt_message = f'{file_name}: {file_url}'
        mqtt_client.publish(MQTT_TOPIC, mqtt_message)
        bot.reply_to(message, "Voice message received and URL sent to MQTT broker.")
        save_message(message.from_user.id, message.from_user.username, "Voice", file_url)


if __name__ == "__main__":
    bot.polling()
