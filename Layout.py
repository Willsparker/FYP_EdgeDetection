from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.image import Image as CoreImage

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
            self.ids.userMatrix.add_widget(TextInput(text="0",multiline=False))
        
    def save(self, path, filename):
        #with open(os.path.join(path, filename), 'w') as stream:
        #    stream.write(self.text_input.text)

        self.dismiss_popup()

    def getKernel(self):
        self.count+=1
        fileName="./test"+str(self.count)+".png"
        print(fileName)
        inputMatrix=[]
        inputMatrix.append([i.text for i in self.ids.userMatrix.children])
        imageMan = kernel.Kernel(self.ids.image_input.source, inputMatrix)
        processIM = imageMan.run()
        processIM.save(fileName)
        #self.ids.image_input.texture=CoreImage(fileName).texture
        self.ids.image_input.source=fileName


class SpatialApp(App):
    def build(self):
        self.load_kv('Spatial.kv')
        return Root()

if __name__ == '__main__':
    SpatialApp().run()