#!/usr/bin/env python3

from configparser import ConfigParser
import io
import json
# import paho.mqtt.client as mqtt
import pinSQL
import requests

v = "a"
dTest = {}
dTest['a'] = "one"
dTest['b'] = "two"
dTest['c'] = "three"

if v in dTest:
    print(f"{v} is a key of dTest")
