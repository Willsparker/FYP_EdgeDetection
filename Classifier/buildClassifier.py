import cv2
import pickle
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from skimage.feature import hog
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC

# This defines if we're building the classifer with Edge Features, or not.
EDGE_FEATURES = False
# Predicts the accuracy of the model
PREDICTION = True
# Number of Principal components to reduce the feature space to
PCA_NO = 2
# Float reprecenting how much of the data to use to build the model
TRAINING_PERCENTAGE = 0.5

CurPath = os.path.dirname(__file__)
# Assumes the Dataset directory is in the same directory as this script
DSPath = os.path.join(CurPath,"Dataset/")

# Returns a numpy array / OpenCV image given the name it appears in, in the data.csv.
def getImage(imageIndex):
    filename = "{}.jpg".format(imageIndex)
    filepath = DSPath + filename
    return cv2.imread(filepath, 0)

# Returns a copy of the input image post FFT returns the array as float
def applyFFT(image):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    fft = 20*np.log(np.abs(fshift))
    # Return as array on np.uint8, as otherwise, it's an array of float, which is not right
    return fft.astype(dtype=np.uint8)

# Returns a copy of the input image post Gabor Filter
def applyGabor(image):
    g_kernel = cv2.getGaborKernel((11, 11), 8.0, np.pi/4, 10.0, 0.5, 0, ktype=cv2.CV_32F)
    filtered_img = cv2.filter2D(image, cv2.CV_8UC3, g_kernel)
    return filtered_img

# Returns a copy of the input image post Edge Detection
def applyEdgeDetection(image):
    return cv2.Canny(image,75,200)
    

# Returns the features of the HoG image
def applyHoG(image):
    _, hog_image = hog(image,
                              visualize=True,
                              block_norm='L2-Hys',
                              pixels_per_cell=(16, 16))
    return hog_image

# Responsible for finding all features of a given image and returning as a 1D array.
def getFeatures(image):
    # Every Descriptor returns a 130,360 array, therefore flatten each to (130*360,)
    f_FFT = applyFFT(image).flatten()
    f_Gabor = applyGabor(image).flatten()
    f_HoG = applyHoG(image).flatten()

    # Get as one big vector
    image_features = np.hstack((f_FFT,f_Gabor,f_HoG))
    if EDGE_FEATURES: 
        # Add edge detection to vector, if we want it on there
        f_Edge = applyEdgeDetection(image).flatten()
        image_features = np.hstack((image_features,f_Edge))
    
    # When using Images of size:                (360,130) 
    # Without Edge Features, vector is size:    (140400,)
    # With Edge Features, vector is size:       (187200,)
    return image_features

# Saves the SVM model for later use
def saveSVM(svm):
    # save the model to disk
    filename = CurPath + '/SVM_model.sav'
    pickle.dump(svm, open(filename, 'wb'))


# load in the data.csv and use it as a label process
labels = pd.read_csv(DSPath + "data.csv", index_col=0)

feature_list = []
# For all images we've got
for id in labels.index:
    image = getImage(id)
    image_features = getFeatures(image)
    feature_list.append(image_features)

feature_matrix = np.array(feature_list)
print("\n[STATUS] feature_matrix shape: ", feature_matrix.shape)
# Standardise the data, and apply PCA, to reduce it
ss = StandardScaler()
standard_fm = ss.fit_transform(feature_matrix)
pca = PCA(PCA_NO)
standard_fm = pca.fit_transform(standard_fm)
print("\n[STATUS] FM shape, post PCA: ", standard_fm.shape)

# Getting 2 dataframes:
#  - 1 with the standardised Feature matrix for each image
#  - 1 with the corresponding labels (i.e. Fake or Not Fake)
X = pd.DataFrame(standard_fm)
y = pd.Series(labels.Fake.values)

# Split data into test / training
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=(1.0-TRAINING_PERCENTAGE))

print("\n[STATUS] Number of training samples: ", len(X_train))
print("\n[STATUS] Example of training data:\n")
print(X_train.head())
# define support vector classifier
svm = SVC(kernel='linear', probability=True, random_state=42)

# fit model & save it
svm.fit(X_train, y_train)
print("\n[STATUS] Finished training model...")
print("[STATUS] Saving to ", CurPath + '/SVM_model.sav')
saveSVM(svm)

# If we want to guage how good the model is:
if PREDICTION:
    # generate predictions
    y_pred = svm.predict(X_test)

    # calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print('\n[STATUS] Model accuracy is: ', accuracy)

    # If we can plot as a 2D graph, we should
    if PCA_NO == 2:
        support_vectors = svm.support_vectors_
        plt.scatter(X_train.iloc[:,0], X_train.iloc[:,1])
        plt.scatter(support_vectors[:,0], support_vectors[:,1], color='red')
        plt.title('Linearly separable data')
        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.show()
