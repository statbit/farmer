#! /usr/bin/python3

import requests
import shutil
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

from farm_settings import Settings
from weather import Weather
import json

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

def getIOD():
    iurl = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
    resp = requests.get(url=iurl)
    data = resp.json()
    imgurl = "http://www.bing.com" + data['images'][0]['url']
    response = requests.get(imgurl, stream=True)
    with open('img.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

weather = Weather(Settings.lat, Settings.lon, Settings.api_key)
weather.getWeather()
getIOD()

font_body = ImageFont.truetype("OpenSans-Regular.ttf", 26)

d = auto()
with Image.open('img.png') as im:
    resImg = im.resize(d.resolution)
    draw = ImageDraw.Draw(resImg)
    draw.text((40,40), str(weather.temp()), font=font_body)
    d.set_image(resImg, saturation=1.0)
    d.show()


