# First things, first. Import the wxPython package.
#import wx
import time
import random
import csv

starTime = 0
n = 1

bestLap = 9999
# sleepTime = 2
lapTime = 0

# User input to configure the race
raceNumber = input("Enter Race Number = : ")    # Enter the race number
laps = int(input("Enter The Number of Laps = : "))  # Typecasting
print('\nThis is the lap data for Race #', raceNumber)

# Initialize starting times
startTime = time.time()
previousTime = startTime
      
for n in range(laps):
    sleepTime = random.randint(1,4)  # Genertes random number for simulated lap time delay
    time.sleep(sleepTime)
    currentTime = time.time()
    lapTime = currentTime - previousTime
    print('Lap #', n + 1, 'Time = ', "%.2f" % lapTime)   # Prints the lap # & lap time to 2 decimal places
    if lapTime < bestLap:
        bestLap = lapTime
    previousTime = currentTime
    if n == (laps-2):
        print('White Flag, Last Lap')
    if n == (laps-1):
        print('Checkered Flag, Race Over!!!')
            
raceTime = time.time() - startTime
endTime = time.time()

# Output race stats to screen
print('\n')
print('This is data for Race #', raceNumber)
print('Start time = ', "%.2f" % startTime)    # Prints the lap # & lap time to 2 decimal places
print('End time = ', "%.2f" % endTime)        # Prints the lap # & lap time to 2 decimal places
print(laps, 'lap race is completed')              # Prints the total laps of the race
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

# Write data to .csv file
with open('raceData.csv', mode='a') as race_data:
    data_writer = csv.writer(race_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(['This is data for Race # ', raceNumber, ' ', ' '])
    data_writer.writerow(['Start Time (sec)', 'End Time (sec)', 'Race Time (sec)', 'Best Lap(sec)'])
    data_writer.writerow([startTimeInString, endTimeInString, raceTimeInString, bestLapInString])


    
    
    
