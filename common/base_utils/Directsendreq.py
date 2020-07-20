# coding=utf-8
import os,sys,json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from common.login.login_basic import *
from config import Config
cf = Config.Config()

# 获取接口地址前缀域名
path = cf.host
app_key=cf.web_appkey


class SendRequests():
    """无需登录就可以调用的接口公共方法"""

    def excelsendReq(sel,url,apiData):
        try:
           # requestUrl = path+url
           req_data = json.dumps(apiData, ensure_ascii=False)
           Body=body(data=req_data, guid=0, app_id='1000001', app_key=app_key)
           print(Body)
           res = requests.post(url=url, json=Body,verify=False)
           print(res.status_code)
           return res

        except Exception as e:
            print(e)


    def sendRequests(sel,url,apiData):
        try:
           # requestUrl = path+url
           Body=body(data=apiData, guid=0, app_id='1000001', app_key=app_key)
           print(Body)
           res = requests.post(url=url, json=Body,verify=False)
           print(res.json())
           return res

        except Exception as e:
            print(e)


if __name__ == '__main__':
    c1=SendRequests()
    c1.sendRequests('https://dajiaying-web.sit.woda.ink/api/v1/VCodeManager/GetVCode',)