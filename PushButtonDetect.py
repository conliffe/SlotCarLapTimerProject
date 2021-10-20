# ==============================================================================
# Filename       : PushButtonDetect.py
# Description    : This progran detects any one of 4 push buttons and counts
# how many times it is pushed.  It is testing the concept that will go into
# detecting a lap in the lap counter
# This code needs Raspberry Pi hardware and circuit electronics in order to run.
# KiCad Filename : Push Button Detector.sch
# Author         : Carl M. Conliffe
# Created        : 6 Jan 2020
# Modification   : 16 Oct 2021
# ==============================================================================

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setting GPIO for push momentary button NO switches
GPIO.setup(26,GPIO.IN) # Lane number 1 switch, yellow
GPIO.setup(19,GPIO.IN) # Lane number 2 switch, blue
GPIO.setup(13,GPIO.IN) # Lane number 3 switch, red
GPIO.setup(6,GPIO.IN) # Lane number 4 switch, green

# Setting GPIO for LEDs to indicate button pushed
GPIO.setup(5,GPIO.OUT) # Lane number 1, Yellow LED
GPIO.setup(4,GPIO.OUT) # Lane number 2, Blue LED
GPIO.setup(17,GPIO.OUT) # Lane number 3, Red LED
GPIO.setup(20,GPIO.OUT) # Lane number 4, Green LED

# Turns all lights off before starting
GPIO.output(5, False)  # Yellow light
GPIO.output(4, False)  # Blue light
GPIO.output(17, False)  # Red light
GPIO.output(20, False)  # Green light
time.sleep(5)   # All lights are off off for 5 seconds before starting

# Intitialize lap counter variables
Yellow1 = 0
Blue2 = 0
Red3 = 0
Green4 = 0

while True:
    if GPIO.input(26) == False:
        GPIO.output(5, True)    # Yellow LED
        # print ("Yellow on")
        Yellow1 = Yellow1 + 1
        time.sleep(1)
        GPIO.output(5, False)
        # print ("Yellow off")
    if GPIO.input(19) == False:
        GPIO.output(4, True)    # Blue LED
        # print ("Blue on")
        Blue2 = Blue2 + 1
        time.sleep(1)
        GPIO.output(4, False)
        # print ("Blue off")
    if GPIO.input(13) == False:
        GPIO.output(17, True)    # Red LED
        # print ("Red on")
        Red3 = Red3 + 1
        time.sleep(1)
        GPIO.output(17, False)
        # print ("Red off")
    if GPIO.input(6) == False:
        GPIO.output(20, True)    # Green LED
        # print ("Green on")
        Green4 = Green4 + 1
        time.sleep(1)
        GPIO.output(20, False)
        # print ("Green off")
    else:
        print ("Yellow = ", Yellow1, ",Blue = ", Blue2, ", Red = ", Red3, ", Green = ", Green4)


#    GPIO.output(18, True)
#    time.sleep(1)
#    GPIO.output(18, False)
#    time.sleep(1)
