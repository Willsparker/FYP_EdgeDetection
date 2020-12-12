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
        oriImg = np.array(self.inputImage.convert('L'))
        mask = np.array(self.mask)
        mask = np.reshape(mask, (maskSize, maskSize))
    #    mask = np.flipud(np.fliplr(mask))  # may be unnecessary

        ### Find shape of new image (Work on Padding)
        outImgX = oriImgX
        outImgY = oriImgY
    #    if self.padding != 0:
    #        outImgX =+ self.padding * 2
    #        outImgY =+ self.padding * 2

        outImg = np.zeros((outImgX,outImgY))

        ### Iterate through image

        kernelOrigin = (int((maskSize-1)/2),int((maskSize-1)/2))

        # Pixels[x][y], where x refers to the rowIndex, y refers to columnIndex

        # NEXT IDEA: Create an array from values around the pixel
        # Times the mask and new array together
        # sum using sum(sum(a*b))
        # See https://stackoverflow.com/questions/26493689/create-numpy-array-from-another-array-by-specifying-rows-and-columns
        for rowIndex in range(oriImgX):
            for columnIndex in range(oriImgY):
                total = 0
                #total += outImg[rowIndex][columnIndex] 

                #for kernelRow in range(len(mask)):
                #    for element in range(len(mask)):
                        # If we've got the kernel origin
                #        if (kernelRow,element) == kernelOrigin:
                #            total+=mask[kernelRow][element]*oriImg[rowIndex][columnIndex]
                #outImg[rowIndex][columnIndex] = total
                                 

        returnImage = Image.fromarray(outImg)
        return returnImage

    def printInfo(self,image):
        print(image.format, image.size, image.mode)

# Test code
if __name__ == '__main__':
    testKernel = Kernel("./small_image.png",[1,2,3,4,5,6,7,8,9], 1)
    test = testKernel.run()
