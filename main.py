# Kivy Stuff
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
from kivy.core.window import Window

# Additional Library stuff
from PIL import Image as pilImage
from PIL import UnidentifiedImageError
from io import BytesIO
from math import sqrt
import os

# Other .py files
import spatialFilter as sf
import blendImage as bi
import combineGradients as cg
import doubleThreshold as dt

# Application Window Options
#Window.set_icon("")

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
    image_blend = ObjectProperty(None)

    # This is to allow the grid to start at 3. Weird this is required tho
    # See: https://www.pisciottablog.com/2020/03/30/troubleshooting-attributeerror-super-object-has-no-attribute-__getattr__/
    def __init__(self, **kwargs):
        super(Root,self).__init__(**kwargs)
        self.initialiseGrid(3)
        self.updateGradientInfo()
    
    def createPopup(self,content):
        popUp = Popup(title='Error', 
            content=Label(text=content,font_size=30),
            size_hint=(0.5,0.5),         #by default this is (1,1)
            )                 # TODO: Make this dynamic
        popUp.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self, mode):
        if mode == 1:
            content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
            self._popup = Popup(title="Load Image", content=content,size_hint=(0.9, 0.9))
        elif mode == 2:
            content = LoadDialog(load=self.loadBlend, cancel=self.dismiss_popup)
            self._popup = Popup(title="Load Image", content=content,size_hint=(0.9, 0.9))
        
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, filename):
        try:
            inputImage = pilImage.open(filename[0])
        except UnidentifiedImageError:
            self.createPopup("Not a viable Image format")
            return

        self.setDisplayImage(inputImage)
        self.saveDisplayImage

        #This try/except allows me to reuse load function for the Undo function
        try:
            self.dismiss_popup()
        except AttributeError:
            pass

    def loadBlend(self, filename):
        # This function is to get the image to blend with the shown image
        try:
            blend_image = pilImage.open(filename[0])
        except UnidentifiedImageError:
            self.createPopup("Not a viable Image format")
            return
        self.dismiss_popup()
        self.blendImages(blend_image)

    def initialiseGrid(self, value):
        self.ids.cbGrey.active = False
        zerosList = [0] * value**2
        self.fillGrid(zerosList)

    def fillGrid(self, valueList):
        matrixSize = int(sqrt(len(valueList)))
        self.ids.grdUsrMatrix.clear_widgets()
        self.ids.grdUsrMatrix.cols = matrixSize
        self.ids.grdUsrMatrix.rows = matrixSize
        self.ids.sldrMatrixSize.value = matrixSize

        for x in valueList:
            self.ids.grdUsrMatrix.add_widget(TextInput(text=str(x),multiline=False,font_size=30))
        
    def save(self, path, filename):
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
        inputMatrix = [int(i.text) for i in self.ids.grdUsrMatrix.children]
        
        try:
            matrixCoefficient = self.getFraction(self.ids.txtMatrixCoeff.text)
        except ValueError:
            self.ids.txtMatrixCoeff.text = "1"
            matrixCoefficient = 1

        if self.image_input:
            self.saveDisplayImage()
        else:
            self.createPopup("Please load in a base image")
            return

        imageMan = sf.spatialFilter(self.image_input, inputMatrix, matrixCoefficient, self.ids.cbGrey.active, self.ids.cbAlpha.active, self.ids.cbGreyVals.active, self.ids.cbSveGrad.active)
        processIM = imageMan.run()
        self.ids.lblInfo.text = imageMan.getInfoString()

        # TODO: I'd like to make this cleaner, have a better way of showing saved gradients
        # Possibly make this so it saved gradients to a file, and then users can select them?
        # Also need to add a `delete gradient` button
        if self.ids.cbSveGrad.active and self.ids.cbGrey.active:
            try:
                if not self.savedGrad is None:
                    self.savedGrad2 = imageMan.getPixelGradients()
                    self.ids.btnResultGrad.disabled = False
            except AttributeError:
                self.savedGrad = imageMan.getPixelGradients()
            finally:
                self.updateGradientInfo()
        
        
        
        self.setDisplayImage(processIM)
    
    def resultantGradient(self):
        try:
            cgObject = cg.mergeGradients(self.savedGrad,self.savedGrad2,False)
        except AttributeError:
            self.createPopup("Don't have 2 saved gradients")
            return
        
        if not cgObject.checkImageDimensions():
            self.createPopup("Error: Images are of 2 different sizes")
            return
        
        cgObject.run()

        self.setDisplayImage(cgObject.getResultImg())

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

        found = False
        with file:
            for line in file:
                if line.startswith(text):
                    found = True
                    break
        
        if not found: 
            self.createPopup("Could not find line in the presetMask file")
            return

        lineList = line.split(" ")
        # Last line will always have a `\n` at the end
        lineList[-1] = lineList[-1].replace("\n","")

        self.ids.txtMatrixCoeff.text = str(lineList[1])
        self.fillGrid(lineList[2].split(","))

        if lineList[3] == "True":
            self.ids.cbGrey.active = True
        else:
            self.ids.cbGrey.active = False
        
        if lineList[4] == "True":
            self.ids.cbGreyVals.active = True
        else:
            self.ids.cbGreyVals.active = False

    def blendImages(self, blend_image):
        if not self.image_input:
            self.createPopup("Nothing to blend the image with!")
            return

        self.image_input.save("./files/tmp.png")
        alpha = self.ids.sldrBlendVal.value / 100
        
        output = bi.blendImage.blend(None, self.image_input, blend_image, alpha, self.ids.cbGrey.active, self.ids.cbAlpha.active)
        self.setDisplayImage(output)

    def saveDisplayImage(self):
        self.image_input.save("./files/tmp.png")

    # Sets the Kivy image widget's texture
    def setDisplayImage(self, image):
        self.image_input = image
        data = BytesIO()
        image.save(data, format='png')
        data.seek(0)
        self.ids.imgInput.texture=CoreImage(BytesIO(data.read()), ext='png').texture
        del data

    # Prints warning if the options are silly
    def checkOptions(self):
        infoString = ""
        if not self.ids.cbGrey.active:
            if self.ids.cbSveGrad.active:
                infoString += "[color=ed300e]* Can't save non greyscale image gradients. Ignoring Option[/color]\n"
            if self.ids.cbAlpha.active:
                infoString += "[color=ebeb15]* Removing blackspace from RGB may not work as expected[/color]\n"
            if self.ids.cbGreyVals.active:
                infoString += "[color=ebeb15]* Normalising values for color images may not act as expected[/color]\n"
        else:
            pass
        
        if infoString == "":
            infoString = "Information Area"
        else:
            infoString = "[size=19]Warning:\n[/size]" + infoString
        
        self.ids.lblInfo.text = infoString

    def doubleThreshold(self):
        try:
            self.image_input = self.image_input.convert("LA")
        except AttributeError:
            self.createPopup("Please load in a base image")
            return

        dtObject = dt.doubleThreshold(self.image_input,int(self.ids.sldrLowerPixThresh.value),int(self.ids.sldrUpperPixThresh.value))
        dtObject.run()
        self.setDisplayImage(dtObject.getImg())

    def updateGradientInfo(self):
        infoString = "Gradient 1 : "
        try:
            if not self.savedGrad is None:
                infoString += "[color=fc03db]Saved[/color]"
        except:
            infoString += "Empty"
        
        infoString += "\nGradient 2 : "

        try:
            if not self.savedGrad2 is None:
                infoString += "[color=fc03db]Saved[/color]"
        except:
            infoString += "Empty"
    
        self.ids.lblGrads.text = infoString



### TODO:
# * BlendImage.py - Need to put the better function into the file, and just ensure it works!
# * Intensity bounds - for greyscale images, implement functions that allow for lower and upper
# boundaries are cut out. ** Sorta Done **
# * Shape detection ... :grimace
# * AS per: https://stackoverflow.com/a/52916385 ; If checkbox, store non normalised pixel values; 
# Then if there's another run, take them and find the Gradient. 

# * Make the Spinner dynamically fill in the __init__ function
# * We need to despararely separate the functionality with the Kivy stuff. Even if we have functions that just call
# from a different class / python file.
# * Go round and fix all the other 'TODO's. Lots of small things to clean up.

class SpatialApp(App):
    def build(self):
        self.title = "Spatial Mask Applicator"
        self.load_kv('main.kv')
        
        # Resize & Centre Window
        initialCenter = Window.center
        Window.size = (1800, 1200)
        variation_x = Window.center[0] - initialCenter[0]
        variation_y = Window.center[1] - initialCenter[1]
        Window.left -= variation_x
        Window.top -= variation_y
        return Root()

if __name__ == '__main__':
    SpatialApp().run()