#!/usr/bin/env python3
########################################################################
# Filename    : Lap_timer_Carl_with_buttons.py
# Description : Reports on the time lapsed between detections of a sensor.
# For this test code a push button will be the sensor for the lap.
# The circuit will flash an LED on each lap detection, and green LED to
#  indicate the fastest lap
# 2 Buttons - one to reset timings and one to display fastest lap.
# The is a countdown christmas tree to start the race.
# Does not use adafruit library to display lap times on 7 segment, 4 digit
#  display yet
#
# Author      : Carl Conliffe based on Scalextric Timer code
# Modification: 24 Jan 2020
########################################################################


# Import libraries
import RPi.GPIO as GPIO
import time
#from Adafruit_7Segment import SevenSegment

# Set i2c address for display, and display zeros
#segment = SevenSegment(address=0x70)
#segment.writeDigit(0, 0)
#segment.writeDigit(1, 0)
#segment.writeDigit(3, 0)
#segment.writeDigit(4, 0)

# Configure the Pi to use the BCM pin names
GPIO.setmode(GPIO.BCM)

# pins used for the switches, reed sensor and LEDs
reset = 16        # GPIO16 pin 36
reed = 20         # GPIO20 pin 38
fastest_lap = 21  # GPIO21 pin 40
red_led = 19      # GPIO19 pin 35, Lap indicator
green_led = 26    # GPIO21 pin 36, Fastest lap indicator
countDown5 =  25  # GPIO22 countdown LEDs on bar LED 
countDown4 =  8   # GPIO8 countdown LEDs on bar LED 
countDown3 =  7   # GPIO7 countdown LEDs on bar LED 
countDown2 = 12   # GPIO12 countdown LEDs on bar LED 
countDown1 = 13   # GPIO13 countdown LEDs on bar LED 
           
# configure outputs for LED
print('The LEDs are being configured.  Red for lap detection and green for fasted lap')
GPIO.setwarnings(False)
GPIO.setup(red_led, GPIO.OUT)     #Red LED channel 19
GPIO.setup(green_led, GPIO.OUT)   #Green LED channel 26
GPIO.setup(countDown5, GPIO.OUT)  #LED bar LED5 channel 25
GPIO.setup(countDown4, GPIO.OUT)  #LED bar LED4 channel 8
GPIO.setup(countDown3, GPIO.OUT)  #LED bar LED3 channel 7
GPIO.setup(countDown2, GPIO.OUT)  #LED bar LED2 channel 12
GPIO.setup(countDown1, GPIO.OUT)  #LED bar LED1 channel 13

