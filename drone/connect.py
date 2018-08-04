#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from dronekit import connect, VehicleMode
import sys
import time
# from picamera import PiCamera

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
  print("alt = ", vehicle.location.global_relative_frame.alt)

def print_important(vehicle):
  print("alt = ", vehicle.location.global_relative_frame.alt)
  print( "Battery: %s" % vehicle.battery)

WIRELESS = 0
WIRED = 1
SITL = 2

mode = WIRELESS
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

#  camera = PiCamera()

while True:
  print_important(vehicle)
  try:
    print('#' * 30)
    sys.argv = raw_input('execute: ').split()
    execfile(sys.argv[0] + '.py')
  except Exception, e:
    print(e)
    print('e.g. takeoff 10, control')
