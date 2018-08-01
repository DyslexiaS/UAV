#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __main__ import vehicle
import sys
from dronekit import VehicleMode

try:
  vehicle.mode = VehicleMode(sys.argv[1].upper())
except Exception, e:
  print(e)
