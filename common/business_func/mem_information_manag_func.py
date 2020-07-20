#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : mem_information_manag_func.py
# @Author   : qiuhaojian
# @Date     : 2020/02/23
# @Desc     : 公共方法


from common.base_utils.comm_utils import get_api_result
from common.venv.api_path_zt import *


class Member_information_management_func():
    def __init__(self, login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login
        # 初始化关键的变量
        self.UserIdcardAuditId = None
        self.UserBankCardAuditId = None
        self.idcardnum = None
        self.UserWorkCardAuditId = None

    def get_idcardlist(
            self,
            auditsts=-9999,
            phone='',
            name='',
            IdCardNum=None,
            RegTimeBegin=None,
            RegTimeEnd=None):
        """
        获取身份证审核列表
        :param auditsts:审核状态，可选，默认全部，1 未审核，2 通过，3 未通过
        :param phone:会员手机号码，可选，默认空
        :param name:会员姓名，可选，默认空
        :return: 函数返回示例：
        {'Code': 0,
             'Data': {'NeedDesen': 0,
                      'RecordCount': 1,
                      'RecordList': [{'AuditBy': '',
                                      'AuditRemark': '',
                                      'AuditSts': 1,
                                      'AuditTm': '',
                                      'BankCardAuditSts': 0,
                                      'CreditScore': '',
                                      'Guid': 313721,
                                      'IdCardNum': '',
                                      'IdcardFrontUrl': 'zhjz/IDCard/tmp_idcard.jpg',
                                      'Mobile': '17256282601',
                                      'RealName': '',
                                      'RegTime': '2020-04-06 14:59:40.920248',
                                      'UserIdcardAuditId': 6027}],
                      'UnAuditRecordCount': 234},
             'Desc': '成功'}
        """
        # 调用获取身份证审核列表接口
        res = self.login.create_api(IDCardInfoList_Api,
                                    SequenceUploadTime=2,
                                    RecordIndex=0,
                                    RecordSize=999,
                                    AuditSts=auditsts,
                                    Mobile=phone,
                                    IdCardNum=IdCardNum,
                                    RegTimeBegin=RegTimeBegin,
                                    RegTimeEnd=RegTimeEnd,
                                    RealName=name)
        response = res.json()
        self.UserIdcardAuditId = get_api_result(response, 'UserIdcardAuditId')
        # pprint.pprint(res)
        # 返回response
        return response

    def audit_idcard(
            self,
            idcardnum,
            rname,
            phone=None,
            useridcardauditid=None):
        """
        身份证审核
        :param idcardnum:会员身份证号，必填
        :param rname:会员名称，必填
        :param phone:会员手机号码，必填
        :param useridcardauditid:身份证认证表主键，可选，默认None
        :return:
        """
        self.idcardnum = idcardnum
        # 查询身份证列表,如果用户未传useridcardauditid的值，使用对象的useridcardauditid值
        if phone:
            self.get_idcardlist(auditsts=1, phone=phone)
            useridcardauditid = self.UserIdcardAuditId[0] if self.UserIdcardAuditId else None
        # 调用审核身份证接口
        res = self.login.create_api(
            AuditIDCard_Api,
            IdCardNum=self.idcardnum,
            RealName=rname,
            UserIdcardAuditId=useridcardauditid)
        response = res.json()
        # pprint.pprint(response)
        # 返回response
        return response

    def IDCardPic(self, useridcardauditid):
        """
                身份证审核看不清
                :param useridcardauditid:身份证审核id，必填
                :return:
                """
        # 调用审核身份证看不清接口
        res = self.login.create_api(ZXX_GetNextIDCardPic_Api,
                                    UserIdcardAuditId=useridcardauditid)

        return res.json()

    def get_bankcardlist(
            self,
            auditsts=-9999,
            idcardnum='',
            phone='',
            name='',
            UploadTimeBegin=None,
            UploadTimeEnd=None):
        """
        获取银行卡审核列表
        :param auditsts:审核状态，可选，默认全部，1 未审核，2 通过，3 未通过
        :param idcardnum:会员身份证号码，可选，默认空
        :param phone:会员手机号码，可选，默认空
        :param name:会员姓名，可选，默认空
        :return:        返回示例：
        {'Code': 0,
             'Data': {'NeedDesen': 0,
                      'RecordCount': 1,
                      'RecordList': [{'AliBucket': 'woda-app-private-test',
                                      'AreaName': '',
                                      'AuditBy': '',
                                      'AuditRemark': '',
                                      'AuditSts': 1,
                                      'AuditTm': '0000-00-00 00:00:00',
                                      'BankCardNum': '',
                                      'BankCardUrl': 'zxx/BankCard/tmp_u=108706899,646491533&fm=26&gp=0.jpg',
                                      'BankName': '',
                                      'CityName': '',
                                      'IdCardAuditSts': 2,
                                      'IdCardNum': '521953667811287984',
                                      'IdcardFrontUrl': '',
                                      'Mobile': '18654445366',
                                      'ProvinceName': '',
                                      'RealName': '同工',
                                      'UploadTime': '2020-04-06 14:20:39.519822',
                                      'UserBankCardAuditId': 5710,
                                      'UserIdcardAuditId': 0}],
                      'UnAuditRecordCount': 62},
             'Desc': '成功'}

        """
        # 调用获取银行卡审核列表接口
        res = self.login.create_api(BankCardInfoList_Api,
                                    SequenceUploadTime=1,
                                    RecordIndex=0,
                                    RecordSize=999,
                                    AuditSts=auditsts,
                                    IsUserDelete=-9999,
                                    Bank3keyAvlSts=-9999,
                                    Bank3keyCheckResult=-9999,
                                    IdCardNum=idcardnum,
                                    Mobile=phone,
                                    UploadTimeBegin=UploadTimeBegin,
                                    UploadTimeEnd=UploadTimeEnd,
                                    RealName=name)
        response = res.json()
        self.UserBankCardAuditId = get_api_result(
            response, 'UserBankCardAuditId')
        # pprint.pprint(response)
        # 返回response
        return response

    def audit_bankcard(
            self,
            bankcardnum,
            bankname,
            phone=None,
            userbankcardauditid=None):
        """
        银行卡审核
        :param bankcardnum:会员身份证号码，可选，默认为None
        :param bankname:会员银行卡号，必填
        :param userbankcardauditid:银行卡认证主键id
        :return:
        """
        if phone:
            self.get_bankcardlist(phone=phone)
            userbankcardauditid = self.UserBankCardAuditId[0]
        # 调用银行卡审核接口
        res = self.login.create_api(AuditBankCard_Api,
                                    BankCardNum=bankcardnum,
                                    BankName=bankname,
                                    UserBankCardAuditId=userbankcardauditid)
        response = res.json()
        # pprint.pprint(response)
        # 返回response
        return response

    # 获取工牌审核列表
    def get_workcardlist(
            self,
            auditsts=-9999,
            idcardnum='',
            phone='',
            name='',
            UploadTimeBegin=None,
            UploadTimeEnd=None,
            RecordSize=10,
            RecordIndex=0):
        """
        返回值示例：
        {'Code': 0,
         'Data': {'NeedDesen': 0,
                  'RecordCount': 5,
                  'RecordList': [{'AuditBy': '张四风',
                                  'AuditRemark': '',
                                  'AuditSts': 2,
                                  'AuditTm': '2020-04-02 17:21:51',
                                  'EntFullName': '神达电脑科技有限公司',
                                  'EntId': 476,
                                  'EntShortName': '昆山昆达电脑',
                                  'IdCardNum': '521953667811287984',
                                  'IneterviewDate': '2020-03-25',
                                  'InterViewEntId': 10082,
                                  'InterViewEntShortNme': '岱哥标准',
                                  'InterviewEntFullName': '贾岱的标准企业',
                                  'Mobile': '18654445366',
                                  'RealName': '同工',
                                  'UploadTime': '2020-04-02 16:50:57.735982',
                                  'UserWorkCardAuditId': 84128,
                                  'WorkCardNo': '22',
                                  'WorkCardUrl': 'zhjz/WorkCard/tmp_u=165670367,2479347840&fm=26&gp=0.jpg'}],
                  'UnAuditRecordcount': 5},
         'Desc': '成功'}
        """
        # 调用获取工牌列表接口
        res = self.login.create_api(WorkCardInfoList_Api,
                                    SequenceUploadTime=2,
                                    RecordIndex=RecordIndex,
                                    RecordSize=RecordSize,
                                    EntId=-9999,
                                    AuditSts=auditsts,
                                    IdCardNum=idcardnum,
                                    Mobile=phone,
                                    UploadTimeBegin=UploadTimeBegin,
                                    UploadTimeEnd=UploadTimeEnd,
                                    RealName=name)
        response = res.json()
        self.UserWorkCardAuditId = get_api_result(
            response, 'UserWorkCardAuditId')
        # pprint.pprint(response)
        # 返回response
        return response

    # 工牌审核
    def audit_workcard(
            self,
            entshortname,
            workcardno,
            phone=None,
            userworkcardauditid=None):
        if phone:
            self.get_workcardlist(phone=phone)
            userworkcardauditid = self.UserWorkCardAuditId[0] if self.UserWorkCardAuditId else None
        # 调用获取企业接口
        res = self.login.create_api(GetPaySalaryEntList_Api,
                                    CoopSts=1,
                                    RecordIndex=0,
                                    RecordSize=9999)
        result = res.json()['Data']['RecordList']
        # pprint.pprint(result)
        entid = None
        for one in result:
            if one['EntShortName'] == entshortname:
                entid = one['EntId']
                break
        # print(entid)
        # 调用工牌审核接口
        res1 = self.login.create_api(AuditWorkCard_Api,
                                     UserWorkCardAuditId=userworkcardauditid,
                                     WorkCardNo=workcardno,
                                     SubmitEntId=entid)

        response = res1.json()
        # pprint.pprint(response)
        # 返回response
        return response

    # web端补卡方法
    def web_repair_clock(
            self,
            WorkCardNo,
            entshortname,
            clockDt,
            clockindt,
            clockoutdt,
            membername='',
            remark=''):
        # 调用获取企业接口
        res = self.login.create_api(GetPaySalaryEntList_Api,
                                    CoopSts=1,
                                    RecordIndex=0,
                                    RecordSize=9999)
        result = res.json()['Data']['RecordList']
        entid = None
        for one in result:
            if one['EntShortName'] == entshortname:
                entid = one['EntId']
                break
        if entid is None:
            raise Exception('未找到企业')
        # 获取uuid
        res = self.login.create_api(
            ZXX_Clock_EntByWorkCard,
            WorkCardNo=WorkCardNo).json()
        members = res['Data']['RecordList']
        # 根据会员姓名获取精确uuid
        mbrUuid = None
        for member in members:
            if membername == member['realName']:
                mbrUuid = member['uuid']
        # 调用web端补卡公共方法
        res = self.login.create_api(WebRepairClock_Api,
                                    WorkCardNo=WorkCardNo,
                                    mbrUuid=mbrUuid,
                                    ClockInDt=clockindt + ' 08:31:42',
                                    ClockOutDt=clockoutdt + ' 20:32:13',
                                    clockDt=clockDt,
                                    Remark=remark,
                                    EntId=entid)

        response = res.json()
        # pprint.pprint(response)
        # 返回response
        return response
