#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __main__ import vehicle
import time
import math
import sys
from dronekit import VehicleMode
# from pynput import keyboard
from set_velocity import send_global_velocity

import sys,tty,termios
class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def rad2deg(rad):
  return 180 * rad / math.pi

def deg2rad(deg):
  return math.pi * deg / 180

def on_press(key):
    control_speed = 0.3
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    if key == keyboard.Key.esc:
      return False # stop listener
    elif k in ['up', 'down']:
      if k == 'up':
        velocity_z = -control_speed
      elif k == 'down':
        velocity_z = control_speed
      else:
        print('ERROR up down: ' + k)
      send_global_velocity(vehicle, 0, 0, velocity_z)
    elif k in ['left', 'right', 'w', 's']:
      direction_delta = 0
      if k == 'left':
        direction_delta = -math.pi/2
      elif k == 'right':
        direction_delta = math.pi/2
      elif k == 'w':
        direction_delta = 0
      elif k == 's':
        direction_delta = math.pi
      else:
        print('ERROR w s left right: ' + k)
        direction_delta = 0

      direction = vehicle.attitude.yaw + direction_delta
      velocity_x = control_speed * math.cos(direction)
      velocity_y = control_speed * math.sin(direction)
      send_global_velocity(vehicle, velocity_x, velocity_y, 0)
    elif k in ['a', 'd']:
      if k == 'a':
        yaw_delta = -10
      elif k == 'd':
        yaw_delta = 10
      else:
        yaw_delta = 0
      vehicle.gimbal.rotate(0, 0, rad2deg(vehicle.attitude.yaw) + yaw_delta)
    elif k in ['p', 'l']:
      if k == 'p':
        cmd = 'detect %d' % idx
      else:
        cmd = 'detect %d 1' % idx
      idx += 1
      sys.argv = cmd.split()
      execfile(sys.argv[0] + '.py')

    print(" is pressed")

def on_release(key):
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    if key == keyboard.Key.esc:
      return False # stop listener
    elif k in ['up', 'down', 'left', 'right', 'w', 's']:
      send_global_velocity(vehicle, 0, 0, 0)

def key2act(k):
    control_speed = 0.5
    global idx

    if k in ['i', 'k']:
      if k == 'i':
        velocity_z = -control_speed
      elif k == 'k':
        velocity_z = control_speed
      else:
        print('ERROR up down: ' + k)
      send_global_velocity(vehicle, 0, 0, velocity_z)
    elif k in ['j', 'l', 'w', 's']:
      direction_delta = 0
      if k == 'j':
        direction_delta = -math.pi/2
      elif k == 'l':
        direction_delta = math.pi/2
      elif k == 'w':
        direction_delta = 0
      elif k == 's':
        direction_delta = math.pi
      else:
        print('ERROR w s left right: ' + k)
        direction_delta = 0

      direction = vehicle.attitude.yaw + direction_delta
      velocity_x = control_speed * math.cos(direction)
      velocity_y = control_speed * math.sin(direction)
      send_global_velocity(vehicle, velocity_x, velocity_y, 0)
    elif k in ['a', 'd']:
      if k == 'a':
        yaw_delta = -10
      elif k == 'd':
        yaw_delta = 10
      else:
        yaw_delta = 0
      vehicle.gimbal.rotate(0, 0, rad2deg(vehicle.attitude.yaw) + yaw_delta)
    elif k in ['p', 'o']:
      if k == 'p':
        cmd = 'detect %d' % idx
      else:
        cmd = 'detect %d 1' % idx
      idx += 1
      sys.argv = cmd.split()
      execfile(sys.argv[0] + '.py')

    print(" is pressed")

try:
  idx = int(sys.argv[1])
except Exception, e:
  print(e)
  print('set default idx=0')
  idx = 0

send_global_velocity(vehicle, 0, 0, 0)
inkey = _Getch()
while True:
  k=inkey()
  print( "\nEnter:", end='')
  if k == 'q':
    break
  elif k == 'm':
    vehicle.mode = VehicleMode('GUIDED')
  key2act(k)


#lis = keyboard.Listener(on_press=on_press, on_release=on_release)
#lis.start() # start to listen on a separate thread
#lis.join() # no this if main thread is polling self.keys
