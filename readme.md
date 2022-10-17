# Python Hobby Project - IoT network (piNet)

This Python based project aims to create an extensible sensor network by using homemade IOT devices to collect, forward and react to data. Each IOT device reports to a central master node using JSON as the interchange format over various transport layers including MQTT, HTTP and AX25 (9600 baud Radio).

A brief description of the project follows.

## Disclaimer !
All code in this project was written as a hobby before I had benefited from CodeClan Professional Software Development Course, please be forgiving ;-) The major purpose of this project was to focus my learning and to enjoy the process.

While planning is everything for most projects it must be understood that this project is driven by *falling into rabbit holes* and discovering new problems to solve. **There is no final product except learning and discovery**.

## Overview
Each node is a Raspberry Pi SBC (Rpi) connected to a central broker node via an isolated local area network. Each node is responsible for one location, for example, 'polyhub' is the pi that monitors my poly tunnel. The Polyhub node reads various sensors directly (using I2C and SPi) and via serial connections to ATMEGA328p microcontrollers. Microcontrollers allow me to use older 5V sensors and to better drive transistor switches and relays while only having to level shift the Rpi required 3V3 once on the serial line. Using the 328p also exposed me to learning the basics of C++ and introduced me to the tooling required to compile and flash embedded devices.

## Sensors
Many different sensors have been used including DS18B20 temperature probes, si7120 for air temperature and humidity (laterly upgraded to BME280), soil moisture sensors, light sensors, water tank levels, flow sensors to name a few. Each sensor has a driver file either utilising third party libraries or manufacturers datasheet examples.

Sensor data is immediately parsed to a known structure by the node using python and JSON for transport to the master node. The node can react by triggering alarms, switching on soil bed heating or lighting or activating pumps to deliver water. All actions are reported to the network.

Sensors are not limited to hardware devices. I wrote a basic PHP API that receives weather alert data from the Met Office RSS feed and parses it to a 'piNet' JSON format. The master node consumes this API and reacts by sending an alert Email to interested parties and sending regular alerts to the network while the alert is in force. Other actions can be taken programmatically by command of a node, for example, turning on soil bed heating when an Ice alert is issued.

## Central Node
All nodes report to a master node by delivering JSON objects with a known shape. Data types include 'sensor', 'command', 'request' and 'alarm' and are wrapped in a standard JSON header format.  Other shapes are available for weather observations and weather warnings.

Various listeners watch the incoming packets and are responsible for filtering data for the front-end, storing records in the database and issuing commands to other nodes if required. For example, sensor records (received every 60 seconds on the wire) are stored in a MySQL database every 5 minutes.

## Front End
Originally this was a terminal application. Some progress has been made in producing a web front end using HTML, CSS and Vanilla JavaScript. I had a strong desire to learn vanilla JavaScript and this project became a focus for that learning. Using the Eclipse Paho MQTT library allowed me to connect to the MQTT broker using web sockets. Each message received from the broker was parsed and the resulting data used to update DOM elements using vanilla JavaScript.

The next iteration of the front end stalled when I joined the CodeClan PSD course. Progress was made in setting up a VPS on Linode and the basics are in place.

## VPS on Linode

The VPS, Artemis, is a stock Debian 10 Linux installation. NginX has been configured as the HTTP server with TLS certificates from LetsEncrypt. Additionally, MariaDB has been installed and configured along with a secure MQTT broker (the main transport). A domain name has been attached to the VPS.

I choose to incorporate a VPS for several reasons, mainly, to gain experience using cloud services that have a public facing server (my home network is behind many NAT layers and is not publicly addressable). Being on a public network also allowed me to take time to consider and gain familiarity with security. 

All protocols are secured using TLS/SSL, this includes MQTT.  The VPS is accessed via a *Jump Box* using SSH keys.

I chose NginX as it is light weight and to gain some experience using a HTTP server other than Apache.  NginX can also act as a reverse proxy and this will allow a new backend to be developed using any language, Java, Python or Node Express.

## Learning Points / Next Steps
This project was a great learning experience and has gone through many iterations. With each iteration the code gets cleaner and more efficient but there is a long way to go. When time allows I would like to rewrite the entire application using Object Orientation and design patterns I have learned while at CodeClan.

Further, I would like to re-write the entire project in Java or C# - I believe this will expose many flaws in my programming prowess and lead to yet more fun overcoming them.
