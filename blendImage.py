from PIL import Image
import numpy as np

class blendImage:
    def blend(self,Image1,Image2,alpha):

        im1 = Image.open(Image1).convert('RGB')
        im2 = Image.open(Image2).convert('RGB')

        # There must be a better way of doing this..
        if im2.size != im1.size:
            im2 = im2.resize(im1.size)
        
        return Image.blend(im1,im2,0.5)
    
if __name__ == '__main__':
    blendImage.blend("./images/test_image.png", "./images/test_image2.png")


