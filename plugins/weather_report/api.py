# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : api.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/23
import requests

from plugins.weather_report.util import get_city_code, guess_province_city_county
from plugins.weather_report.weather import Weather


def get_by_guess(pcc_name, day_index=1):
    guess_address, city_id = guess_province_city_county(pcc_name)
    if guess_address is None or len(guess_address) != 3 or city_id is None:
        return f"未查询到<{pcc_name}>天气"
    weather_str = get(city_id, day_index)
    weather_str = "\n".join(["".join(guess_address), weather_str])
    print(weather_str)
    return weather_str


def get(city_id, day_index=1):
    url = "http://www.weather.com.cn/weather/{city_id}.shtml".format(city_id=city_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        wea = Weather(r.content, day_index)
        return wea.weather
    return "为查询到天气"


get_by_guess("阜阳")
