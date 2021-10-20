===============================================================================
# Author      : Carl M. Conliffe
# Date        : 2 January 2020
# Description : This program simulates a traffic signal.
# It stays green for 20 secounds this goes yellow for 2 seconds
# then stays red for 20 seconds.
# This code needs Raspberry Pi hardware and circuit electronics in order to run.
===============================================================================

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)

# Turns all lights off before starting
GPIO.output(21, False)  # Green light
GPIO.output(23, False)  # Yellow light
GPIO.output(16, False)  # Red light
time.sleep(5)   # All lights are off off for 5 seconds before starting


while True:
    # Green Light
    GPIO.output(21, True)   # Light turns on
    time.sleep(10)  # Light stays on for this amount of seconds
    GPIO.output(21, False)
#    time.sleep(1)

    # Yellow Light
    GPIO.output(23, True)   # Light turns on
    time.sleep(2)   # Light stays on for this amount of seconds
    GPIO.output(23, False)
#    time.sleep(1)

    #Red Light
    GPIO.output(16, True)   # Light turns on
    time.sleep(10)  # Light stays on for this amount of seconds
    GPIO.output(16, False)
#    time.sleep(1)
