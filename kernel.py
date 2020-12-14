from PIL import Image
import numpy as np
import math
import cv2

class Kernel:
    def __init__(self, image, matrix, padding):
        self.inputImage=Image.open(image)
        # Reverse as Kivy has the list going from bottom right, up and left
        self.mask=matrix
        self.mask.reverse()
        self.padding = padding

    def run (self):
        ### Initialisation ( i.e. find new image size, get everything in right data type)
        # oriImg[x|y] stands for original Image [x|y]
        oriImgX, oriImgY = self.inputImage.size
        maskSize=int(math.sqrt(len(self.mask)))
        oriImg = np.array(self.inputImage.convert("L"))

        ### This is for the RGB stuff. Currently have it working on a single channel at a time
        # Maybe think about multi-threading each channel? That'd be cool :D
        r,g,b = self.inputImage.convert("RGB").split()
        r_channel = np.array(r)
        oriImg = np.array(g)
        b_channel = np.array(b)

        mask = np.array(self.mask)
        mask = np.reshape(mask, (maskSize, maskSize))
        mask = np.flipud(np.fliplr(mask))  # may be unnecessary

        ### Find shape of new image (Work on Padding) - may be unnecessary now
        outImgX = oriImgX
        outImgY = oriImgY
    #    if self.padding != 0:
    #        outImgX =+ self.padding * 2
    #        outImgY =+ self.padding * 2

        outImg = np.zeros((outImgX, outImgY),np.uint8)

        ### Iterate through image

        #kernelOrigin = (int((maskSize-1)/2),int((maskSize-1)/2))
        offset = int((maskSize-1)/2)
        # Pixels[x][y], where x refers to the rowIndex, y refers to columnIndex
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

        #returnImage = Image.fromarray(outImg.transpose())
        returnImage = Image.merge("RGB", (Image.fromarray(r_channel), Image.fromarray(outImg.transpose()), Image.fromarray(b_channel)))
        return returnImage

    def printInfo(self,image):
        print(image.format, image.size, image.mode)

# Test code
if __name__ == '__main__':
    testKernel = Kernel("./images/other_small_image.png",[-1,-2,-1,0,8,0,1,2,1], 1)
    test = testKernel.run()
