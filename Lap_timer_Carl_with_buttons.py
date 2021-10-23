#!/usr/bin/env python3
# ==============================================================================
# Filename    : Lap_timer_Carl_with_buttons.py
# Description : Reports on the time lapsed between detection of a sensor.
# For this test code a momentary push button will be the sensor for the lap.
# Also will flash a yellow LED on each lap detection, and green LED to indicate
# fastest lap
# 2 Buttons - one to reset timing, and one to display fastest lap.
# This code needs Raspberry Pi hardware and circuit electronics in order to run.
# KiCad Filename: LapTimeCounter.sch
# Uses adafruit library to display lap times on 7 segment, 4 digit display
#
# Author       : Carl Conliffe based on Scalextric Timer code
# Created      : 24 Jan 2020
# Modification : 22 Oct 2021, Documentation improvements in the code.  Added GPIO2
# assignment table.  Added table for list of variables.  Added List of functions.
# Changed name of fastest_lap variable that was used for push button since it was
# used for time a well.  New name is fastestlapButton.

# Issues to debug:
#  1) Lap times over 9.99 sec do not get displayed in 7 segment display.
#     The display only shows "09:99" for 9.99 sec.  This makes sense as
#     there is not digit "0" in the display(time) function.
#  2) Need to implement 5 second countdown to start with Christmas tree.
#  3) Implement "race over" functionality based on number of laps.
#  4) When this code get uncommented and fastest lap goes to 7 segment
#     the green push button to display fastest lap not longer works. See
#     display_fastest() function.  Lines 154.
# ==============================================================================

# ================================ GPIO ASSIGNMENTS ===============================================
# GPIO Name/Num   | Pin | Variable/Signal | I/O || GPIO Name/Num   | Pin | Variable/Signal | I/O ||
# ----------------|-----|-----------------|-----||-----------------|-----|-----------------|-----||
# 3.3V            |  1  | N/A             | Out || 5V              |  2  | N/A             | Out ||
# I2C SDA  GPIO2  |  3  |                 |     || 5V              |  4  | N/A             | Out ||
# I2C SCL  GPIO3  |  5  |                 |     || GND             |  6  | N/A             | Out ||
#          GPIO4  |  7  |                 | In  || UART TXD GPIO14 |  8  |                 |     ||
# GND             |  9  | N/A             | Out || UART RXD GPIO15 | 10  |                 |     ||
#          GPIO17 | 11  |                 | In  || PCM CLK  GPIO18 | 12  |                 |     ||
#          GPIO27 | 13  |                 | In  || GND             | 14  | N/A             | Out ||
#          GPIO22 | 15  |                 | Out ||          GPIO23 | 16  |                 | Out ||
# 3.3V            | 17  | N/A             | Out ||          GPIO24 | 18  |                 | Out ||
# SPI MOSI GPIO10 | 19  |                 |     || GND             | 20  | N/A             | Out ||
# SPI MISO GPIO9  | 21  |                 |     ||          GPIO25 | 22  | led_5           | Out ||
# SPI SCLK GPIO11 | 23  |                 |     || SPI CE0  GPIO8  | 24  | led_4           | Out ||
# GND             | 25  | N/A             | Out || SPI CE1  GPIO7  | 26  | led_3           | Out ||
# ID SD           | 27  | N/A             |     || ID SC           | 28  | N/A             |     ||
#          GPIO5  | 29  |                 | In  || GND             | 30  | N/A             | Out ||
#          GPIO6  | 31  |                 | In  ||          GPIO12 | 32  | led_2           | Out ||
#          GPIO13 | 33  | led_1           | Out || GND             | 34  | N/A             | Out ||
# PCM FS   GPIO19 | 35  | yellow_led      | Out ||          GPIO16 | 36  | reset           | In  ||
#          GPIO26 | 37  | green_led       | Out || PCM DIN  GPIO20 | 38  | reed            | In  ||
# GND             | 39  | N/A             | Out || PCM DOUT GPIO21 | 40  | fastestLapButton| In  ||
# =================================================================================================

