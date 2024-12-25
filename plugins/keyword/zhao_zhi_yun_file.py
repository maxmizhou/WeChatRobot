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

from sqlalchemy.orm import sessionmaker
from wcferry import WxMsg, Wcf

from plugins.keyword.params import KeyWordParams
from storage.tables.entity.chat import ChatAutoDownload

auto_download = False
msg_dict = {}
conn = None


def execute(param: KeyWordParams) -> bool:
    # 文本消息
    if param.msg.is_text():
        return __group_text__(param)
    # 文件消息
    if param.msg.type == 3 or param.msg.type == 43:
        return __group_download_file__(param)
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


def __group_download_file__(param: KeyWordParams):
    thumb = param.msg.thumb
    if thumb is None or len(thumb) <= 0:
        return False
    if not __get_

    if not auto_download:
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


def __group_text__(param: KeyWordParams):
    constr = param.msg.content
    if not constr:
        return False
    if "开启自动下载" == constr or "关闭自动下载" == constr:
        with sessionmaker(bind=param.engine)() as session:
            auto = session.query(ChatAutoDownload).first()
            if "开启自动下载" == constr and auto.auto == 0:
                auto.auto = 1
                session.commit()
            if "关闭自动下载" == constr and auto.auto == 1:
                auto.auto = 0
                session.commit()
        param.wcf.send_text(constr + "成功", param.msg.roomid)
        return True
    return False


def __update_auto_download__(auto: bool):
    pass
