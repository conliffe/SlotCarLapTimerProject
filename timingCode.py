#############################################################################
# Author: Carl M. Conliffe
# Date: 2 January 2020
# Description: This program simulates a slot car race with one car and user
# specified laps.  It displays lap information real time and then logs the
# final race data to a filename.txt file in the same directory as the code
#############################################################################

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
