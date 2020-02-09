#!/usr/bin/env python3
########################################################################
# Filename    : SlotCarlapTimer.py
# Description : This code is for a Raspberry Pi circuit that will detect slot
# car laps and lime them.  It used IR sensors.  The program will calculate lap
# time, fasted lap and time a race duration for the number of laps inputed by
# the user as the race duration.  There is also a countdown to start shown with
# 5 LEDs.  Data fro the race is reported to a .csv file while also being
# displayed to the screne.  There are also 4 push buttons that 1) rested lap
# time and counter, 2) force a lap to be counted.  This is a debug feature and
# not used for a real race.  3) display fasted lap on request during the race
# and 4) lets user trigger start of race.  This is prompted from the screen
# display.
# The circuit will flash an LED on each lap detection, and green LED to
# indicate the fastest lap.  The schematic name that coresponds to this code is
# "Lap_Timer_Counter.sch" drans in KiCad.
# Program does not currently use adafruit library to display lap times on 7
# segment, 4 digit display yet
#
# Author      : Carl Conliffe based on Scalextric Timer code
# Modification: 8 February 2020
########################################################################

# ================================ GPIO ASSIGNMENTS ===============================================
# GPIO Name/Num   | Pin | Variable/Signal | I/O || GPIO Name/Num   | Pin | Variable/Signal | I/O ||
# ----------------|-----|-----------------|-----||-----------------|-----|-----------------|-----||
# 3.3V            |  1  | N/A             | Out || 5V              |  2  | N/A             | Out ||
# I2C SDA  GPIO2  |  3  |                 |     || 5V              |  4  | N/A             | Out ||
# I2C SCL  GPIO3  |  5  |                 |     || GND             |  6  | N/A             | Out ||
#          GPIO4  |  7  | lapSensor1      | In  || UART TXD GPIO14 |  8  |                 |     ||
# GND             |  9  | N/A             | Out || UART RXD GPIO15 | 10  |                 |     ||
#          GPIO17 | 11  | getFastestLap   | In  || PCM CLK  GPIO18 | 12  |                 |     ||
#          GPIO27 | 13  | startRace       | In  || GND             | 14  | N/A             | Out ||
#          GPIO22 | 15  | redLed          | Out ||          GPIO23 | 16  | countDown4      | Out ||
# 3.3V            | 17  | N/A             | Out ||          GPIO24 | 18  | countDown3      | Out ||
# SPI MOSI GPIO10 | 19  |                 |     || GND             | 20  | N/A             | Out ||
# SPI MISO GPIO9  | 21  |                 |     ||          GPIO25 | 22  | countDown5      | Out ||
# SPI SCLK GPIO11 | 23  |                 |     || SPI CE0  GPIO8  | 24  |                 |     ||
# GND             | 25  | N/A             | Out || SPI CE1  GPIO7  | 26  |                 |     ||
# ID SD           | 27  | N/A             |     || ID SC           | 28  | N/A             |     ||
#          GPIO5  | 29  | lapSensor2      | In  || GND             | 30  | N/A             | Out ||
#          GPIO6  | 31  | lapSensorTest   | In  ||          GPIO12 | 32  | countDown2      | Out ||
#          GPIO13 | 33  | countDown1      | Out || GND             | 34  | N/A             | Out ||
# PCM FS   GPIO19 | 35  |                 |     ||          GPIO16 | 36  | reset           | In  ||
#          GPIO26 | 37  | greenLed        | Out || PCM DIN  GPIO20 | 38  |                 |     ||
# GND             | 39  | N/A             | Out || PCM DOUT GPIO21 | 40  |                 |     ||
# =================================================================================================


###### List of variables ###########
# channel
# countDown1, 2, 3, 4, 5
# currentTime               # Stores the current Time
# driverName                # Name of the driver
# fastestLap                # This is the fastest lap of the race
# fastestLapInString        # fasted lap time as a string and not float
# getFastestLap
# greenled
# i
# lapNumber                 # This is the current lap number the racer is on.
# lapSensor1
# lapSensor2
# lapSensorTest
# lapTime                   # Stores the lap time for the current lap
# lapTimeInString           # Stores the lap time as a string and not float
# numberOfLaps              # Number of laps in the race.  User inputted value
# previousTime              # This is the current time at the start of the lap
# raceFinishTime            # This is the time in epoch at race finish
# raceFinishTimeFormatted   # This is the human readable time at race finish
# raceStartTime             # This is the time in epoch at race start
# raceStartTimeFormatted    # This is the human readable time at race start
# redLed
# reset
# startRace
# time
####################################

