This directory is where the images I intend for the classifier are kept.

**Note:** As I don't own the rights to the CASIS-TWIN database, I can't provide actual images.

### Directories
_Images_ contains the full, non iris-detected images.

_Iris_ contains the images post iris-detection.

_PrintedImages_ contains the Printed (fake) non iris-detected images.

_PrintedIris_ contains the Printed (fake) images, post circular cropping. (See _defineCircles.py_)

_Dataset_ contains the standardised images, post _buildDataset.py_


### Files:

_defineCircles.py_ : Due to the iris detector not working for the fake images, this python script will run through the _PrintedImages_ directory, where the user should click 2 points, the first defining the centre of the pupil and the second defining the edge of the iris (at any point). The centre and radius of each image is then put into the _PrintedImages/IrisPositions.txt_ file

_checkIrisPos.py_ : Applies the circles found in _defineCircles.py_, to the images, for reviewing.

_getCroppedPrintedIris.py_ : Crops the Fake images so only the Iris is kept, and store in _PrintedIris_. (Not entirely needed for the classifier)

_buildDataset.py_ : Goes through the Images and PrintedImages directory, and standarising the images so, the iris is unwrapped & reshaped to (360,130). 

### Expectations:

These scripts are used with the following assumptions:

- The printed eye photos are in _PrintedImages_.
- The actual eye photos are in _Images_.
- The Iris folder contains the output of the Iris Detector from the SpatialFilter application.
- An _IrisPositions.txt_ file resides in _Images_ that contains information about where the iris is. 

    