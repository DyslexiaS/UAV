import cv2
import math
import numpy as np

def imread(path):
  return cv2.imread(path,0)

def imwrite(path, img):
  cv2.imwrite(path,img)

def rgb2blue(img):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  lower_blue = np.array([90,43,46])
  upper_blue = np.array([124,255,255])
  mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
  res_blue = cv2.bitwise_and(img, img, mask=mask_blue)
  return res_blue

def alt2diagonal(alt):
  angle = 1.293 # rad.
  return 2*alt*math.tan(angle/2)

def detect_circles(img, alt):
  img = cv2.medianBlur(img,13)
  error = 0.2
  absolute_error = 80
  relative_error = 0.2
  min_alt = alt*(1-relative_error) - absolute_error
  if min_alt <= 0:
    min_alt = 0.1
  max_alt = alt*(1+relative_error) + absolute_error
  minRadius = int(math.floor(35.6 * 865 / alt2diagonal(max_alt) / 2))
  maxRadius = int(math.ceil(35.6 * 865 / alt2diagonal(min_alt) / 2))

  circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
      param1=50,param2=20, minRadius=minRadius, maxRadius=maxRadius)
  print(alt, minRadius, maxRadius)
  print(circles)
  return circles

def best_circle(circles):
  return None if circles is None else circles[0][0]

def draw_circle(img, circle):
  if circle is None:
    return
  center = circle[0], circle[1]
  radius = circle[2]
  cv2.circle(img, center, 3, (0, 0, 0), -1, 8, 0)
  cv2.circle(img, center, radius, (255,255,255),3, 8, 0)
  return img

  # if circles is not None  :
  #   for i in circles[0,:]:
  #     center = (i[0], i[1])
  #     radius = i[2]
  # cv2.imwrite("%d_qq.jpg" % (dis), img)

  # cv2.namedWindow("detected circles",0);
  # cv2.resizeWindow("detected circles", 1280, 960);
  # cv2.imshow("detected",img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()
