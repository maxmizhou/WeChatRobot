# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : chat.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/25
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from storage.tables.base import Base

"""
聊天文件
"""


class ChatFile(Base):
    __tablename__ = 'chat_file'

    id = Column(Integer, primary_key=True)  # 主键
    path = Column(String(100), nullable=True)  # 文件路径
    file_type = Column(Integer, default=0)
    create_date = Column(DateTime, default=datetime.now())


"""
聊天消息记录
        self._is_self = msg.is_self
        self._is_group = msg.is_group
        self.type = msg.type
        self.id = msg.id
        self.ts = msg.ts
        
        self.sign = msg.sign
        self.xml = msg.xml
        self.sender = msg.sender
        self.roomid = msg.roomid
        self.content = msg.content
        self.thumb = msg.thumb
        self.extra = msg.extra
        
        type (int): 消息类型，可通过 `get_msg_types` 获取
        id (str): 消息 id
        xml (str): 消息 xml 部分
        sender (str): 消息发送人
        roomid (str): （仅群消息有）群 id
        content (str): 消息内容
        thumb (str): 视频或图片消息的缩略图路径
        extra (str): 视频或图片消息的路径
"""


class ChatMessage(Base):
    __tablename__ = 'chat_message'

    id = Column(Integer, primary_key=True)  # 主键
    is_self = Column(Integer, nullable=True)
    is_group = Column(Integer, nullable=True)
    type = Column(Integer, nullable=True)
    msgId = Column(BigInteger, nullable=True)  # 消息ID
    ts = Column(BigInteger, nullable=True)
    sign = Column(String(255), nullable=True)
    xml = Column(Text, nullable=True)
    sender = Column(String(100), nullable=True)
    room_id = Column(String(100), nullable=True)
    content = Column(Text, nullable=True)
    thumb = Column(String(255), nullable=True)
    extra = Column(String(255), nullable=True)
    create_date = Column(DateTime, default=datetime.now())


"""
bot 插件
"""


class ChatPlugin(Base):
    __tablename__ = 'chat_plugin'

    id = Column(Integer, primary_key=True)  # 主键
    path = Column(String(255), nullable=True)  # 插件地址
    roomId = Column(String(255), nullable=True)
    senderId = Column(String(255), nullable=True)
    plugin_type = Column(Integer, nullable=True)  # 插件类型
    receiver = Column(String(100), nullable=True)  # 接收人
    params = Column(String(100), nullable=True)  # 插件参数
    cron = Column(String(100), nullable=True)  # 定时时间


"""
标识 常量
"""


class ChatStatus(Base):
    __tablename__ = 'chat_auto_download'

    id = Column(Integer, primary_key=True)  # 主键
    key = Column(String(100), nullable=True)
    status = Column(Integer, nullable=True)
