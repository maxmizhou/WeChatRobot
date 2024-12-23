# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : weather.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/23

from spiders.wearher import get_by_guess_str


def main(pcc_name: str):
    return get_by_guess_str(pcc_name)
