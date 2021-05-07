import numpy as np
import pandas as pd
import glob
from cv2 import cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCOEFF_NORMED, minMaxLoc, imread, rectangle, imdecode, \
    imshow, waitKey, resize, INTER_AREA, imwrite, IMREAD_COLOR
import urllib.request
import random
from flask import Flask, render_template
import keyboard
from PIL import ImageGrab
import threading
from time import sleep

i = str
w = str
op = 0
od = 0
scrVal = 0
pic_list = []

def temp():
    images = []
    while True:
        if scrVal == 1:
            def rescaleFrame(frame, width=200, height=200):
                dimensions = (width, height)

                return resize(frame, dimensions, interpolation=INTER_AREA)

            def saveTemp():
                list_b = i.to_string(index=False)
                pic_list = list_b.split('\n')[1:-1]

                for picValue in range(len(pic_list)):
                    print(picValue)
                    url_response = urllib.request.urlopen(pic_list[picValue])
                    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                    img = imdecode(img_array, -1)
                    resized_image = rescaleFrame(img)
                    img_gray = cvtColor(img, COLOR_BGR2GRAY)
                    template = imread('screenshot.png', 0)
                    wi, h = template.shape[::-1]

                    res = matchTemplate(img_gray, template, TM_CCOEFF_NORMED)
                    threshold = 0.9
                    loc = np.where(res >= threshold)

                    for pt in zip(*loc[::-1]):
                        rectangle(img, pt, (pt[0] + wi, pt[1] + h), (0, 0, 255), 2)
                        break
                    imwrite(f'images/res{picValue}.png', resized_image)
                    images.append(picValue)


            def match():
                for i in range(len(images)):
                    try:
                        img_rgb = imread('screenshot.png')
                        img_gray = cvtColor(img_rgb, COLOR_BGR2GRAY)
                        template = imread(f'images/res{i}.png', 0)
                        wi, h = template.shape[::-1]

                        res = matchTemplate(img_gray, template, TM_CCOEFF_NORMED)
                        threshold = 0.9
                        loc = np.where(res >= threshold)

                        for pt in zip(*loc[::-1]):
                            rectangle(img_rgb, pt, (pt[0] + wi, pt[1] + h), (0, 0, 255), 2)
                        imwrite('detected.jpg', img_rgb)

                    except Exception as e:
                        print("#ERROR debug Info {}\n".format(e))

            saveTemp()
            match()
        else:
            sleep(0.01)

def scrS():
    global scrVal
    while True:
        try:
            if keyboard.is_pressed("p"):
                image = ImageGrab.grab()
                image.save("screenshot.png")
                print("Screenshot Saved!")
                scrVal = 1
                break

            else:
                sleep(0.01)

        except Exception as e:
            print("#ERROR debug Info {}\n".format(e))

def webFunc():
    list_a = w.to_string(index=False)
    web_list = list_a.split('\n')[1:-1]
    random.shuffle(web_list)  # if user picks randomizer pressing a key then it will randomize

    return web_list


def webPage():
    app = Flask(__name__)

    @app.route('/')
    def dynamic_page():
        return render_template('page.html', web_list=webFunc())

    if __name__ == '__main__':
        app.run(host='localhost', debug=True)

    sleep(0.01)


def documentFunc():
    global i, w
    path = 'dataset/'
    documents = ['photos', 'keywords', 'collections', 'conversions', 'colors']
    datasets = {}
    subsets = []

    for doc in documents:
        files = glob.glob(f"{path}{doc}.tsv*")
        if doc != 'photos':
            # print("ight") # For debugging purposes
            break

        for filename in files:
            df = pd.read_csv(filename, index_col=False, sep='\t', header=0, usecols=[2])
            i = (df.query('index < @op'))  # will eventually be for user input instead of ('index < user_in') when prompting user for how many photos he wants to generate
            w = (df.query('index < @od'))
            subsets.append(df)
            # print(subsets) # For debugging purposes

        datasets[doc] = pd.concat(subsets, axis=0, ignore_index=True)


def opencvFunc():
    global pic_list
    list_b = i.to_string(index=False)
    pic_list = list_b.split('\n')[1:-1]

    # print(pic_list) # For debugging purposes

    # print(str("test"), list_a) # Testing list
    def rescaleFrame(frame, width=800, height=620):
        dimensions = (width, height)

        return resize(frame, dimensions, interpolation=INTER_AREA)

    def getUrls():
        for url in pic_list:
            url_response = urllib.request.urlopen(url)
            img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
            img = imdecode(img_array, -1)
            resized_image = rescaleFrame(img)
            imshow('URL Image', resized_image)

            key = waitKey(500) & 0xFF
            if key == ord("q"):
                break

    getUrls()

def photosCV():
    global op
    try:
        user_in = int(input("Pick a number of photos to train with 1-25: "))
        op = user_in + 1

        if op >= 1 and op <= 25:
            print(f"{op} : number of photos trained!")
    except:
        print("Sorry try again")
        photosCV()


def photoWeb():
    global od
    try:
        pop_in = int(input("Pick a number of photos to generate on the webpage 5-50: "))
        od = pop_in + 1

        if od >= 5 and od <= 50:
            print(f"{od} : number of photos on webpage!")
    except:
        print("Sorry try again")
        photoWeb()


def userFunc():
    photosCV()

    photoWeb()

    documentFunc()

    user_in_two = input("enter y to see opencv photos, else input anything: ")
    if user_in_two == 'y':
        opencvFunc()


finders = threading.Thread(target=scrS)
finders.start()
finders2 = threading.Thread(target=temp)
finders2.start()

userFunc()

webPage()
