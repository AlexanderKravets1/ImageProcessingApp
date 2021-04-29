import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder



class LoadPage(Screen):
    #will need function to determine % white and % black
    #will need to update labels with those numbers
    def preview(self, file):
        try:
            self.ids.layout.remove_widget(self.img)
        except:
            pass
        finally:
            img = Image(source = file)
            img.id = 'img'
            #adds image below file explorer
            self.ids.layout.add_widget(img, -1)
            #saves a reference to the img
            self.img = img


class ColorPage(Screen):
    wheel = ObjectProperty(None)

    def press(self):
        #likely to use hex, but rgba and hsv are options
        rgb = str(self.wheel.color)
        hsv = str(self.wheel.hsv)
        hex_color = str(self.wheel.hex_color)

        print(f"RGBA = {rgb} ")
        print(f"HSV = {hsv}")
        print(f"HEX = {hex_color}")
        #will need function to determine the color % for that image
        self.ids.sc.text = f'This image is #% selected color'

class PageManager(ScreenManager):
    pass


kv = Builder.load_file("style.kv")
class ImageApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    ImageApp().run()

