from PIL import Image
from multiprocessing import Pool
import numpy as np
# TODO: Only import the required function
import math

from SpatialApplicator import pixelModifications as pm

class spatialFilter:
    pixelGradients = None

    def __init__(self, image, matrix, matCoeff, greyCheck, alphaCheck, normGreyCheck, pixelGradCheck):
        self.infoString = ""
        self.inputImage = image
        self.mask = matrix
        self.matrixCo = matCoeff
        self.mask.reverse()
        self.greyCheck = greyCheck
        self.alphaCheck = alphaCheck
        self.normGreys = normGreyCheck
        self.pixelGradCheck = pixelGradCheck
        maskSize = int(math.sqrt(len(matrix)))
        maskMat = np.array(matrix).reshape(maskSize,maskSize)

        self.infoString += "\nMask: \n" + str(maskMat)
        self.infoString += "\nMatrix Coefficient: " + str(matCoeff)
        self.infoString += "\nGreyScale: " + str(greyCheck)
        self.infoString += "\nRm BlankSpace: " + str(alphaCheck)
        self.infoString += "\nNormalise Greys: " + str(normGreyCheck)

    def processChannel(self, inputArray):
        # When multithreading, could use pool.starmap
        # See: https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments
        # Saves time so I don't have to find these variables 3 times.
        oriImgX, oriImgY = inputArray.shape
        oriImg = inputArray
        maskSize=int(math.sqrt(len(self.mask)))
        mask = self.matrixCo * np.array(self.mask).reshape(maskSize,maskSize)

        offset = int((maskSize-1)/2)
        outImg = np.zeros((oriImgX, oriImgY),dtype=float)
        self.loopPos = 0
        for rowIndex in range(oriImgX-1):
            for columnIndex in range(oriImgY-1):
                sum = 0
                self.loopPos = oriImgX * (rowIndex+1) + (columnIndex+1)
                # This implementation is slower for larger masks - I may make a check so if maskSize is over a certain amount
                for maskRowIndex in range(maskSize):
                    for maskColIndex in range(maskSize):
                        try:
                            imgPosX = rowIndex - offset + maskRowIndex
                            imgPosY = columnIndex - offset + maskColIndex
                            sum  += oriImg[imgPosX][imgPosY] * mask[maskRowIndex][maskColIndex]
                        except IndexError:
                            # IF this is goes beyond the bounds of the image, I'd just add 0 to the sum anyway,
                            # So lets just pass
                            pass
                outImg[rowIndex][columnIndex] = sum

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
            
            returnImage = Image.merge("RGBA", (Image.fromarray(pro_rchannel), Image.fromarray(pro_gchannel), Image.fromarray(pro_bchannel), Image.fromarray(alpha_channel)))
        else:
            grey, a = self.inputImage.convert('LA').split()
            grey_channel = self.processChannel(np.array(grey))
            
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

    def getInfoString(self):
        return self.infoString

    def getPixelGradients(self):
        return self.pixelGradients

    def getLoopPosition(self):
        return self.loopPos



# Test code
if __name__ == '__main__':
    im = Image.open("./images/NOT_ON_GITHUB/No fake lens.bmp")
    testKernel = spatialFilter(im,[1,0,-1,2,0,-2,1,0,-1], 0.5, True,True, False, True)
    test = testKernel.run()
    print(testKernel.getInfoString())