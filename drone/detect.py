#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __main__ import vehicle, camera, print_important
import math
import time

from os import listdir
from os.path import isfile, join, dirname
from set_velocity import send_global_velocity

import signal
import sys
sys.path.append(join(dirname(__file__), '..', 'Opencv'))
from lib import *

img_dir = '../img'
resolution = (150, 150)
camera.resolution = resolution

try:
  idx = int(sys.argv[1])
except Exception, e:
  print(e)
  print('set default idx=0')
  idx = 0

try:
  infinite = int(sys.argv[2])
except Exception, e:
  print(e)
  print('set default: only take 1 photo')
  infinite = 0

def signal_handler(sig, frame):
  global keep_running
  print("stop detecting...")
  keep_running[0] = False

save_result = True
keep_running = [True]
signal_old = signal.signal(signal.SIGINT, signal_handler)

cv2.namedWindow("demo", cv2.cv.CV_WINDOW_NORMAL)
cv2.resizeWindow('demo', 600,600)
cv2.startWindowThread()

while keep_running[0]:
  print_important(vehicle)
  print('#'*20)

  alt = int(100*vehicle.location.global_relative_frame.alt)

  img_name = '%d_%d.jpg' % (idx, alt)
  img_path = join(img_dir, img_name)
  idx += 1

  # take photo
  camera.capture(img_path)
  print(img_path)

  # detect circles
  img = imread(img_path)
  img_ = rgb2blue(img)
  blue_img_name = img_name[:-4]+'_blue.jpg'
  imwrite(join(img_dir, blue_img_name), img_)
  circles = detect_circles(img_, 0)
  circle = best_circle(circles, img, resolution=camera.resolution)

  if circle is None:
    send_global_velocity(vehicle, 0, 0, -0.2)
    print("can't detect any circle")
  else:
    if save_result:
      img = draw_circle(img, circle)
      save_img_name = img_name[:-4]+'_save.jpg'
      plot_arrow(img, (circle[0], circle[1]), center=(75,75), color=(0,0,255), line_width=2)
      imwrite(join(img_dir, save_img_name), img)
    displacement = circle[0]-camera.resolution[0]//2, circle[1]-camera.resolution[1]//2
    radius = circle[2]

    direction = math.atan2(displacement[1], displacement[0])
    direction += math.pi / 2
    relative_direction = direction
    direction += vehicle.attitude.yaw

    distance_per_pixel = 2670 / radius
    # alt = distance_per_pixel * camera.resolution[0]
    displacement = [d*distance_per_pixel for d in displacement]

    distance = math.sqrt(displacement[0]**2 + displacement[1]**2)



    angle = math.atan(distance/alt)

    # scale
    scale_xy = 0.01
    scale_z = 0.02
    max_speed = 0.5

    speed_xy = scale_xy * distance
    speed_z = scale_z * math.sqrt(alt if alt > 0 else 1) * (math.radians(20) - angle)
    if speed_xy > max_speed:
      speed_xy = max_speed
    elif speed_xy < -max_speed:
      speed_xy = -max_speed
    if speed_z > max_speed:
      speed_z = max_speed
    elif speed_z < -max_speed:
      speed_z = -max_speed

    velocity_x = speed_xy * math.cos(direction)
    velocity_y = speed_xy * math.sin(direction)

    velocity_z = speed_z

    print("direction %.2f, speed_xy = %.2f, speed_z = %.2f, alt = %d, angle = %.2f\n" % (math.degrees(relative_direction), speed_xy, speed_z, alt, angle))
    send_global_velocity(vehicle, velocity_x, velocity_y, velocity_z)

  if infinite == 0:
    print('infinite == 0')
    keep_running[0] = False

  cv2.imshow("demo", np.hstack((img, img_)))

signal.signal(signal.SIGINT, signal_old)