# +++++++++++ List of variables +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# count                     # Counts the number of laps.
# fastestLapButton          # This is the push button switch that request the fasted lap of the race be displayed.
# fastest_lap               # This is a global variable that is the fastest lap time.
# i                         # Index for loops.
# green_led                 # is the output to drive the green LED.
# lap_time                  # This is a global variable that is the current lap time.
# led_1, 2, 3, 4, 5         # Each represents an LED on the countdown christmas tree for race start.
# reed                      # TBD
# reset                     # Input to GPIO to reset lap counter & time
# yellow_led                # is the output to drive the yellow LED
# segment                   # Address of the Adafruit 7 segment Featherwing 4 digit LED display
# time_1                    # This is a global variable that is the previous time (time at start of lap)
# time_2                    # This is a global variable that is the current time (time at end of lap)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ---------- List of functions -----------------------------------------------------------------------
# display(time)               --  Displays current lap time to 7 segment display.
# displayFastestLap(channel)  --  Displays fasted lap to 7 segment display [not used yet]
# fastest_flash()             --  Flashes the green LED when a fastest lap occurs.
# lap_detect()                --  Blinks yellow lap indicator LED once when lap is detected.
# newLap(channel)             --  Determines what to do when a new lap is detected (increment lap counter, compute lap times & fasted lap)
# reset(channel)              --  Resets the race laps and fastest lap number
# -----------------------------------------------------------------------------------------------------

# Import libraries
import RPi.GPIO as GPIO
import time
from Adafruit_7Segment import SevenSegment

# Set i2c address for display, and display zeros
segment = SevenSegment(address=0x70)
segment.writeDigit(0, 0)
segment.writeDigit(1, 0)
segment.writeDigit(3, 0)
segment.writeDigit(4, 0)

# Configure the Pi to use the BCM pin names
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #to disable warnings

# pins used for the switches, reed sensor and LED
reset = 16  # GPIO16 pin 36, I think this is connected to a momentary switch to reset the timer
reed = 20   # GPIO20 pin 38
fastestLapButton = 21    #GPIO21 pin 40.  This is fasted lap request button.
yellow_led = 19    #GPIO19 pin 35
green_led = 26  #GPIO26 pin 37
led_5 = 25  #GPIO25 pin 22, Bar LED #5
led_4 = 8   #GPIO8 pin 24, Bar LED #4
led_3 = 7   #GPIO7 pin 26, Bar LED #3
led_2 = 12  #GPIO12 pin 32, Bar LED #2
led_1 = 13  #GPIO13 pin 33, Bar LED #1

# configure outputs for LED
print('The LEDs are being configured.  yellow for lap detection and green for fasted lap')
GPIO.setup(yellow_led, GPIO.OUT) #Yellow LED channel 19
GPIO.setup(green_led, GPIO.OUT)  #Green LED channel 26
GPIO.setup(led_5, GPIO.OUT)      #Bar LED #5 channel 25
GPIO.setup(led_4, GPIO.OUT)      #Bar LED #4 channel 8
GPIO.setup(led_3, GPIO.OUT)      #Bar LED #3 channel 7
GPIO.setup(led_2, GPIO.OUT)      #Bar LED #2 channel 12
GPIO.setup(led_1, GPIO.OUT)      #Bar LED #1 channel 13

