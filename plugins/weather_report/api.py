# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : api.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/23
import requests

from plugins.weather_report import url, headers
from plugins.weather_report.util import guess_province_city_county
from plugins.weather_report.weather import Weather


def get_by_guess(pcc_name, day_index=1):
    guess_address, city_id = guess_province_city_county(pcc_name)
    if guess_address is None or len(guess_address) != 3 or city_id is None:
        return f"未查询到<{pcc_name}>天气"
    weather_str = get(city_id, day_index)
    weather_str = "\n".join(["".join(guess_address), weather_str])
    return weather_str


def get(city_id, day_index=1):
    r = requests.get(url.format(city_id=city_id), headers=headers)
    if r.status_code == 200:
        wea = Weather(r.content, day_index)
        return wea.weather
    return "未查询到天气"


if __name__ == "__main__":
    print(get_by_guess("颍上"))
