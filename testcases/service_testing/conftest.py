# 获取根路径
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)

import pytest
from common.business_func.mem_information_manag_func import Member_information_management_func
from common.business_func.applet_func import Applet_func
from common.business_func.group_management import GroupManagement
from common.business_func.namelist import NameList
from common.business_func.orders import Order
from common.business_func.advance_management import AdvanceManage
from config.Config import Config

cf = Config()


@pytest.fixture(scope='class')
def name_manage(weblogin):
    """初始化名单实例"""
    return NameList(weblogin)


@pytest.fixture(scope='class')
def order_manage(weblogin):
    """初始化名单实例"""
    return Order(weblogin)


@pytest.fixture(scope='class')
def group_manage(weblogin):
    """初始化集团管理实例"""
    return GroupManagement(weblogin)


@pytest.fixture(scope='class')
def member_manage(weblogin):
    """初始化会员管理实例"""
    return Member_information_management_func(weblogin)


@pytest.fixture(scope='class')
def applet_manage(weblogin):
    """初始化小程序管理实例"""
    return Applet_func(weblogin)


@pytest.fixture(scope='class')
def advance_manage(weblogin):
    """初始化可预支管理实例"""
    return AdvanceManage(weblogin)
