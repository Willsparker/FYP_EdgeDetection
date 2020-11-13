from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

class StartApp(App):
    def build(self):
        b=BoxLayout()
        return b


if __name__ == '__main__':
    StartApp().run()
