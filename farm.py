#! /usr/bin/python3

import sys
import requests
import textwrap
from farm_settings import Settings
from weather import Weather

sys.path.append("lib")

from datetime import *
from calendar import TextCalendar
from PIL import Image, ImageDraw, ImageFont
from waveshare import epd7in5bc
import json

font_body = ImageFont.truetype("OpenSans-Regular.ttf", 26)
font_quote = ImageFont.truetype("OpenSans-Regular.ttf", 16)
font_heading = ImageFont.truetype("OpenSans-Regular.ttf", 56)
font_big = ImageFont.truetype("OpenSans-Regular.ttf", 128)
font_cal = ImageFont.truetype("DroidSansMono.ttf", 26)

epd = epd7in5bc.EPD()

def load():
    with open('out.json') as f:
        data = json.load(f)
        return data

def writeData(weather, img, x, idx):
    day, min, max, con = weather.getForecast(idx)
    
    draw = ImageDraw.Draw(img)

    draw.text((x,400), day, font=font_body) 
    draw.text((x,430), min, font=font_body) 
    draw.text((x,460), max, font=font_body) 
    draw.text((x,490), con, font=font_body) 

    icon = Image.open("./img/" + weather.getIcon(idx) + ".png").convert("1")
    img.paste(icon, (x, 520))


def makeImage(weather, img):
    writeData(weather, img, 50, 0)
    writeData(weather, img, 150, 1)
    writeData(weather, img, 250, 2)

def getQuote():
    qurl = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"
    resp = requests.get(url=qurl)
    data = resp.json()
    quote = data[0]
    return quote

def verticalImages():
    height=epd.width
    width=epd.height

    # height=600
    # width=380

    today = date.today()
    image = Image.new("1", size = (width, height), color = 255)
    imagey = Image.new("1", size = (width, height), color = 255)

    cal = TextCalendar().formatmonth(today.year, today.month)

    draw = ImageDraw.Draw(image)
    drawy = ImageDraw.Draw(imagey)

    draw.text((50, 10), today.strftime("%b %d %Y"), font = font_heading)
    drawy.text((50, 80), today.strftime("%A"), font = font_heading)
    draw.text((40, 160), cal, font = font_cal)
    # drawy.text((50, 400), "\n".join(textwrap.wrap(getQuote(), width=30)), font = font_quote)

    weather = Weather(Settings.lat, Settings.lon, Settings.api_key)
    weather.getWeather()
    makeImage(weather, imagey)

    return image, imagey

def horizontalImages():
    width=epd.width
    height=epd.height

    today = date.today()
    image = Image.new("1", size = (width, height), color = 255)
    imagey = Image.new("1", size = (width, height), color = 255)

    cal = TextCalendar().formatmonth(today.year, today.month)

    draw = ImageDraw.Draw(image)
    drawy = ImageDraw.Draw(imagey)

    draw.text((50, 10), today.strftime("%b"), font = font_heading)
    draw.text((30, 70), today.strftime("%d"), font = font_big)
    draw.text((50, 220), today.strftime("%Y"), font = font_heading)
    drawy.text((210, 30), cal, font = font_cal)
    draw.text((210, 220), today.strftime("%A"), font = font_heading)
    drawy.text((50, 300), "\n".join(textwrap.wrap(getQuote())), font = font_quote)
    return image, imagey


def getImages():
    if(len(sys.argv) == 2 and sys.argv[1] == "vert"):
        return verticalImages() 
    else:
        return horizontalImages()

image, imagey = getImages()

# image.save("bw.jpg")
# imagey.save("by.jpg")

epd.init()
epd.Clear()
epd.display(epd.getbuffer(image), epd.getbuffer(imagey))

