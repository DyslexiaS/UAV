import cv2
import math
import numpy as np
from os import listdir
from os.path import isfile, join, dirname

import sys
sys.path.append(join(dirname(__file__), 'Opencv'))
from lib import imread, rgb2blue, detect_circles

mypath = 'img'
mask = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and 'mask' in f and 'qq' not in f]

# img = cv2.imread('~/image.jpg', cv2.IMREAD_GRAYSCALE)
for f in mask:
  print(f)
  img = imread(f)
  detect_circles(img, int(f[-7:-4]))
