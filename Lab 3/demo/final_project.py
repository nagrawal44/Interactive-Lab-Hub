import eventlet
eventlet.monkey_patch()

from flask import Flask, Response,render_template
from flask_socketio import SocketIO, send, emit
from subprocess import Popen, call

import time
import board
import busio
#import adafruit_apds9960.apds9960
#import adafruit_mpu6050
import json
import socket
import digitalio
import os

import signal
import sys
from queue import Queue
#from adafruit_apds9960.apds9960 import APDS9960

i2c = busio.I2C(board.SCL, board.SDA)
#mpu = adafruit_mpu6050.MPU6050(i2c)
int_pin = digitalio.DigitalInOut(board.D5)
#apds = APDS9960(i2c, interrupt_pin=int_pin)

hostname = socket.gethostname()
hardware = 'plughw:2,0'

app = Flask(__name__)
socketio = SocketIO(app)
audio_stream = Popen("/usr/bin/cvlc alsa://"+hardware+" --sout='#transcode{vcodec=none,acodec=mp3,ab=256,channels=2,samplerate=44100,scodec=none}:http{mux=mp3,dst=:8080/}' --no-sout-all --sout-keep", shell=True)

#apds.enable_proximity = True
#apds.proximity_interrupt_threshold = (0, 175)
#apds.enable_proximity_interrupt = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

def speak2me(val):
    call(f"espeak '{val}'", shell=True)
    
#speak2me("Welcome to your navigation buddy, Please tell me where you would like to go")

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/remote'

i2c = busio.I2C(board.SCL, board.SDA)

count = 0
while True:
    buttonA = digitalio.DigitalInOut(board.D23)
    buttonB = digitalio.DigitalInOut(board.D24)
    buttonA.switch_to_input()
    buttonB.switch_to_input()
   
    if buttonB.value and not buttonA.value:  # just button A pressed
        #publishing to MQTT and saying remote bot
        print(count)
        print("buttonA pressed")
        val = f"Button pressed!"
        client.publish(topic, val)
        speak2me("Remote Bot")
    if buttonA.value and not buttonB.value:  # just button B pressed
        speak2me("Ok now turn left and walk five steps, the fridge will be on your left")
    else:
        pass

        
@socketio.on('speak')
def handel_speak(val):
    call(f"espeak '{val}'", shell=True)

@socketio.on('connect')
def test_connect():
    print('connected')
    emit('after connect',  {'data':'Lets dance'})


@app.route('/')
def index():
    return render_template('index.html', hostname=hostname)

def signal_handler(sig, frame):
    print('Closing Gracefully')
    audio_stream.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
