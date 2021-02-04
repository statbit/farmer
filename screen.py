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
    epd=None

    def __init__(self, *, mode='epaper', orientation='vert'):
        if mode == 'epaper':
            self.epd = epd7in5bc.EPD()
        else:
            self.mode = mode

    def dimension(self, dim):
        if dim == 'width':
            if self.mode == 'epaper' :
                return self.epd.width
            else:
                return 380
        else:
            if self.mode == 'epaper' :
                return self.epd.height
            else :
                return 600

    def width(self):
        if self.orientation == 'vert':
            return self.dimension('height')
        else:
            return self.dimension('width')

    def height(self):
        if self.orientation == 'vert':
            return self.dimension('width')
        else:
            return self.dimension('height')

    def drawImages(self, image, imagey):
        image.save("bw.jpg")
        imagey.save("by.jpg")

        if self.mode == 'epaper':
            self.epd.init()
            self.epd.Clear()
            self.epd.display(self.epd.getbuffer(image), self.epd.getbuffer(imagey))

