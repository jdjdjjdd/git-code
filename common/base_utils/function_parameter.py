#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : function_parameter.py
# @Author   : jd
# @Date     : 2020/06/16
# @Update   : 新增
# @Desc     : 工具

def function_parameter(a:dict):
    """
    json转换为函数入参格式
    入参为请求的data，json格式
    """
    jsonadd = str(a)
    jsonadd = jsonadd.replace("'",'')
    jsonadd = jsonadd.replace(':','=')
    print(jsonadd)


def request_body(a:dict):
    """
    json转换为请求体格式
    入参为请求的data，json格式
    """
    jsondic = a
    jsonkey = list(jsondic.keys())
    for i in range(len(jsondic)):
        jsondic[jsonkey[i]] = jsonkey[i]

    jsonadd = str(jsondic)
    jsonadd = jsonadd.replace("'", '')
    jsonadd = jsonadd.replace(':', '=')
    print(jsonadd)









function_parameter({"CoopEntId":235,"CoopEntName":"胜狮小时工","IsEnabled":2,"EntId":208,"RcrtType":2,"Flag":0})
request_body({"CoopEntId":235,"CoopEntName":"胜狮小时工","IsEnabled":2,"EntId":208,"RcrtType":2,"Flag":0})
