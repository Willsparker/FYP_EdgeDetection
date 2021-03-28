import cv2
import os
import re
from math import hypot
import numpy as np


CurPath = os.path.dirname(__file__)
# Path to output txt file:
iris_pos_file = CurPath + '/PrintedImages/IrisPositions.txt'
image_dir = CurPath + '/PrintedImages/'
output_dir = CurPath + '/PrintedIris/'

# Get all printed images, if they're .jpg
def getPrintedImageNames():
    return [os.path.splitext(f)[0] for f in os.listdir(image_dir) if os.path.splitext(f)[1] == ".jpg"]

def cropImage(image,centre,radius):
    mask = np.zeros(image.shape, dtype=np.uint8)
    cv2.circle(mask, centre, radius, (255,255,255), -1)

    # Bitwise-and for ROI
    ROI = cv2.bitwise_and(image, mask)

    # Crop mask and turn background white
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    x,y,w,h = cv2.boundingRect(mask)
    result = ROI[y:y+h,x:x+w]
    mask = mask[y:y+h,x:x+w]
    result[mask==0] = (0,0,0)

    return result

for image_path in getPrintedImageNames():
    with open(iris_pos_file,"r") as file:
        for line in file:
            if re.search(image_path, line):
                # Get all details from text file
                centre = line.split(' ')[1]
                centre = (int(centre.split(",")[0]),int(centre.split(",")[1]))
                distance = line.split(' ')[2]
                # Read image and draw the circle on it 
                image = cv2.imread(image_dir + image_path + ".jpg")
                cv2.imwrite(output_dir+image_path+".jpg",cropImage(image,centre,int(float(distance))))



