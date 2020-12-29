from PIL import Image
import numpy as np

class blendImage:
    def blend(self,Image1,Image2,alpha,greyCheck):
        im1 = Image.open(Image1).convert('RGB')
        im2 = Image.open(Image2).convert('RGB')
        if greyCheck:
            im1 = im1.convert('L')
            im2 = im2.convert('L')

        # There must be a better way of doing this..
        if im2.size != im1.size:
            im2 = im2.resize(im1.size)
        
        return Image.blend(im1,im2,alpha)
    
if __name__ == '__main__':
    blendImage.blend(None, "./images/test_image.png", "./images/test_image2.png", 0.5, False)


