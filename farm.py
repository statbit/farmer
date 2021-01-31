#! /usr/bin/python3

import sys
import requests
import textwrap
from farm_settings import Settings
from weather import Weather
from image import LegoImage

sys.path.append("lib")

from datetime import *
from calendar import TextCalendar
from PIL import Image, ImageDraw, ImageFont
from waveshare import epd7in5bc
import json

epd = epd7in5bc.EPD()

def load():
    with open('out.json') as f:
        data = json.load(f)
        return data

def getQuote():
    qurl = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"
    resp = requests.get(url=qurl)
    data = resp.json()
    quote = data[0]
    return quote


width=epd.width
height=epd.height

weather = Weather(Settings.lat, Settings.lon, Settings.api_key)
weather.getWeather()

legoImage = None

if(len(sys.argv) == 2 and sys.argv[1] == "vert"):
    legoImage = LegoImage(orientation="vert", weather=weather, width = height, height = width)
else:
    legoImage = LegoImage(orientation="hor", weather=weather, width = width, height = height)

image, imagey = legoImage.getImages()

image.save("bw.jpg")
imagey.save("by.jpg")

epd.init()
epd.Clear()
epd.display(epd.getbuffer(image), epd.getbuffer(imagey))

