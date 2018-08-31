#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import math
import time
import numpy as np

from os import listdir
from os.path import isfile, join, dirname
from set_velocity import send_global_velocity

import signal
import sys
sys.path.append(join(dirname(__file__), '..', 'Opencv'))
from lib import *
import cv2

from picamera import PiCamera
camera = PiCamera()
camera.resolution = (150, 150)



def signal_handler(sig, frame):
  global keep_running
  print("stop detecting...")
  keep_running[0] = False

img_dir = '../img'
save_result = True
keep_running = [True]
signal_old = signal.signal(signal.SIGINT, signal_handler)

img_name = 'test.jpg'
skip_once = False
cv2.namedWindow("demo", cv2.cv.CV_WINDOW_NORMAL)
cv2.resizeWindow('demo', 600,600)
cv2.startWindowThread()
alt = 0
while keep_running[0]:
  print('#'*20)


  img_path = join(img_dir, img_name)

  # take photo
  camera.capture(img_path)

  # detect circles
  img = imread(img_path)
  img_ = rgb2blue(img)
  blue_img_name = img_name[:-4]+'_blue.jpg'
  imwrite(join(img_dir, blue_img_name), img_)
  circles = detect_circles(img_, alt)
  circle = best_circle(circles, img, resolution=camera.resolution)


  if circle is None:
    if skip_once == False:
        skip_once = True
    else:
        skip_once = False
    alt = 0
    img = circle_not_found(img)
  else:
    skip_once = False
    displacement = circle[0]-camera.resolution[0]//2, circle[1]-camera.resolution[1]//2
    radius = circle[2]

    print('raius', radius)
    alt = 2670 / radius
    print('alt', alt)
    distance_per_pixel = float(alt) / camera.resolution[0]
    print('distance_per_pixel ',distance_per_pixel)

    displacement = [d*distance_per_pixel for d in displacement]
    print('displacement ',displacement)

    distance = math.sqrt(displacement[0]**2 + displacement[1]**2)
    print('distance ',distance)

    if save_result:
      img = draw_circle(img, circle)
      plot_arrow(img, (circle[0], circle[1]), center=(75,75), color=(0,0,255), line_width=2)
      add_text(img, H=alt, D=distance, Min=10, Max=30)
      save_img_name = img_name[:-4]+'_save.jpg'
      imwrite(join(img_dir, save_img_name), img)
  if not skip_once:
    cv2.imshow("demo", np.hstack((img, img_)))


signal.signal(signal.SIGINT, signal_old)
cv2.destroyAllWindows()
