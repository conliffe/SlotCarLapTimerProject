# Scalextric Timer
# Reports on the time lapsed between detections on the reed sensor
# Also flashes an LED on each lap detection, and green to indicate fastest lap
# 2 Buttons - one to reset timings, one to display fastest lap
# Uses adafruit library to display lap times on 7 segment, 4 digit display

# Carl Conliffe modified as a tool to learn the code

# Import libraries
#import RPi.GPIO as GPIO
import time
#from Adafruit_7Segment import SevenSegment

# Set i2c address for display, and display zeros
#segment = SevenSegment(address=0x70)
#segment.writeDigit(0, 0)
#segment.writeDigit(1, 0)
#segment.writeDigit(3, 0)
#segment.writeDigit(4, 0)

# Configure the Pi to use the BCM pin names
#GPIO.setmode(GPIO.BCM)

# pins used for the switches, reed sensor and LED
reset = 18  # I think this is connected to a momentary switch to reset the timer
fastest_lap = 23
reed = 24
red_led = 17
green_led = 27

# configure outputs for LED
print('The LEDs are being configured.  Red for lap detection and green for fasted lap')
#GPIO.setup(red_led, GPIO.OUT)    #Red LED channel 17
#GPIO.setup(green_led, GPIO.OUT)     #Green LED channel 27

# Configure inputs using event detection, pull up resistors
print('Configuring the detection input channels for the GPIO')
#GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Reset signal channel 18
#GPIO.setup(fastest_lap, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #fastest_lap channel 23
#GPIO.setup(reed, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #reed switch channel 24

# Switch off LEDs
print('Switching all LEDs off')
#GPIO.output(red_led, False)
#GPIO.output(green_led, False)

# Define new variables for lap counting and remembering fastest lap time
count = 0
fastest_lap = 99.99

# Function to flash red LED once
def lap_detect():
    print('Lap was detected. Flashing a Red LED')
    print('Red LED ON')
#    GPIO.output(red_led, True)
#    time.sleep(0.1)
    print('Red LED off')
#    GPIO.output(red_led, False)

# Function to repeatedly flash green LED when a fastest lap occurs
def fastest_flash():
    for i in range(0,5):
        print('You just completed your fastest lap!')
        print('Green LED ON')
#        GPIO.output(green_led, True)
        time.sleep(0.1)
        print('Green LED OFF')
#        GPIO.output(green_led, False)
        time.sleep(0.1)

# Function to write lap time to the 7 Segment display
def display(time):
    print('This is value for lap time that gets displayed in the 7 segment display')
    print('Your lap time = ', "%.3f" %time)
#    segment.writeDigit(1, int(str(time)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(time)[2]))
#    segment.writeDigit(4, int(str(time)[3]))

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
        print("Lap: " + str(count)) # Prings the current lap number completed
        print("%.2f" % lap_time)    # Prints the lap time to 2 decimal places
        time_1 = time_2    # This sets the lap end time to be the start time of the next lap
        count = count + 1   # Increments the lap counter
        if lap_time < fastest_lap:
            print('New fastest lap!! Lap Time =' "%.3f" % lap_time) # Prints the fasted lap time when it happens
            fastest_flash() # Calls function that lights the green LED ofr fastest lap indicator
            fastest_lap = lap_time    # Serts a new fasted lap standard to hit
        if lap_time < 10:   # DOT SURE WHY IT ONLT CALLS & SEGMENT WHEN LAP TIME IS LESS THAN 10 SEC
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

while True:
    buttonPushed = input("Type 'reset', 'fast lap', 'new lap' or 'go' to simulate putton pushed or sensor : ")    # Simulate button pushing
    if buttonPushed == "reset":
        reset(18)
    #GPIO.add_event_detect(18, GPIO.FALLING, callback=reset, bouncetime=200)
    if buttonPushed == "fast lap":
        display_fastest(23)
    #GPIO.add_event_detect(23, GPIO.FALLING, callback=display_fastest, bouncetime=200)
    if buttonPushed == "new lap":
        new_lap(24)
    #GPIO.add_event_detect(24, GPIO.FALLING, callback=new_lap, bouncetime=2000)
    try:

        while True:
            time.sleep(0.01)
            pass

    finally:
        print('Done!!  The Race is over.')
#    segment = SevenSegment(address=0x70)
#    GPIO.cleanup()
