import numpy as np
import os
from cv2 import cv2
from math import hypot
from PIL import Image
import matplotlib.pyplot as plt

class irisDetector:
    def __init__(self, img):
        img = img.convert('RGB')
        img = np.array(img)
        self.img = img[:, :, ::-1].copy() 
    
    def run(self):
        original_image = self.img.copy()
        # Grabcut
        self.img = self.grab_cut(self.img.copy())
        # Get Inverted Greyscale Image
        self.img = cv2.cvtColor(self.img.copy(), cv2.COLOR_BGR2GRAY)
        gsInvertedImg = cv2.bitwise_not(self.img.copy())
        # Enhance black pixel intensities
        bhImage = self.blackHat(gsInvertedImg.copy())
        # Remove surface relection
        self.img = self.rmReflection(gsInvertedImg.copy(),bhImage.copy())
        # Edge Detection(?)
        self.img = self.canny_edge(self.img.copy())

        circles = self.hough_circle(self.img.copy())
        if circles is not None:
            inner_circle = self.draw_circle(circles,original_image)
            self.img = original_image
            x = self.img.shape[0]
            y = self.img.shape[1]
            self.crop_image(x,y,inner_circle,original_image)
            return True
        else:
            return False

    # Finds foreground against background
    def grab_cut(self,raw_image):
        number_of_interation = 5
        channel_mask = np.zeros((raw_image.shape[0], raw_image.shape[1]), np.uint8)
        region_of_interest = (50, 50, 450, 290)
        background_model = np.zeros((1,65),np.float64)
        foreground_model = np.zeros((1,65),np.float64)
        mode_of_operation = cv2.GC_INIT_WITH_RECT
        cv2.grabCut(raw_image, channel_mask, region_of_interest, background_model, foreground_model, number_of_interation, mode_of_operation)
        normalization_mask = np.where((channel_mask == 2)|(channel_mask == 0), 0, 1).astype('uint8')
        removed_background_image = raw_image * (normalization_mask[:,:,np.newaxis])
        return removed_background_image

    def blackHat(self,img):
        return cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, np.ones((5, 5), np.uint8))

    def rmReflection(self,bhImage,gsInvertedImg):
        img = cv2.add(gsInvertedImg, bhImage)
        return cv2.equalizeHist(cv2.medianBlur(img,5))

    def canny_edge(self,img):
        region_of_interest = cv2.bitwise_not(img)
        mode_of_operation = cv2.THRESH_BINARY_INV
        _, thresholded_image = cv2.threshold(region_of_interest, 50, 255, mode_of_operation)
        return cv2.Canny(thresholded_image, 200, 100)

    def hough_circle(self,img):
        mode_of_operation = cv2.HOUGH_GRADIENT
        return cv2.HoughCircles(img, mode_of_operation, 1, 20, param1 = 200, param2 = 20, minRadius = 0)

    def draw_circle(self,circles,img):
        inner_circle = np.uint16(np.around(circles[0][0])).tolist()
        self.iris_circle = inner_circle
        cv2.circle(img, (inner_circle[0], inner_circle[1]), inner_circle[2], (0, 255, 0), 1)
        return inner_circle

    def crop_image(self,x,y,inner_circle,img):
        for j in range(x):
            for k in range(y):
                if hypot(k - inner_circle[0], j - inner_circle[1]) >= inner_circle[2]:
                    img[j, k] = 0
        self.img = img

    def getImage(self):
        return Image.fromarray(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))

    def getIrisCircle(self):
        return self.iris_circle