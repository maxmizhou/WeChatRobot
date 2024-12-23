# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : weather.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/23

from weathers.api import get_by_guess


def main(pcc_name: str):
    return get_by_guess(pcc_name)
