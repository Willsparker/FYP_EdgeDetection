import numpy as np
from math import sqrt
from PIL import Image

import pixelModifications as pm

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
        self.outImg = pm.cutOffImageValues(self.outImg)

    def mergePixelGradients(self):
        width, height = self.firstImage.shape
        self.outImg = np.zeros([width,height])

        for x in range(width):
            for y in range(height):
                self.outImg[x,y] = sqrt(self.firstImage[x,y]**2 + self.secondImage[x,y]**2)        

    # Returns the np.Array as a PIL Image
    def getResultImg(self):
        return Image.fromarray(self.outImg)
        
