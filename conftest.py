# 获取根路径
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)

import time
import pytest
from common.login.web_login import Web_Login
from config.Config import Config

cf = Config()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    print(terminalreporter.stats)
    print("total:", terminalreporter._numcollected)
    print('passed:', len(terminalreporter.stats.get('passed', [])))
    print('failed:', len(terminalreporter.stats.get('failed', [])))
    print('error:', len(terminalreporter.stats.get('error', [])))
    print('skipped:', len(terminalreporter.stats.get('skipped', [])))
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times:', duration, 'seconds')


@pytest.fixture(scope='session', autouse=True)
def weblogin():
    login = Web_Login()
    login.login(cf.web_login_name)
    return login
