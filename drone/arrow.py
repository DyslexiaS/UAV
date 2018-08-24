#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import math
import cv2

from os import listdir
from os.path import isfile, join, dirname

import sys
sys.path.append(join(dirname(__file__), '..', 'Opencv'))
from lib import imread, imwrite, rgb2blue, detect_circles, alt2diagonal, best_circle, draw_circle, plot_arrow

def plot_arrow(img, point, center=(360,240)):
  cv2.line(img, center, point, (0,0,255), 5)
  pi = 3.1415926
  angle = math.atan2(center[1]-point[1], center[0]-point[0])
  arrow_x = point[0] + 20* math.cos(angle+pi*30/180)
  arrow_y = point[1] + 20* math.sin(angle+pi*30/180)
  cv2.line(img, point, (int(arrow_x),int(arrow_y)), (0,0,255), 5)
  arrow_x = point[0] + 20* math.cos(angle-pi*30/180)
  arrow_y = point[1] + 20* math.sin(angle-pi*30/180)
  cv2.line(img, point, (int(arrow_x),int(arrow_y)), (0,0,255), 5)
  return img

img_path = '../img/img_196.jpg'
img = imread(img_path)
# detect circles
img_ = rgb2blue(img)
circles = detect_circles(img_, 0)
circle = best_circle(circles, img_)
img = plot_arrow(img, (circle[0], circle[1]))
cv2.imshow('haha', img)
cv2.waitKey(0)
