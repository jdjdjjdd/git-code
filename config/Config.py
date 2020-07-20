# -*- coding: utf-8 -*-

import datetime
import os
from configparser import ConfigParser

from common.base_utils import Log


class Config:
    # titles:
    TITLE_DEBUG = "sit"
    TITLE_RELEASE = "prd"
    TITLE_EMAIL = "mail"

    # values:
    # [sit\prd]
    VALUE_WEB_APPKEY = "web_appkey"
    VALUE_APPLET_APPKEY = "applet_appkey"
    VALUE_APP_APPKEY = "app_appkey"
    VALUE_WEB_APPID = "web_appid"
    VALUE_APPLET_APPKID = "applet_appid"
    VALUE_APP_APPKID = "app_appid"
    VALUE_HOST = "host"
    VALUE_DATABASE = "database"
    VALUE_WEB_LOGIN_NAME = 'web_login_name'
    VALUE_PQAPP_LOGIN_NAME = 'pqapp_login_name'
    VALUE_ZPAPP_LOGIN_NAME = 'zpapp_login_name'
    VALUE_DB_HOST = 'db_host'


    # [mail]
    VALUE_SMTP_SERVER = "smtpserver"
    VALUE_SENDER = "sender"
    VALUE_RECEIVER = "receiver"
    VALUE_USERNAME = "username"
    VALUE_PASSWORD = "password"

    # path
    path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

    def __init__(self):
        """
        初始化
        """
        self.config = ConfigParser()
        self.log = Log.MyLog()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_env_config.ini')
        self.xml_report_path = Config.path_dir+'/report/xml'
        self.html_report_path = Config.path_dir+'/report/html'

        if not os.path.exists(self.conf_path):
            raise FileNotFoundError("请确保配置文件存在！")

        self.config.read(self.conf_path, encoding='utf-8')

        self.web_appkey = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_WEB_APPKEY)
        self.app_appkey = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_APP_APPKEY)
        self.applet_appkey = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_APPLET_APPKEY)
        self.web_appid = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_WEB_APPID)
        self.app_appid = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_APP_APPKID)
        self.applet_appid = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_APPLET_APPKID)
        self.host = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_HOST)
        self.database = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_DATABASE)
        self.web_login_name = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_WEB_LOGIN_NAME)
        self.pqapp_login_name = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_PQAPP_LOGIN_NAME)
        self.zpapp_login_name = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_ZPAPP_LOGIN_NAME)
        self.db_host = self.get_conf(Config.TITLE_DEBUG, 'db_host')
        self.db_user = self.get_conf(Config.TITLE_DEBUG, 'db_user')
        self.db_password = self.get_conf(Config.TITLE_DEBUG, 'db_password')
        self.db_port = self.get_conf(Config.TITLE_DEBUG, 'db_port')
        self.db_zt = self.get_conf(Config.TITLE_DEBUG, 'db_zt')
        self.db_mb = self.get_conf(Config.TITLE_DEBUG, 'db_mb')
        self.db_charset = self.get_conf(Config.TITLE_DEBUG, 'db_charset')
        # self.web_appkey_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_WEB_APPKEY)
        # self.app_appkey_prd = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_APP_APPKEY)
        # self.applet_appkey_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_APPLET_APPKEY)
        # self.web_appid_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_WEB_APPID)
        # self.app_appid_prd = self.get_conf(Config.TITLE_DEBUG, Config.VALUE_APP_APPKID)
        # self.applet_appid_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_APPLET_APPKID)
        # self.host_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_HOST)
        # self.database_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_DATABASE)
        # self.web_login_name_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_WEB_LOGIN_NAME)
        # self.app_login_name_prd = self.get_conf(Config.TITLE_RELEASE, Config.VALUE_APP_LOGIN_NAME)

        self.smtpserver = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_SMTP_SERVER)
        self.sender = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_SENDER)
        self.receiver = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_RECEIVER)
        self.username = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_USERNAME)
        self.password = self.get_conf(Config.TITLE_EMAIL, Config.VALUE_PASSWORD)
        # 根路径
        curPath = os.path.abspath(os.path.dirname(__file__))
        self.rootPath = curPath[:curPath.find("autotest") + len("autotest")]

        # 压缩包名称
        self.zipname = '测试报告' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.zip'

        # 登陆信息
        self.login_func = None


    def get_conf(self, title, value):
        """
        配置文件读取
        :param title:
        :param value:
        :return:
        """
        return self.config.get(title, value)

    def set_conf(self, title, value, text):
        """
        配置文件修改
        :param title:
        :param value:
        :param text:
        :return:
        """
        self.config.set(title, value, text)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)

    def add_conf(self, title):
        """
        配置文件添加
        :param title:
        :return:
        """
        self.config.add_section(title)
        with open(self.conf_path, "w+") as f:
            return self.config.write(f)
