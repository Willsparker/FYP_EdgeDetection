from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.image import Image as CoreImage

from PIL import Image as pilImage


from io import BytesIO
from math import sqrt

import spatialFilter
import blendImage
import os

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    image_input = ObjectProperty(None)

    def createPopup(self,content):
        popUp = Popup(title='Test', 
            content=Label(text=content),
            size_hint=(None, None),         #by default this is (1,1)
            size=(400,400))                 # TODO: Make this dynamic
        popUp.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, filename):
        try:
            inputImage = pilImage.open(filename[0])
        except:
            self.createPopup("Not a viable Image format")
            return

        data = BytesIO()
        inputImage.save(data, format='png')
        data.seek(0)
        self.ids.image_input.texture = CoreImage(BytesIO(data.read()), ext='png').texture

        try:
            self.dismiss_popup()
        except AttributeError:
            print("Not in a popup")
        finally:
            del data

    def initialiseGrid(self, value):
        self.ids.greyCheck.active = False
        zerosList = [0] * value**2
        self.fillGrid(zerosList)

    def fillGrid(self, valueList):
        self.ids.userMatrix.clear_widgets()
        self.ids.userMatrix.cols = int(sqrt(len(valueList)))
        self.ids.userMatrix.rows = int(sqrt(len(valueList)))
        for x in valueList:
            self.ids.userMatrix.add_widget(TextInput(text=str(x),multiline=False,font_size=30))
        
    def save(self, path, filename):
        # This currently doesn't handle images that haven't
        # been modified
        # TODO: Fix this
        filename = path + "/" + filename
        if not filename.endswith(".png"):
            filename += ".png"
        try:
            self.image_input.save(filename)
        except:
            self.createPopup("Can't save a non altered image")
        self.dismiss_popup()

    def getFraction(self,str):
        # https://stackoverflow.com/a/30629776
        # A pure python way of getting it from a string
        try:
            return float(str)
        except ValueError:
            num, denom = str.split('/')
            try:
                leading, num = num.split(' ')
                whole = float(leading)
            except ValueError:
                whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac

    def applyTransform(self):
        # TODO: Put try / except here for in case the inputs aren't numbers
        inputMatrix = [int(i.text) for i in self.ids.userMatrix.children]
        matrixCoefficient = self.getFraction(self.ids.matrixCoeff.text)

        # TODO: STOP THIS IN CASE THERE'S NO IMAGE LOADED
        self.ids.image_input.export_to_png(filename='./files/tmp.png')
        try:
            imageMan = spatialFilter.spatialFilter('./files/tmp.png', inputMatrix, matrixCoefficient, self.ids.greyCheck.active)
            processIM = imageMan.run()
        except AttributeError:
            self.createPopup("Please load a base image in")
            return
        
        # See: https://stackoverflow.com/a/52340135
        self.image_input = processIM
        data = BytesIO()
        processIM.save(data, format='png')
        data.seek(0)
        self.ids.image_input.texture=CoreImage(BytesIO(data.read()), ext='png').texture
        del data

    def undoTransform(self):
        try:
            self.load(['./files/tmp.png'])
        except FileNotFoundError:
            self.createPopup("No previously altered image")

    def on_spinner_change(self, text):
        text = text.lower().replace(" ", "")
        try:
            file = open("./files/presetMasks","r")
        except FileNotFoundError:
            self.createPopup("Cannot find the presetMasks file")
            return

        # Terrible:
        found = False
        with file:
            for line in file:
                if line.startswith(text):
                    found = True
                    break
        
        if not found: 
            self.createPopup("Could not find line in the preset Folders")
            return

        lineList = line.split(" ")
        self.ids.matrixCoeff.text = str(lineList[1])
        self.fillGrid(lineList[2].split(","))
        self.ids.greyCheck.active = (lineList[3])  
    
    def blendImages(self):
        output = blendImage.blendImage.blend(None,"./images/test_image.png", "./images/test_image2.png", 0.75)
        data = BytesIO()
        output.save(data, format='png')
        data.seek(0)
        self.ids.image_input.texture=CoreImage(BytesIO(data.read()), ext='png').texture

### TODO:
# 1) Separate the functions needed to set the display image into separeate function with image as argument.
# 2) We need to despararely separate the functionality with the Kivy stuff. Even if we have functions that just call
# from a different class / python file.
# 3) Sliders to control alpha for the blend function
# 4) Tidy up stuff (i.e. move the 'test' button to the float diagram and rename; rename variables to follow a set ruleset)
# 5) Go round and fix all the other 'TODO's. Lots of small things to clean up.

class SpatialApp(App):
    def build(self):
        self.load_kv('main.kv')
        return Root()

if __name__ == '__main__':
    SpatialApp().run()