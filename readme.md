# piNet3 Python Experiments

This Python based project aims to create an extensible sensor network by using homemade IOT devices to collect, forward and react to data.  Each IOT device reports to a central master node using JSON as the interchange format over various transport layers including MQTT, HTTP and AX25 (9600 baud Radio).  

A breif description of the project follows.

## Disclaimer !
All code in this project was written as a hobbyist before I had benefited from CodeClan Professional Software Development Course, please be forgiving ;-)  The major purpose of this project was to focus my learning.

## Overview

Each node is a Raspberry Pi SBC (Rpi) connected to a central broker node via an isolated local area network.  Each node is responsible for one location, for example, 'polyhub' is the pi that monitors my poly tunnel.  The Polyhub node reads various sensors directly and via serial connections to ATMEGA328p microcontrollers.  Microcontrollers allow me to use older 5V sensors and to better drive transitor switches and relays while only having to level shift the the Rpi required 3V3 once on the serial line.  Using the 328p also exposed me to learning the basics of C++ and introduced me to the tooling required to compile and flash devices.

## Sensors 
Many different sensors have been used including DS18B20 temperature probes, si7120 for air temperature and humidity (laterly upgraded to BME280), soil moisture sensors, light sensors, water tank levels, flow sensors to name a few.  Each sensor has a driver file either utilising third party libraries or manufacturers datasheet examples.

Sensor data is immeadiately parsed to a known structure using python dictionaries for processing within a node and JSON for transport over the network
