# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : zhao_zhi_yun_file.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/24
import os
import sqlite3
import csv
from datetime import datetime
from wcferry import WxMsg, Wcf

auto_download = False
msg_dict = {}
conn=None

def execute(wcf: Wcf, msg: WxMsg) -> bool:
    if not msg.from_group() or "49723492951@chatroom" != msg.roomid:
        return False
    if msg.is_text():
        return __group_text__(wcf, msg)
    if msg.type == 3 or msg.type == 43:
        return __group_download_file__(wcf, msg, msg.type)

    return False


def __save_the_path__(msg_id: int, save_path: str):
    data = [{"ID": msg_id, "PATH": save_path}]
    with open("storage/data/zhao_zhi_yun_file.csv", mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def __get_the_path__(msg_id: int):
    with open("storage/data/zhao_zhi_yun_file.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['ID']) == msg_id:
                return row['PATH']
        return ""


def __group_download_file__(wcf: Wcf, msg: WxMsg, type: int):
    thumb = msg.thumb
    if thumb is None or len(thumb) <= 0:
        return False
    if not auto_download:
        msg_dict[msg.id] = msg
        wcf.send_text(f"upload\n{msg.id}", msg.roomid)
        return True
    if type == 3:
        if len(__get_the_path__(msg.id)):
            wcf.send_text("已经上传", msg.roomid)
            return True
        path = datetime.now().strftime("%Y/%m/%d")
        path = os.path.join("storage/file/zhao_zhi_yun", path)
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            print(e)
        path = os.path.abspath(path)
        save_path = wcf.download_image(msg.id, msg.extra, path)
        if len(save_path):
            __save_the_path__(msg.id, save_path)
            wcf.send_text("下载成功", msg.roomid)

    return False


def __group_text__(wcf: Wcf, msg: WxMsg):
    constr = msg.content
    if "开启自动下载" == constr or "关闭自动下载" == constr:
        if "开启自动下载" == constr:
            auto_download = True
        if "关闭自动下载" == constr:
            auto_download = False
        wcf.send_text(constr + "成功", msg.roomid)
        return True
    return False

def __update_auto_download__(auto: bool):

