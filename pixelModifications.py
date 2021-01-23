# Separate .py file for storing all the functions used to modify pixel values

# PIL may not be needed
from PIL import Image
from cv2 import cv2
import numpy as np

# Takes in the Image, and check referring to if the image is greyscale or not
# Returns the image having turned all black pixels transparent
def rmBlackSpace(img, greyCheck):
    pixdata = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            # Remove BlackSpace
            if all(v == 0 for v in pixdata[x,y][:-1]):
                if greyCheck:
                    pixdata[x,y] = (0,0)
                else:
                    pixdata[x,y] = (0,0,0,0)
    return img

# Takes in float images, ensures all pixel values are between 0-255
# returns the normalised image, as type np.uint8
def normaliseImageValues(img):
    vMin, vMax = np.min(img) , np.max(img)
    width, height = img.shape
    for x in range(width):
        for y in range(height):
            img[x,y] = ((img[x,y] - vMin)/(vMax - vMin)) * 255
    return img.astype(np.uint8)

# When we want to just round values to 0-255 (i.e. -VEs become 0, 256+ become 255)
# returns the image w/cutoff pixel values as type np.uint8
def cutOffImageValues(img):
    np.clip(img,0,255,out=img)
    return img.astype(np.uint8)

# Takes in 2 images that we want to blend together
# Returns the 2 images as PIL Image
def blend(im1,im2,alpha,greyCheck):

    if greyCheck:
        im1 = im1.convert('LA')
        im2 = im2.convert('LA')
    else:
        im1 = im1.convert('RGBA')
        im2 = im2.convert('RGBA')

    if im2.size != im1.size:
        im2 = im2.resize(im1.size)

    return Image.blend(im1,im2,alpha)

def applyCircles(img):
    # PIL Image to OpenCV Image
    pilImg = img.convert('RGB')
    ocvImg = np.array(pilImg)
    img = ocvImg[:, :, ::-1].copy()
    gsImg = cv2.cvtColor(ocvImg[:, :, ::-1].copy(), cv2.COLOR_BGR2GRAY)
    # Find cirlces
    circles = cv2.HoughCircles(gsImg, cv2.HOUGH_GRADIENT, 1, 20, param1 = 200, param2 = 20, minRadius = 0)#
    if circles is not None:
        draw_circle(circles,ocvImg)
        img = ocvImg
    # openCV to PIL
    return Image.fromarray(img)#cv2.cvtColor(img, cv2.COLOR_GRAY2RGB))

def draw_circle(circle,img):
    inner_circle = np.uint16(np.around(circles[0][0])).tolist()
    cv2.circle(img, (inner_circle[0], inner_circle[1]), inner_circle[2], (0, 255, 0), 1)