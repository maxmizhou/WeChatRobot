# -*- coding: utf-8 -*-
import ast
import importlib
import importlib.util
import logging
import os
import re
import time
import xml.etree.ElementTree as ET
from queue import Empty
from threading import Thread
from sqlalchemy.orm import sessionmaker
from wcferry import Wcf, WxMsg
from base.func_bard import BardAssistant
from base.func_chatglm import ChatGLM
from base.func_chatgpt import ChatGPT
from base.func_chengyu import cy
from base.func_tigerbot import TigerBot
from base.func_xinghuo_web import XinghuoWeb
from base.func_zhipu import ZhiPu
from configuration import Config
from constants import ChatType
from job_mgmt import Job

__version__ = "39.2.4.0"

from plugins.keyword.params import KeyWordParams

from storage.tables.entity.chat import ChatPlugin


class Robot(Job):
    """个性化自己的机器人
    """

    def __init__(self, config: Config, wcf: Wcf, engine, chat_type: int, ) -> None:
        self.engine = engine
        self.wcf = wcf
        self.config = config
        self.LOG = logging.getLogger("Robot")
        self.wxid = self.wcf.get_self_wxid()
        self.allContacts = self.wcf.get_contacts()
        self.functions = []
        self.__load_functions__()
        if ChatType.is_in_chat_types(chat_type):
            if chat_type == ChatType.TIGER_BOT.value and TigerBot.value_check(self.config.TIGERBOT):
                self.chat = TigerBot(self.config.TIGERBOT)
            elif chat_type == ChatType.CHATGPT.value and ChatGPT.value_check(self.config.CHATGPT):
                self.chat = ChatGPT(self.config.CHATGPT)
            elif chat_type == ChatType.XINGHUO_WEB.value and XinghuoWeb.value_check(self.config.XINGHUO_WEB):
                self.chat = XinghuoWeb(self.config.XINGHUO_WEB)
            elif chat_type == ChatType.CHATGLM.value and ChatGLM.value_check(self.config.CHATGLM):
                self.chat = ChatGLM(self.config.CHATGLM)
            elif chat_type == ChatType.BardAssistant.value and BardAssistant.value_check(self.config.BardAssistant):
                self.chat = BardAssistant(self.config.BardAssistant)
            elif chat_type == ChatType.ZhiPu.value and ZhiPu.value_check(self.config.ZhiPu):
                self.chat = ZhiPu(self.config.ZhiPu)
            else:
                self.LOG.warning("未配置模型")
                self.chat = None
        else:
            if TigerBot.value_check(self.config.TIGERBOT):
                self.chat = TigerBot(self.config.TIGERBOT)
            elif ChatGPT.value_check(self.config.CHATGPT):
                self.chat = ChatGPT(self.config.CHATGPT)
            elif XinghuoWeb.value_check(self.config.XINGHUO_WEB):
                self.chat = XinghuoWeb(self.config.XINGHUO_WEB)
            elif ChatGLM.value_check(self.config.CHATGLM):
                self.chat = ChatGLM(self.config.CHATGLM)
            elif BardAssistant.value_check(self.config.BardAssistant):
                self.chat = BardAssistant(self.config.BardAssistant)
            elif ZhiPu.value_check(self.config.ZhiPu):
                self.chat = ZhiPu(self.config.ZhiPu)
            else:
                self.LOG.warning("未配置模型")
                self.chat = None

        self.LOG.info(f"已选择: {self.chat}")

    def __load_functions__(self):
        start_time = time.time()
        with sessionmaker(bind=self.engine)() as session:
            plugins = session.query(ChatPlugin).filter_by(plugin_type=2).all()
        if not plugins:
            return
        for plugin in plugins:
            if not plugin.path.endswith(".py"):
                continue
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), plugin.path)
            try:
                # 打开文件并读取内容
                with open(file_path, "r", encoding="utf-8") as file:
                    tree = ast.parse(file.read(), filename=file_path)
            except (FileNotFoundError, IOError) as e:
                print(f"Error reading file {plugin.path}: {e}")
                continue
            module_name = file_path[:-3]
            # 查找符合条件的函数
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if (node.name == "execute" and
                            len(node.args.args) == 1 and
                            node.args.args[0].arg == "param" and
                            isinstance(node.args.args[0].annotation, ast.Name) and
                            node.args.args[0].annotation.id == "KeyWordParams" and
                            isinstance(node.returns, ast.Name) and
                            node.returns.id == "bool"):
                        # 动态导入模块
                        try:
                            spec = importlib.util.spec_from_file_location("execute", file_path)
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            self.functions.append({plugin: getattr(module, "execute")})
                        except (ImportError, AttributeError) as e:
                            print(f"Error importing module {module_name}: {e}")
                            continue
        elapsed_time = time.time() - start_time
        self.LOG.info(f"已加载:{len(self.functions)}个插件用时:{elapsed_time:.4f}秒")

    @staticmethod
    def value_check(args: dict) -> bool:
        if args:
            return all(value is not None for key, value in args.items() if key != 'proxy')
        return False

    def toAt(self, msg: WxMsg) -> bool:
        """处理被 @ 消息
        :param msg: 微信消息结构
        :return: 处理状态，`True` 成功，`False` 失败
        """
        return self.toChitchat(msg)

    def toChengyu(self, msg: WxMsg) -> bool:
        """
        处理成语查询/接龙消息
        :param msg: 微信消息结构
        :return: 处理状态，`True` 成功，`False` 失败
        """
        status = False
        texts = re.findall(r"^([#|?|？])(.*)$", msg.content)
        # [('#', '天天向上')]
        if texts:
            flag = texts[0][0]
            text = texts[0][1]
            if flag == "#":  # 接龙
                if cy.isChengyu(text):
                    rsp = cy.getNext(text)
                    if rsp:
                        self.sendTextMsg(rsp, msg.roomid)
                        status = True
            elif flag in ["?", "？"]:  # 查词
                if cy.isChengyu(text):
                    rsp = cy.getMeaning(text)
                    if rsp:
                        self.sendTextMsg(rsp, msg.roomid)
                        status = True

        return status

    def toChitchat(self, msg: WxMsg) -> bool:
        """闲聊，接入 ChatGPT
        """
        if not self.chat:  # 没接 ChatGPT，固定回复
            rsp = None
        else:  # 接了 ChatGPT，智能回复
            q = re.sub(r"@.*?[\u2005|\s]", "", msg.content).replace(" ", "")
            rsp = self.chat.get_answer(q, (msg.roomid if msg.from_group() else msg.sender))

        if rsp:
            if msg.from_group():
                self.sendTextMsg(rsp, msg.roomid, msg.sender)
            else:
                self.sendTextMsg(rsp, msg.sender)

            return True
        else:
            self.LOG.error(f"无法从 ChatGPT 获得答案")
            return False

    def processMsg(self, msg: WxMsg) -> None:
        """当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
        此处可进行自定义发送的内容,如通过 msg.content 关键字自动获取当前天气信息，并发送到对应的群组@发送者
        群号：msg.roomid  微信ID：msg.sender  消息内容：msg.content
        content = "xx天气信息为："
        receivers = msg.roomid
        self.sendTextMsg(content, receivers, msg.sender)
        """

        # 来自非群聊的特殊消息处理
        if not msg.from_group():
            # 自动通过好友申请请求
            if msg.type == 37 and True:
                self.autoAcceptFriendRequest(msg)
                return
            if msg.type == 10000:
                self.sayHiToNewFriend(msg)
                return

                # 群聊消息
        if self.to_keyword_plugin(msg):
            return

        if msg.from_group():
            # 如果在群里被 @
            if msg.roomid not in self.config.GROUPS:  # 不在配置的响应的群列表里，忽略
                return

            if msg.is_at(self.wxid):  # 被@
                self.toAt(msg)

            else:  # 其他消息
                self.toChengyu(msg)

            return  # 处理完群聊信息，后面就不需要处理了
        if msg.type == 0x01:  # 文本消息
            # 让配置加载更灵活，自己可以更新配置。也可以利用定时任务更新。
            if msg.from_self():
                if msg.content == "^更新$":
                    self.config.reload()
                    self.LOG.info("已更新")
            else:
                self.toChitchat(msg)  # 闲聊

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    # self.LOG.info(msg)
                    self.processMsg(msg)
                except Empty:
                    continue  # Empty message
                except Exception as e:
                    self.LOG.error(f"Receiving message error: {e}")

        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name="GetMessage", args=(self.wcf,), daemon=True).start()

    def sendTextMsg(self, msg: str, receiver: str, at_list: str = "") -> None:
        """ 发送消息
        :param msg: 消息字符串
        :param receiver: 接收人wxid或者群id
        :param at_list: 要@的wxid, @所有人的wxid为：notify@all
        """
        # msg 中需要有 @ 名单中一样数量的 @
        ats = ""
        if at_list:
            if at_list == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = at_list.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f" @{self.wcf.get_alias_in_chatroom(wxid, receiver)}"

        # {msg}{ats} 表示要发送的消息内容后面紧跟@，例如 北京天气情况为：xxx @张三
        if ats == "":
            self.LOG.info(f"To {receiver}: {msg}")
            self.wcf.send_text(f"{msg}", receiver, at_list)
        else:
            self.LOG.info(f"To {receiver}: {ats}\r{msg}")
            self.wcf.send_text(f"{ats}\n\n{msg}", receiver, at_list)

    def keepRunningAndBlockProcess(self) -> None:
        """
        保持机器人运行，不让进程退出
        """
        while True:
            self.runPendingJobs()
            time.sleep(1)

    def autoAcceptFriendRequest(self, msg: WxMsg) -> None:
        try:
            xml = ET.fromstring(msg.content)
            v3 = xml.attrib["encryptusername"]
            v4 = xml.attrib["ticket"]
            scene = int(xml.attrib["scene"])
            self.wcf.accept_new_friend(v3, v4, scene)

        except Exception as e:
            self.LOG.error(f"同意好友出错：{e}")

    def sayHiToNewFriend(self, msg: WxMsg) -> None:
        nick_name = re.findall(r"你已添加了(.*)，现在可以开始聊天了。", msg.content)
        if nick_name:
            # 添加了好友，更新好友列表
            self.allContacts.append(self.wcf.get_info_by_wxid(msg.sender))
            self.sendTextMsg(f"Hi {nick_name[0]} 。", msg.sender)

    def start_cron(self):
        # 创建会话类
        with sessionmaker(bind=self.engine)() as session:
            plugins = session.query(ChatPlugin).filter_by(plugin_type=1).all()
        if not plugins:
            return
        for plugin in plugins:
            corn = plugin.cron
            receiver = plugin.receiver
            plugin_dir = plugin.path
            params = plugin.params
            if not receiver or len(str(receiver)) <= 0:
                self.onEveryTime(corn, self.execute_corn, receiver=receiver, plugin_dir=plugin_dir, params=params)

    def execute_corn(self, receiver, plugin_dir, params):
        spec = importlib.util.spec_from_file_location("execute", plugin_dir)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result = module.execute(params)
        if result is not None and len(result) > 0:
            for ree in receiver.spilt(","):
                self.sendTextMsg(result, ree)

    def to_keyword_plugin(self, msg: WxMsg):
        for plugin_dict in self.functions:
            for plugin, func in plugin_dict.items():
                if not self.__auth_room_id_and_sender_id(plugin.roomId, plugin.senderId, msg.roomid, msg.sender):
                    continue
                if func(KeyWordParams(self.wcf, msg, self.engine)):
                    return True

    @staticmethod
    def __auth_room_id_and_sender_id(room_ids: str, sender_ids: str, room_id: str, sender: str) -> bool:
        """
        验证消息的 room_id 和 sender 是否有权限执行插件。

        :param room_ids: 允许的 room_id 列表（逗号分隔）
        :param sender_ids: 允许的 sender 列表（逗号分隔）
        :param room_id: 消息的 room_id
        :param sender: 消息的 sender
        :return: 是否有权限
        """
        # 将逗号分隔的字符串转换为集合
        allowed_rooms = set(room_ids.split(",")) if room_ids else set()
        allowed_senders = set(sender_ids.split(",")) if sender_ids else set()

        # 私聊消息
        if not room_id:
            return sender in allowed_senders

        # 群聊消息
        if room_id not in allowed_rooms:
            return False

        # 如果 sender_ids 为空，则允许所有 sender
        if not sender_ids:
            return True

        # 检查 sender 是否在允许的列表中
        return sender in allowed_senders
