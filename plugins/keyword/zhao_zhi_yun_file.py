# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : zhao_zhi_yun_file.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/24
import os
from datetime import datetime
import shutil
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker
from wcferry import Wcf

from plugins.keyword.params import KeyWordParams
from storage.tables.entity.chat import ChatStatus, ChatFile

auto_download = False
msg_dict = {}
conn = None


def execute(param: KeyWordParams) -> bool:
    # 文本消息
    if param.msg.is_text():
        return __group_text__(param)
    # 文件消息
    if param.msg.type == 3 or param.msg.type == 43:
        return __group_download_file(param)
    return False


def __save_the_path(engine: Engine, file_type: int, save_path: str):
    with sessionmaker(bind=engine)() as session:
        session.add(ChatFile(path=save_path, file_type=file_type))


def __is_auto_download(engine: Engine):
    with sessionmaker(bind=engine)() as session:
        status = session.query(ChatStatus).filter_by(key="auto_download").first().status
    return status == 1


def __download_attach(wcf: Wcf, id: int, thumb: str, extra: str, move_path: str):
    status = wcf.download_attach(id, thumb, extra)
    if status == 0:
        file_path = os.path.dirname(thumb)
        image_name = os.path.basename(thumb)
        mp4_name = str(os.path.splitext(image_name)[0]) + ".mp4"
        mp4 = file_path + "/" + mp4_name
        new_mp4 = os.path.join(move_path, mp4_name)
        shutil.copyfile(mp4, new_mp4)
        os.remove(mp4)
        return new_mp4
    return ""


def __group_download_file(param: KeyWordParams):
    thumb = param.msg.thumb
    if thumb is None or len(thumb) <= 0:
        return False
    # 没有开自动下载
    if not __is_auto_download(param.engine):
        param.wcf.send_text(f"upload\n{param.msg.id}", param.msg.roomid)
        return True
    # 已经开启自动下载
    # 1.图片
    path = datetime.now().strftime("%Y/%m/%d")
    path = os.path.join("storage/file/zhao_zhi_yun", path)
    path = os.path.abspath(path)
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(e)
    save_path = ""
    file_type = 0
    if param.msg.type == 3:
        file_type = 1
        save_path = param.wcf.download_image(param.msg.id, param.msg.extra, path)
    if param.msg.type == 43:
        file_type = 2
        save_path = __download_attach(param.wcf, param.msg.id, param.msg.thumb, param.msg.extra, path)
    if len(save_path):
        __save_the_path(param.engine, file_type, save_path)
        param.wcf.send_text("上传成功", param.msg.roomid)
        return True
    return False


def __group_text__(param: KeyWordParams):
    constr = param.msg.content
    if not constr:
        return False
    if "开启自动下载" == constr or "关闭自动下载" == constr:
        with sessionmaker(bind=param.engine)() as session:
            auto = session.query(ChatStatus).filter_by(key="auto_download").first()
            if "开启自动下载" == constr and auto.status == 0:
                auto.status = 1
                session.commit()
            if "关闭自动下载" == constr and auto.status == 1:
                auto.status = 0
                session.commit()
        param.wcf.send_text(constr + "成功", param.msg.roomid)
        return True
    return False
