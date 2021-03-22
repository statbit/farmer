from PIL import Image, ImageDraw, ImageFont
from farm_settings import Settings
import requests
from io import BytesIO
from datetime import *



class BingImage:
    url='http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    api='https://api.bing.microsoft.com/v7.0/images/search'
    width=0
    height=0

    font_heading = ImageFont.truetype("OpenSans-Regular.ttf", 126)

    headers = None
    bgImage = None
    dayImage = None

    def __init__(self, *, width=380, height=600):
        self.width=width
        self.height=height
        # self.headers = {"Ocp-Apim-Subscription-Key" : Settings.bing_key}

    def search(self, query):
        params  = {"q": query, "license": "public", "imageType": "photo", "safeSearch" : "strict"}
        resp = requests.get(self.api, headers=self.headers, params=params)
        resp.raise_for_status()
        return resp.json()["value"][2]["contentUrl"]

    def searchImage(self):
        url = self.search("spring")
        print(url)
        imageReq = requests.get(url)
        imageReq.raise_for_status()
        image = Image.open(BytesIO(imageReq.content))
        resized = image.resize((self.width, self.height))
        self.bgImage = resized.convert("1").crop((0, 0, self.width, self.height))

    def retrieveBackground(self):
        resp = requests.get(url=self.url)
        data = resp.json()
        imagePath = data['images'][0]['url']
        fullUrl = "https://www.bing.com%s" % imagePath
        imageReq = requests.get(fullUrl)
        image = Image.open(BytesIO(imageReq.content))
        resized = image.resize((self.width, self.height))
        self.bgImage = resized.convert("1").crop((0, 0, self.width, self.height))

    def makeDayImage(self):
        today = date.today()
        self.dayImage = Image.new("1", size=(self.width, self.height), color=255)
        drawy = ImageDraw.Draw(self.dayImage)
        drawy.text((90, self.height/2 - 55), today.strftime("%d"), font=self.font_heading)


    def getImages(self):
        self.retrieveBackground()
        self.makeDayImage()

        return self.bgImage, self.dayImage



