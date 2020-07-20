#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# 判断环境系统
pip = 'pip' if sys.platform == 'win32' else 'pip3'

# 第三方库列表
libs = ['requests', 'oss2', 'pymysql', 'openpyxl', 'xlrd', 'jsonpath', 'pytest', 'pytest-assume', 'pytest-ordering',
        'python-consul']

# 安装第三方库
try:
    for lib in libs:
        os.system(pip + ' install ' + lib + ' -i http://pypi.douban.com/simple --trusted-host pypi.douban.com')
except:
    print('install failed')
