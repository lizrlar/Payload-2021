#!/bin/bash
#Camera Script in drone flight ready form
FILE=/home/pi/Desktop/Camera-Test-0/detect.txt
if test -f "$FILE"; then
	echo "File detected, halting program"
else	
	raspistill -cs 0 -n -t 600000 -tl 2750 -o /home/pi/Desktop/Camera-Test-0/cam0_%03d.jpg &	
	raspistill -cs 1 -n -t 600000 -tl 2750 -o /home/pi/Desktop/Camera-Test-1/cam1_%03d.jpg 	 	
	echo "Why are you looking in this file? There is nothing to see here :) (Though please remember to remove me or else the script won't run!)" > /home/pi/Desktop/Camera-Test-0/detect.txt	
	sleep 100
	poweroff
fi