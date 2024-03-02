from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

# today = datetime.now()
start_date = os.environ['START_DATE']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://v1.yiketianqi.com/api?unescape=1&version=v63&appid=58187358&appsecret=v3O0eLBo&city=德清"
  res = requests.get(url).json()
  city = res['city']
  date1 = res['date']
  week = res['week']
  weather = res['wea']
  temperature = res['tem']
  tips = res['air_tips']
  return city, date1, week, weather, temperature, tips

def get_count():
  delta = datetime.now() - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
      next = next.replace(year=next.year + 1)
  return (next - datetime.now()).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
city, date1, week, weather, temperature, tips = get_weather()
data = {"weather":{"value":weather},"temperature":{"value":temperature},"city":{"value":city},"date1":{"value":date1},"week":{"value":week},"tips":{"value":tips},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
