from PIL import Image
from multiprocessing import Pool
from itertools import repeat
import numpy as np
import math
import cv2

class Kernel:
    def __init__(self, image, matrix, padding):
        self.inputImage=Image.open(image)
        # Reverse as the grid is read backwards
        self.mask=matrix
        self.mask.reverse()
        self.padding = padding

    
    # Separate function to allow for multi-threading later
    def processChannel(self, inputArray):
        # When multithreading, could use pool.starmap
        # See: https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments
        # Saves time so I don't have to find these variables 3 times.
        oriImgX, oriImgY = self.inputImage.size
        oriImg = inputArray
        maskSize=int(math.sqrt(len(self.mask)))

        mask = np.array(self.mask)
        mask = np.reshape(mask, (maskSize, maskSize))
        mask = np.flipud(np.fliplr(mask))  

        offset = int((maskSize-1)/2)
        outImg = np.zeros((oriImgX, oriImgY),np.uint8)
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
                ## Theres a better way of doing this outside the loops with np.clip(a,0,255)
                # But because outImg is a uint8 array, it wraps around anyway (look at changing them)
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImg[rowIndex][columnIndex] = int(sum(sum(tmpArray * mask)))
        return outImg


    def run (self):
        # TODO: Use Checkbox to determine if RGB or not.
        # Could use 3 / 4 to determine which channels to process.
        r,g,b = self.inputImage.convert("RGB").split()
        r_channel = np.array(r)
        g_channel = np.array(g)
        b_channel = np.array(b)
        
        pro_rchannel = self.processChannel(r_channel).transpose()
        pro_gchannel = self.processChannel(g_channel).transpose()
        pro_bchannel = self.processChannel(b_channel).transpose()

        ### Find shape of new image (Work on Padding) - may be unnecessary now
    #    outImgX = oriImgX
    #    outImgY = oriImgY
    #    if self.padding != 0:
    #        outImgX =+ self.padding * 2
    #        outImgY =+ self.padding * 2

        returnImage = Image.merge("RGB", (Image.fromarray(pro_rchannel), Image.fromarray(pro_gchannel), Image.fromarray(pro_bchannel)))
        return returnImage

    # Debug code
    def printInfo(self,image):
        print(image.format, image.size, image.mode)

# Test code
if __name__ == '__main__':
    testKernel = Kernel("./images/other_small_image.png",[-1,-2,-1,0,8,0,1,2,1], 1)
    test = testKernel.run()
