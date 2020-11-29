from PIL import Image
import numpy as np
import cv2

class Kernel:
    mask=[]
    def __init__(self, image, matrix):
        self.inputImage=Image.open(image)
        self.mask=matrix

    def run (self):
        # Get image width & height
        width, height = self.inputImage.size
        self.printInfo(self.inputImage)
        pixels = np.array(self.inputImage)

        # Pixels[x][y], where x refers to the rowIndex, y refers to columnIndex
        print(pixels.shape)

        for rowIndex in range(height):
            for columnIndex in range(width):
                # Test function
                pixels[rowIndex][columnIndex] = 1.25 * pixels[rowIndex][columnIndex]


        returnImage = Image.fromarray(pixels)

        print("Return Image type: ", type(returnImage))
        return returnImage

    def printInfo(self,image):
        print(image.format, image.size, image.mode)

# Test code
if __name__ == '__main__':
    testKernel = Kernel("./small_image.png",[])
    test = testKernel.run()
