#!/usr/bin/env python3

"""
cpu.py: Read Raspberry Pi CPU TEmp and report to MQTT Broker.
Version 2.0.0 - Include hostname and load averages as JSON.
Version 2.1.0 - Read loads/uptime directly from /proc

E.g., 
{
    "uptime": "1828270",  # SECONDS 
    "users": "1",
    "loadAvg": {
        "L15": "0.00",
        "L5": "0.00",
        "L1": "0.00"
    },
    "cpuTemp": "42.9",
    "device": "nexus",
    "cpuType": "Pi 3 Model B (Sony)"
}
"""

__author__ = 'Mike Langley'

import os
import platform
import json
import piNetMQTT
import piNetDate
import time

thisPi = platform.uname()[1]
mqtt_topic = "/piNet/{}/system".format(thisPi)

dRev = {}
dRev['0002'] = "Pi B Rev 1"
dRev['0003'] = "Pi B Rev 1"
dRev['0004'] = "Pi B Rev 2"
dRev['0005'] = "Pi B Rev 2"
dRev['0006'] = "Pi B Rev 2"
dRev['0007'] = "Pi A"
dRev['0008'] = "Pi A"
dRev['0009'] = "Pi A"
dRev['000d'] = "Pi B Rev 2"
dRev['000e'] = "Pi B Rev 2"
dRev['000f'] = "Pi B Rev 2"
dRev['0010'] = "Pi B+"
dRev['0013'] = "Pi B+"
dRev['900032'] = "Pi B+"
dRev['0011'] = "Pi Compute Module"
dRev['0014'] = "Pi Compute Module"
dRev['0012'] = "Pi A+"
dRev['0015'] = "Pi A+"
dRev['a01041'] = "Pi 2 Model B V1.1 (Sony)"
dRev['a21041'] = "Pi 2 Model B V1.1 (Embest)"
dRev['a22042'] = "Pi 2 Model B V1.2"
dRev['900092'] = "Pi Zero v1.2"
dRev['900093'] = "Pi Zero v1.3"
dRev['9000C1'] = "Pi Zero W"
dRev['a02082'] = "Pi 3 Model B (Sony)"
dRev['a22082'] = "Pi 3 Model B (Embest)"
dRev['a03111'] = "Pi 4b 1GB"
dRev['b03111'] = "Pi 4b 2GB"
dRev['b03112'] = "Pi 4b 2GB"
dRev['c03111'] = "Pi 4b 4GB"
dRev['c03112'] = "Pi 4b 4GB"
dRev['d03114'] = "Pi 4b 8GB"



def getCPUrevision():
    # Read rPi /proc/cpu info & return poc type
    rev = "0000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:8] == 'Revision':
                rev = line[11:len(line)-1]
        f.close()
    except:
        rev = "0000"  # error

    return rev


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    res = res.replace("temp=", "").replace("\n", "")
    res = res[0:4]

    return(res)


def getUserCount():
    res = os.popen('users').readline().strip()
    users = res.split(" ")
    return len(users)


def getLoadAverages():
    with open("/proc/loadavg") as f:
        line = f.readline()
        la = line.split(" ")
        dLoad = {"L1": la[0], "L5": la[1], "L15": la[2]}
        return dLoad


def getUptime():
    with open("/proc/uptime") as f:
        data = f.read()
        uptime = data.split(" ")
        uptime = uptime[0].split(".")
        return int(uptime[0])


def main(client):
    dData = {}
    dData['cpuTemp'] = getCPUtemperature()
    dData['cpuType'] = dRev[getCPUrevision()]
    dData['users'] = getUserCount()
    dData['uptime'] = getUptime()
    dData['loadAvg'] = getLoadAverages()
    
    dOut = {}
    dOut['epoch'] = int(time.time())
    dOut['machine'] = thisPi
    dOut['type'] = "cpu"
    dOut['data'] = dData
    
    client.publish(mqtt_topic, json.dumps(dOut), 1, False)
    print(json.dumps(dOut))


if __name__ == '__main__':
    client = piNetMQTT.mqtt_connect(thisPi)
    main(client)
    piNetMQTT.mqtt_disconnect(client)
    os._exit(0)
