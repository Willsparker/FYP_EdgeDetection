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
from io import BytesIO

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
    displayImage = ObjectProperty()

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

        self.setDisplayImage(displayImage)
        self._popup.dismiss()

    # Sets the Kivy image widget's texture
    def setDisplayImage(self, image):
        self.displayImage = image
        data = BytesIO()
        image.save(data, format='png')
        data.seek(0)
        self.ids.imgInput.texture=CoreImage(BytesIO(data.read()), ext='png').texture
        del data

    def start(self):
        # Checks to see if there is an image loaded in
        if self.displayImage is None:
            Popup(title='Error', 
              content=Label(text="Please load in a viable image first",font_size=30),
              size_hint=(0.5,0.5)
            ).open()
            return

        # 

        self.WriteToInfo("[STATUS] Loading Classifier ... ")



    def WriteToInfo(self, text):
        self.infoText += "\n" + text


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