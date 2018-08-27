#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from os import listdir
from os.path import isfile, join, dirname
import cv2

import sys
sys.path.append(join(dirname(__file__), '..', 'Opencv'))
from lib import imread, imwrite, rgb2blue, detect_circles, alt2diagonal, best_circle, draw_circle, plot_arrow

def haha(name, kk):
  cv2.waitKey(0)

from picamera import PiCamera
import time
camera = PiCamera()
camera.resolution=(150,150)
cv2.namedWindow('haha',cv2.WINDOW_NORMAL)
img_path = 'test.jpg'
first = True
while True:
  camera.capture(img_path)
  img = imread(img_path)
  # detect circles
  img_ = rgb2blue(img)
  circles = detect_circles(img_, 0)
  circle = best_circle(circles, img_, camera.resolution)
  if circle is not None:
    img = plot_arrow(img, (circle[0], circle[1]), center=(camera.resolution[0]//2, camera.resolution[1]//2))
    img = add_text(img, H=100, D=80, Min=0, Max=100):
  cv2.startWindowThread()
  cv2.imshow('haha', img)
cv2.destroyAllWindows()

  # cv2.waitKey(0)
  # if first:
  #   first = False
  #   import thread
  #   thread.start_new_thread(haha, (1,2))
