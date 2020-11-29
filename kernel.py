from PIL import Image
import numpy as np

class Kernel:
    mask=[]
    def __init__(self, image, matrix):
        self.inputImage=Image.open(image)
        self.mask=matrix

    def run (self):
        # Get image width & height
        height , width = self.inputImage.size

        # If it's RGBA, we don't want Alpha
        imageData=self.inputImage.getdata().convert('RGB')
        
        bw_list=[int((sum(x) / float(len(x)))) for x in imageData]

        print("Height: ", height)
        print("Width: ", width)

        recon_image=np.empty([width,height])

        for x in range(width):
            for y in range(height):
                recon_image[x,y]=bw_list[width*x + y]
                

        print("DONE")
        return Image.fromarray(recon_image.astype(np.uint8))

# Test code
if __name__ == '__main__':
    testKernel = Kernel("/home/will/Documents/FYP/FYP_EdgeDetection/small_image.png",[])
    test = testKernel.run()
