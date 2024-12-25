# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : params.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/25
from sqlalchemy import Engine
from wcferry import Wcf, WxMsg


class KeyWordParams:

    def __init__(self, wcf: Wcf, msg: WxMsg, engin: Engine):
        self.wcf = wcf
        self.msg = msg
        self.engine = engin
