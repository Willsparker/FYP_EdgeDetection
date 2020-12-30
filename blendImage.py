from PIL import Image
import numpy as np

class blendImage:
    def blend(self,im1,im2,alpha,greyCheck,alphaCheck):

        if greyCheck:
            im1 = im1.convert('LA')
            im2 = im2.convert('LA')
        else:
            im1 = im1.convert('RGBA')
            im2 = im2.convert('RGBA')
        
        # See: https://stackoverflow.com/questions/765736/how-to-use-pil-to-make-all-white-pixels-transparent
        # Just testing tbh
        newData = []
        data1 = im1.getdata()
        data2 = im2.getdata()
        if alphaCheck:
            for item in data1:
                # LA
                if len(item) == 2:
                    if item[0] == 0 or item[0] == 255:
                        newData.append((255,0))
                    else:
                        newData.append(item)
                # RGBA
                elif len(item) == 4:
                    if item[0] == 0 and item[1] == 0 and item[2] == 0:
                        newData.append((255,255,255,0))
                    else:
                        newData.append(item)

        if im2.size != im1.size:
            im2 = im2.resize(im1.size)
        print(alpha)
        return Image.blend(im1,im2,alpha)
    
if __name__ == '__main__':
    im1 = Image.open("./images/test_image.png")
    im2 = Image.open("./images/test_image2.png")
    blendImage.blend(None, im1,im2, 0.5, False, True)


