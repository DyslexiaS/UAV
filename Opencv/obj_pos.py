#!/usr/bin/python2
from __future__ import print_function
import numpy as np
import imutils
import cv2
import time

def readImage():
    img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)
    ret, thresh = cv2.threshold(img, 127, 225, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    print ('there are ' + str(len(contours)) + 'contours')
    cnt = contours[0]
    print ('there are ' + str(len(cnt)) + 'points in contours[0]')
    print (cnt)

    cnt = contours[1]
    print ('there are ' + str(len(cnt)) + 'points in contours[1]')
    print (cnt)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def centerOfContours():
    #tStart = time.time()
    img = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5,5), 0)
    thresh = cv2.threshold(blurred, 60, 225, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]
    for c in contours:
        M = cv2.moments(c)
        if M['m00'] != 0:
            cX = int(M['m10']/M['m00'])
            cY = int(M['m01']/M['m00'])
        else:
            cX, cY = 0, 0

    #draw the center of shape
    cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
    cv2.circle(img, (cX, cY), 7, (0, 0, 0), -1)
    height, width = img.shape[:2]
    print (cX-width/2, -(cY-height/2))
    #tEnd = time.time()
    #print('time = %f' %(tEnd - tStart))
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    #readImage()
    while True:
        centerOfContours()

if __name__ == '__main__':
    main()
