# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : zhao_zhi_yun_file.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/24
from wcferry import WxMsg, Wcf

auto_download = False


def execute(wcf: Wcf, msg: WxMsg) -> bool:
    if not msg.from_group() or "49723492951@chatroom" != msg.roomid:
        return False

    if msg.is_text():
        __group_text__(wcf, msg)
    return False


def __group_text__(wcf: Wcf, msg: WxMsg):
    constr = msg.content
    if "开启自动下载" == constr or "关闭自动下载" == constr:


    if len(constr) > 0 and constr == "开启自动下载":
        auto_download = True

    if len(constr) > 0 and constr == "关闭自动下载":
        auto_download = False
