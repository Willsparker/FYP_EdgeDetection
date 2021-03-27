# Due to the Printed Eyes being much larger images than the originals,
# as well as using two different methods of finding the Iris, standardisation
# of all the data needs to be done.
#
# This file is responsible for :
#   - Taking the original images
#   - Applying the circle (either through IrisDetection.py, or using the Iris_Positions.txt file)
#   - Unwrapping the Iris using that circle
#   - Resizing to the right shape, and outputting to the 'Dataset' Directory

import cv2
import numpy as np
import os
import csv
# This is a copy of the 'IrisUnwrap.py' file, in the Classifier directory, setup to use OpenCV images, not PILImages
import IrisUnwrapper as iU
import re

# Path to original images
oriImgPath = "/home/will/Documents/FYP/FYP_EdgeDetection/Classifier/Images/"
# Path to printed images
priImgPath = "/home/will/Documents/FYP/FYP_EdgeDetection/Classifier/PrintedImages/"
# Path to Dataset dir
DSPath = "/home/will/Documents/FYP/FYP_EdgeDetection/Classifier/Dataset/"

# Get all image names into a list ( all files that are .jpg)
image_names = [ x for x in os.listdir(oriImgPath) + os.listdir(priImgPath) if str(x).endswith('.jpg') ]

# Write datafile, if it doesn't already exist
if not os.path.isfile(DSPath + 'data.csv'):
    with open(DSPath + 'data.csv', 'a') as file:
        fieldnames = ['Image_Index', 'Fake']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for index in range(len(image_names)):
            # If the iris is printed
            if image_names[index].startswith("I"):
                writer.writerow({'Image_Index': index, 'Fake': True})
            # If the iris is not printed
            else:
                writer.writerow({'Image_Index': index, 'Fake': False})


for name in image_names:
    image_index = image_names.index(name)
    
    # If these are the printed Iris'
    if name.startswith("I"):
        img = cv2.imread(priImgPath + name)
        filePath = priImgPath + "IrisPositions.txt"
        regex = name.split(".")[0]

    # If these are the non-printed Iris'
    else:
        img = cv2.imread(oriImgPath + name)
        filePath = oriImgPath + "IrisPositions.txt"
        regex = name

    regex += ".*"
    # Retrieve circle representing the Iris
    textfile = open(filePath, 'r')
    filetext = textfile.read()
    textfile.close()

    # Only one match should be found
    match = re.findall(regex, filetext)
    x = match[0].split(" ")[1].split(",")[0]
    y = match[0].split(" ")[1].split(",")[1]
    radius = match[0].split(" ")[2]
    # Useful for progress
    print(image_index)
    unwrappedIris = iU.irisUnwrapping(img,[int(x),int(y),int(float(radius))])

    # Reshape to 360 width, as thats how many samples taken. 130 was decided based on trial and error
    unwrappedIris = cv2.resize(unwrappedIris,(360,130))
    cv2.imwrite(DSPath + str(image_index) + ".jpg", unwrappedIris)
    
    
    




