#!/usr/bin/env python3


"""
PROTOTYPE
Data structures for piNet MQTT/socket xmission.

Purpose:  Define/Test JSON packet shape and associated functions,
excluding wxObs.
Allow for new types by adding new 'type parser'.
Packet should be self contained and agnostic of transmission method.
MQTT Topics only to organsise network (sub/pub to only what is needed by drone)

PROTO Start with base pkt ...OUTER JSON common to all piNet.  
ADD EPCOH
{
    "epoch": int(time.time()),
    "machine": "str",
    "type": "str|cpu|alarm|sensor|command",
    "data":
        {
            "data":"per type",
            "JSON":"Obj"
        }
}

"""


# Imports
import json
import logging
import time
logging.basicConfig(filename='logs/piNet.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

#  setup
allowed_cmd = ['command1', 'command2', 'Test_CMD']
allowed_types = ['alarm', 'cmd', 'cpu', 'message', 'sensor', 'other']

#
# DEV JSON packets
#
bad_json = """{
    "epoch": 1369550494,
    "machine": BAD,
    "data": "temperature": 13.8, "humidity": 3.8,
    "sensor_name": "ph-air",
    "type": "sensor"
}
"""

j_alarm = """{
    "epoch": 1369550494,
    "machine": "sandbox",
    "data": {"alarm_sid": "ph-air", "alarm_param": "Temp", "alarm_value": "T_HIGH"},
    "alarm_name": "ph-air-temp",
    "type": "alarm"
}
"""


j_cmd = """
{
    "epoch": 1369550494,
    "machine": "Sentinel21",
    "type": "cmd",
    "data" : {
        "cmd": "TEST_CMD",
        "param": "on",
        "value": 12.12
        }
}
"""

j_msg = """
{
    "epoch": 1369550494,
    "machine": "thisPi/service",
    "type": "message",
    "data" : {"msg_type":"msg|bcast", "message_text":"messgae text string"}
}
"""

j_cpu = """
{
    "epoch": 1369550494,
     "machine": "sandbox",
     "type": "cpu",
     "data": {
         "device": "sandbox",
         "cpuTemp": "30.9",
         "cpuType": "Pi Zero v1.3",
         "users": 1,
         "uptime": 2078248,
         "loadAvg": {
             "L1": "0.03",
             "L5": "0.08",
             "L15": "0.08"
         }
     }
 }

"""
j_request = """
{
    "epoch": 1369550494,
    "machine": "nexus",
    "type": "req|reqack|response",
    "data": {
        "rType": "hx",
        "wants": "ph-air-T",
        "number": 10
    }
}
"""
j_sensor = """
{
    "epoch": 1369550494,
    "machine": "polyhub",
    "data": {"temperature": 13.8, "humidity": 3.8},
    "sid": "ph-air",
    "type": "sensor"
    }
"""


#
# DEFS
#

def validateJSON(jsonData):
    try:
        j = json.loads(jsonData)
    except ValueError:
        return False
    return j


def alarm(j):
    print(f"alarm >>> {j}")


def cmd(j):
    # print(f"{j['machine']} >>> {j['data']['cmd']} {j['data']['param']} {j['data']['value']}")
    
    if j['data']['cmd'] in allowed_cmd:
        # logging.info(f"{j['data']['cmd']} ({j['data']['param']}) from {j['machine']}")
        globals()[j['data']['cmd']](j)



def cpu(j):
    print(f"cpu >>> {j}")
 

def message(j):
    print(f"Message >>> {j}")


def sensor(j):
    print(f"Sensor def >>> {j}")


# command parsers
# functions for type['cmd']
def Test_CMD(c):
    val = c['data'].get('value','')
    # print(type(val))
    logStr = (
        f"{time.time():^13.0f} EXEC {c['machine']:10}"
        f"{c['data']['cmd']:^12} P:{c['data']['param']:8} V:{val:6} "
        )
    logging.info(logStr)

def command1(c):
    val = c['data'].get('value','')
    # print(f"Command ONE: {j['machine']} >>> {c['data']['cmd']}, {c['data']['param']}, {val}")

    logStr = (
        f"{time.time():^13.0f} EXEC {c['data']['cmd']:^12}"
        f"{c['machine']:10} P:{c['data']['param']:8} V:{val:6} "
        )
    logging.info(logStr)


j = validateJSON(j_msg)

if j:
    if j['type'] in allowed_types and 'data' in j and 'machine' in j:
        print(j['type'])
        # logging.info(f"DSPC {time.time():13.0f} {j['machine']:12} >>> {j['data']['cmd']} ")
        globals()[j['type']](j)
