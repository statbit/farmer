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

class Paper:
    mode = 'epaper'
    orientation = 'vert'

    def __init__(self, *, mode='epaper', orientation='vert'):
        if mode == 'epaper':
            epd = epd7in5bc.EPD()
        else:
            self.mode = mode

    def dimension(self, dim):
        if dim == 'width':
            if self.mode == 'epaper' :
                return epd.width
            else:
                return 380
        else:
            if self.mode == 'epaper' :
                return epd.height
            else :
                return 600

    def width(self):
        if self.orientation == 'vert':
            return self.dimension('width')
        else:
            return self.dimension('height')

    def height(self):
        if self.orientation == 'vert':
            return self.dimension('height')
        else:
            return self.dimension('width')

    def drawImages(self, image, imagey):
        image.save("bw.jpg")
        imagey.save("by.jpg")

        if self.mode == 'epaper':
            epd.init()
            epd.Clear()
            epd.display(epd.getbuffer(image), epd.getbuffer(imagey))

