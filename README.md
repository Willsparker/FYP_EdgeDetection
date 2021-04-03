# FYP_EdgeDetection
Final year university project to research the application of edge detectors for image fraud detection

## What it does:

This is a manual implementation of applying spatial filters to user selected images. Despite this being possible in OpenCV, I specifically avoided it (primarily to make it harder for myself). The user can specifiy both the image and the mask that will be applied to them.

OR, Iris classification can be performed, to predict the liklihood that a presented image of an iris is printed. Information on how to build the classifier is in the Classifier directory.

## How it works:

The program uses Python 3.8 and the Kivy UI Library to present the application. Running `main.py` will present the SpatialApplicator GUI. The IrisDetector can be accessed via this GUI, or the `IrisDetector.py` can be run directly. 

TODO: Make this README.md better :grin