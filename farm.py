#! /usr/bin/python3

from farm_settings import Settings
from weather import Weather
from image import LegoImage
from screen import Paper
from chatgpt import ChatGPT

import json
from string import Template
from PIL import Image
import random
import datetime

paper = Paper(mode='epaper', orientation='vert')

def load():
    with open('out.json') as f:
        data = json.load(f)
        return data

def choose_random_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        random_line = random.choice(lines)
        return random_line.strip()

def flip_coin():
    return random.choice(['Heads', 'Tails'])

# def getQuote():
#     qurl = "https://ron-swanson-quotes.herokuapp.com/v2/quotes"
#     resp = requests.get(url=qurl)
#     data = resp.json()
#     quote = data[0]
#     return quote

gpt = ChatGPT()

file_path =  './prompts.txt' if flip_coin() == 'Heads' else './longprompts.txt'
random_line = choose_random_line(file_path)
longai = file_path == './longprompts.txt'
prompt_template = Template(random_line)
this_day =datetime.today().strftime("%B %d")
history = gpt.ask(prompt_template.substitute(this_day=this_day))

weather = Weather(Settings.lat, Settings.lon, Settings.api_key)
weather.getWeather()

legoImage = LegoImage(orientation="vert", weather=weather, history=history, width = paper.width(), height = paper.height(), longai=longai)
image, imagey = legoImage.getImages()

# legoImage = LegoImage(orientation="vert", weather=weather, history=history, width = 448, height = 600, longai=longai)
# image, imagey = legoImage.getImages()
# image.save("output.jpg")  
# imagey.save("outputy.jpg")  

paper.drawImages(image,imagey)
