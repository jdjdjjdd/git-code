import requests

from common.login.login_basic import app_login, body_a
from config.Config import Config

cf = Config()

class AppLogin():
    def login(self, phone=None,TenantType=2):
        # 登录获取返回结果
        result = app_login(phone=phone,app_key= cf.app_appkey,appid=cf.app_appid,TenantType=TenantType)['Data']
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
        req_body = body_a(data, guid=self.Guid, token=self.access_token,app_key='DJYWeb')
        if '/fw/' in url:
            req_body = body_a(data, app_id=self.zt_tid, guid=self.zt_guid, token=self.zt_token, app_key='DJYWeb')
        api_name = url.split("/")[-1]
        result = requests.post(url=url, json=req_body, verify=False)
        return result
