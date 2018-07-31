from picamera import PiCamera
from time import sleep
import sys

camera = PiCamera()

#camera.start_preview()
#sleep(2)

camera.capture(sys.argv[1] + '.jpg')
#camera.stop_preview()
