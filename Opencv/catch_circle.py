import cv2
import numpy as np
import math
from os import listdir
from os.path import isfile, join

def catch_circle(path, dis):
  img = cv2.imread(path,0)
  img = cv2.medianBlur(img,13)

  error = 0.2
  min_dis = min(dis*(1-error), dis-100)
  if min_dis <= 0:
    min_dis = 0.1
  max_dis = min(dis*(1+error), dis+100)
  minRadius = int(math.floor(35.6 * 865 / (max_dis*1.38*2)))
  maxRadius = int(math.ceil(35.6 * 865 / (min_dis*1.38*2)))

  circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
      param1=50,param2=20, minRadius=minRadius, maxRadius=maxRadius)
  circles = np.uint16(np.around(circles))
  print(dis, minRadius, maxRadius)
  print(circles)

  if circles is not None  :
    for i in circles[0,:]:
      center = (i[0], i[1])
      radius = i[2]
      cv2.circle(img, center, 3, (0, 0, 0), -1, 8, 0)
      cv2.circle(img, center, radius, (255,255,255),3, 8, 0)
  cv2.imwrite(path+'qq.jpg', img)
  # cv2.namedWindow("detected circles",0);
  # cv2.resizeWindow("detected circles", 1280, 960);
  # cv2.imshow("detected",img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()
