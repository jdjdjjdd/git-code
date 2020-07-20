#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : configuration_management.py
# @Author   : yht
# @Date     : 2020/02/28
# @Update   : 日期加名称
# @Desc     : 配置项管理

from common.venv.api_path_mb import *


class Modify_Config():
    def __init__(self,login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login


    def modify_config(self,key,value,comment='',namespace='tech.name'):
        res_result = self.login.create_api(ModifyConfig,Key=key,Value=value,Comment=comment,NameSpace=namespace)
        return res_result.json()