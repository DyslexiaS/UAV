import cv2
import numpy as np

img = cv2.imread('/home/user/cam1.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_blue = np.array([98,43,46])
upper_blue = np.array([102,255,255])
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
res_blue = cv2.bitwise_and(img,img, mask= mask_blue)
cv2.imwrite('save.jpg',res_blue)
