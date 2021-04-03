import numpy as np
import colorsys

from math import sqrt, atan
from PIL import Image

from SpatialApplicator import pixelModifications as pm

class mergeGradients:
    outImg = None
    theta = None
    
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

    def mergePixelGradients(self):
        # See: https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123
        Ix = self.firstImage
        Iy = self.secondImage
        G = np.hypot(Ix, Iy)
        self.outImg = G / G.max() * 255 # Normalisation
        self.theta = np.arctan2(Iy,Ix)

    # Returns the np.Array as a PIL Image
    def getResultImg(self):
        return Image.fromarray(self.outImg).convert('L')

    # Returns the array of angles
    def getTheta(self):
        return self.theta
    
    # Returns the np.Array as an array
    def getOutImg(self):
        return self.outImg


