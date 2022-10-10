#!/usr/bin/env python3


"""
test2.py
Central Command interpreter proto
SELF CONTAINED TEST

NEXT --> skel command listener for drones as service
Finnalise command JSON structure.
"""

from configparser import ConfigParser
import json
import paho.mqtt.client as mqtt
import os
import platform
import piNetDate
import pinSQL
import time

# Config
thisPi = f"ComSys-{platform.uname()[1]}"
config = ConfigParser()
config.read('/home/pi/piNet/config/config.ini')
broker = config.get('mqtt', 'broker')
base_topic = config.get("mqtt", "baseTopic")
announce_topic = f"{base_topic}/{thisPi}"
last_will_topic = f"{announce_topic}/alarm"

# Topics to subscribe to and accept commands from.
# List of tuples (topic, qos)
command_topics = [
    ("/piNet/command", 1),
    ("/piNet/testCommand", 1),
    ("/piNet/tetra", 1)
]

# List of commands available on this dispatcher.
commands = ['command1', 'command2', 'command3']

# MQTT Functions


def mqtt_connect(clientID):
    client = mqtt.Client(clientID)
    client.username_pw_set(config.get('mqtt', 'username'),
                           config.get('mqtt', 'password'))
    client.will_set(last_will_topic, "LAST WILL ISSUED >>>  HELP", 0, False)
    client.connect(broker)
    print(announce_topic)
    client.publish(announce_topic, f"{thisPi} ACIVATED", 1, False)
    client.on_connect = on_connect
    client.on_message = dispatcher
    client.loop_forever()
    return client


def mqtt_disconnect(client):
    client.disconnect()
    client.loop_stop()


def mqttSendMsg(client, msg, topic, qos, retained=False):
    client.publish(topic, msg, qos, retained)


# The callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    # Print result of connection attempt
    print(f"{thisPi} COMSYS Connected with RC:{rc} {base_topic}")
    client.subscribe(command_topics)


def parseTopic(topic):
    topic = topic.split("/")
    topic = topic[1:]
    return(topic)

#  Dispatcher functions


def command1(payload, topic):
    print(f"Command 1 has executed: {payload} from {topic}")


def command2(payload, topic):
    print(f"Command 2 has executed: {payload} from {topic}")


def command3(payload, topic):
    print(f"Command 3 has executed: {payload} from {topic}.  BYE!")


# IS THIS SAFE?????
# Further reading required - this feels unsafe, verify.
def doStuff(c):
    if c in commands:
        return globals()[c]()
    else:
        return False


# Main message dispatcher.
def dispatcher(client, userdata, msg):

    # types: command|CPU|message|sensor

    payload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    topic_parts = parseTopic(msg.topic)
    print(f"Topic Parsed --> {topic_parts}")

    for tpl in command_topics:
        #   Parse JSON Command

        if topic == tpl[0]:
            print(f"{topic_parts[1]} has authority")
            if payload in commands:
                globals()[payload](payload, topic)


if __name__ == "__main__":

    client = mqtt_connect(thisPi)
