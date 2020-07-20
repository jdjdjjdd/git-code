#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import requests,time,hashlib,json,uuid
from config import Config
cf = Config.Config()



def databuild(**kwargs):
    """
    公用的函数，构造data参数
    :param kwargs:
    :return:
    """
    data = json.dumps(kwargs)
    print(data)
    return data


def body(data: str, guid=0, app_id='1000001', app_key='DJYWeb', token='', sign='', ) -> dict:
    # 获取时间戳，先转换成整形，再转换字符串
    t = int(time.time())
    timestamp = str(t)
    # 构造nonce_str
    nonce_str = str(uuid.uuid1())
    # 通用请求头
    dic = {
        'app_id': app_id,
        'timestamp': timestamp,
        'nonce_str': nonce_str,
        'token': token,
        'sign': sign,
        'data': data
    }
    # 去除空值的键,构造新字典
    dic = {key: value for key, value in dic.items() if value}
    # 对key做字典升序排序，得到有序参数列表ascending_order_dic
    ascending_order_dic = sorted(dic.items(), key=lambda d: d[0], reverse=False)
    # 按照URL键值对的格式拼接成字符串
    list_str = ""
    for k, v in ascending_order_dic:
        list_str += k + '=' + v + '&'
    # 进行MD5运算
    m = hashlib.md5()
    m.update(list_str.encode('UTF-8'))
    strMD5 = m.hexdigest()
    # 字符串转大写，得到请求签名signature
    signature = strMD5.upper()
    # 构造body
    body = {
        'app_id': app_id,
        'guid': guid,
        'timestamp': timestamp,
        'nonce_str': nonce_str,
        'token': token,
        'app_key': app_key,
        'data': data,
        'signature': signature,
    }

    return body

def body_a(data: str, guid=0, app_id='1000001', app_key='DJYWeb', token='', sign='',AppVer='1.0',DeviceType='android',Lang='zh' ) -> dict:
    # 获取时间戳，先转换成整形，再转换字符串
    t = int(time.time())
    timestamp = str(t)
    # 构造nonce_str
    nonce_str = str(uuid.uuid1())
    # 通用请求头
    dic = {
        'app_id': app_id,
        'timestamp': timestamp,
        'nonce_str': nonce_str,
        'token': token,
        'sign': sign,
        'data': data
    }
    # 去除空值的键,构造新字典
    dic = {key: value for key, value in dic.items() if value}
    # 对key做字典升序排序，得到有序参数列表ascending_order_dic
    ascending_order_dic = sorted(dic.items(), key=lambda d: d[0], reverse=False)
    # 按照URL键值对的格式拼接成字符串
    list_str = ""
    for k, v in ascending_order_dic:
        list_str += k + '=' + v + '&'
    # 进行MD5运算
    m = hashlib.md5()
    m.update(list_str.encode('UTF-8'))
    strMD5 = m.hexdigest()
    # 字符串转大写，得到请求签名signature
    signature = strMD5.upper()
    # 构造body
    body = {
        'app_id': app_id,
        'guid': guid,
        'timestamp': timestamp,
        'nonce_str': nonce_str,
        'token': token,
        'app_key': app_key,
        'data': data,
        'signature': signature,
        'AppVer' : AppVer,
        'DeviceType' : DeviceType,
        'Lang' : Lang
    }

    return body


def djy_get_vcode(phonenum,app_id,app_key):
    """
    大佳营模板获取验证码
    :param phonenum:
    :param url:
    :return: vcode
    """
    data = databuild(SPhone=phonenum)
    Body = body(data=data, guid=0, app_id=app_id, app_key=app_key)
    response = requests.post(url=cf.host + 'api/v1/VCodeManager/GetVCode', json=Body)
    try:
        vcode = response.json()['Data']
        return vcode
    except Exception:
        print(Exception)

def labor_pre_login(phonenum, vcode,app_key):
    """
    大佳营模板预登陆接口
    :param phonenum:
    :param vcode:
    :param url:
    :return: tenanttype
    """
    data = databuild(Mobile=phonenum, VerifyCode=vcode)
    Body = body(data=data, guid=0, app_id='1000001', app_key=app_key)
    response = requests.post(url=cf.host+'api/v1/DJY_Login/Labor_Pre_Login', json=Body)
    try:
        tenanttype = response.json()['Data']['TenantType']
        return tenanttype
    except Exception:
        print(Exception)

def labor_weblogin(phonenum,app_key):
    """
    劳务模板登陆接口
    :param phonenum:
    :return: Data
    """
    vcode = djy_get_vcode(phonenum=phonenum, app_id='1000001', app_key=app_key)
    tenanttype = labor_pre_login(phonenum=phonenum,vcode=vcode,app_key=app_key)
    data = databuild(Mobile=phonenum, VerifyCode=vcode, tenanttype=tenanttype)
    Body = body(data=data, guid=0, app_id='1000001', app_key=app_key)
    response = requests.post(url=cf.host+'api/v1/DJY_Login/Labor_WebLogin', json=Body)
    try:
        Data = response.json()['Data']
        return Data
    except Exception:
        print(Exception)

def applet_login(phonenum,vcode,appid,appkey,tenantype):
    """小程序登陆"""
    #构建data
    data = databuild(mobile=phonenum, vcode=vcode,tenant_type=tenantype)
    #构建body体
    Body = body(data=data, guid=0, app_id=appid, app_key=appkey)
    response = requests.post(url=cf.host+'api/v1/DJY_Login/MiniLogin', json=Body,verify=False)
    try:
        result = response.json()
        return result
    except Exception:
        print("登陆失败，请定位")

def app_login(phone,appid,app_key,TenantType):
    # 构建data
    vcode = djy_get_vcode(phonenum=phone, app_id='1000001', app_key=app_key)
    data = databuild(Mobile=phone, VerifyCode=vcode,DeviceID='863178040256927',TenantType=TenantType)
    # 构建body体
    Body = body_a(data=data, guid=0, app_id=appid, app_key=app_key,AppVer='1.0')
    response = requests.post(url=cf.host + 'api/v1/DJY_Login/Labor_S_AppLogin', json=Body, verify=False)
    try:
        result = response.json()
        return result
    except Exception:
        print("登陆失败，请定位")

if __name__ == '__main__':
    res = app_login(phone='13340000001',appid='1000001',app_key='DJYApp',TenantType=2)
    print(res)
    # res = labor_weblogin('13340000001',app_key='DJYWeb')
    # print(res)