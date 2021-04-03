import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def irisUnwrapping(img, iris_circle):
    img = img.convert('RGB')
    img = np.array(img)
    image = img[:, :, ::-1].copy() 

    center = (iris_circle[0], iris_circle[1])
    iris_radius = int(iris_circle[2])

    nsamples = 360
    samples = np.linspace(0, 2 * np.pi, nsamples)[:-1]

    polar = np.zeros((iris_radius, nsamples))

    for r in range(iris_radius):
        for theta in samples:
            x = int(r * np.cos(theta) + center[0])
            y = int(r * np.sin(theta) + center[1])
        
            polar[r][int(theta * nsamples / 2.0 / np.pi)] = image[y][x][0]


    return Image.fromarray(polar).convert('RGB')


    