###### List of funcions ############
# display(time)
# displayFastestLap(channel)
# endingRoutine()
# fastestLapLEDflash
# inputRaceData()
# lapDetect()
# logDataToCSV()
# logFinalDataToCSV()
# newLap(channel)
# openCSVFile()
# reset(channel)
# startSequence()
####################################


# Import libraries
import RPi.GPIO as GPIO    # Has setups for using GPIO with Raspberry Pi board
import time     # Has all the time funtions I need
import sys      # Has function to exit program
import csv      # Has functions to handle .csv files
#from Adafruit_7Segment import SevenSegment

# Set i2c address for display, and display zeros
#segment = SevenSegment(address=0x70)
#segment.writeDigit(0, 0)
#segment.writeDigit(1, 0)
#segment.writeDigit(3, 0)
#segment.writeDigit(4, 0)

# Configure the Pi to use the BCM pin names
GPIO.setmode(GPIO.BCM)

# Pin assignments used for the switches, IR diodes as sensor and LEDs
reset = 16          # GPIO16 pin 36, lap and fastest lap reset
lapSensor1= 4       # GPIO4 pin 7, This is for the break IR beam sensor
lapSensor2= 5       # GPIO5 pin 29, This is for the reflective IR sensor
lapSensorTest= 6    # GPIO6 pin 31, This is for the push button lap trigger
getFastestLap = 17  # GPIO17 pin 11, This is a push button to display fastest lap
startRace = 27      # GPIO27 pin 13, This is a push button to start the race
redLed = 22         # GPIO22 pin 15, Lap indicator
greenLed = 26       # GPIO26 pin 37, Fastest lap indicator
countDown5 = 25     # GPIO25 pin 22, countdown LEDs on bar LED
countDown4 = 23     # GPIO23 pin 16, countdown LEDs on bar LED
countDown3 = 24     # GPIO24 pin 18, countdown LEDs on bar LED
countDown2 = 12     # GPIO12 pin 32, countdown LEDs on bar LED
countDown1 = 13     # GPIO13 pin 33, countdown LEDs on bar LED

# configure outputs for LED
print('The LEDs are being configured.  Red for lap detection and green for fasted lap.')
GPIO.setwarnings(False)
GPIO.setup(redLed, GPIO.OUT)      # Red LED channel 22
GPIO.setup(greenLed, GPIO.OUT)    # Green LED channel 26
GPIO.setup(countDown5, GPIO.OUT)  # LED bar LED5 channel 25
GPIO.setup(countDown4, GPIO.OUT)  # LED bar LED4 channel 23
GPIO.setup(countDown3, GPIO.OUT)  # LED bar LED3 channel 24
GPIO.setup(countDown2, GPIO.OUT)  # LED bar LED2 channel 12
GPIO.setup(countDown1, GPIO.OUT)  # LED bar LED1 channel 13

