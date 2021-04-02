#!/usr/bin/env python3

"""
piCom.py
Central Command and control for piNet
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
config = ConfigParser()
config.read('/home/pi/piNet/config/config.ini')
broker = config.get('mqtt', 'broker')
base_topic = config.get("mqtt", "baseTopic")


thisPi = platform.uname()[1]
mqtt_topic = "/piNet/{}/piCommand".format(thisPi)
command_topic = "/piNet/#"
# MQTT Functions


def mqtt_connect(clientID):
    client = mqtt.Client(clientID)
    client.username_pw_set(config.get('mqtt', 'username'),
                           config.get('mqtt', 'password'))
    client.connect(broker)
    client.publish(mqtt_topic, "piNet DB Listener ACIVATED", 1, False)
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
    print("{1} SQL Listener Connected with RC:{0}".format(str(rc), thisPi))
    client.subscribe(command_topic)


def parseTopic(topic):
    topic = topic.split("/")
    topic = topic[1:]
    return(topic)


def write_local_wx(json_data):

    # data = '''{
    #     "UV": 0.0,
    #     "dateTime": 1592941155,
    #     "delay": 4,
    #     "inHumidity": 60.0,
    #     "inTemp": 22.5,
    #     "outHumidity": null,
    #     "outTemp": null,
    #     "outTempBatteryStatus": 0,
    #     "pressure": 1002.8000000000001,
    #     "ptr": 46716,
    #     "radiation": 25.544150000000002,
    #     "rain": null,
    #     "rainTotal": 110.73,
    #     "rxCheckPercent": 0,
    #     "status": 64,
    #     "usUnits": 16,
    #     "windDir": null,
    #     "windGust": null,
    #     "windSpeed": null
    # }'''

    d = json.loads(json_data)

    cnx = pinSQL.connect_db("wxObs")
    cursor = cnx.cursor()
    sql = """INSERT INTO Observations
        (station_id, apiUser, ts, delay, inHumidity, outHumidity, outTemp, pressure, ptr,radiation, rain, rainTotal, rxCheckPercent, status, usUnits, windDir, windGust, windSpeed, UV) 
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    vals = (1, 1, d['dateTime'], d['delay'], d['inHumidity'], d['outHumidity'], d['outTemp'],
            d['pressure'], d['ptr'], d['radiation'], d['rain'], float(
                d['rainTotal']), d['rxCheckPercent'],
            d['status'], d['usUnits'], d['windDir'], d['windGust'], d['windSpeed'], d['UV'])

    cursor.execute(sql, vals)
    cnx.commit()
    d.clear()


def exec_local():
    pass


def on_message(client, userdata, msg):
    # dispatcher
    # accept command json packet
    # { "pi":"polyhub", "type":"command", "command":"ph-pump-1", "parameter":"on"}
    # { "pi":"machine", "type":"sql", "sensor":"ph-temp-green", "parameter":"13.5"}
    # types: command|CPU|message|sensor

    payload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    topic_parts = parseTopic(msg.topic)
    # print(f"Message --> {topic_parts} -> {topic} > {payload}")

    if topic == "/piNet/WX/obs":
        # print(payload)
        write_local_wx(payload)
        print("WX OBS WRITE")

    # SANDBOX TEST
    if topic_parts[1] == "sandbox":
        print(f"SANDBOX")
        j = json.loads(payload)
        print(f"{j['machine']} {j['type']} {j['sensor_name']} {j['data']}")


if __name__ == "__main__":
    client = mqtt_connect(thisPi)
    # mqtt_disconnect(client)
    # os._exit(0)