# Configure inputs using event detection, pull up resistors
print('Configuring the detection input channels for the GPIO')
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Reset signal channel GPIO16 pin 36
GPIO.setup(reed, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Reed switch channel GPIO20 pin 38
GPIO.setup(fastest_lap, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #fastest_lap channel GPIO21 pin 40

# Switch off LEDs
print('Switching all LEDs off')
GPIO.output(red_led, False)
GPIO.output(green_led, False)

# Define new variables for lap counting and remembering fastest lap time
count = 0
fastest_lap = 99.99

# Funtion to run the start sequence countdown
def startSequence():
    GPIO.output(countDown5, False)  #Turn off LED
    GPIO.output(countDown4, False)  #Turn off LED
    GPIO.output(countDown3, False)  #Turn off LED
    GPIO.output(countDown2, False)  #Turn off LED
    GPIO.output(countDown1, False)  #Turn off LED
    print('Gentlemen start your engines')
    time.sleep(1)
    GPIO.output(countDown5, True)  #Turn on LED
    print('Five!')
    time.sleep(1)
    GPIO.output(countDown4, True)  #Turn off LED
    print('Four!')
    time.sleep(1)
    GPIO.output(countDown3, True)  #Turn off LED
    print('Three!')
    time.sleep(1)
    GPIO.output(countDown2, True)  #Turn off LED
    print('Two!')
    time.sleep(1)
    GPIO.output(countDown1, True)  #Turn off LED
    print('One!')
    time.sleep(1)
    GPIO.output(countDown5, False)  #Turn off LED
    GPIO.output(countDown4, False)  #Turn off LED
    GPIO.output(countDown3, False)  #Turn off LED
    GPIO.output(countDown2, False)  #Turn off LED
    GPIO.output(countDown1, False)  #Turn off LED
    print('GO!!!!')

# Function to flash red LED once
def lap_detect():
#    print('Lap was detected. Flashing a Red LED')
#    print('Red LED ON')
    GPIO.output(red_led, True)
    time.sleep(0.1)
#    print('Red LED off')
    GPIO.output(red_led, False)

# Function to repeatedly flash green LED when a fastest lap occurs
def fastest_flash():
    for i in range(0,5):
#        print('Green LED ON')
        GPIO.output(green_led, True)
        time.sleep(0.1)
#        print('Green LED OFF')
        GPIO.output(green_led, False)
        time.sleep(0.1)
    print('You just completed your fastest lap!')

# Function to write lap time to the 7 Segment display
def display(time):
    print('This is value for lap time that gets displayed in the 7 segment display')
    print('Your lap time = ', "%.3f" %time, ' seconds')
#    segment.writeDigit(1, int(str(time)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(time)[2]))
#    segment.writeDigit(4, int(str(time)[3]))
    
# Function to determine what actions to take on new lap detection
def new_lap(channel):
    lap_detect()
    global count     # This variable is the lap count.  May want to make this user inputable.
    global time_1    # This is the previous time or time at start of lap
    global time_2    # This is the current time or time at end of lap
    global lap_time  # This is the current lap time 
    global fastest_lap    # This is the fasted lap time
    if count < 1:    # This executes on the first lap only to set the start time
        time_1 = time.time()    # This is the start time and the time at the begining of lap #1
        print("Lap: " + str(count))
        count = count + 1   # Increments the lap counter
    else:
        time_2 = time.time()          # Grabs the current time
        lap_time = time_2 - time_1    # Current time minus previous time gets you the current lap time.
        print(' ')
        print("Lap: " + str(count), " Lap time = %.3f" % lap_time, ' seconds') # Prints the current lap number and lap time
        time_1 = time_2     # This sets the lap end time to be the start time of the next lap
        count = count + 1   # Increments the lap counter
        if lap_time < fastest_lap:
            print('New fastest lap!! Lap Time = ' "%.3f" % lap_time, ' seconds') # Prints the fasted lap time when it happens
            fastest_flash() # Calls function that lights the green LED ofr fastest lap indicator
            fastest_lap = lap_time    # Serts a new fasted lap standard to hit
        #if lap_time < 10:   # DOT SURE WHY IT ONLY CALLS & SEGMENT WHEN LAP TIME IS LESS THAN 10 SEC
        display(lap_time)    # Calls function that sisplays lap time on 7 Segment display

# Function to reset lap times and counts
def reset(channel):
    global count
    global fastest_lap
    count = 0
    fastest_lap = 99999
    print('Lap times reset to zero')
#    segment.writeDigit(0, 0)
#    segment.writeDigit(1, 0)
#    segment.writeDigit(3, 0)
#    segment.writeDigit(4, 0)

# Function to write the fastest lap time to the display
def display_fastest(channel):
    global fastest_lap
    print('Displaying fastest lap to 7 segment display.  Fastest lap = ' "%.3f" % fastest_lap)
#    segment.writeDigit(1, int(str(fastest_lap)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(fastest_lap)[2]))
#    segment.writeDigit(4, int(str(fastest_lap)[3]))

startSequence()   # Calls the start sequence
GPIO.add_event_detect(16, GPIO.FALLING, callback=reset, bouncetime=200) # This is reset
GPIO.add_event_detect(20, GPIO.FALLING, callback=new_lap, bouncetime=2000) # The is new lap
GPIO.add_event_detect(21, GPIO.FALLING, callback=display_fastest, bouncetime=200) # This is display fasted lap
  
try:
    
    while True:
        time.sleep(0.01)
        pass
    
finally:
    print('Done!!  The Race is over.')
#    segment = SevenSegment(address=0x70)
    GPIO.cleanup()