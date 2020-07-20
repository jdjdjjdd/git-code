# -*- coding: utf-8 -*-


import requests

from config import Config
from .login_basic import labor_weblogin, body

cf = Config.Config()

class Web_Login():
    # 登录web端
    def login(self, phone=None):
        # 登录获取返回结果
        result = labor_weblogin(phone,cf.web_appkey)
        self.Guid = result['Guid']
        self.Name = result['Name']
        self.zt_tid = result['zt_tid']
        self.access_token = result['access_token']
        self.client_id = result['client_id']
        self.client_secret = result['client_secret']
        self.expires_in = result['expires_in']
        self.refresh_token = result['refresh_token']
        self.zt_token = result['zt_access_token']
        self.zt_guid = result['zt_guid']
        self.sp_id = result['sp_id']
        self.login_phone = phone
        return result

    def create_api(self, url, **kwargs):
        """
        构造接口的函数
        :param url:
        :param kwargs:
        :return:
        """
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        data = str(kwargs).replace('\'', '\"')
        # 如果接口地址包含fw则为中台接口，token使用中台token

        if '/fw/' not in url:
            req_body = body(data, guid=self.Guid, token=self.access_token, app_key=cf.web_appkey)
        else:
            req_body = body(data, app_id=self.zt_tid, guid=self.zt_guid, token=self.zt_token, app_key=cf.web_appkey)
        api_name = url.split("/")[-1]
        result = requests.post(url=url, json=req_body, verify=False)
        print(url)
        print('接口地址为: {0}\n'
              '调用参数: {1}\n'
              '返回结果: {2}\n'.format(api_name, req_body, result.json()))
        return result