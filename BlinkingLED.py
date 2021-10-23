# ==============================================================================
# Filename    : BlinkingLED.py
# Description : This code makes an LED blink at 1 second interval
# This code needs Raspberry Pi hardware and circuit electronics in order to run.
# Author      : CanaKit Exercise
# Date        : 2 January 2020
# ==============================================================================

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

while True:
    GPIO.output(18, True)
    time.sleep(1)
    GPIO.output(18, False)
    time.sleep(1)
