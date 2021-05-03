import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as kImage
from kivy.properties import ObjectProperty
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

import PIL
from PIL import Image
import webcolors
import pandas as pd
import operator
from collections import defaultdict

#images are resized to 300*300 so using as default
#these two variables are used between the screen classes
pixels = 300*300
named_colors_dict = defaultdict(int)

class LoadPage(Screen):
    #will need function to determine % white and % black
    #will need to update labels with those numbers
    def preview(self, file):
        try:
            self.ids.layout.remove_widget(self.img)
        except:
            pass
        finally:
            img = kImage(source = file)
            img.id = 'img'
            #adds image below file explorer
            self.ids.layout.add_widget(img, -1)
            #saves a reference to the img
            self.img = img

    def process(self, file):
        with Image.open(file) as img:
            image = img.convert('RGB')
            #resize the image
            image = image.resize((300,300))
            counted_colors = []
            global pixels
            pixels = image.width * image.height
            counted_colors = image.getcolors(pixels)
            colors = self.color_names(counted_colors)
            col_per = round(colors[0][1]/(pixels),2) * 100
            text = f"Dominant color is {colors[0][0]} and is {col_per}% of the image"
            return text

    def color_names(self, colors):
        named_colors_list = []
        for color in colors:
            try:
                #get the color name and store the number of occurrences with it
                named_colors_list.append(((webcolors.rgb_to_name(color[1])),color[0]))
            except ValueError:
                #get the closest color name and store the number of occurrences with it
                named_colors_list.append(((self.closest_color(color[1])),color[0]))
        #clears dictionary for every image
        named_colors_dict.clear()
        for color in named_colors_list:
            named_colors_dict[color[0]] += color[1]
        unique_color_names = []
        for color in named_colors_dict:
            unique_color_names.append((color, named_colors_dict[color]))
        unique_color_names = sorted(unique_color_names, key=operator.itemgetter(1), reverse=True)
        return unique_color_names



    #This function was found on StackOverflow as a solution to getting a ValueError from
    #the webcolors to_name when there isn't a direct match
    def closest_color(self, requested_color):
        min_colours = {}
        for key, name in webcolors.css3_hex_to_names.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_color[0]) ** 2
            gd = (g_c - requested_color[1]) ** 2
            bd = (b_c - requested_color[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

class ColorPage(Screen):
    wheel = ObjectProperty(None)

    def press(self):
        #converts the color wheels' rgb to a percentage tuple
        r = self.normalize(self.wheel.color[0])
        g = self.normalize(self.wheel.color[1])
        b = self.normalize(self.wheel.color[2])
        rgb_percent = (r,g,b)
        rgb = webcolors.rgb_percent_to_rgb(rgb_percent)
        try:
            name = webcolors.rgb_to_name(rgb)
        except ValueError:
            name = LoadPage.closest_color(self, rgb)
        if name in named_colors_dict:
            value = named_colors_dict[name]
            col_per = round(value/pixels,3) *100
            self.ids.sc.text = f'This image is {col_per}% {name}'
        else:
            self.ids.sc.text = f'This image is does not contain {name}'


    def normalize(self, v):
        return str(v*100) +'%'


class PageManager(ScreenManager):
    pass


kv = Builder.load_file("style.kv")
class ImageApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    ImageApp().run()