# Configure inputs using event detection, pull up resistors
print('Configuring the detection input channels for the GPIO')
GPIO.setup(reset, GPIO.IN, pull_up_down=GPIO.PUD_UP)          # Reset signal channel GPIO16 pin 36
GPIO.setup(lapSensorTest, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # lapSensorTest switch channel GPIO6 pin 31
GPIO.setup(lapSensor1, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # lapSensor1 channel GPIO4 pin 7
GPIO.setup(lapSensor2, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # lapSensor2 channel GPIO5 pin 39
GPIO.setup(getFastestLap, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # getFastestLap channel GPIO17 pin 11
GPIO.setup(startRace, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # startRace channel GPIO27 pin 13

# Switch off LEDs
print('Switching all LEDs off')
GPIO.output(redLed, False)
GPIO.output(greenLed, False)

# Define new variables for lap counting and remembering fastest lap time
numberOfLaps = 0
fastestLap = 9999
lapNumber = 0
lapTime = 0

## This section of code is where all the functions exist ##
# Funtion to run the start sequence countdown
def startSequence():
    global raceStartTimeFormatted
    global raceStartTime
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
    GPIO.output(countDown4, True)  #Turn on LED
    print('Four!')
    time.sleep(1)
    GPIO.output(countDown3, True)  #Turn on LED
    print('Three!')
    time.sleep(1)
    GPIO.output(countDown2, True)  #Turn on LED
    print('Two!')
    time.sleep(1)
    GPIO.output(countDown1, True)  #Turn on LED
    print('One!')
    time.sleep(1)
    GPIO.output(countDown5, False)  #Turn off LED
    GPIO.output(countDown4, False)  #Turn off LED
    GPIO.output(countDown3, False)  #Turn off LED
    GPIO.output(countDown2, False)  #Turn off LED
    GPIO.output(countDown1, False)  #Turn off LED
    print('GO!!!!')
    raceStartTime = time.localtime()    # This returns the local start time of the race
    raceStartTimeFormatted = time.strftime("%a, %d %b %Y %H:%M:%S %Z", raceStartTime)
    raceStartTime = time.time()         # This returns the start time of the race as epoch
    print('\nOfficial Race Start Time = ', raceStartTimeFormatted)

# Function to flash LED once lap is detected
def lapDetect():
    GPIO.output(redLed, True)    # Turns red LED on
    time.sleep(0.1)
    GPIO.output(redLed, False)    # Turns red LED off

# Function to repeatedly flash green LED when a fastest lap occurs
def fastestLapLEDflash():
    for i in range(0,5):
        GPIO.output(greenLed, True)    # Turns green LED on
        time.sleep(0.1)
        GPIO.output(greenLed, False)    # Turns green LED off
        time.sleep(0.1)
    print('You just completed your fastest lap!')

# Function to write lap time to the 7 Segment display
def display(time):
    print('This is value the for lap time that gets displayed in the 7 segment display')
    print('Your lap time = ', "%.3f" %time, ' seconds')
#    segment.writeDigit(1, int(str(time)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(time)[2]))
#    segment.writeDigit(4, int(str(time)[3]))

# Function to open, create and configure .csv file
def openCSVFile():
    print("Creating .csv file")
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['This is data for: ', raceName])
        data_writer.writerow(['This race will consist of (laps):', numberOfLaps])
        data_writer.writerow(['On lane #1 is car UID#:', lane1CarUID])
        data_writer.writerow(['Lap #', 'Lap Time (sec)', 'Fastest Lap(sec)'])

# Function to write data to .csv file for one line at a time
def writeDatatoCSVFile():
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([lapNumber, lapTime, fastestLap])

# Function to determine what actions to take on new lap detection
def newLap(channel):
    lapDetect()
    global numberOfLaps    # This variable is the lap count.  May want to make this user inputable.
    global lapNumber       # This is the current lap the racer is on
    global previousTime    # This is the previous time or time at start of lap
    global currentTime     # This is the current time or time at end of lap
    global lapTime         # This is the current lap time
    global fastestLap      # This is the fasted lap time
    if lapNumber == 0:   # First lap detection is crossing start/finish/lap sensor
        previousTime = time.time()    # This is the start time and the time at the begining of lap #1
        print('Crossed Start/Finish.  You are racing!')
        lapNumber += 1   # Increments the lap counter
#        writeDatatoCSVFile()
    else:
        currentTime = time.time()          # Grabs the current time
        lapTime = currentTime - previousTime    # Current time minus previous time gets you the current lap time.
        print(' ')
        print('Lap #', lapNumber, " Lap time = %.3f" % lapTime, ' seconds') # Prints the current lap number and lap time
        previousTime = currentTime     # This sets the lap end time to be the start time of the next lap
        if lapTime < fastestLap:
            print('New fastest lap!! Lap Time = ' "%.3f" % lapTime, ' seconds') # Prints the fasted lap time when it happens
            fastestLapLEDflash() # Calls function that lights the green LED ofr fastest lap indicator
            fastestLap = lapTime    # Sets a new fasted lap standard to hit
        writeDatatoCSVFile()
        #if lapTime < 10:   # NOT SURE WHY IT ONLY CALLS & SEGMENT WHEN LAP TIME IS LESS THAN 10 SEC
        display(lapTime)    # Calls function that displays lap time on 7 Segment display
        if numberOfLaps == lapNumber:
            endingRoutine()
        else:
            lapNumber += 1   # Increments the lap counter

# Function to reset lap times and counts
def reset(channel):
    global count
    global fastestLap
    lapNumber = 0
    fastestLap = 99999
    print('Lap times reset to zero')
#    segment.writeDigit(0, 0)
#    segment.writeDigit(1, 0)
#    segment.writeDigit(3, 0)
#    segment.writeDigit(4, 0)

# Function to write the fastest lap time to the display
def displayFastestLap(channel):
    global fastestLap
    print('Displaying fastest lap to 7 segment display.  Fastest lap = ' "%.3f" % fastestLap)
#    segment.writeDigit(1, int(str(fastestLap)[0]))
#    segment.setColon(True)
#    segment.writeDigit(3, int(str(fastestLap)[2]))
#    segment.writeDigit(4, int(str(fastestLap)[3]))

# Funtion for user to input race data
def inputRaceData():
    global numberOfLaps
    global raceName
    global lane1CarUID
    global driverName
    raceName = input("Enter Race Name: ")    # Enter the race information
    numberOfLaps = int(input("Enter The Number of Laps: "))  # Typecasting
    lane1CarUID = input("Enter UID for car on lane #1: ")    # Enter the race information
    driverName = input("Enter the name of the driver on lane #1: ")    # Enter the race information
    print(raceName, 'will be a ', numberOfLaps, ' lap race.')

# This is the funtion that cleans house the the program endingRoutine
def endingRoutine():
    global raceFinishTimeFormatted
    global raceFinishTime
    print('Done!!  The Race is over.')
    raceFinishTime = time.localtime()    # This returns the local finish time of the race
    raceFinishTimeFormatted = time.strftime("%a, %d %b %Y %H:%M:%S %Z", raceFinishTime)
    print("\nOfficial Race Finish Time: ", raceFinishTimeFormatted)
    raceFinishTime = time.time()    # This returns the finish time of the race as epoch
#    segment = SevenSegment(address=0x70)
    print('The winner is... TBD once code gets added ')
    logFinalDataToCSV()
    GPIO.cleanup()
    sys.exit('program exiting')

# This is the funtion logs the final bit of race data to the .csv file
def logFinalDataToCSV():
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#        data_writer.writerow([lapNumber, lapTime, fastestLap])
        data_writer.writerow(['The race started at: ', raceStartTimeFormatted])
        data_writer.writerow(['The race ended at: ', raceFinishTimeFormatted])
        data_writer.writerow(['Laps completed by winner: ', lapNumber])
        raceTimeDuration = raceFinishTime - raceStartTime
        data_writer.writerow(['The race duration was (sec): ', raceTimeDuration])
        data_writer.writerow(['The fastest race lap was (sec): ', fastestLap])
        data_writer.writerow(['The race winner is: '])


inputRaceData()    # calls function for user to input race data
openCSVFile()
print ('Waiting for marshall to push "Start" button.')
GPIO.wait_for_edge(27, GPIO.FALLING, bouncetime=2000)   # This is the start button being pressed
print('The Race has started.')
startSequence()   # Calls the start sequence
GPIO.add_event_detect(16, GPIO.FALLING, callback=reset, bouncetime=200)  # This is reset
GPIO.add_event_detect(6, GPIO.FALLING, callback=newLap, bouncetime=2000) # The is new lap test button
GPIO.add_event_detect(17, GPIO.FALLING, callback=displayFastestLap, bouncetime=200) # This is display fasted lap
GPIO.add_event_detect(4, GPIO.FALLING, callback=newLap, bouncetime=200)  # The is new lap Break Beam Detection
GPIO.add_event_detect(5, GPIO.FALLING, callback=newLap, bouncetime=200)  # The is new lap Reflective Detection


try:
    #print ('Waiting racer to push "Start" button')
    #GPIO.wait_for_edge(27, GPIO.FALLING, bouncetime=2000)   # This is the start buttong being pressed
    #print('The Race has started.')
    while True:
        time.sleep(0.01)
        pass    # Does nothing.  Kind of like a no op

finally:
    print('Done!!  The Race is over.')
#    raceFinishTime = time.localtime()     # This returns the local finish time of the race
#    raceFinishTimeFormatted = time.strftime("%a, %d %b %Y %H:%M:%S %Z ", raceFinishTime)
#    print("\nOfficial Race Finish Time = ", raceFinishTimeFormatted)
#    segment = SevenSegment(address=0x70)
    GPIO.cleanup()

### This might be a better way to do the previous try/Except ###
# try:
#    print "Waiting for falling edge on port TBD"
#    GPIO.wait_for_edge(TBD GPIO port #, GPIO.FALLING)
#    print('Done!!  The Race is over.')
#
#except KeyboardInterrupt:
#    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
#    print('Done!!  The Race is over.')
#print('Done!!  The Race is over.')
#GPIO.cleanup()           # clean up GPIO on normal exit
#################################################################
