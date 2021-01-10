from PIL import Image
from multiprocessing import Pool
import numpy as np
import math

import pixelModifications as pm

class spatialFilter:
    pixelGradients = None

    def __init__(self, image, matrix, matCoeff, greyCheck, alphaCheck, normGreyCheck, pixelGradCheck):
        self.infoString = ""
        self.inputImage = image
        self.imagePath = image
        self.mask = matrix
        self.matrixCo = matCoeff
        self.mask.reverse()
        self.greyCheck = greyCheck
        self.alphaCheck = alphaCheck
        self.normGreys = normGreyCheck
        self.pixelGradCheck = pixelGradCheck

        self.infoString += "\nMask: " + str(matrix)
        self.infoString += "\nMatrix Coefficient: " + str(matCoeff)
        self.infoString += "\nGreyScale: " + str(greyCheck)
        self.infoString += "\nRm BlankSpace: " + str(alphaCheck)
        self.infoString += "\nNormalise Greys: " + str(normGreyCheck)

    def processChannel(self, inputArray):
        # When multithreading, could use pool.starmap
        # See: https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments
        # Saves time so I don't have to find these variables 3 times.
        oriImgX, oriImgY = self.inputImage.size
        oriImg = inputArray
        maskSize=int(math.sqrt(len(self.mask)))
        mask = self.matrixCo * np.array(self.mask).reshape(maskSize,maskSize)
    
        offset = int((maskSize-1)/2)
        outImg = np.zeros((oriImgX, oriImgY),dtype=float)

        # Possibly a better way of doing this?!
        # https://www.cs.utexas.edu/~theshark/courses/cs324e/lectures/cs324e-6.pdf
        for rowIndex in range(oriImgX-1):
            for columnIndex in range(oriImgY-1):
                x = [item for item in (list(range(rowIndex-offset,rowIndex)) + list(range(rowIndex,rowIndex+offset+1))) if item >=0 if item < (oriImgX) ]
                y = [item for item in (list(range(columnIndex-offset,columnIndex)) + list(range(columnIndex,columnIndex+offset+1))) if item >=0 if item < (oriImgY) ]
                tmpArray = np.zeros((maskSize,maskSize))
                newArray = oriImg[np.ix_(y,x)]
                x_offset, y_offset = 0,0

                if 0 in x:
                    x_offset = maskSize - newArray.shape[0]
                if 0 in y:
                    y_offset = maskSize - newArray.shape[1]

                tmpArray[x_offset:newArray.shape[0]+x_offset,y_offset:newArray.shape[1]+y_offset] = newArray
                outImg[rowIndex][columnIndex] = int(sum(sum(tmpArray * mask)))
        
        # Returning outImg as a float, as not to overflow.
        # Overflowed values are sorted later 
        return outImg

    def run (self):
        if not self.greyCheck:
            r,g,b,a = self.inputImage.convert("RGBA").split()
            r_channel = np.array(r)
            g_channel = np.array(g)
            b_channel = np.array(b)
            alpha_channel = np.array(a)
            p = Pool(3)
            pro_rchannel, pro_gchannel, pro_bchannel = p.map(self.processChannel,[r_channel,g_channel,b_channel])
            if self.normGreys:
                pro_rchannel, pro_gchannel, pro_bchannel = p.map(pm.normaliseImageValues, [pro_rchannel,pro_gchannel,pro_bchannel])
            else:
                pro_rchannel, pro_gchannel, pro_bchannel = p.map(pm.cutOffImageValues, [pro_rchannel,pro_gchannel,pro_bchannel])
            
            returnImage = Image.merge("RGBA", (Image.fromarray(pro_rchannel.transpose()), Image.fromarray(pro_gchannel.transpose()), Image.fromarray(pro_bchannel.transpose()), Image.fromarray(alpha_channel)))
        else:
            grey, a = self.inputImage.convert('LA').split()
            
            grey_channel = self.processChannel(np.array(grey)).transpose()
            
            if self.pixelGradCheck:
                # The need for `copy` here messed me up
                # Python's pass by reference rules are a bit confusing :/
                self.pixelGradients = np.copy(grey_channel)

            if self.normGreys:
                grey_channel = pm.normaliseImageValues(grey_channel)
            else:
                grey_channel = pm.cutOffImageValues(grey_channel)
            
            alpha_channel = np.array(a)

            returnImage = Image.merge("LA", (Image.fromarray(grey_channel), Image.fromarray(alpha_channel)))

        if self.alphaCheck:
            returnImage = pm.rmBlackSpace(returnImage,self.greyCheck)

        

        return returnImage

    # Debug code
    def getInfoString(self):
        return self.infoString

    def getPixelGradients(self):
        return self.pixelGradients



# Test code
if __name__ == '__main__':
    im = Image.open("./images/NOT_ON_GITHUB/No fake lens.bmp")
    testKernel = spatialFilter(im,[1,0,-1,2,0,-2,1,0,-1], 0.5, True,True, False, True)
    test = testKernel.run()
    print(testKernel.getInfoString())