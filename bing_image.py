from PIL import Image, ImageDraw, ImageFont
from farm_settings import Settings
import requests
from io import BytesIO



class BingImage:
    url='http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    width=0
    height=0

    def __init__(self, *, width=380, height=600):
        self.width=width
        self.height=height

    def getImage(self):
        resp = requests.get(url=self.url)
        data = resp.json()
        imagePath = data['images'][0]['url']
        fullUrl = "https://www.bing.com%s" % imagePath
        print(fullUrl)
        imageReq = requests.get(fullUrl)
        image = Image.open(BytesIO(imageReq.content))
        # resized = image.resize((self.width, self.height))
        img = image.convert("1").crop((0, 0, self.width, self.height))
        img.save("wallpaper.jpg")

