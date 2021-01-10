from PIL import Image
import numpy as np

class doubleThreshold:
    # Takes in a PIL Image, and the 2 boundaries we want to filter out
    def __init__(self,img, lowerBound, upperBound):
        self.img = img
        self.lBound = lowerBound
        self.uBound = upperBound

    def run(self):
        self.quanitize(self.lBound, True)
        self.quanitize(self.uBound, False)

    # BoundType in this instance is a bool:
    #   - True means values lower than 'bound' are quantized to 0
    #   - False means values higher than 'bound' are quanitzed to 255
    def quanitize(self, bound, boundType):
        width, height = self.img.size
        pixData = self.img.load()
        for x in range(width):
            for y in range(height):
                if boundType and pixData[x,y][0] < bound:
                    pixData[x,y] = ( 0, pixData[x,y][1])
                elif not boundType and pixData[x,y][0] > bound:
                    pixData[x,y] = ( 255 , pixData[x,y][1])

    def getImg(self):
        return self.img

if __name__ == '__main__':
    im = Image.open("./images/NOT_ON_GITHUB/No fake lens.bmp")
    im = im.convert("LA")
    dT = doubleThreshold(im,100,150)
    dT.run()
    im = dT.getImg()



