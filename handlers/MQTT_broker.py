import datetime
import time

import paho.mqtt.client as mqtt
import pytz
import random

MQTT_BROKER = "mqtt.iotserver.uz"
MQTT_PORT = 1883
MQTT_TOPIC = "ttpu/User"
USERNAME = "userTTPU"
PASSWORD = "mqttpass"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

tz = pytz.timezone('Asia/Tashkent')


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker", flush=True)
    else:
        print(f"Failed to connect to MQTT broker with result code {rc}", flush=True)


client = mqtt.Client(protocol=mqtt.MQTTv311)

client.on_connect = on_connect

client.username_pw_set(USERNAME, PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    now = datetime.datetime.now(tz)
    epoch_time = int(now.timestamp())
    client.publish(MQTT_TOPIC, epoch_time)

    message = now.strftime("[%d.%m.%Y-%H:%M:%S]") + f"Published time {epoch_time} to {MQTT_TOPIC}"
    print(message, flush=True)
    time.sleep(30)