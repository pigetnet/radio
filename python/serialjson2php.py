#!/usr/bin/python
from lib import Socket
from lib import PhpRequest
from lib import Lock
import sys
import time
import os
import serial
import json
import string

""" Main Program """

""" Variables """
timeout = 3
time_end = 0
last_data = ""
lock = False
data = ""
path = "/do/kana/www"


# Get port
with open('/do/radio/python/port', 'r') as port_file:
    content = port_file.read()
    socket_port = int(content.strip())

# Get configuration
with open('/user/config/radio/radio.json') as settings_file:
    settings = json.load(settings_file)

serial_port = settings["port"]
serial_speed = int(settings["speed"])

Socket.Start(socket_port)

"""
Json (to move to JsonParser)
"""


def is_json(jsonLine):
    try:
        json_object = json.loads(jsonLine)
    except ValueError, e:
        return False
    return True

"""
Serial
"""
try:
    ser = serial.Serial(serial_port, serial_speed, timeout=1)
except:
    print "Serial connection failed"
    print "speed:" + serial_speed
    print "port:" + serial_port
    os._exit(12)
# Flush Buffer
ser.flushInput()

print "Serial:"+str(serial_port)

try:
    while True:
        data = False
        try:
                data = ser.readline().strip()
                message = Socket.Listen()
        # print message
        except:
            print "Close Communication : Serial Communication failure"
            os._exit(2)

        if message is not False:
            # print "Founded something to tell to the arduino"
            # print message
            ser.write(message + "\n")

        if data:
            print data
            if is_json(data):
                json_object = json.loads(data)
                # print json_object
                if 'data' in json_object:
                    dataRaw = json_object['data']
                    if dataRaw == last_data:
                        lock = Lock.check(timeout, time_end)
                        time_end = lock[0]
                        lock = lock[1]
                        print "BLOCKED------"
                        print "LAST:" + str(last_data)
                        print "NEW:" + str(dataRaw)
                        print "BLOCKED------"
                    else:
                        lock = False

                    if lock is False:
                        last_data = dataRaw
                        print "SENDING-----"
                        print "Serial:"+str(dataRaw)
                        PhpRequest.send(path, dataRaw)
                        Socket.Send(dataRaw)
                        data = False
                        print "SENDING-----"
except KeyboardInterrupt:
    print "Closing Collector : Keyboard Interrupt"
    # server_socket.close()
    ser.close()
    os._exit(13)
