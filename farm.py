#! /usr/bin/python3

import sys
import requests
import textwrap
from farm_settings import Settings

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

def getWeather():
    qurl = "https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly&lat={}&lon={}&appid={}&unit=imperial".format(Settings.lat, Settings.lon, Settings.api_key)
    resp = requests.get(url=qurl)
    data = resp.json()
    return data

def load():
    with open('out.json') as f:
        data = json.load(f)
        return data

def writeData(data, draw, x):
    day = datetime.fromtimestamp(data['dt'])
    draw.text((x,400), day.strftime("%a"), font=font_body) 

    tof = lambda k: int((1.8 * (k - 273)) + 32)

    min = tof(data['temp']['min'])
    max = tof(data['temp']['max'])
    
    draw.text((x,450), str(min) + "°", font=font_body) 
    draw.text((x,500), str(max) + "°", font=font_body) 
    draw.text((x,550), str(data['weather'][0]['main']), font=font_body) 

def makeImage(data, draw):
    width=380
    height=600

    d1data = data['daily'][0]
    d2data = data['daily'][1]
    d3data = data['daily'][2]

    # image = Image.new("1", size=(width,height), color=255)
    # draw = ImageDraw.Draw(image)

    writeData(d1data, draw, 50)
    writeData(d2data, draw, 150)
    writeData(d3data, draw, 250)


def getQuote():
    qurl = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"
    resp = requests.get(url=qurl)
    data = resp.json()
    quote = data[0]
    return quote

def verticalImages():
    height=epd.width
    width=epd.height

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

    makeImage(getWeather(), drawy)

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

# image.save("test.jpg")
# imagey.save("testy.jpg")

epd.init()
epd.Clear()
epd.display(epd.getbuffer(image), epd.getbuffer(imagey))

