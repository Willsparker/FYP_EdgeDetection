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

import kernel
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

    def load(self, path, filename):
        inputImage = pilImage.open(filename[0])
        data = BytesIO()
        inputImage.save(data, format='png')
        data.seek(0)
        try:
            self.ids.image_input.texture = CoreImage(BytesIO(data.read()), ext='png').texture
        except:
            print("Error")   
        self.dismiss_popup()

    def fillGrid(self, value):
        ## TODO: Make the grid look nicer; Initialise with 3x3 grid
        try:
            self.ids.userMatrix.clear_widgets()
        except AttributeError:
            print("Grid has no children")
        self.ids.userMatrix.cols=value
        self.ids.userMatrix.rows=value

        for _ in range(value**2):
            self.ids.userMatrix.add_widget(TextInput(text="0",multiline=False,font_size=30))
        
    def save(self, path, filename):
        # This currently doesn't handle images that haven't
        # been modified
        filename = path + "/" + filename
        if not filename.endswith(".png"):
            filename += ".png"
        #try:
        self.image_input.save(filename)
        #except:
            #self.createPopup("Can't save a non altered image")
        self.dismiss_popup()

    def getKernel(self):
        # TODO: Put try / except here for in case the inputs aren't numbers
        inputMatrix = [int(i.text) for i in self.ids.userMatrix.children]
        # This saves the texture of the image as png, so we can make it into a PIL image in kernel.py
        # Hacky, but could be useful later
        self.ids.image_input.export_to_png(filename='./tmp/tmp.png')
        try:
            imageMan = kernel.Kernel('./tmp/tmp.png', inputMatrix, self.ids.greyCheck.active)
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



class SpatialApp(App):
    def build(self):    
        self.load_kv('Spatial.kv')
        return Root()

if __name__ == '__main__':
    SpatialApp().run()