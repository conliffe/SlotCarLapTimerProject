# First things, first. Import the wxPython package.
#import wx
import time
import random
import csv

lapNumber = 0
bestLap = 9999
lapTime = 0

## This section is for definition of functions ##
#
# Function to open, create and configure .csv file
def openCSVFile():
    print("Creating .csv file")
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(['This is data for: ', raceNumber])
        data_writer.writerow(['Lap #', 'Lap Time (sec)', 'Best Lap(sec)'])

# Function to write data to .csv file
def writeDatatoCSVFile():
    with open('raceData.csv', mode='a') as race_data:
        data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        bestLapInString = str(bestLap)              # float -> str
        lapNumberInString = str(lapNumber)          # float -> str
        lapTimeInString = str(lapTime)              # float -> str
        data_writer.writerow([lapNumberInString, lapTimeInString, bestLapInString])
## End of section for definition of functions ##  

# Stat on main program
# User input to configure the race
raceNumber = input("Enter Race Information = : ")    # Enter the race information
laps = int(input("Enter The Number of Laps = : "))  # Typecasting
print('\nThis is the lap data for ', raceNumber)
openCSVFile()

# Initialize starting times
startTime = time.time()
previousTime = startTime
                            
for n in range(laps):
    lapNumber += 1
    sleepTime = random.randint(1,4)  # Genertes random number for simulated lap time delay
    time.sleep(sleepTime)
    currentTime = time.time()
    lapTime = currentTime - previousTime
    print('Lap #', lapNumber, 'Time = ', "%.2f" % lapTime)   # Prints the lap # & lap time to 2 decimal places
    writeDatatoCSVFile()
    if lapTime < bestLap:
        bestLap = lapTime
    previousTime = currentTime
    if lapNumber == (laps-1):
        print('White Flag, Last Lap')
    if lapNumber == (laps):
        print('Checkered Flag, Race Over!!!')
            
raceTime = time.time() - startTime
endTime = time.time()

# Output race stats to screen
print('\n')
print('This is data for Race #', raceNumber)
print('Start time = ', "%.2f" % startTime)    # Prints the lap # & lap time to 2 decimal places
print('End time = ', "%.2f" % endTime)        # Prints the lap # & lap time to 2 decimal places
print(laps, 'lap race is completed')          # Prints the total laps of the race
print('Race Time = ', "%.2f" % raceTime)      # Prints the lap # & lap time to 2 decimal places
print('Best Lap Time = ', "%.2f" % bestLap)   # Prints the lap # & lap time to 2 decimal places

# Write data to .txt file
startTimeInString = str(startTime)          # float -> str
endTimeInString = str(endTime)              # float -> str
raceTimeInString = str(raceTime)            # float -> str
bestLapInString = str(bestLap)              # float -> str
f = open('raceData.txt', 'a')               # Write and append to the file
f.write('This is data for Race #' + raceNumber + '\n')
f.write('Start Time = ' + startTimeInString + '\n')
f.write('End Time = ' + endTimeInString + '\n')
f.write('Race Time = ' + raceTimeInString + '\n')
f.write('Best Lap = ' + bestLapInString + '\n')
f.write('\n')
f = close('raceData.txt, 'a' )
    
    
    
