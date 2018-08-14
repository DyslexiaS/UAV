#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import connect, VehicleMode
import sys
import time
import math
from pynput import keyboard
from set_velocity import send_global_velocity

# from picamera import PiCamera
# camera = PiCamera()

def print_info(vehicle):
  print("Autopilot Firmware version: %s" % vehicle.version)
  # 全球定位信息（经纬度，高度相对于平均海平面）
  print( "Global Location: %s" % vehicle.location.global_frame)
  # 全球定位信息（经纬度，高度相对于home点）
  print( "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
  # 相对home点的位置信息（向北、向东、向下）；解锁之前返回None
  print( "Local Location: %s" % vehicle.location.local_frame)
  # 无人机朝向（欧拉角：roll，pitch，yaw，单位为rad，范围-π到+π）
  print( "Attitude: %s" % vehicle.attitude)
  # 三维速度（m/s）
  print( "Velocity: %s" % vehicle.velocity)
  # GPS信息
  print( "GPS: %s" % vehicle.gps_0)
  # 地速（m/s）
  print( "Groundspeed: %s" % vehicle.groundspeed)
  # 空速（m/s）
  print( "Airspeed: %s" % vehicle.airspeed)
  # 云台信息（得到的为当前目标的roll, pitch, yaw，而非测量值。单位为度）
  print( "Gimbal status: %s" % vehicle.gimbal)
  # 电池信息
  print( "Battery: %s" % vehicle.battery)
  # EKF（拓展卡曼滤波器）状态
  print( "EKF OK?: %s" % vehicle.ekf_ok)
  # 超声波或激光雷达传感器状态
  print( "Rangefinder: %s" % vehicle.rangefinder)
  # 无人机朝向（度）
  print( "Heading: %s" % vehicle.heading)
  # 是否可以解锁
  print( "Is Armable?: %s" % vehicle.is_armable)
  # 系统状态
  print( "System status: %s" % vehicle.system_status.state)
  # 当前飞行模式
  print( "Mode: %s" % vehicle.mode.name)
  # 解锁状态
  print( "Armed: %s" % vehicle.armed)

def print_important(vehicle):
  print("alt = ", vehicle.location.global_relative_frame.alt)
  print( "Battery: %s" % vehicle.battery)

WIRELESS = 0
WIRED = 1
SITL = 2

mode = WIRED
try:
  mode = int(sys.argv[1])
except Exception, e:
  print(e)

print(mode)

if mode == WIRELESS:
  vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=False)
  vehicle.wait_ready(True, timeout=180)
elif mode == WIRED:
  vehicle = connect('/dev/ttyACM0', baud=115200, wait_ready=False)
  vehicle.wait_ready(True, timeout=180)
else:
  connect_Sitl = '127.0.0.1:14551'
  vehicle = connect(connect_Sitl, wait_ready = True)

def rad2deg(rad):
  return 180 * rad / math.pi

def deg2rad(deg):
  return math.pi * deg / 180

def on_press(key):
    control_speed = 0.5
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
    print(" is pressed")

def on_release(key):
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    if key == keyboard.Key.esc:
      return False # stop listener
    elif k in ['up', 'down', 'left', 'right', 'w', 's']:
      send_global_velocity(vehicle, 0, 0, 0)

def arm_and_takeoff(aTargetAltitude):
    print('arm and takeoff to %d' % (aTargetAltitude))
    print("Basic pre-arm checks")
    # vehicle.is_armable会检查飞控是否启动完成、有无GPS fix、卡曼滤波器
    # while not vehicle.mode.name == "INITIALISING":
    while not vehicle.is_armable:
        print(vehicle.mode.name + " Waiting for vehicle to initialise...")
        time.sleep(1)

    # 解锁无人机（电机将开始旋转）
    print("Arming motors")
    # 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机）
    vehicle.mode = VehicleMode("GUIDED")
    # 通过设置vehicle.armed状态变量为True，解锁无人机
    vehicle.armed = True

    # 在无人机起飞之前，确认电机已经解锁
    while not vehicle.armed:
      print(" Waiting for arming...")
      time.sleep(1)

    # 发送起飞指令
    print("Taking off!")
    # simple_takeoff将发送指令，使无人机起飞并上升到目标高度
    vehicle.simple_takeoff(aTargetAltitude)

    # 在无人机上升到目标高度之前，阻塞程序
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环
        # vehicle.location.global_relative_frame.alt为相对于home点的高度
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        # 等待1s
        time.sleep(1)

print_important(vehicle)
arm_and_takeoff(2)

send_global_velocity(vehicle, 0, 0, 0)
print( "Enter:", end='')
lis = keyboard.Listener(on_press=on_press, on_release=on_release)
lis.start() # start to listen on a separate thread
lis.join() # no this if main thread is polling self.keys

vehicle.mode = VehicleMode('ALT_HOLD')
while True:
  time.sleep(1)


# while True:
#   print_important(vehicle)
#   try:
#     print('#' * 30)
#     sys.argv = raw_input('execute: ').split()
#     execfile(sys.argv[0] + '.py')
#   except Exception, e:
#     print(e)
#     print('e.g. takeoff 10, control')
