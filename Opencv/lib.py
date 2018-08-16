import cv2
import math
import numpy as np

def imread(path):
  return cv2.imread(path)

def imwrite(path, img):
  cv2.imwrite(path, img)

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
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

  circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20,
      param1=50,param2=20, minRadius=0, maxRadius=0)
      # param1=50,param2=20, minRadius=minRadius, maxRadius=maxRadius)
  print(alt, minRadius, maxRadius)
  print(circles)
  return circles

def best_circle(circles,img):
    if circles is None:
      return None
    # standard blue [176,122,61]
    s_color = [176,122,61] #s_color -> standard color
    circles = np.uint16(np.around(circles)) #need to round the x y coordinate for img[y,x]
    lost = 0
    circle_index = 0
    counter = 0
    for index in circles[0,:]:
        radius_2 = index[2]//2
        points = [(0,0), (radius_2, 0), (-radius_2, 0), (0, radius_2), (0, -radius_2)]
        B, G, R = 0, 0, 0
        for p in points:
            x, y = index[0]+p[0], index[1]+p[1]
            if x >= 720:
                x = 719
            elif x < 0:
                x = 0
            if y >= 480:
                y = 479
            elif y < 0:
                y = 0
            # average the color among center and other four points around it
            B += int(img[y,x][0])
            G += int(img[y,x][1])
            R += int(img[y,x][2])
        B = B // 5
        G = G // 5
        R = R // 5
        #print 'B:',B,'G:',G,'R:',R
        tmp_lost = (B-s_color[0])**2 + abs(G-s_color[1]) + abs(R-s_color[2]) #give blue color more weight
        tmp_lost = tmp_lost * (counter * 0.5 + 1) # set weight for circle order
        if lost == 0:
            lost = tmp_lost
        else:
            if lost > tmp_lost:
                lost = tmp_lost
                circle_index = counter
        counter += 1
        #print lost

    return circles[0][circle_index]   #return a 3d array [[[a,b,c]]]

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
