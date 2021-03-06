import cv2
import math
import numpy as np

def imread(path):
  return cv2.imread(path)

def imwrite(path, img):
  cv2.imwrite(path, img)

def rgb2blue(img):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  lower_blue = np.array([78,0,46]) #[78,0,46]
  upper_blue = np.array([155,255,255])
  mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
  res_blue = cv2.bitwise_and(img, img, mask=mask_blue)
  return res_blue

def alt2diagonal(alt):
  angle = 1.293 # rad.
  return 2*alt*math.tan(angle/2)

def detect_circles(img, alt):
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img = cv2.medianBlur(img,13)
  if alt != 0:
    absolute_error = 8
    relative_error = 0 #0.1
    min_alt = alt*(1-relative_error) - absolute_error
    if min_alt <= 0:
      min_alt = 0.1
    max_alt = alt*(1+relative_error) + absolute_error
    minRadius = int(2670/max_alt)
    maxRadius = int(2670/min_alt)
  else:
    minRadius = 0
    maxRadius = 0
  # param1=50,param2=20, minRadius=minRadius, maxRadius=maxRadius)

  try:
    circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20,
      param1=50,param2=6, minRadius=minRadius, maxRadius=maxRadius)
  except:
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
      param1=50,param2=6, minRadius=minRadius, maxRadius=maxRadius)
  print(alt, minRadius, maxRadius)
  print(circles)
  return circles

def best_circle(circles,img,resolution=(150,150)):
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
            if x >= resolution[0]:
                x = resolution[0] - 1
            elif x < 0:
                x = 0
            if y >= resolution[1]:
                y = resolution[1] - 1
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

def plot_arrow(img, point, center=(75,75), color=(0,0,255), line_width=5):
  cv2.line(img, center, point, color, line_width)
  pi = 3.1415926
  angle = math.atan2(center[1]-point[1], center[0]-point[0])
  arrow_x = point[0] + 20* math.cos(angle+math.pi*30/180)
  arrow_y = point[1] + 20* math.sin(angle+math.pi*30/180)
  cv2.line(img, point, (int(arrow_x),int(arrow_y)), color, line_width)
  arrow_x = point[0] + 20* math.cos(angle-math.pi*30/180)
  arrow_y = point[1] + 20* math.sin(angle-math.pi*30/180)
  cv2.line(img, point, (int(arrow_x),int(arrow_y)), color, line_width)
  return img

def add_text(img, H=100, D=80, Min=0, Max=100):
  if D>Max:
      color = (0,0,255)
  elif D<Min:
      color = (0,255,0)
  else:
      color = (0,255*(Max-D)/(Max-Min),255-255*(Max-D)/(Max-Min))

  text = 'Height: '+ str(H)
  cv2.putText(img,text,(75,120),cv2.FONT_HERSHEY_DUPLEX,0.3,color,1)
  text = 'Distance: '+ str(D)
  cv2.putText(img,text,(75,130),cv2.FONT_HERSHEY_DUPLEX,0.3,color,1)
  return img

def circle_not_found(img):
  text = "circle not found"
  cv2.putText(img,text,(5,75),cv2.FONT_HERSHEY_DUPLEX,0.5,(0,0,255),1)
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
