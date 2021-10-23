

# License Notice
This project uses i2C libraries written by Limor Fried/Ladyada for Adafruit Industries. <br />
Copyright (c) 2012 Adafruit Industries<br />
https://github.com/adafruit/Adafruit-LED-Backpack-Library<br />
https://www.adafruit.com/

# Quick Overview
<ul>
<li>Using a reed sensor to detect changes in magnetic field as slot car passes over track</li>
<li>Uses Adafruit segment display and i2C libraries to display lap times</li>
<li>In additional, an RGB LED is used to indicate a new lap being recorded, and fastest lap being achieved</li>
<li>2 buttons have been added to display fastest recorded lap or reset times</li>
<li>Coded in Python using GPIO pins on Raspberry Pi</li>
</ul>

# Descriptions of files ########################################################
<b> This is the description of what the Python files in this project do. </b><br>
# Lap_timer_Carl_with_buttons
Lap_timer_Carl_with_buttons.py
<ul>
<li> Reports on the time lapsed between detection of a sensor. </li>
<li> A yellow momentary push button is the sensor for the lap. </li>
<li> A yellow LED on each lap detection. </li>
<li> Green LED flashes to indicate fastest lap. </li>
<li> 2 Buttons - one to reset timing, and one to display fastest lap. </li>
<li> This code needs Raspberry Pi hardware and circuit electronics in order to run. </li>
<li> Schematic for this circuit is drawn in KiCad LapTimeCounter.sch. </li>
<li> Uses adafruit library to display lap times on 7 segment, 4 digit display. </li>
(/ul>
<br>
# Scalextric_timer
Scalextric_timer.py
<ul>
<li> Reports on the time lapsed between detections on the reed sensor. </li>
<li> Also flashes an LED on each lap detection, and green to indicate fastest lap. </li>
<li> There are 2 Buttons - one to reset timings, one to display fastest lap. </li>
<li> This is the code that I used to base all my code on. </li>
(/ul>
<br>

# SlotCarlapTimer
SlotCarlapTimer.py
<ul>
<li> This code is for a Raspberry Pi circuit that will detect slot car laps and time them. </li>
<li> It uses IR sensors. </li>
<li> Calculates lap time, fasted lap and time a race duration for the number of laps inputed by the user as the race duration. </li>
<li> There is also a countdown to start shown with 5 LEDs. </li>
<li> Data from the race is reported to a .csv file while also being displayed to the screen. </li>
<li> There are also 4 push buttons that </li>
<ol>
<li> Reset lap number time and number counter. </li>
<li> Force a lap to be counted.  This is a debug feature and not used for a real race. </li>
<li> Display fasted lap on request during the race and
<li> Lets user trigger start of race.  This is prompted from the screen display. </li>
(/ol>
<li> The circuit will flash an LED on each lap detection, and blinking colored LED to  indicate the fastest lap. </li>
<li> The schematic name that corresponds to this code is "Lap_Timer_Counter.sch" drawn in KiCad. </li>
(/ul>
<br>

# timingCode
timingCode.py:
<ul>
<li> Simulates a slot car race with one car. </li>
<li> Lets user specify the number of laps. </li>  
<li> It displays lap information real time. </li>
<li> Logs the final race data to a "filename.txt" file in the same directory as the code. </li>
(/ul>
<br>

<b> This is all of the test code I used to check out functionality that goes into the code above </b?<br>
# AdafruitTestCode1
AdafruitTestCode1.py
<ul>
<li> This is test code to check out how to use the Adafruit code in the lap timer code. </li>
<li> Uses adafruit library to display lap times on 7 segment, 4 digit display. </li>
(/ul>
<br>
# BlinkingLED
BlinkingLED.py
<ul>
<li> This code makes an LED blink at 1 second interval </li>
<li> This code needs Raspberry Pi hardware and circuit electronics in order to run. </li>
(/ul>
<br>
# ControlingLEDwithButton
ControlingLEDwithButton.py
<ul>
<li> When you push the button the Red LED turns on. </li>
<li> This code needs Raspberry Pi hardware and circuit electronics in order to run. </li>
(/ul>
<br><b> This is a list of the test code written to try out functionality that is used in code above. </b><br>
# StartCountdownLED
StartCountdownLED.py
<ul>
<li> This code does a race start sequence using LED bar. </li>
<li> It uses a 5 LED segment to count down to start. </li>
<li> All LED's initially lit then every second one turns off until all 5 are off. </li>
<li> You can make all lights turn on green for go. </li>
<li> This simulates a start Christmas tree. </li>
(/ul>
<br>
# Stoplight
Stoplight.py
<ul>
<li> This program simulates a traffic signal. </li>
<li> It stays green for 20 sec. then goes yellow for 2 sec. then stays red for 20 sec. </li>
<li> This code needs Raspberry Pi hardware and circuit electronics in order to run. </li>
(/ul>
<br>
# StopWatch
StopWatch.py
<ul>
<li> Controls 4_Digit_7_Segment_Display with 74HC595. </li>
<li> This code needs Raspberry Pi hardware in order to run. </li>
(/ul>
<br>
# TestCodeWritingTo7SegDisplay
TestCodeWritingTo7SegDisplay.py:
<ul>
<li> This test code gets input from the user and has it written to 7 segment Adafruit display. </li>
<li> Uses a simple circuit that drives the Adafruit 4 digit 7 segment featherwing display. </li>
(/ul>
<br>#Time_Examples
Time_Examples.py:
<ul>
<li> This program shows different functions for using time. </li>
(/ul>
<br>
