from PIL import Image
import numpy as np
import math
import cv2

class Kernel:
    def __init__(self, image, matrix):
        self.inputImage=Image.open(image)
        # Reverse as Kivy has the list going from bottom right, up and left
        self.mask=matrix
        self.mask.reverse()

    def run (self):
        #TODO: Make this work with RGB and Greyscale images
        width, height = self.inputImage.size
        matrixSize=math.sqrt(len(self.mask))
        pixels = np.array(self.inputImage.convert('L'))
        newImage = np.empty_like(pixels)

        userMatrix=np.empty((matrixSize, matrixSize))
        # Pixels[x][y], where x refers to the rowIndex, y refers to columnIndex

        # 8/12/20: Trying to convert mask to np array, to then iterate through

        #maskSum=sum(self.mask)   Will be required for guassian stuff
        for element in range(len(self.mask)):
            pos_x=int(element / math.sqrt(len(self.mask)))
            pos_y=int(element % math.sqrt(len(self.mask)))

        for rowIndex in range(height):
            for columnIndex in range(width):
                total = 0
                for element in range(len(self.mask)):
                    pass    

                #newImage[rowIndex][columnIndex] = 1.75 * pixels[rowIndex][columnIndex]
                #print(pixels[rowIndex-1][columnIndex-1])
                #newImage[rowIndex][columnIndex] = value               

        returnImage = Image.fromarray(newImage)
        return returnImage

    def printInfo(self,image):
        print(image.format, image.size, image.mode)

# Test code
if __name__ == '__main__':
    testKernel = Kernel("./small_image.png",[])
    test = testKernel.run()
