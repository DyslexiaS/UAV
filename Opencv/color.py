import cv2
import numpy as np
while True:
	inimg=raw_input("name:")
	img = cv2.imread("/home/user/git/UAV/img/"+inimg)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower_blue = np.array([90,43,46])
	upper_blue = np.array([124,255,255])
	mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
	res_blue = cv2.bitwise_and(img,img, mask= mask_blue)
	cv2.imwrite('mask_'+inimg+'.jpg',res_blue)
