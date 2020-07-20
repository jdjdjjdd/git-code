#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : applet_func.py
# @Author   : qiuhaojian
# @Date     : 2020/02/23
# @Desc     : 公共方法


from common.venv.var import *
import oss2
from common.venv.api_path_zt import *
import os
import pprint



class Applet_func():
    """小程序相关功能"""
    def __init__(self,login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login
        #初始化关键的变量
        self.entid = None

    def get_ent(self,entname):
        """
        查询标准企业
        :param entname:标准企业名称，必填
        :return:
        """
        res = self.login.create_api(GetEcTenantEntListByName,
                              CoopSts=0,RecordIndex=0,
                              RecordSize=9999,
                              Name=entname)
        ents = res.json()['Data']['RecordList']
        for ent in ents:
            if entname == ent['EntShortName']:
                self.entid = ent['EntId']
        return res.json()

    def upload_idcard(self,IdCardFile):
        """上传身份证公共方法"""
        #获取AccessKeyId，AccessKeySecret，SecurityToken
        response=self.login.create_api(ALI_GetAliSTS)
        self.AccessKeyId = response.json()['Data']['AccessKeyId']
        self.AccessKeySecret = response.json()['Data']['AccessKeySecret']
        self.SecurityToken = response.json()['Data']['SecurityToken']
        #获取auth
        auth = oss2.StsAuth(self.AccessKeyId, self.AccessKeySecret, self.SecurityToken)
        #获取bucket对象
        bucket=oss2.Bucket(auth,'http://oss-cn-shanghai.aliyuncs.com', 'woda-app-private-test')
        # 获取IdCardFrontUrl的参数和上传到OSS的文件名
        fname = os.path.basename(IdCardFile)
        IdCardpath = f'zhjz/IDCard/tmp_{fname}'
        #上传文件
        result = bucket.put_object_from_file(IdCardpath, IdCardFile)
        pprint.pprint(result)

        #调用上传身份证接口
        res=self.login.create_api(UploadIDCard,IdCardFrontUrl=IdCardpath)
        pprint.pprint(res.json())
        return res.json()

    def upload_bankcard(self,bankname,bankCardFile):
        """上传银行卡公共方法"""
        #获取AccessKeyId，AccessKeySecret，SecurityToken
        response=self.login.create_api(ALI_GetAliSTS)
        self.AccessKeyId = response.json()['Data']['AccessKeyId']
        self.AccessKeySecret = response.json()['Data']['AccessKeySecret']
        self.SecurityToken = response.json()['Data']['SecurityToken']
        #获取auth
        auth = oss2.StsAuth(self.AccessKeyId, self.AccessKeySecret, self.SecurityToken)
        #获取bucket对象
        bucket=oss2.Bucket(auth,'http://oss-cn-shanghai.aliyuncs.com', 'woda-app-private-test')
        # 获取BankCardUrl的参数和上传到OSS的文件名
        fname = os.path.basename(bankCardFile)
        BankCardpath = f'zxx/BankCard/tmp_{fname}'
        #上传文件
        result = bucket.put_object_from_file(BankCardpath, bankCardFile)
        pprint.pprint(result)
        #调用上传银行卡接口
        res=self.login.create_api(AddBankCard_Api,
                                  ProvinceId=-9999,
                                  ProvinceName='请选择',
                                  CityId=-9999,
                                  CityName='请选择',
                                  AreaName='请选择',
                                  CfgBankId=None,
                                  BankName=bankname,
                                  BankCardUrl=bankCardFile)
        pprint.pprint(res.json())
        return res.json()

    def upload_workcard(self,entname,workCardFile):
        """上传工牌公共方法"""
        #获取企业列表
        self.get_ent(entname)
        entid=self.entid
        #获取AccessKeyId，AccessKeySecret，SecurityToken
        response=self.login.create_api(ALI_GetAliSTS)
        self.AccessKeyId = response.json()['Data']['AccessKeyId']
        self.AccessKeySecret = response.json()['Data']['AccessKeySecret']
        self.SecurityToken = response.json()['Data']['SecurityToken']
        #获取auth
        auth = oss2.StsAuth(self.AccessKeyId, self.AccessKeySecret, self.SecurityToken)
        #获取bucket对象
        bucket=oss2.Bucket(auth,'http://oss-cn-shanghai.aliyuncs.com', 'woda-app-public-test')
        # 获取IdCardFrontUrl的参数和上传到OSS的文件名
        fname = os.path.basename(workCardFile)
        WorkCardpath = f'zhjz/WorkCard/tmp_{fname}'
        #上传文件
        result = bucket.put_object_from_file(WorkCardpath, workCardFile)

        #调用上传工牌接口
        res=self.login.create_api(UploadWorkCard_Api,EntId=entid,WorkCardUrl=WorkCardpath)
        pprint.pprint(res.json())
        return res.json()


    def colock_in(self,clocktype):
        """打卡公共方法"""
        #调用打卡接口
        res=self.login.create_api(Clock_Api,Lng=120.992716,
                                  Lat=31.388361,
                                  Type=clocktype,
                                  WorkAddress='江苏省苏州市昆山市前进东路1527号',
                                  Device='')
        response=res.json()
        pprint.pprint(response)
        #返回response
        return response


    def repair_clock(self,clockdate,clocktm,clocktyp):
        """补卡公共方法
            clockdate:补卡日期
            clocktm：补卡时间
            clocktyp：补卡类型，1为上班卡，2为下班卡
        """
        # data={"Lng":120.975374,"Lat":31.378497,"Device":"","ClockDt":"2020-07-01","clockTm":"2020-07-01 08:01:00","clockTyp":1}

        #调用补卡接口
        res=self.login.create_api(RepairClock_Api,Lng=120.992716,
                                  Lat=31.388361,
                                  Device='',
                                  ClockDt=clockdate,
                                  clockTm=clocktm,
                                  clockTyp=clocktyp)
        response = res.json()
        pprint.pprint(response)
        # 返回response
        return response



