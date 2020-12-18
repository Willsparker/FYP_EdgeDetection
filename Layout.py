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
    count = 0

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
        try:
            self.ids.image_input.texture =''
            self.ids.image_input.source = filename[0]
        except:
            print("Error")

        self.dismiss_popup()

    def fillGrid(self, value):
        ## TODO: Make the grid look nicer; Initialise with 2x2 grid
        try:
            self.ids.userMatrix.clear_widgets()
        except AttributeError:
            print("Grid has no children")
        self.ids.userMatrix.cols=value
        self.ids.userMatrix.rows=value

        for _ in range(value**2):
            self.ids.userMatrix.add_widget(TextInput(text="0",multiline=False,font_size=30))
        
    def save(self, path, filename):
        #with open(os.path.join(path, filename), 'w') as stream:
        #    stream.write(self.text_input.text)

        # processIM.save(fileName) was used before... however, I don't want to store the PIL Image object
        # in memory ... 
        # This may be the only way tho :/ 
        #self.ids.image_input.save()

        self.dismiss_popup()

    def getKernel(self):
        self.count+=1
        inputMatrix = [int(i.text) for i in self.ids.userMatrix.children]
        try:
            # This is hacky af, but the only way I can get it working :/ 
            # See: https://stackoverflow.com/a/52340135
            imageMan = kernel.Kernel(self.ids.image_input.source, inputMatrix, 1)
            processIM = imageMan.run()
            data = BytesIO()
            processIM.save(data, format='png')
            data.seek(0)
            self.ids.image_input.texture=CoreImage(BytesIO(data.read()), ext='png').texture
        except AttributeError:
            #TODO: Error message popup
            print("Error")
    
        


class SpatialApp(App):
    def build(self):    
        self.load_kv('Spatial.kv')
        return Root()

if __name__ == '__main__':
    SpatialApp().run()