from datetime import *
from calendar import TextCalendar
from PIL import Image, ImageDraw, ImageFont

today = date.today()
print(today)

image = Image.new("1", size = (800, 480), color = 255)

font_body = ImageFont.truetype("OpenSans-Regular.ttf", 26)
font_heading = ImageFont.truetype("OpenSans-Regular.ttf", 56)
font_big = ImageFont.truetype("OpenSans-Regular.ttf", 128)

cal = TextCalendar().formatmonth(today.year, today.month)

draw = ImageDraw.Draw(image)
draw.text((30,10), today.strftime("%b"), font = font_heading)
draw.text((10,70), today.strftime("%d"), font = font_big)
draw.text((30,220), today.strftime("%Y"), font = font_heading)
draw.text((200, 30), cal, font = font_body)
image.save("test.jpg")


