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
"""


class ChatMessage(Base):
    __tablename__ = 'chat_message'

    id = Column(Integer, primary_key=True)  # 主键
    msgId = Column(BigInteger, nullable=True)  # 消息ID
    message = Column(Text, nullable=True)  # 消息体
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


class ChatAutoDownload(Base):
    __tablename__ = 'chat_auto_download'

    id = Column(Integer, primary_key=True)  # 主键
    auto = Column(Integer, nullable=True)
