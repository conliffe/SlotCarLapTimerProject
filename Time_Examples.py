#!/usr/bin/env python3
########################################################################
# Filename    : Time_Examples.py
# Description :  This program shows different funtions for using time
#
# Author      : Carl Conliffe
# Created     : 2 February 2020
# Modification: Date
########################################################################

###### List of variables ###########
# timeUTCEpoch
# currentTime
#
####################################

###### List of funcions ############
# 
####################################


# Import libraries
# import RPi.GPIO as GPIO
import time

# Configure the Pi to use the BCM pin names
# GPIO.setmode(GPIO.BCM)    # Use channel numbering
# GPIO.setmode(GPIO.BOARD)  # Use PHYSICAL GPIO Numbering


# pins used for the switches, IR diodes as sensor and LEDs
#

# Configure GPIO outputs
#

# Configure GPIO inputs
#

# This section is for definition of functions
#
# Function to ...
#
##############################################

# Main program here

# Return the time in seconds since the epoch as a floating point number. 
# The specific date of the epoch and the handling of leap seconds is platform 
# dependent. On Windows and most Unix systems, the epoch is 
# January 1, 1970, 00:00:00 (UTC) and leap seconds are not counted towards 
# the time in seconds since the epoch. This is commonly referred to as Unix 
# time. To find out what the epoch is on a given platform,
timeUTCEpoch = time.time()
print("Current time in epoch UTC: ", timeUTCEpoch)

# Convert a time expressed in seconds since the epoch to a string of a form:
# 'Sun Jun 20 23:21:05 1993' representing local time. The day field is two
# characters long and is space padded if the day is a single digit, 
# e.g.: 'Wed Jun  9 04:26:40 1993'
currentTime = time.ctime()
print("\nCurrent time in Day, Month, date, time(hr:min:sec), year: ", currentTime)

time1 = time.localtime()
print("\nCurrent time in [time.struct_time (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)]: ", time1)

# Suspend execution of the calling thread for the given number of seconds. 
# The argument may be a floating point number to indicate a more precise 
# sleep time. 
print("\nTaking a 1.5 sec delay between the next line executed")
time.sleep(1.5)

# Convert a tuple or struct_time representing a time as returned by gmtime() 
# or localtime() to a string as specified by the format argument. 
# time.strftime(format[, t])
#time2 = time.strftime("%a, %d %b %Y %H:%M:%S %Z ", time1)
time2 = time.strftime("%H:%M:%S %Z ", time1)
print("\nCurrent time in [Day, date month year HH:MM:SS] format: ", time2)
print("The user can format how the output appears. \n")


