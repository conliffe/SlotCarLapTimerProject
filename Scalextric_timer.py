# Scalextric Timer
# Reports on the time lapsed between detections on the reed sensor
# Also flashes an LED on each lap detection, and green to indicate fastest lap
# 2 Buttons - one to reset timings, one to display fastest lap
# Uses adafruit library to display lap times on 7 segment, 4 digit display

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

# pins used for the switches, reed sensor and LED
reset = 18
fastest_lap = 23
reed = 24
red_led = 17
green_led = 27

# configure outputs for LED
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)

# Configure inputs using event detection, pull up resistors
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fastest_lap, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reed, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Switch off LEDs
GPIO.output(red_led, False)
GPIO.output(green_led, False)

# Define new variables for lap counting and remembering fastest lap time
count = 0
fastest_lap = 99.99

# Function to flash red LED once
def lap_detect():
    GPIO.output(red_led, True)
    time.sleep(0.1)
    GPIO.output(red_led, False)

# Function to repeatedly flash green LED
def fastest_flash():
    for i in range(0,5):
        GPIO.output(green_led, True)
        time.sleep(0.1)
        GPIO.output(green_led, False)
        time.sleep(0.1)

# Function to write time to display
def display(time):
    segment.writeDigit(1, int(str(time)[0]))
    segment.setColon(True)
    segment.writeDigit(3, int(str(time)[2]))
    segment.writeDigit(4, int(str(time)[3]))
    
# Function to determine what actions to take on new lap detection
def new_lap(channel):
    lap_detect()
    global count
    global time_1
    global time_2
    global lap_time
    global fastest_lap
    if count < 1:
        time_1 = time.time()
        print("Lap: " + str(count))
        count += 1
    else:
        time_2 = time.time()
        lap_time = time_2 - time_1
        print(' ')
        print("Lap: " + str(count))
        print("%.2f" % lap_time)
        time_1 = time_2
        count += 1
        if lap_time < fastest_lap:
            print('New fastest lap!!')
            fastest_flash()
            fastest_lap = lap_time
        if lap_time < 10:
            display(lap_time)

# Function to reset lap times and counts
def reset(channel):
    global count
    global fastest_lap
    count = 0
    fastest_lap = 99999
    print('Lap times reset')
    segment.writeDigit(0, 0)
    segment.writeDigit(1, 0)
    segment.writeDigit(3, 0)
    segment.writeDigit(4, 0)

# Function to write the fastest lap time to the display
def display_fastest(channel):
    global fastest_lap
    segment.writeDigit(1, int(str(fastest_lap)[0]))
    segment.setColon(True)
    segment.writeDigit(3, int(str(fastest_lap)[2]))
    segment.writeDigit(4, int(str(fastest_lap)[3]))

GPIO.add_event_detect(18, GPIO.FALLING, callback=reset, bouncetime=200)
GPIO.add_event_detect(23, GPIO.FALLING, callback=display_fastest, bouncetime=200)
GPIO.add_event_detect(24, GPIO.FALLING, callback=new_lap, bouncetime=2000)


try:
    
    while True:
        time.sleep(0.01)
        pass
    
finally:
    segment = SevenSegment(address=0x70)
    GPIO.cleanup()  

    
