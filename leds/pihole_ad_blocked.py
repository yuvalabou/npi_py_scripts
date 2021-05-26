"""App to blink an LED each time a quary has been blocked."""

import RPi.GPIO as GPIO #https://github.com/friendlyarm/RPi.GPIO_NP
from time import sleep
import subprocess
import os
import signal
import atexit
from select import poll

# Settings
alertPin = 25
statusPin = 24

LOG_FILE = "/var/log/pihole.log"
MATCH_STRING = "/etc/pihole/gravity.list"
FALSE_POS = "read /etc/pihole/gravity.list"
DISABLE_FILE = "/etc/pihole/gravity.list.bck"

# Functions
def checkLogTailResult():
    if p.poll(1):
        line = f.stdout.readline()
        if MATCH_STRING in line and FALSE_POS not in line:
                alert(line)

def checkPiholeStatus():
    if piholeIsEnabled():
        GPIO.output(statusPin, GPIO.HIGH)
    else:
        GPIO.output(statusPin, GPIO.LOW)

def piholeIsEnabled():
    return not os.path.isfile(DISABLE_FILE)

def alert(logLine, blinkTime = .2):
    print("Ad Blocked!  ==>  " + logLine)
    GPIO.output(alertPin, GPIO.HIGH)
    sleep(blinkTime)
    GPIO.output(alertPin, GPIO.LOW)
    #make sure led blinks instead of staying on continuously when multiple ads are blocked in short succession
    sleep(.1)

def handleExit():
    print("Cleaning up GPIO...")
    GPIO.output(alertPin, GPIO.LOW)
    GPIO.output(statusPin, GPIO.LOW)
    GPIO.cleanup()

# Bind exit function
atexit.register(handleExit)
signal.signal(signal.SIGTERM, handleExit)
signal.signal(signal.SIGINT, handleExit)

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(alertPin, GPIO.OUT)
GPIO.setup(statusPin, GPIO.OUT)

# Tail Pihole logfile
f = subprocess.Popen(['tail','-F',LOG_FILE],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = poll()
p.register(f.stdout)

# Main loop
while True:
    checkPiholeStatus()
    checkLogTailResult()
    #reduces load
    sleep(.1)
