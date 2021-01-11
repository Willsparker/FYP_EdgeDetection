import numpy as np
from PIL import Image

class cannyEdgeDetection:
    def __init__(self,img,theta):
        self.img = img
        self.theta = theta

    def run(self):
        self.nonMaxSuppression()
        self.doubleThreshold()
        self.hysteresis()

    def nonMaxSuppression(self):
        img = self.img
        M, N = img.shape
        Z = np.zeros((M,N), dtype=np.int32)
        angle = self.theta * 180. / np.pi
        angle[angle < 0] += 180
    
        for i in range(1,M-1):
            for j in range(1,N-1):
                try:
                    q = 255
                    r = 255
                #angle 0
                    if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                        q = img[i, j+1]
                        r = img[i, j-1]
                #angle 45
                    elif (22.5 <= angle[i,j] < 67.5):
                        q = img[i+1, j-1]
                        r = img[i-1, j+1]
                #angle 90
                    elif (67.5 <= angle[i,j] < 112.5):
                        q = img[i+1, j]
                        r = img[i-1, j]
                #angle 135
                    elif (112.5 <= angle[i,j] < 157.5):
                        q = img[i-1, j-1]
                        r = img[i+1, j+1]

                    if (img[i,j] >= q) and (img[i,j] >= r):
                        Z[i,j] = img[i,j]
                    else:
                        Z[i,j] = 0

                except IndexError:
                    pass
        
        self.img = Z

    def doubleThreshold(self):
        
        img = self.img
        lowThresholdRatio=0.05
        highThresholdRatio=0.09
    
        highThreshold = img.max() * highThresholdRatio;
        lowThreshold = highThreshold * lowThresholdRatio;
    
        M, N = img.shape
        res = np.zeros((M,N), dtype=np.int32)
    
        weak = np.int32(25)
        strong = np.int32(255)
    
        strong_i, strong_j = np.where(img >= highThreshold)
        zeros_i, zeros_j = np.where(img < lowThreshold)
    
        weak_i, weak_j = np.where((img <= highThreshold) & (img >= lowThreshold))
    
        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak
        
        self.weak = weak
        self.strong = strong
        self.img = res
    
    def hysteresis(self):
        weak = self.weak
        strong = self.strong
        img = self.img
        
        M, N = img.shape  
        for i in range(1, M-1):
           for j in range(1, N-1):
            if (img[i,j] == weak):
                try:
                    if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
                        or (img[i, j-1] == strong) or (img[i, j+1] == strong)
                        or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
                        img[i, j] = strong
                    else:
                        img[i, j] = 0
                except IndexError:
                    pass
        
    def getImage(self):
        return Image.fromarray(self.img).convert('L')

    def getImageArray(self):
        return self.img

    