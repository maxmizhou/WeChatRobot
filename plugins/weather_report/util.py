# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : util.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/23
# -*- coding: utf-8 -*-
import os
import sys

_ver = sys.version_info

is_py2 = (_ver[0] == 2)

if is_py2:
    import codecs

    open = codecs.open


def guess_province_city_county(pcc_name: str):
    count = 1
    guess = None
    city_id = None
    city_ids = __get_city_ids__()
    for key in city_ids:
        keys = key.split(",")
        contain_count = keys.count(pcc_name)
        if contain_count >= count:
            count = contain_count
            guess = keys
            city_id = city_ids[key]
    return guess, city_id


def __get_city_ids__():
    city_id_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "city_id.py")
    city_ids = {}
    with open(city_id_path, encoding="utf-8") as f:
        for line in f:
            line = line.encode('utf-8') if is_py2 else line
            city_id, county, city, province = line.split(",")
            key = province.strip() + "," + city.strip() + "," + county.strip()
            city_ids[key] = city_id.strip()
    return city_ids


def get_city_code(province, city, county):
    """
    :param province: 一级城市(省)
    :param city: 二级城市(市)
    :param county: 三级城市(县)
    :return:城市id
    """
    city_ids = __get_city_ids__()
    key = province.strip() + "," + city.strip() + "," + county.strip()
    if key in city_ids:
        return city_ids[key]


class Error(Exception):
    def __init__(self, error):
        self.error_ = error

    def __str__(self):
        return repr(self.error_)
