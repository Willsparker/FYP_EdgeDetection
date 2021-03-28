import cv2
import os
import re

CurPath = os.path.dirname(__file__)
iris_pos_file = CurPath + '/PrintedImages/IrisPositions.txt'
image_dir = CurPath + '/PrintedImages/'

# Get all printed images, if they're .jpg
def getPrintedImageNames():
    return [os.path.splitext(f)[0] for f in os.listdir(image_dir) if os.path.splitext(f)[1] == ".jpg"]

# Create OpenCV Window, and make fullscreen
cv2.namedWindow('img', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("img",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

for image_path in getPrintedImageNames():
    with open(iris_pos_file,"r") as file:
        for line in file:
            if re.search(image_path, line):
                # Get all details from text file
                centre = line.split(' ')[1]
                distance = line.split(' ')[2]
                # Read image and draw the circle on it 
                image = cv2.imread(image_dir + image_path + ".jpg")
                image = cv2.circle(image,(int(centre.split(",")[0]),int(centre.split(",")[1])),int(float(distance)),(255,0,0),3)
                while True:
                    cv2.imshow('img', image)    
        
                    # Wait, and allow the user to quit with the 'esc' key
                    k = cv2.waitKey(1)
                    # If user presses 'esc' break 
                    if k == 27: break 