import numpy as np
import colorsys

from math import sqrt, atan
from PIL import Image

import pixelModifications as pm

class mergeGradients:
    outImg = None
    
    def __init__(self,img1,img2,enableColor):
        self.firstImage = img1
        self.secondImage = img2
        self.color = enableColor

    def checkImageDimensions(self):
        if self.firstImage.shape != self.secondImage.shape:
            return False
        else:
            return True

    def run(self):
        self.mergePixelGradients()
        if not self.color:
            self.outImg = pm.cutOffImageValues(self.outImg)

    def mergePixelGradients(self):
        width, height = self.firstImage.shape
        self.outImg = np.zeros([width,height])
        R = np.zeros([width,height])
        G = np.zeros([width,height])
        B = np.zeros([width,height])
        for x in range(width):
            for y in range(height):
                self.outImg[x,y] = sqrt(self.firstImage[x,y]**2 + self.secondImage[x,y]**2)
                # This color thing kind of works, but times getting on
                # We'll see if I can get it working in future
                if self.color:
                    hue = atan(self.secondImage[x,y]/self.firstImage[x,y])
                    RGB = colorsys.hls_to_rgb(hue,0.5,0.5)
                    R[x,y] = int(RGB[0] * 255)
                    G[x,y] = int(RGB[1] * 255)
                    B[x,y] = int(RGB[2] * 255)
        
        if self.color:
            self.colourImage = Image.merge("RGB", (Image.fromarray(R).convert('L'), Image.fromarray(G).convert('L'), Image.fromarray(B).convert('L')))

    # Returns the np.Array as a PIL Image
    def getResultImg(self):
        if self.color:
            return self.colourImage
        return Image.fromarray(self.outImg)
        
