#SLI 2021 Payload Camera Program (PCP)
#Developed by Bready and Liz

#IMPORTANT: Remember to delete Important_File.txt before running program
#Also, remember to create and/or change the directories where the images will be saved

from picamera import PiCamera
import time
import threading
from os import path
from subprocess import call #New Bit

camera0 = PiCamera(0)
camera1 = PiCamera(1)
#camera0.rotation = 180
#camera1.rotation = 180

#This is the ammount of time we have to assemble the rocket before it starts taking pictures. Enter time in seconds
time.sleep(5)

if path.exists('Important_File.txt'):
  print("Important File exists. Aborting Program.")
else:
  timer = 5 #Enter in Seconds
  interval = 0.25 #Enter in Fractions of a Second

  #This converts the time in seconds into the number of times the program needs to run
  timer = timer / interval

  def cameraCapture0():
    i = 1
    while i <= timer:
        camera0.capture   ('/home/pi/Desktop/CameraPictures/Camera_0/cam0_%03d.jpg' % i)
        print (f"Cam0 :: {i}")
        i += 1
        time.sleep(interval)
    f= open("Important_File.txt","w+")
    print("Program Finished") #End Message
    call("sudo poweroff", shell=True) #New Bit

  def cameraCapture1():
    i = 1 
    while i <= timer:
        camera1.capture('/home/pi/Desktop/CameraPictures/Camera_1/cam1_%03d.jpg' % i)
        print (f"Cam1 :: {i}")
        i += 1
        time.sleep(interval)

  t1 = threading.Thread(target = cameraCapture0)
  t2 = threading.Thread(target = cameraCapture1)

  t1.start()
  t2.start()