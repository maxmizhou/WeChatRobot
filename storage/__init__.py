# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : WeChatRobot
# @File     : __init__.py
# @Author   : ZhouMiLi
# @Date     : 2024/12/25
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from storage.tables import Base


def __init_tables__(data: dict):
    data_type = data.get('type', 'sqlite')
    database = data.get('database', 'mi_zhou_bot.db')
    host = data.get('host', '')
    username = data.get('username', '')
    password = data.get('password', '')
    if "sqlite" == data_type:
        url = f"sqlite:///{database}"
    if "mysql" == data_type:
        url = f"mysql://{username}:{quote_plus(password)}@{host}/{database}"
    engine = create_engine(url=url, echo=False)
    Base.metadata.create_all(engine)
    return engine
