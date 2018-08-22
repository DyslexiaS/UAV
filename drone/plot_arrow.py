#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from os import listdir
from os.path import isfile, join, dirname

import sys
sys.path.append(join(dirname(__file__), '..', 'Opencv'))
from lib import imread, imwrite, rgb2blue, detect_circles, alt2diagonal, best_circle, draw_circle, plot_arrow

def haha(name, kk):
  import cv2
  cv2.waitKey(0)

from picamera import PiCamera
camera = PiCamera()

first = True
while True:
  camera.capture(img_path)
  img = imread(img_path)
  # detect circles
  img_ = rgb2blue(img)
  circles = detect_circles(img_, 0)
  circle = best_circle(circles, img_)
  img = plot_arrow(img, (circle[0], circle[1]))
  cv2.imshow('haha', img)
  if first:
    first = False
    import thread
    thread.start_new_thread(haha, (1,2))

import time
while True:
  time.sleep(1)
  print('haha')
