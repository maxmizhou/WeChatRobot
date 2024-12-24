# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : news.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/24
from spiders.news import get_new


def execute(param: str):
    return get_new()
