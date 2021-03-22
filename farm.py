#! /usr/bin/python3

import requests

from farm_settings import Settings
from weather import Weather
from image import LegoImage
from bing_image import BingImage
import random

from screen import Paper

import json

paper = Paper(mode="epaper", orientation="vert")

def load():
    with open("out.json") as f:
        data = json.load(f)
        return data


def getQuote():
    qurl = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"
    resp = requests.get(url=qurl)
    data = resp.json()
    quote = data[0]
    return quote

def imageBuilder(type):
    type = random.randint(0,5)
    type = 5

    if(type == 5):
        return BingImage()
    else:
        return LegoImage(
            orientation="vert",
            weather=weather,
            width=paper.width(),
            height=paper.height())

image, imagey = imageBuilder('img').getImages()
image.save("bw.jpg")
imagey.save("y.jpg")
paper.drawImages(image, imagey)
