import numpy as np
from math import atan
from colorsys import hls_to_rgb
from PIL import Image

class colourize():
    def __init__(self, img, theta):
        self.img = img
        self.theta = theta

    def run(self):
        self.colourize()
    
    def colourize(self):
        img = self.img
        M, N = img.shape
        R = np.zeros([M,N])
        G = np.zeros([M,N])
        B = np.zeros([M,N])
        for i in range(1,M-1):
            for j in range(1,N-1):
                # If not the background
                if img[i,j] > 0:
                    hue = atan(self.theta[i,j])
                    RGB = hls_to_rgb(hue,0.5,0.5)
                    R[i,j] = int(RGB[0] * 255)
                    G[i,j] = int(RGB[1] * 255)
                    B[i,j] = int(RGB[2] * 255)
                # If part of background
                else:
                    R[i,j], G[i,j], B[i,j] = 0,0,0
        
        self.img = Image.merge('RGB',(Image.fromarray(R).convert('L'),Image.fromarray(G).convert('L'),Image.fromarray(B).convert('L')))

    def getImage(self):
        return self.img

    