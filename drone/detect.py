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
from lib import imread, imwrite, rgb2blue, detect_circles, alt2diagonal, best_circle, draw_circle

img_dir = '../img'

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
  print("stop detecting...")
  keep_running[0] = False

save_result = True
keep_running = [True]
signal_old = signal.signal(signal.SIGINT, signal_handler)

log_file = "log"
with open(log_file, "a") as f:
  print("absolute_direction, relative_direction, angle, alt, v_x, v_y, v_z\n", file=f)

while keep_running[0]:
  time.sleep(2)
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
  img = rgb2blue(img)
  circles = detect_circles(img, alt)
  circle = best_circle(circles, img)

  if save_result and circle is not None:
    img = draw_circle(img, circle)
    save_img_name = 'save_' + img_name
    imwrite(join(img_dir, save_img_name), img)

  if circle is None:
    send_global_velocity(vehicle, 0, 0, -0.2)
    print("can't detect any circle")
  else:
    displacement = circle[0]-360, circle[1]-240

    # # first quadrant
    # if displacement[0] >= 0 and displacement[1] >= 0:
    #   direction = math.atan2(displacement[1], displacement[0])
    # # second quadrant
    # elif displacement[0] >= 0 and displacement[1] < 0:
    #   direction = -math.atan2(-displacement[1], displacement[0])
    # # third quadrant
    # elif displacement[0] < 0 and displacement[1] < 0:
    #   direction = math.pi + math.atan2(-displacement[1], -displacement[0])
    # # fourth quadrant
    # else:
    #   direction = math.pi - math.atan2(displacement[1], -displacement[0])
    direction = math.atan2(displacement[1], displacement[0])
    direction -= math.pi / 2

    displacement = [alt2diagonal(alt) * d / 865 for d in displacement]

    distance = math.sqrt(displacement[0]**2 + displacement[1]**2)


    relative_direction = direction
    # convert to relative direction
    direction += vehicle.attitude.yaw

    angle = math.atan(distance/alt)


    # scale
    scale_xy = 0.01
    scale_z = 0.01
    max_speed = 0.5

    speed_xy = scale_xy * distance
    if speed_xy > max_speed:
      speed_xy = max_speed
    elif speed_xy < -max_speed:
      speed_xy = -max_speed
    speed_z = scale_z * math.sqrt(alt if alt > 0 else 1)

    velocity_x = speed_xy * math.cos(direction)
    velocity_y = speed_xy * math.sin(direction)

    velocity_z = speed_z * (math.radians(20) - angle)

    send_global_velocity(vehicle, velocity_x, velocity_y, velocity_z)
    print(circle)
    with open(log_file, "a") as f:
      print("%.2f\t%.2f\t %.4f\t%d\t%.5f\t%.5f\t%.5f\n" % (math.degrees(direction), math.degrees(relative_direction),
          math.degrees(angle), alt, velocity_x, velocity_y, velocity_z), file=f)
    print("%.2f\t%.2f\t %.4f\t%d\t%.5f\t%.5f\t%.5f\n" % (math.degrees(direction), math.degrees(relative_direction),
        math.degrees(angle), alt, velocity_x, velocity_y, velocity_z))

    if infinite == 0:
      print('infinite == 0')
      keep_running[0] = False

signal.signal(signal.SIGINT, signal_old)
