from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180

camera.start_preview(fullscreen=False, window = (100,20,640,480))
for i in range(3):
    sleep(5)
    camera.capture('/home/pi/Desktop/test%s.jpg' % i)
camera.stop_preview()