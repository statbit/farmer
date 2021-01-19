#! /usr/bin/python3

import sys
sys.path.append("lib")

from datetime import *
from calendar import TextCalendar
from PIL import Image, ImageDraw, ImageFont
from waveshare import epd7in5bc

epd = epd7in5bc.EPD()

today = date.today()
print(today)

image = Image.new("1", size = (epd.width, epd.height), color = 255)
imagey = Image.new("1", size = (epd.width, epd.height), color = 255)

font_body = ImageFont.truetype("OpenSans-Regular.ttf", 26)
font_heading = ImageFont.truetype("OpenSans-Regular.ttf", 56)
font_big = ImageFont.truetype("OpenSans-Regular.ttf", 128)
font_cal = ImageFont.truetype("DroidSansMono.ttf", 26)

cal = TextCalendar().formatmonth(today.year, today.month)

draw = ImageDraw.Draw(image)
drawy = ImageDraw.Draw(imagey)

draw.text((50,10), today.strftime("%b"), font = font_heading)
draw.text((30,70), today.strftime("%d"), font = font_big)
draw.text((50,220), today.strftime("%Y"), font = font_heading)
drawy.text((210, 30), cal, font = font_cal)
draw.text((210,220), today.strftime("%A"), font = font_heading)

epd.init()
epd.Clear()

epd.display(epd.getbuffer(image), epd.getbuffer(imagey))

    # Drawing on the Horizontal image
    # HBlackimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126
    # HRYimage = Image.new('1', (epd.width, epd.height), 255)  # 298*126  ryimage: red or yellow image
