from PIL import Image
from multiprocessing import Pool
import numpy as np
import math

class spatialFilter:
    def __init__(self, image, matrix, matCoeff, greyCheck, alphaCheck, normGreyCheck):
        self.infoString = ""
        self.inputImage = image
        self.imagePath = image
        self.mask = matrix
        self.matrixCo = matCoeff
        self.mask.reverse()
        self.greyCheck = greyCheck
        self.alphaCheck = alphaCheck
        self.normGreys = normGreyCheck

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
        mask = np.array(self.mask)
        mask = np.reshape(mask, (maskSize, maskSize))
        mask = mask * self.matrixCo

        offset = int((maskSize-1)/2)
        outImg = np.zeros((oriImgX, oriImgY),dtype=float)
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

                # I really want to get np.clip working.
                if value > 255 and not self.normGreys: 
                    value = 255
                elif value < 0 and not self.normGreys:
                    value = 0
                outImg[rowIndex][columnIndex] = value
        
        # This is where I realised Python can't pass by reference...
        if self.normGreys:
            outImg = self.normaliseImage(outImg)
        
        #outImg = np.clip(outImg,0,255)     
        return outImg.astype(np.uint8)


    def run (self):
        if not self.greyCheck:
            r,g,b,a = self.inputImage.convert("RGBA").split()
            r_channel = np.array(r)
            g_channel = np.array(g)
            b_channel = np.array(b)
            alpha_channel = np.array(a)
            p = Pool(3)
            pro_rchannel, pro_gchannel, pro_bchannel = p.map(self.processChannel,[r_channel,g_channel,b_channel])
            returnImage = Image.merge("RGBA", (Image.fromarray(pro_rchannel.transpose()), Image.fromarray(pro_gchannel.transpose()), Image.fromarray(pro_bchannel.transpose()), Image.fromarray(alpha_channel)))
        else:
            grey, a = self.inputImage.convert('LA').split()
            grey_channel = np.array(grey)
            alpha_channel = np.array(a)
            returnImage = Image.merge("LA", (Image.fromarray(self.processChannel(grey_channel).transpose()), Image.fromarray(alpha_channel)))

        ### Find shape of new image (Work on Padding) - may be unnecessary now
    #    outImgX = oriImgX
    #    outImgY = oriImgY
    #    if self.padding != 0:
    #        outImgX =+ self.padding * 2
    #        outImgY =+ self.padding * 2
        if self.alphaCheck:
            returnImage = self.rmBlankSpace(returnImage)
        return returnImage

    # Debug code
    def getInfoString(self):
        return self.infoString

    def rmBlankSpace(self, img):
        pixdata = img.load()
        width, height = img.size

        for y in range(height):
            for x in range(width):
                # Remove BlackSpace
                if all(v == 0 for v in pixdata[x,y][:-1]):
                    if self.greyCheck:
                        pixdata[x,y] = (0,0)
                    else:
                        pixdata[x,y] = (0,0,0,0)
                # Remove WhiteSpace
                if all(v == 255 for v in pixdata[x,y][:-1]):
                    if self.greyCheck:
                        pixdata[x,y] = (255,0)
                    else:
                        pixdata[x,y] = (255,255,255,0)

        return img

    # We want all values to be within the range of 0-255
    def normaliseImage(self, img):
        vMin, vMax = np.min(img) , np.max(img)
        width, height = img.shape
        for x in range(width):
            for y in range(height):
                img[x,y] = ((img[x,y] - vMin)/(vMax - vMin)) * 255
        return img


# Test code
if __name__ == '__main__':
    im = Image.open("./images/No fake lens.bmp")
    testKernel = spatialFilter(im,[1,0,-1,2,0,-2,1,0,-1], 0.5, True,True, True)
    test = testKernel.run()
    print(testKernel.getInfoString())
