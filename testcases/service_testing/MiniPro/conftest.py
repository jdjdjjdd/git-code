# 获取根路径
import os,sys
import pytest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)
from config.Config import Config
from common.venv.var import *
from common.login.applet_login import Applet_Login
from common.base_utils.comm_utils import *
from common.business_func.applet_func import *
from common.login.web_login import Web_Login
from common.business_func.mem_information_manag_func import *

cf = Config()


@pytest.fixture(scope='class')
def minilogin():
    """
    预置条件：录入名单
    :param weblogin:登陆信息
    :return: nameid，idnum，mobile
    """
    # 创建小程序登陆实例对象
    Minilogin = Applet_Login()
    # 创建web登录对象
    weblogin = Web_Login()
    # 创建Member_information_management_func对象
    management_func = Member_information_management_func(weblogin)
    # 创建Applet_func实例对象
    appletfunc = Applet_func(Minilogin)
    # 初始化数据库实例对象
    db = OperateMDdb()
    #生成系统中不存在的手机号码
    # 生成系统中不存在的手机号码
    while True:
        # 生成手机号码
        mobile = create_phone()
        # 校验手机号码是否存在
        mobilesql = f"select guid from center_user where login_name={mobile}"
        res = db.selectsql(mobilesql)
        if res == ():
            break
    #登录小程序
    Minilogin.applogin(2,mobile)

    return Minilogin

@pytest.fixture(scope='function')
def mini_uploadidcard(login):
    Minilogin,mobile=login()
    # 创建Applet_func实例对象
    appletfunc = Applet_func(Minilogin)
    appletfunc.upload_idcard(fakeridcardpicture)

    return Minilogin


@pytest.fixture(scope='function')
def mini_upload_allstatus_bankcard(login):
    Minilogin,mobile=login()
    # 创建Applet_func实例对象
    appletfunc = Applet_func(Minilogin)
    appletfunc.upload_idcard(fakeridcardpicture)

    return Minilogin
