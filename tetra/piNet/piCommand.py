#!/usr/bin/env python3

"""
piCom.py
Central Command and control for piNet
"""

from configparser import ConfigParser
import paho.mqtt.client as mqtt
import os
import piNetDate
import platform
import time

# Config
config = ConfigParser()
config.read('/home/pi/piNet/config/config.ini')
broker = config.get('mqtt', 'broker')
base_topic = config.get("mqtt", "baseTopic")


thisPi = platform.uname()[1]
mqtt_topic = "/piNet/{}/piCommand".format(thisPi)
command_topic = "/piNet/piCommand"
# MQTT Functions


def mqtt_connect(clientID):
    client = mqtt.Client(clientID)
    client.username_pw_set(config.get('mqtt', 'username'),
                           config.get('mqtt', 'password'))
    client.connect(broker)
    client.publish(mqtt_topic, "I am here", 1, False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
    return client


def mqtt_disconnect(client):
    client.disconnect()
    client.loop_stop()


def mqttSendMsg(client, msg, topic, qos):
    client.publish(topic, msg, qos, False)


# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    # Print result of connection attempt
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe(command_topic)


def parseTopic(topic):
    topic = topic.split("/")
    topic = topic[1:]
    return(topic)

def exec_local():
    pass

def on_message(client, userdata, msg):
    # dispatcher
    # accept command json packet - SOMETHING LIKE ...
    # { "pi":"polyhub", "type":"command", "command":"ph-pump-1", "parameter":"on"}
    # { "pi":"machine", "type":"sql", "sensor":"ph-temp-green", "parameter":"13.5"}

    payload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    topic_parts = parseTopic(msg.topic)
    print(f"Message --> {topic_parts} -> {topic} > {payload}")

    if topic == command_topic:
        print("COMMAND MODE")

        if payload == "command here":
            print(f"REQ {payload} from {topic_parts[1]}")


if __name__ == "__main__":
    client = mqtt_connect(thisPi)
    mqtt_disconnect(client)
    os._exit(0)
