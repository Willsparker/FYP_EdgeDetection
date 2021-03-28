This directory is specifically for the building of the classifier and are exclusive of the spatialFilter application

**Note:** For the project, I have used the CASIA-Iris-v4 Twin Database. Under the terms and conditions I am unable to redistribute this database.

### Directories
_Images_ contains the full, non iris-detected images.

_Iris_ contains the images post iris-detection. 

_PrintedImages_ contains the Printed (fake) non iris-detected images. 

_PrintedIris_ contains the Printed (fake) images, post circular cropping. (See _defineCircles.py_).

_Dataset_ contains the standardised images, post _buildDataset.py_.

**Note:** The _*Iris_ directories aren't required for the classifier - they just provide an example of iris detection.

### Files:

_defineCircles.py_ : Due to the iris detector not working for the fake images, this python script will run through the _PrintedImages_ directory, where the user should click 2 points, the first defining the centre of the pupil and the second defining the edge of the iris (at any point). The centre and radius of each image is then put into the _PrintedImages/IrisPositions.txt_ file.

**Note:** This can be done with the non-printed images too, if required. Just need to change some of the paths :-) 

_checkIrisPos.py_ : Applies the circles found in _defineCircles.py_, to the images, for reviewing.

_getCroppedPrintedIris.py_ : Crops the Fake images so only the Iris is kept, and store in _PrintedIris_. (Not entirely needed for the classifier)

_buildDataset.py_ : Goes through the Images and PrintedImages directory, and standarising the images so, the iris is unwrapped & reshaped to (360,130). 

_buildClassifier.py_ : As the name would suggest, this builds an SVM classifier, using the data in _Dataset_. The model is saved to *SVM_model.sav*. There are several parameters that can be tweaked at the beginning of the file, to change how the model learns.

### Expectations:

These scripts are used with the following assumptions:

- The actual eye photos are in _Images_.
- The printed eye photos are in _PrintedImages_.
- The _Iris_ folder contains the output of the Iris Detector from the SpatialFilter application.
- An _IrisPositions.txt_ file resides in _Images_ that contains information about where the iris is. 

    