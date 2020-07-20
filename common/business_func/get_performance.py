#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.venv.api_path_mb import *
class GetPerformance():

    def __init__(self,login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login


    def getPerformanceDetailList(self,StDate,EndDate):




        res = self.login.create_api(url=GetPerformanceDetailList,
                                FromAppOrWeb=1,
                                 StDate=StDate,
                                 EndDate=EndDate,
                                 SearchKey="",
                                 WorkStatus=0,
                                 SearchType=1,
                                 PerformanceBrokerId=2390,
                                 RecordIndex=0,
                                 RecordSize=10)


        print(res.json())
        self.record_count = res.json()['Data']['RecordCount']




