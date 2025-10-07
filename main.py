from datetime import datetime, date
from time import localtime
from requests import post

from APIs import *


# 推送信息
def send_message(to_user, access_token, template_id, today, week, love_days, boy_next_birth, girl_next_birth, boy_city,
                 boy_weather, boy_day_temp, boy_night_temp, boy_note, girl_city, girl_weather, girl_day_temp,
                 girl_night_temp, girl_note, caihongpi, shici):
    data = {
        "touser": to_user,
        "template_id": template_id,
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "love_days": {
                "value": love_days,
                "color": get_color()
            },
            "caihongpi": {
                "value": caihongpi,
                "color": get_color()
            },
            "shici": {
                "value": shici,
                "color": get_color()
            },
            "boy_next_birth": {
                "value": boy_next_birth,
                "color": get_color()
            },
            "girl_next_birth": {
                "value": girl_next_birth,
                "color": get_color()
            },
            "boy_city": {
                "value": boy_city,
                "color": get_color()
            },
            "boy_weather": {
                "value": boy_weather,
                "color": get_color()
            },
            "boy_day_temp": {
                "value": boy_day_temp,
                "color": get_color()
            },
            "boy_note": {
                "value": boy_note,
                "color": get_color()
            },
            "boy_night_temp": {
                "value": boy_night_temp,
                "color": get_color()
            },
            "girl_city": {
                "value": girl_city,
                "color": get_color()
            },
            "girl_weather": {
                "value": girl_weather,
                "color": get_color()
            },
            "girl_day_temp": {
                "value": girl_day_temp,
                "color": get_color()
            },
            "girl_night_temp": {
                "value": girl_night_temp,
                "color": get_color()
            },
            "girl_note": {
                "value": girl_note,
                "color": get_color()
            },
        }

    }

    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("./config.json", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    app_id = config["app_id"]
    app_secret = config["app_secret"]
    accessToken = get_access_token(app_id, app_secret)

    # 相爱日期
    love_date = config["love_date"]
    today, week, love_days = get_date(love_date)
    # 获取所有生日数据
    boy_birth = config["boy_birth"]
    girl_birth = config["girl_birth"]
    year = localtime().tm_year
    boy_next_birth = get_birthday(boy_birth, year, today)
    girl_next_birth = get_birthday(girl_birth, year, today)
    # 传入省份和市获取天气信息
    api_key = config["gaode_api"]
    boy_city_code = config["boy_city_code"]
    girl_city_code = config["girl_city_code"]
    boy_city, boy_weather, boy_day_temp, boy_night_temp, boy_note = get_gaode_weather(api_key, boy_city_code)
    girl_city, girl_weather, girl_day_temp, girl_night_temp, girl_note = get_gaode_weather(api_key, girl_city_code)

    # 彩虹屁
    tianxing_api = config["tianxing_api"]
    caihongpi = caihongpi(tianxing_api)
    # 每日诗词
    shici = get_shici()
    # 公众号推送消息
    users = config["user"]
    template_id = config["template_id"]
    for user in users:
        send_message(user, accessToken, template_id, today, week, love_days, boy_next_birth, girl_next_birth, boy_city,
                     boy_weather, boy_day_temp, boy_night_temp, boy_note, girl_city, girl_weather, girl_day_temp,
                     girl_night_temp, girl_note, caihongpi, shici)
    import time

    time_duration = 3.5
    time.sleep(time_duration)
