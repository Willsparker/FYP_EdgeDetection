import kivy

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder


## Find tutorial on what this does exactly
# Retrieved from: https://stackoverflow.com/questions/43452697/browse-an-image-file-and-display-it-in-a-kivy-window
Builder.load_string("""
<My`Widget>:
    id: Widget
    FileChooserListView:
        id: filechooser
        on_selection: Widget.selected(filechooser.selection)
    Image:
        id: image
        source: ""
""")

### Below is trialing layouts, using boxlayout. Quite like it :D

#    def build(self):
#
#
#      windowLayout = BoxLayout(spacing=10)
#      infoLayout = BoxLayout(spacing=10)
#      imageCanvas = BoxLayout(spacing=10)
#      btn_loading = Button(text="Load Image")
#      btn_loading.bind(on_press = self.load_img)
#
#      test_img = Image(source="test_image.png")
#      imageCanvas.add_widget(test_img)
#
#      infoLayout.add_widget(btn_loading)
#      windowLayout.add_widget(imageCanvas)
#      windowLayout.add_widget(infoLayout)
#      return windowLayout
#
#    def load_img(self, event):
#        print("Load Image")

class MyWidget(BoxLayout):
    
    def selected(self,filename):
        self.ids.image.source = filename[0]

class ImgApp(App):
    def build(self):
        return MyWidget()



if __name__ == '__main__':
    ImgApp().run()
