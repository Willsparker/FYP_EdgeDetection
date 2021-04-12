# Kivy Stuff
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView


# Additional Library stuff
from PIL import Image as pilImage
from PIL import UnidentifiedImageError
from PIL import ImageDraw
from io import BytesIO

# Import other written files
from IrisDetector import getCircle as gC
from SpatialApplicator import irisUnwrap as iU
from Classifier import buildClassifier as bC

# Other libraries
import numpy as np
import cv2
import pickle

class TouchPoint(Image):
    def on_touch_down(self, touch):
        if not self.load_image.collide_point(*touch.pos):
            return False
        else:print(touch)

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    infoText = StringProperty()
    displayImage = ObjectProperty(None)
    circle = ObjectProperty(None)
    classified = False

    def __init__(self, **kwargs):
        super(Root,self).__init__(**kwargs)
        self.infoText = "To start, load in an image and click start.\nClick 2 points in the image that\
 correspond to the middle of the pupil and the iris boundary\n\nAlternatively, manually enter the centre,\
 in the form 'x,y', and radius as an integer"

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Image", content=content,size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, filename):
        try:
            displayImage = pilImage.open(filename[0])
        except UnidentifiedImageError:
            Popup(title='Error', 
              content=Label(text="Please load in a viable image format",font_size=30),
              size_hint=(0.5,0.5)
            ).open()
            return

        self.classified = False
        self.setDisplayImage(displayImage)
        self.displayImage.save("./files/tmp.png")
        self._popup.dismiss()

    def undo(self):
        try:
            self.load(['./files/tmp.png'])
        except FileNotFoundError:
            Popup(title='Error', 
            content=Label(text="Somethings gone wrong - no `./files/tmp.png`",font_size=30),
            size_hint=(0.5,0.5)
            ).open()
            return False
        return True

    # Sets the Kivy image widget's texture
    def setDisplayImage(self, image):
        self.displayImage = image
        data = BytesIO()
        image.save(data, format='png')
        data.seek(0)
        self.ids.imgInput.texture=CoreImage(BytesIO(data.read()), ext='png').texture
        del data

    def startCircle(self):
        flag = False
        # Checks to see if there is an image loaded in
        if self.displayImage is None:
            Popup(title='Error', 
              content=Label(text="Please load in a viable image first",font_size=30),
              size_hint=(0.5,0.5)
            ).open()
            return
        elif self.classified:
            Popup(title='Error', 
              content=Label(text="Please load in a new image",font_size=30),
              size_hint=(0.5,0.5)
            ).open()
            return
        # Checks to see if this is the second circle. If it is, remove the original
        elif self.circle is not None:
            flag = True
            self.WriteToInfo("[STATUS] Removing Old Circle ...", True)
            if not self.undo():
                return


        # Cache the last image.
        self.displayImage.save("./files/tmp.png")

        if not self.ids.txtIrisCentre.text == "" and not self.ids.txtIrisRadius.text == "":
            try:
                circle = []
                circle.append(int(self.ids.txtIrisCentre.text.split(",")[0]))
                circle.append(int(self.ids.txtIrisCentre.text.split(",")[1]))
                circle.append(int(self.ids.txtIrisRadius.text))
            except:
                circle = gC.run()
        else:
            # Find the circle
            circle = gC.run()

        self.circle = circle
        self.classified = False
        # Information Printing
        self.WriteToInfo("[STATUS] Pupil center position :", not flag)
        self.WriteToInfo(str(circle[0]) + "," + str(circle[1]),False)
        self.WriteToInfo("[STATUS] Iris Radius :", False)
        self.WriteToInfo(str(int(circle[2])),False)

        self.setDisplayImage(gC.drawCircle(self.circle))

        self.WriteToInfo("[STATUS] Unwrapping Iris ...", False)


    def startClassification(self):
        if self.circle is None:
            Popup(title='Error', 
              content=Label(text="Please load in a viable image first",font_size=30),
              size_hint=(0.5,0.5)
            ).open()
            return
        elif self.classified:
            if not self.undo():
                return
        
        circle = self.circle
        self.classified = True
        self.displayImage.save("./files/tmp.png")

        # Returns Iris as PILImage
        # TODO: If the circle is larger than the image, this breaks.
        unwrappedIris = iU.irisUnwrapping(self.displayImage,circle)
        
        self.WriteToInfo("[STATUS] Unwrapped Iris Size : " + str(unwrappedIris.size), True)

        # Converts the PILImage to CV image, and resizes to 360,130
        unwrappedIris = cv2.resize(np.array(unwrappedIris.convert('L')),(360,130))
        self.WriteToInfo("[STATUS] Converted Iris Size : " + str(unwrappedIris.shape), False)
        # Retrieve the features of the unwrapped iris
        feature_list = bC.getFeatures(unwrappedIris, self.ids.cbEdgeFeatures.active)
        self.WriteToInfo("[STATUS] Feature Matrix Size: " + str(feature_list.shape), False)

        # See Log Book, 30/3/21
        # (DON'T) Apply PCA
        #pca_feature_list = bC.applyPCA(feature_list)
        #self.WriteToInfo("[STATUS] Feature Matrix Size, post PCA: " + str(pca_feature_list.shape), False)

        # Load classifier
        if self.ids.cbEdgeFeatures.active:
            modelName = "Classifier/SVM_model_EDGES.sav"
        else:
            modelName = "Classifier/SVM_model.sav"
    
        loaded_model = pickle.load(open(modelName, 'rb'))
        # Apply classifier
        feature_list = feature_list.reshape(1,-1)
        prediction_probabilities = loaded_model.predict_proba(feature_list)
                
        # Show on output image
        for i in range(2):
            if prediction_probabilities[0][i] == max(prediction_probabilities[0]):
                result = i
                break
        text = ""
        if result == 0:
            text += "Real: "
        else:
            text += "Fake: "

        pred_percent = float(np.max(prediction_probabilities) * 100)
        text += "{:.2f}".format(pred_percent) + "%"
        
        self.setDisplayImage(self.WriteOnImage(text))
        self.WriteToInfo("[STATUS] Result : " + text, False)

    def WriteToInfo(self, text, clear):
        if clear:
            self.infoText = ""
        self.infoText += "\n" + text

    def WriteOnImage(self, text):
        # Convert to OpenCV Image
        img = self.displayImage.convert('RGB')
        img = np.array(img)
        img = img[:, :, ::-1].copy() 

        # Scale, depending on the size of the image
        scale = 0.1
        fontScale = min(img.shape[0],img.shape[1])/(25/scale)
        positionScale = ((int(0.1*img.shape[0]),int(0.1*img.shape[1])))

        # Write Text on image
        cv2.putText(img, text,
         positionScale,
         cv2.FONT_HERSHEY_SIMPLEX,
         fontScale,
         (0,0,255),
         3)

        # Convert back to PILImage
        return pilImage.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


class IrisDetectorScreen(App):
    def build(self):
        self.title = "Fake Iris Detector"
        self.load_kv('IrisDetector.kv')
        
        # Resize & Centre Window
        initialCenter = Window.center
        Window.size = (1800, 1200)
        variation_x = Window.center[0] - initialCenter[0]
        variation_y = Window.center[1] - initialCenter[1]
        Window.left -= variation_x
        Window.top -= variation_y
        return Root()


if __name__ == "__main__":
    IrisDetectorScreen().run()