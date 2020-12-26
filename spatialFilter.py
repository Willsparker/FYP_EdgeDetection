from PIL import Image
from multiprocessing import Pool
import numpy as np
import math
import cv2

class spatialFilter:
    def __init__(self, image, matrix, matCoeff, greyCheck):
        self.inputImage = Image.open(image)
        # Reverse as the grid is read backwards
        self.mask = matrix
        self.matrixCo = matCoeff
        self.mask.reverse()
        self.greyCheck = greyCheck

    def processChannel(self, inputArray):
        # When multithreading, could use pool.starmap
        # See: https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments
        # Saves time so I don't have to find these variables 3 times.
        oriImgX, oriImgY = self.inputImage.size
        oriImg = inputArray
        maskSize=int(math.sqrt(len(self.mask)))
        mask = np.array(self.mask)
        mask = np.reshape(mask, (maskSize, maskSize))
        #mask = np.flipud(np.fliplr(mask))
        mask = mask * self.matrixCo

        offset = int((maskSize-1)/2)
        outImg = np.zeros((oriImgX, oriImgY),dtype=float    )
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
                value = int(sum(sum(tmpArray * mask)))
                if value > 255: 
                    value = 255
                elif value < 0:
                    value = 0
                outImg[rowIndex][columnIndex] = value
        
        #outImg = np.clip(outImg,0,255)     
        return outImg.astype(np.uint8)


    def run (self):
        if not self.greyCheck:
            r,g,b = self.inputImage.convert("RGB").split()
            r_channel = np.array(r)
            g_channel = np.array(g)
            b_channel = np.array(b)
            # Not a great implementation of multithreading- can take awhile :/ 
            p = Pool(3)
            pro_rchannel, pro_gchannel, pro_bchannel = p.map(self.processChannel,[r_channel,g_channel,b_channel])
            returnImage = Image.merge("RGB", (Image.fromarray(pro_rchannel.transpose()), Image.fromarray(pro_gchannel.transpose()), Image.fromarray(pro_bchannel.transpose())))
        else:
            greyImg = np.array(self.inputImage.convert('L'))
            returnImage = Image.fromarray(self.processChannel(greyImg).transpose())

        ### Find shape of new image (Work on Padding) - may be unnecessary now
    #    outImgX = oriImgX
    #    outImgY = oriImgY
    #    if self.padding != 0:
    #        outImgX =+ self.padding * 2
    #        outImgY =+ self.padding * 2

        return returnImage

    # Debug code
    def printInfo(self,image):
        print(image.format, image.size, image.mode)

# Test code
if __name__ == '__main__':
    testKernel = Kernel("./images/other_small_image.png",[0,0,0,0,2,0,0,0,0], 0.5, True)
    test = testKernel.run()
