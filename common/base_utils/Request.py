# -*- coding: utf-8 -*-
import json,requests
from common.login.login_basic import body
from common.login.applet_login import Applet_Login
from common.login.web_login import Web_Login
from common.login.app_login import AppLogin
from common.base_utils.comm_utils import create_phone
from config import Config
cf = Config.Config()

class SendRequest(object):
    def __init__(self):
        self.web_res = Web_Login().login(cf.web_login_name)
        self.applet_res = Applet_Login().applogin(create_phone())
        self.pq_app_res = AppLogin().login(phone=cf.pqapp_login_name, TenantType=2)
        self.zp_app_res = AppLogin().login(phone=cf.zpapp_login_name, TenantType=1)

    def send_request(self,url,data,platform=None):
        appkey = ''
        if not platform:
            self.res = self.web_res
            appkey = cf.web_appkey
        if platform == 'applet':
            self.res = self.applet_res
            appkey = cf.applet_appkey
        elif platform == 'pq_app':
            self.res = self.pq_app_res
            appkey = cf.app_appkey
        elif platform == 'zp_app':
            self.res = self.zp_app_res
            appkey = cf.app_appkey
        self.data = data
        self.url = url

        req_data = json.dumps(self.data, ensure_ascii=False)
        # 区分中台和模板接口，传不同参数
        if '/fw/' not in self.url:
            req_body = body(req_data, guid=self.res['Guid'], token=self.res['access_token'], app_key='DJYWeb')
        else:
            req_body = body(req_data, app_id=self.res['zt_tid'], guid=self.res['zt_guid'],
                            token=self.res['zt_token'], app_key=appkey)
        # 发起请求
        res = requests.post(url=self.url, json=req_body)
        return res
