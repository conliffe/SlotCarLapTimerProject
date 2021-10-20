# =============================================================================
# Filename    : fileneme.py
# Description : This test code gets input from the user and has it writen to
# 7 segment Adafruit display.  This code uses a simple circcuit that drives the
# Adafruit 4 digit 7 segment featherwing display.
# Author      : Carl Conliffe
# Created     : 18 October 2021
# Modification: Date
# =============================================================================

import time
import board
import busio
import adafruit_ht16k33.segments
from adafruit_ht16k33 import segments

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
#display = segments.Seg7x4(i2c)
display = adafruit_ht16k33.segments.Seg7x4(i2c)
#display = adafruit_ht16k33.Seg7x4(i2c, address=0x70)

# Clear the display.
display.fill(0)

displayValue = input("Enter Date to display on 7 segment: ")  3Request value from user

# Can just print a number
#display.print(8586)
#display[0] = '1'  # Most significant digit
#display[1] = '2'
#display[2] = '3'
#display[3] = 'F'  # Least significant digit


#display.show()
#display.fill(0)
display.print(displayValue)
#time.sleep(1)
