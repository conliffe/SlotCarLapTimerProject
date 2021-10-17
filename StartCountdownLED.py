########################################################################
# Filename    : StartCountdownLED.py
# Description : This code does a race start sequence using LED bar.  It
# uses a 5 LED segment to count down to start.  All LED's intially Lit
# then every second one turns off until all 5 are off.  You can make all
# lights turn on green for go.  This simulates a start christmas tree.
# Author      : Carl Conliffe
# Created     : 16 October 2021
# Modification: Date
########################################################################

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13,GPIO.OUT) # LED #5
GPIO.setup(12,GPIO.OUT) # LED #4
GPIO.setup(7,GPIO.OUT) # LED #3
GPIO.setup(8,GPIO.OUT) # LED #2
GPIO.setup(25,GPIO.OUT) # LED #1

# Clear all LEDs
GPIO.output(13, False)
GPIO.output(12, False)
GPIO.output(7, False)
GPIO.output(8, False)
GPIO.output(25, False)
time.sleep(1)
# Turn all LED segments on
GPIO.output(13, True)
GPIO.output(12, True)
GPIO.output(7, True)
GPIO.output(8, True)
GPIO.output(25, True)
time.sleep(1)
# Count down sequence
GPIO.output(13, False)  # Turn off LED #5
time.sleep(1)
GPIO.output(12, False)  # Turn off LED #4
time.sleep(1)
GPIO.output(7, False)   # Turn off LED #3
time.sleep(1)
GPIO.output(8, False)   # Turn off LED #2
time.sleep(1)
GPIO.output(25, False)  # Turn off LED #1
time.sleep(1)
# Go!!!!
