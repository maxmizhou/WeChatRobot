# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : download.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/24
from wcferry import WxMsg, Wcf


def execute(wcf: Wcf, msg: WxMsg) -> bool:
    if not msg.from_group() or "49723492951@chatroom" != msg.roomid:
        return False

    print(msg)
    return False
