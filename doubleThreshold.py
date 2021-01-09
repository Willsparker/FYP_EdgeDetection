from PIL import Image
import numpy as np

class doubleThreshold:
    # Takes in a PIL Image, and the 2 boundaries we want to filter out
    def __init__(self,img, bound):
        self.img = img
        self.bound = bound

    def run(self):
        self.quanitize(self.bound)

    def quanitize(self, bound):
        width, height = self.img.size
        pixData = self.img.load()
        for x in range(width):
            for y in range(height):
                if pixData[x,y][0] > bound:
                    pixData[x,y] = ( 255, pixData[x,y][1])
                else:
                    pixData[x,y] = ( 0 , pixData[x,y][1])

    def getImg(self):
        return self.img

if __name__ == '__main__':
    im = Image.open("./images/NOT_ON_GITHUB/No fake lens.bmp")
    im = im.convert("LA")
    dT = doubleThreshold(im,100)
    dT.run()
    im = dT.getImg()



