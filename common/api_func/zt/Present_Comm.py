#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : Present_Comm.py
# @Author   : yht
# @Date     : 2020/05/11
# @Update   :
# @Desc     : 通用服务


from common.lib.venv.api_path_zt import *
from common.lib.module_tools.analyze_result import get_api_result


class PresentComm:

    def __init__(self,login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login

    def get_labor(self, url, LaborName=None):
        """
        # 获取招聘、派遣端录名单时需要的去向
        :param url: 调用获取去向劳务的接口地址，必填
        :param LaborName: 去向劳务，可选，默认为空
        :return:
        """
        res = self.cs.create_api(url).json()
        if url == get_labor:
            self.TargetSpId = int(get_api_result(res, 'SpId')[0])
            self.SpName = get_api_result(res, 'SpShortName')[0]
        else:
            # 企业不为空，获取企业列表
            laborlist = res['Data']['RecordList']
            # 遍历列表寻找指定名称的id，找到id后赋值给SpEntID，没找到传入的名称抛出异常
            for labor in laborlist:
                if labor['SpShortName'] == LaborName:
                    self.TargetSpId = labor['SpId']
                    self.SpName = LaborName
                    break
        return res