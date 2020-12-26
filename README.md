# FYP_EdgeDetection
Final year university project to research the application of edge detectors for image fraud detection

## What it does:

This is a manual implementation of applying spatial filters to user selected images. Despite this being possible in OpenCV, I specifically avoided it (primarily to make it harder for myself). The user can specifiy both the image and the mask that will be applied to them.

## How it works:

The program uses Python 3.8 and the Kivy UI Library to present the application. Running `main.py` will present the GUI. `spatialFilter.py` can be run individually, but this works as a test to ensure the spatialFilter Class actually works.
