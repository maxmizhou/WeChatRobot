# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : weather.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/23
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from prettytable import PrettyTable


class DayWeatherInfo(object):
    __slots__ = ['index_', 'date_', 'day_wea_', 'temperature_range_', 'wind_direction_', 'wind_level_']

    def __init__(self, index, date, day_wea, temperature_range, wind, wind_power):
        self.index_ = index
        self.date_ = date
        self.day_wea_ = day_wea
        self.temperature_range_ = temperature_range
        self.wind_direction_ = wind
        self.wind_level_ = wind_power


def parse(weather_data):
    soup = BeautifulSoup(weather_data, 'lxml')
    div_7d = soup.find("div", {'id': "7d"})
    weather_infos = []
    if div_7d:
        list_li = div_7d.find("ul", {'class': 't clearfix'})
        if list_li:
            for index, li in enumerate(list_li.find_all("li")):
                date = li.find("h1").text.strip()
                # 提取天气描述
                weather_desc = li.find("p", class_="wea").text.strip()
                # 提取温度范围
                temperature_range = li.find("p", class_="tem").text.strip()
                # 提取风向和风力
                wind_info = li.find("p", class_="win")
                wind_direction = wind_info.find("span")["title"]
                wind_level = wind_info.text.strip()
                weather_infos.append(
                    DayWeatherInfo(index + 1, date, weather_desc, temperature_range, wind_direction, wind_level))
    return weather_infos


class Weather(object):
    def __init__(self, weather_data, day_index):
        self.weather_infos_ = parse(weather_data)
        self.day_index_ = day_index
        self.__create_pretty_table()

    def __create_pretty_table(self):
        pretty_table = PrettyTable(["日期", "天气状况", "温度", "风向"])
        pretty_table.align["日期"] = "l"
        pretty_table.padding_width = 1
        return pretty_table

    @property
    def weather(self):
        pretty_table = self.__create_pretty_table()
        if 1 <= self.day_index_ <= 7:
            weather_info = self.weather_infos_[self.day_index_ - 1]
            pretty_table.add_row([weather_info.date_, weather_info.day_wea_,
                                  weather_info.temperature_range_,
                                  "".join([weather_info.wind_direction_, weather_info.wind_level_])])
        else:
            for weather_info in self.weather_infos_:
                pretty_table.add_row([weather_info.date_, weather_info.day_wea_,
                                      weather_info.temperature_range_,
                                      "".join([weather_info.wind_direction_, weather_info.wind_level_])])
        return str(pretty_table)
