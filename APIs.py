import http.client
import json
import os
import random
import sys
import urllib
from datetime import date, datetime
from time import time, localtime

import requests
from requests import get, post
from zhdate import ZhDate

import cityinfo


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


def get_access_token(app_id, app_secret):
    url = "https://api.weixin.qq.com/cgi-bin/stable_token"
    params = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret,
    }
    try:
        access_token = post(url, json=params).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    return access_token


def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday
    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn


def get_gaode_weather(api_key, city_code):
    try:
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={api_key}&extensions=all"
        response = requests.get(url)

        # 检查请求是否成功
        if response.status_code == 200:
            data = response.json()["forecasts"][0]
            city = data["city"]
            today_cast = data["casts"][0]
            day_weather = today_cast["dayweather"]
            # night_weather = today_cast["nightweather"]
            day_temp = today_cast["daytemp"]
            night_temp = today_cast["nighttemp"]
            note = ""
            if "雨" in day_weather:
                note = "今日有雨，记得带伞"
            elif int(day_temp) < 18:
                note = "天冷了，记得添衣"
            elif int(day_temp) > 25:
                note = "天热了，注意防晒"
            elif int(day_temp) < 5:
                note = "天巨冷，注意防寒"
            else:
                note = "天气凉爽，记得开心"
            return city, day_weather, day_temp, night_temp, note
    except:
        return "高德天气API调用失败！"


# 词霸每日一句
def get_shici():
    try:
        url = "https://v2.jinrishici.com/one.json"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        shici = r.json()["data"]["content"]
        return shici
    except:
        return "今日诗词API调取错误！"


# 彩虹屁
def caihongpi(tianxing_api):
    try:
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': tianxing_api})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/caihongpi/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        if ("XXX" in data):
            data = data.replace("XXX", "超超")
        return data
    except:
        return ("彩虹屁API调取错误，请检查API是否正确申请或是否填写正确")


# 励志名言
def get_lizhi(tianxing_api):
    try:
        conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
        params = urllib.parse.urlencode({'key': tianxing_api})
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        conn.request('POST', '/lzmy/index', params, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        print(data["newslist"][0]["saying"])
        return data["newslist"][0]["saying"]
    except:
        return ("励志古言API调取错误，请检查API是否正确申请或是否填写正确")

def get_date(love_date):
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(love_date.split("-")[0])
    love_month = int(love_date.split("-")[1])
    love_day = int(love_date.split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = int(str(today.__sub__(love_date)).split(" ")[0]) + 1
    return today, week, str(love_days)