
class Kernel:

    mask=[]
    def __init__(self, image, matrix):
        self.inputImage=image
        self.mask=matrix

    def run (self):
        print(type(self.inputImage))

    # Image tutorial
    # https://blog.kivy.org/2014/01/kivy-image-manipulations-with-mesh-and-textures/
