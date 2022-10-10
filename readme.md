# piNet3 Python Experiments

This Python based project aims to create an extensible sensor network by using homemade IOT devices to collect, forward and react to data.  Each IOT device reports to a central master node using JSON as the interchange format over various transport layers including MQTT, HTTP and AX25 (9600 baud Radio).  

A breif description of the project follows.

## Disclaimer !
All code in this project was written as a hobbyist before I had benefited from CodeClan Professional Software Development Course, please be forgiving ;-)  The major purpose of this project was to focus learning.

## Overview

Each node is a Raspberry Pi SBC (Rpi) connected to a central broker node via an isolated local area network.  Each node is responsible for one location, for example, 'polyhub' is the pi that monitors my poly tunnel.  The Polyhub node reads various sensors directly and via serial connections microcontrollers.  Microcontrollers allow me to use older 5V sensors and to better drive transitor switches and relays while only having to level shift the the Rpi required 3V3 once on the serial line.
