import numpy as np
from math import sqrt
from PIL import Image

class mergeGradients:
    outImg = None
    
    def __init__(self,img1,img2):
        self.firstImage = img1
        self.secondImage = img2

    
    def checkImageDimensions(self):
        if self.firstImage.shape != self.secondImage.shape:
            return False
        else:
            return True

    def run(self):
        self.mergePixelGradients()
        #self.normaliseImageValues()
        self.cutOffImageValues()

    def mergePixelGradients(self):
        width, height = self.firstImage.shape
        self.outImg = np.zeros([width,height])

        for x in range(width):
            for y in range(height):
                self.outImg[x,y] = sqrt(self.firstImage[x,y]**2 + self.secondImage[x,y]**2)        
        
    def normaliseImageValues(self):
        vMin, vMax = np.min(self.outImg) , np.max(self.outImg)
        width, height = self.outImg.shape
        for x in range(width):
            for y in range(height):
                self.outImg[x,y] = ((self.outImg[x,y] - vMin)/(vMax - vMin)) * 255
        
        self.outImg = self.outImg.astype(np.uint8)

    def cutOffImageValues(self):
        np.clip(self.outImg,0,255,out=self.outImg)
        self.outImg = self.outImg.astype(np.uint8)

    def getResultImg(self):
        return Image.fromarray(self.outImg)
        
