#!/usr/bin/env python3
===============================================================================
# Filename    : TestCode1.py
# Description : This is test code to check out how to use the Adafruit
# code in the lap timer code.
# Uses adafruit library to display lap times on 7 segment, 4 digit display
#
# Author      : Carl Conliffe
# Created     : 18 October 2021
# Modification:
===============================================================================

# Import libraries
#import time
#import board
#import busio
#import adafruit_ht16k33.segments
#from adafruit_ht16k33 import segments
import RPi.GPIO as GPIO
from Adafruit_7Segment import SevenSegment

# Set i2c address for display
segment = SevenSegment(address=0x70)

# Display zeros pn all 4 digits
segment.writeDigit(0, 0) #Left most digit of 4 (MSB)
segment.writeDigit(1, 0) #Second digit from left
segment.writeDigit(3, 0) #Third digit from left
segment.writeDigit(4, 0) #Right most digit of 4 (LSB)

# This is to set the colon. "0" is off & "1" is on
#segment.setColon(0)

#def writeDigit(self, charNumber, value, dot=False)
#segment.writeDigit(1, 10, True) # True/False turns on/off decimal point after digit

#def writeDigitRaw(self, charNumber, value):
#segment.writeDigitRaw(3, 125)
