import sys
import textwrap
import imgkit
import os
import io

from datetime import *
from calendar import TextCalendar, HTMLCalendar
from PIL import Image, ImageDraw, ImageFont

class LegoImage:
    orientation = ""
    width = 380
    height = 600
    weather = None
    history = None
    longai = False

    font_body = ImageFont.truetype("OpenSans-Regular.ttf", 20)
    font_quote = ImageFont.truetype("OpenSans-Regular.ttf", 14)
    font_heading = ImageFont.truetype("OpenSans-Regular.ttf", 56)
    font_big = ImageFont.truetype("OpenSans-Regular.ttf", 128)
    font_cal = ImageFont.truetype("DroidSansMono.ttf", 26)

    def __init__(self, *, orientation = "vert", width=380, height=600, weather, history, longai):
        self.orientation = orientation
        self.width = width
        self.height = height
        self.weather = weather
        self.history = history
        self.longai = longai

    def writeData(self, img, x, idx):
        day, min, max, con = self.weather.getForecast(idx)

        draw = ImageDraw.Draw(img)
        draw.text((x,430), day, font=self.font_body) 
        draw.text((x,450), min, font=self.font_body) 
        draw.text((x,470), max, font=self.font_body) 
        draw.text((x,490), con, font=self.font_body) 

        icon = Image.open("./img/" + self.weather.getIcon(idx) + ".png").convert("1")
        img.paste(icon, (x, 520))


    def makeImage(self, img):

        file = datetime.now().strftime("special/%m_%d.jpg")
        filemsg = datetime.now().strftime("special/%m_%d.txt")

        if(os.path.isfile(file)):
            specialImage = Image.open(file).convert("1")
            specialText = "".join(io.open(filemsg).readlines()).strip()
            img.paste(specialImage, (90, 400))
            draw = ImageDraw.Draw(img)
            draw.text((40,620), specialText, font=self.font_body) 
        else:
            self.writeData(img, 50, 0)
            self.writeData(img, 150, 1)
            self.writeData(img, 250, 2)

    def makeCalImg(self):
        today = date.today()

        if today.day < 10:
            top = "-.4em"
            left = "-.6em"
        else:
            top = "-.3em"
            left = "-.25em"

        style = """<style>
            #day { position: relative; color: black; }
            tr { padding-top: 2px; }
            .thisday::before {
              position: absolute;
              top: TOP;
              left: LEFT;
              z-index: -1;
              content: " ";
              display: block;
              background-color: white;
              border: 2px solid black;
              width: 1.5em;
              height: 1.5em;
              border-radius: 1em;
            }
            th { padding: .1em}
            td { padding: 1px}
            th.month {display: none}
            table { font-family: courier; font-size: 14pt }
            </style>"""

        style = style.replace("TOP", top).replace("LEFT", left)
        htmlcal = HTMLCalendar().formatmonth(today.year, today.month, withyear=False)
        html = htmlcal.replace( 
            ">%s<" % str(today.day), 
            "><div id=day><span class=thisday>%s</span></div><" % str(today.day) 
        )

        styledcal = "<html>%s %s</html>" % (style, html)
        with open("cal.html", "w") as f:
            f.write(styledcal)
        imgkit.from_string(styledcal, 'cal.jpg')

    def verticalImages(self):
        today = date.today()
        image = Image.new("1", size = (self.width, self.height), color = 255)
        imagey = Image.new("1", size = (self.width, self.height), color = 255)

        # cal = TextCalendar().formatmonth(today.year, today.month)

        draw = ImageDraw.Draw(image)
        drawy = ImageDraw.Draw(imagey)

        draw.text((50, 10), today.strftime("%b %d %Y"), font = self.font_heading)
        drawy.text((50, 80), today.strftime("%A"), font = self.font_heading)
        self.makeCalImg()

        if(self.longai):
            print("longai")
            draw.text((40, 160), "\n".join(textwrap.wrap(self.history, width=50)), font = self.font_quote)
        else:
            calimg = Image.open("./cal.jpg").convert("1")
            image.paste(calimg, (40, 160))
            draw.text((50, 330), "\n".join(textwrap.wrap(self.history, width=50)), font = self.font_quote)

        # draw.text((40, 160), cal, font = self.font_cal)
        # drawy.text((50, 400), "\n".join(textwrap.wrap(getQuote(), width=40, replaceWhitespace=false)), font = self.font_quote)
        self.makeImage(imagey)

        return image, imagey

    def horizontalImages(self):

        today = date.today()
        image = Image.new("1", size = (self.width, self.height), color = 255)
        imagey = Image.new("1", size = (self.width, self.height), color = 255)

        cal = TextCalendar().formatmonth(today.year, today.month)

        draw = ImageDraw.Draw(image)
        drawy = ImageDraw.Draw(imagey)

        draw.text((50, 15), today.strftime("%b"), font = self.font_heading)
        draw.text((30, 70), today.strftime("%d"), font = self.font_big)
        draw.text((50, 220), today.strftime("%Y"), font = self.font_heading)
        drawy.text((210, 30), cal, font = self.font_cal)
        draw.text((210, 220), today.strftime("%A"), font = self.font_heading)
        drawy.text((50, 300), "\n".join(textwrap.wrap(getQuote())), font = self.font_quote)
        return image, imagey

    def getImages(self):
        if(self.orientation == "vert"):
            return self.verticalImages() 
        else:
            return self.horizontalImages()
