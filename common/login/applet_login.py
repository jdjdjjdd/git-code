#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : applet_login.py
# @Author   : qiuhaojian
# @Date     : 2020/02/23
# @Desc     : 公共方法


import requests

from common.login.login_basic import djy_get_vcode, applet_login, body
from config import Config

cf = Config.Config()

class Applet_Login():
#小程序登录
    def applogin(self,tenantype,phone=None,):
        #获取验证码
        result = djy_get_vcode(phone, '1000001', cf.applet_appkey)
        vcode = result
        result = applet_login(phone, vcode, '1000001', cf.applet_appkey, tenantype)
        self.Guid = result['Data']['user_id']
        self.Name = result['Data']['member_name']
        # self.TId = result['Data']['zt_tid']
        self.access_token = result['Data']['access_token']
        self.client_id = result['Data']['client_id']
        self.client_secret = result['Data']['client_secret']
        self.expires_in = result['Data']['expires_in']
        self.refresh_token = result['Data']['refresh_token']
        self.zt_token = result['Data']['zt_access_token']
        self.uuid = result['Data']['uuid']
        self.zt_client_id = result['Data']['zt_client_id']
        return result

    def create_api(self,url, **kwargs):
        """
        构造接口的函数
        :param url:
        :param kwargs:
        :return:
        """
        #构建data参数
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        data = str(kwargs).replace('\'', '\"')
        # 构建body参数

        api_name = url.split("/")[-1]
        # if api_name == 'GetTenantEntListByName':
        #     req_body = body(data, guid=self.Guid, token=self.zt_token,app_id='1000006')
        # else:
        req_body = body(data, guid=self.Guid, token=self.zt_token, app_key=cf.applet_appkey,
                        app_id=self.zt_client_id.split('-')[0])
        result = requests.post(url=url, json=req_body, verify=False)
        print('接口地址为: {0}\n'
              '调用参数: {1}\n'
              '返回结果: {2}\n'.format(api_name, req_body, result.json()))
        return result


    #excel自动化发送接口请求方法
    def sendRequests(self,apiData):
        """
        构造接口的函数
        :param apiData:
        :return:
        """
        # 获取data参数
        data = apiData['data']
        # 获取url参数
        if apiData["url"] == '':
            raise Exception('请求的接口为空')
        else:
            requestUrl = cf.host + apiData['url']

        # 构建body参数
        api_name = requestUrl.split("/")[-1]

        req_body = body(data, guid=self.Guid, token=self.zt_token, app_key='JFFApp',app_id='1000006')


        result = requests.post(url=requestUrl, json=req_body, verify=False)
        return result.json()


if __name__=='__main__':
    a=Applet_Login()
    a.applogin('13300000000')