#!/usr/bin/env python3

# ==============================================================================
# Filename     : timingCode.py
# Description: This program simulates a slot car race with one car and user
# specified laps.  It displays lap information real time and then logs the
# final race data to a filename.txt file in the same directory as the code
# Author: Carl M. Conliffe
# Created: 2 January 2020
# Modification : 23 Oct 2021; Cleaned up the comments inthe code and placed it
# in standard template format to include tables of variables and function.
# ==============================================================================

# ++++++++++++++++++++++++ List of variables +++++++++++++++++++++++++++++++++++
# data_writer            #
# f                      #
# raceName               # This is the user defined name of race.
# numberOfLaps           # Thisis the user specicfied number of laps inthe race.
# lane1CarUID            # This is the user specified unique name of the car
# startTime              # This is the start time of the race
# localStartTime         # This is the local start time of the race
# previousTime           # This is the time of the previous lap.
# lapNumber              # This is the lap number.
# n                      # Index for loops.
# sleepTime              # Randomly generated number in seconds for simulated lap time.
# currentTime            # This is the current time of day.
# lapTime                # This is the current lap time.
# raceTime               # This it the total elapsed timeof the race.
# endTime                # This is the time of day at the end of the race.
# localEndTime           # This is the local time at the end of the race.
# startTimeInString      # This is the start time of the race as a string.
# endTimeInString        # This is the end time of the race as a string.
# raceTimeInString       # This is the race time as a string.
# fastestLapInString     # This is the fastest lap time of the race as a string.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ---------- List of functions -------------------------------------------------
# openCSVFile()            --  Opens and formats the .csv file the the race data will be written to.
# writeDatatoCSVFile()     -- Writes data to the .csv file
# inputRaceData():         -- This allows the user to input the race data.
# ------------------------------------------------------------------------------

# First things, first. Import the wxPython package.
#import wx
import time
import random
import csv

lapNumber = 0
fastestLap = 9999
lapTime = 0

## This section is for definition of functions ##
#
# Function to open, create and configure .csv file
def openCSVFile():
    print("Creating .csv file")
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['This is data for: ', raceName])
        data_writer.writerow(['This race will consist of (lap) :', numberOfLaps])
        data_writer.writerow(['On lane #1 is car UID# :', lane1CarUID])
        data_writer.writerow(['Lap #', 'Lap Time (sec)', 'Fastest Lap(sec)'])

# Function to write data to .csv file for one line at a time
def writeDatatoCSVFile():
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([lapNumber, lapTime, fastestLap])

# Funtion for user to input race data
def inputRaceData():
    global numberOfLaps
    global raceName
    global lane1CarUID
    raceName = input("Enter Race Name: ")    # Enter the race information
    numberOfLaps = int(input("Enter The Number of Laps: "))  # Typecasting
    lane1CarUID = input("Enter UID for car on lane #1: ")    # Enter the race information
    print(raceName, 'will be a ', numberOfLaps, ' lap race.')

## End of section for definition of functions ##

# Start on main program
# User input to configure the race
inputRaceData()
openCSVFile()

# Initialize starting times
startTime = time.time()
localStartTime = time.localtime()
previousTime = startTime

for n in range(numberOfLaps):
    lapNumber += 1
    sleepTime = random.randint(1,4)  # Genertes random number for simulated lap time delay
    time.sleep(sleepTime)
    currentTime = time.time()
    lapTime = currentTime - previousTime
    print('Lap #', lapNumber, 'Time = ', "%.2f" % lapTime)   # Prints the lap # & lap time to 2 decimal places
    writeDatatoCSVFile()
    if lapTime < fastestLap:
        fastestLap = lapTime
    previousTime = currentTime
    if lapNumber == (numberOfLaps - 1):
        print('White Flag, Last Lap')
    if lapNumber == (numberOfLaps):
        print('Checkered Flag, Race Over!!!')

raceTime = time.time() - startTime
endTime = time.time()
localEndTime = time.localtime()

# Output race stats to screen
print('This is data for: ', raceName)
formattedStartTime = time.strftime("%d %B %Y at %H:%M:%S %Z ", localStartTime)
print("Race start: ", formattedStartTime)  # Prints the time and date the race started
formattedEndTime = time.strftime("%d %B %Y at %H:%M:%S %Z ", localEndTime)
print("Race finish: ", formattedEndTime)  # Prints the time and date the race ended
print(numberOfLaps, 'lap race is completed')          # Prints the total laps of the race
print('Race Time = ', "%.2f" % raceTime, " seconds")      # Prints the lap # & lap time to 2 decimal places
print('Fastest Lap Time = ', "%.2f" % fastestLap, " seconds")   # Prints the lap # & lap time to 2 decimal places
print('Writing race data to a text file named "RaceData.txt"')

# Write data to .txt file
startTimeInString = str(formattedStartTime)          # float -> str
endTimeInString = str(formattedEndTime)              # float -> str
raceTimeInString = str(raceTime)            # float -> str
fastestLapInString = str(fastestLap)              # float -> str
f = open('raceData.txt', 'a')               # Write and append to the file
f.write('This is data for: ' + raceName + '\n')
f.write('Start Time = ' + startTimeInString + '\n')
f.write('End Time = ' + endTimeInString + '\n')
f.write('Race Time = ' + raceTimeInString + ' seconds\n')
f.write('Fastest Lap = ' + fastestLapInString + ' seconds\n')
f.write('\n')
f = f.close()
