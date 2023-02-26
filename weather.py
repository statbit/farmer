import sys
import requests
from datetime import *

class Weather:
    lat=0
    lon=0
    apikey="missing"
    data = None

    def __init__(self, lat, lon, apikey):
       self.lat = lat
       self.lon = lon
       self.apikey = apikey

    def getWeather(self):
        qurl = "https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly&lat={}&lon={}&appid={}&unit=imperial".format(self.lat, self.lon, self.apikey)
        resp = requests.get(url=qurl)
        data = resp.json()
        self.data = data
        return data

    def temp(self):
        tof = lambda k: int((1.8 * (k - 273)) + 32)
        return tof(self.data['current']['temp'])

    def getIcon(self, day):
        dayData = self.data['daily'][day]
        return dayData['weather'][0]['icon']

    def getForecast(self, day):
        dayData = self.data['daily'][day]
        day = datetime.fromtimestamp(dayData['dt'])
        daystr = day.strftime("%a")

        tof = lambda k: int((1.8 * (k - 273)) + 32)
        min = str(tof(dayData['temp']['min'])) + "°"
        max = str(tof(dayData['temp']['max'])) + "°"
        cond = dayData['weather'][0]['main']
        return (daystr, min, max, cond)


