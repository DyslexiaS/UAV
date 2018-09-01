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

# cv2.namedWindow("demo", cv2.cv.CV_WINDOW_NORMAL)
# cv2.resizeWindow('demo', 600,600)
# cv2.startWindowThread()
direct_down_mode = False
hit_twice = False

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
    send_global_velocity(vehicle, 0, 0, -0.1)
    print("can't detect any circle")
    hit_twice = False
  else:
    displacement = circle[0]-camera.resolution[0]//2, circle[1]-camera.resolution[1]//2
    radius = circle[2]

    direction = math.atan2(displacement[1], displacement[0])
    direction -= math.pi
    relative_direction = direction
    direction += vehicle.attitude.yaw

    try:
      distance_per_pixel = 2670 / radius
    except Exception, e:
      print(e)
      distance_per_pixel = 100
      print('set distance_per_pixel = 100')
      print('$' * 50)


    alt = distance_per_pixel * camera.resolution[0]
    displacement = [d*distance_per_pixel for d in displacement]

    distance = math.sqrt(displacement[0]**2 + displacement[1]**2)

    if radius >= 50 and distance <= 90:
      print('HIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
      if hit_twice == False:
        hit_twice = True
      else:
        direct_down_mode = True
        break
    else:
      hit_twice = False

    try:
      angle = math.atan(distance/alt)
    except Exception, e:
      print(e)
      angle = 0
      print('_' * 50)
      print('set distance_per_pixel = 100')

    # scale
    scale_xy = 0.007
    scale_z = 0.1
    max_speed = 0.2
    max_speedz = 0.1

    speed_xy = scale_xy * distance
    speed_z = scale_z if distance < alt else -scale_z#  * (math.radians(30) - angle)
    if speed_xy > max_speed:
      speed_xy = max_speed
    elif speed_xy < -max_speed:
      speed_xy = -max_speed
    if speed_z > max_speedz:
      speed_z = max_speedz
    elif speed_z < -max_speedz:
      speed_z = -max_speedz

    velocity_x = speed_xy * math.cos(direction)
    velocity_y = speed_xy * math.sin(direction)

    velocity_z = speed_z

    print("direction %.2f, speed_xy = %.2f, speed_z = %.2f, alt = %d, angle = %.2f\n" % (math.degrees(relative_direction), speed_xy, speed_z, alt, math.degrees(angle)))
    send_global_velocity(vehicle, velocity_x, velocity_y, velocity_z)

    if save_result:
      img = draw_circle(img, circle)
      save_img_name = '%s_save_%d_%d_%d_%d.jpg' % (img_name[:-4], radius, distance, int(100*speed_xy), int(100*speed_z))
      plot_arrow(img, (circle[0], circle[1]), center=(75,75), color=(0,0,255), line_width=2)
      imwrite(join(img_dir, save_img_name), img)

  if infinite == 0:
    print('infinite == 0')
    keep_running[0] = False

  # cv2.imshow("demo", np.hstack((img, img_)))

signal.signal(signal.SIGINT, signal_old)

if direct_down_mode == True:
  send_global_velocity(vehicle, 0, 0, 0.1)
  count_down = 5
  while count_down:
    print(count_down)
    count_down -= 1
    time.sleep(1)
  k = raw_input('disarmed? y/n')
  if k == 'y':
      vehicle.armed = False
