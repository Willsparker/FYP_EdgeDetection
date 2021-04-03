import cv2
import numpy as np
from math import sqrt
from PIL import Image

click_list = []

def callback(event, x, y, flags, param):
    if event == 1: 
        click_list.append((x,y))

def calculateDistanceBetweenPoints(x1,y1,x2,y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def run():# Create OpenCV Window, and make fullscreen

    cv2.namedWindow('img', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('img', callback)

    img = cv2.imread("files/tmp.png",0)
    while True:
        cv2.imshow('img',img)
        k = cv2.waitKey(1)
        if k == 27: 
            break
        if len(click_list) == 2:
            break
    cv2.destroyAllWindows()

    x1, y1 = click_list[0][0], click_list[0][1]
    x2, y2 = click_list[1][0], click_list[1][1]
    distance = calculateDistanceBetweenPoints(x1,y1,x2,y2)
    click_list.clear()
    return [x1,y1,distance]

def drawCircle(circle):
    image = cv2.imread("files/tmp.png",0)
    image = cv2.circle(image,(int(circle[0]),int(circle[1])),int(float(circle[2])),(0,0,0),3)
    return Image.fromarray(image).convert('L')
