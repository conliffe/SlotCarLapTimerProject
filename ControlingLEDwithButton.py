# Author: CanaKit Exercise
# Date: 2 January 2020
# Description: TWhen you push the button the Red LED turns on.

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT) # Red LED
GPIO.setup(25,GPIO.IN)

while True:
    if GPIO.input(25):  # When you push button input goes false
        GPIO.output(18, False)
    else:
        GPIO.output(18, True)
