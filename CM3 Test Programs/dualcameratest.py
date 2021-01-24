from picamera import PiCamera
from time import sleep

camera1 = PiCamera(0)
camera2 = PiCamera(1)
camera1.rotation = 180
camera2.rotation = 180

camera1.start_preview(fullscreen=False, window = (100,20,640,480))
for i in range(3):
    sleep(5)
    camera1.capture('/home/pi/Desktop/cam1test%s.jpg' % i)
camera1.stop_preview()

camera2.start_preview(fullscreen=False, window = (100, 20, 640, 480))
for i in range(3):
    sleep(5)
    camera2.capture('/home/pi/Desktop/cam2test%s.jpg' % i)
camera2.stop_preview()