# Configure inputs using event detection, pull up resistors
print('Configuring the detection input channels for the GPIO')
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Reset signal channel GPIO16 pin 36
GPIO.setup(reed, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Reed switch channel GPIO20 pin 38
GPIO.setup(fastestLapButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #fastest_lap channel GPIO21 pin 40

# Switch off LEDs
print('Switching all LEDs off')
GPIO.output(yellow_led, False)
GPIO.output(green_led, False)
GPIO.output(led_5, False)
GPIO.output(led_4, False)
GPIO.output(led_3, False)
GPIO.output(led_2, False)
GPIO.output(led_1, False)

# Define new variables for lap counting and remembering fastest lap time
count = 0
fastest_lap = 99999

# Function to flash yellow LED once
def lap_detect():
    print('Lap was detected. Flashing a yellow LED')
    print('yellow LED ON')
    GPIO.output(yellow_led, True)  # turns yellow LED on
    time.sleep(0.1)
    print('yellow LED off')    # turns yellow LED off
    GPIO.output(yellow_led, False)

# Function to repeatedly flash green LED when a fastest lap occurs
def fastest_flash():
    for i in range(0,5):     #Loop to control number of flashes for fastest lap.
        print('You just completed your fastest lap!')
        print('Green LED ON')
        GPIO.output(green_led, True)    # turns green LED on for time secs below.
        time.sleep(0.1)
        print('Green LED OFF')
        GPIO.output(green_led, False)  # turns green LED on
        time.sleep(0.1)

# Function to write lap time to the 7 Segment display
def display(time):
    print('This is value for lap time that gets displayed in the 7 segment display')
    print('Your lap time = ', "%.3f" %time, ' seconds')
    segment.writeDigit(1, int(str(time)[0]))
    segment.setColon(True)
    segment.writeDigit(3, int(str(time)[2]))
    segment.writeDigit(4, int(str(time)[3]))

# Function to determine what actions to take on new lap detection
def new_lap(channel):
    lap_detect()
    global count    # This variable is the lap count.  May want to make this user inputable.
    global time_1    # This is the previous time or time at start of lap
    global time_2    # This is the current time or time at end of lap
    global lap_time  # This is the current lap time
    global fastest_lap    # This is the fasted lap time
    if count < 1:   # This executes on the first lap only to set the start time
        time_1 = time.time()    # this is the start time and the time at the begining of lap #1
        print("Lap: " + str(count))
        count = count + 1   # Increments the lap counter
    else:
        time_2 = time.time()    # Grabs the current time
        lap_time = time_2 - time_1    # Current time minus previous time gets you the current lap time.
        print(' ')
        print("Lap: " + str(count)) # Prints the current lap number completed
        print("%.3f" % lap_time, ' seconds')    # Prints the lap time to 3 decimal places
        time_1 = time_2    # This sets the lap end time to be the start time of the next lap
        count = count + 1   # Increments the lap counter
        if lap_time < fastest_lap:
            print('New fastest lap!! Lap Time =' "%.3f" % lap_time, ' seconds') # Prints the fasted lap time when it happens
            fastest_flash() # Calls function that lights the green LED ofr fastest lap indicator
            fastest_lap = lap_time    # Serts a new fasted lap standard to hit
        if lap_time < 10:   # DOT SURE WHY IT ONLY CALLS & SEGMENT WHEN LAP TIME IS LESS THAN 10 SEC
            display(lap_time)    # Calls function that sisplays lap time on 7 Segment display

# Function to reset lap times and counts
def reset(channel):
    global count
    global fastest_lap
    count = 0
    fastest_lap = 99999
    print('Lap times reset to zero')
    segment.writeDigit(0, 0)
    segment.writeDigit(1, 0)
    segment.writeDigit(3, 0)
    segment.writeDigit(4, 0)

# Function to write the fastest lap time to the display
def display_fastest(channel):
    global fastest_lap
    print('Displaying fastest lap to 7 segment display.  Fastest lap = ' "%.3f" % fastest_lap)
#    segment.writeDigit(1, int(str(fastest_lap)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(fastest_lap)[2]))
#    segment.writeDigit(4, int(str(fastest_lap)[3]))

#while True:
#    buttonPushed = input("Type 'reset', 'fast lap', 'new lap' or 'go' to simulate button pushed or sensor : ")    # Simulate button pushing
#    if buttonPushed == "reset":
#        reset(36)
GPIO.add_event_detect(16, GPIO.FALLING, callback=reset, bouncetime=200) # This is reset
#    if buttonPushed == "new lap":
#        new_lap(24)
GPIO.add_event_detect(20, GPIO.FALLING, callback=new_lap, bouncetime=2000) # The is new lap
#    if buttonPushed == "fast lap":
#        display_fastest(23)
GPIO.add_event_detect(21, GPIO.FALLING, callback=display_fastest, bouncetime=200) # This is display fasted lap

try:

    while True:
        time.sleep(0.01)
        pass

finally:
    print('Done!!  The Race is over.')
#    segment = SevenSegment(address=0x70)
#    GPIO.cleanup()
