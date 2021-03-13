#! /usr/bin/python3

import requests

from farm_settings import Settings
from weather import Weather
from image import LegoImage
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


legoImage = LegoImage(
    orientation="vert",
    weather=weather,
    width=paper.width(),
    height=paper.height())

image, imagey = legoImage.getImages()
paper.drawImages(image, imagey)
