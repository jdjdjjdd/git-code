#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : month_management.py
# @Author   : sam
# @Date     : 2020/03/30
# @Desc     : 月薪方法


from common.base_utils.edit_excel import edit_exctwo
from common.base_utils.aliyun_import import AlImport
from common.venv.var import *
from common.venv.api_path_zt import *
from common.business_func.advance_management import AdvanceManage
from common.base_utils.comm_utils import get_api_result
import requests
import time


class MonthManage():

    def __init__(self, login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login

    # 月薪管理
    def get_agent(self, agentname):
        """
        获取来源id
        :param agentname: 来源名称
        :return: self.agentid 来源id
        """
        req = self.login.create_api(
            get_agent,
            CoopSts=1,
            RecordIndex=0,
            RecordSize=9999)
        agentlist = req.json()['Data']['RecordList']
        self.agentid = None
        for i in range(len(agentlist)):
            if agentname == agentlist[i]['LaborName']:
                self.agentid = agentlist[i]['SpId']
        return self.agentid

    def get_ent(self, entname):
        """
        获取标准企业id
        :param entname: 标准企业名称
        :return: self.entid 标准企业id
        """
        print(entname)
        req = self.login.create_api(
            GetPaySalaryEntList_Api,
            CoopSts=1,
            RecordIndex=0,
            RecordSize=9999)
        print(req.json())
        entlist = req.json()['Data']['RecordList']
        for i in range(len(entlist)):
            try:
                if entname == entlist[i]['EntShortName']:
                    self.entid = entlist[i]['EntId']
                    print(type(self.entid))
            except Exception as e:
                print(e, '未找到标准企业', entname)
        return self.entid

    def month_import(self,
                     entname,
                     monthdate,
                     names,
                     idcadnums,
                     workcards,
                     realpay,
                     work_entry_date,
                     workhour,
                     workstatedate=None,
                     workstatus='在职',
                     remark=None,
                     salarytype=1):
        """
        # 月薪导入
        :param entname: 标准企业名称 必填
        :param monthdate: 所属月份，必填
        :param salarytype: 月薪导入类型，必填
        :param name: 会员名称，必填
        :param idcadnum: 会员身份证号码，必填
        :param workcard: 会员工牌，必填
        :param realpay: 实发工资，必填
        :param workdate: 会员入职日期，必填
        :param workstatus: 会员在职状态，选填，默认在职
        :param workhour: 出勤小时数，必填
        :return:
        """

        self.monthdate = monthdate
        # self.phone = send_user
        # 编辑可预支导入模板
        edit_exctwo(
            names=names,
            idcards=idcadnums,
            workcards=workcards,
            realpay=realpay,
            work_entry_date=work_entry_date,
            workstatus=workstatus,
            workhours=workhour,
            workstatedate=workstatedate,
            remark=remark)
        # 将目标导入阿里云
        alimport = AlImport(login=self.login)
        alimport.ali_import(
            myLocalFile=myLocalFile_month,
            myObjectName=myObjectName_month,
            bucketname='woda-app-public-test')
        # 获取标准企业id
        self.get_ent(entname=entname)
        # 导入预览
        req = self.login.create_api(
            MonthBillGen_ImportCheck,
            SheetName='Sheet1',
            BucketKey='woda-app-public-test',
            EnterpriseID=self.entid,
            FileName=myObjectName_month,
            Month=monthdate,
            SalaryType=1)

        BizID = req.json()['Data']['BizID']
        # 等待预览加载完毕
        while True:
            req = self.login.create_api(
                MonthBillGen_GetImportCheckResult,
                BizID=BizID,
                EnterpriseID=self.entid)
            time.sleep(2)
            if req.json()['Data']['State'] == 2:
                json_url = req.json()['Data']['ResultUrl']
                break
        json_res = requests.get(json_url)
        print('json_res',json_res)
        print(json_res.json())
        fileMd5 = json_res.json()['Data']['FileMd5']
        fileName = json_res.json()['Data']['FileName']

        # 获取来源id
        advance = AdvanceManage(self.login)
        res = advance.zxx_getNameList(StartDate=work_entry_date,EndDate=work_entry_date,IdCardNum=idcadnums[0])
        agentid = get_api_result(res,'SrceSpId')[0]
        print('agentid',agentid)
        # 下载json

        # 提交保存
        req = self.login.create_api(MonthBillGen_GenerateBatchByBizID,
                                    ImportBizID=BizID,
                                    AgentID=agentid,
                                    EnterpriseID=self.entid,
                                    FileMd5=fileMd5,
                                    FileName=fileName,
                                    OPType=1,
                                    Month=self.monthdate,
                                    SalaryType=salarytype,
                                    GeneratePayroll=2,
                                    BucketKey='woda-app-public-test')
        bizid = req.json()['Data']['BizID']
        # 等待保存完毕
        while True:
            req = self.login.create_api(
                MonthBillGen_GetGenerateBatchResult,
                BizID=bizid,
                EnterpriseID=self.entid)
            time.sleep(2)
            if req.json()['Data']['State'] == 2:
                break

    def select_monthbill(
            self,
            agentname=None,
            monthdate=None,
            BillAudit=1,
            Entname=None,
            Operator=None):
        """
        # 查询月薪账单
        :param agentname: 来源名称，可选，默认None
        :param monthdate: 所属月份，可选，默认None
        :param EndDt:预支周期结束日期，可选，默认None
        :param BillAudit:账单审核状态，可选，默认1：待审核，2已审核，3审核不通过
        :param Entname: 标准企业名称，可选，默认None
        :param Operator:
        :return:
        """

        if monthdate is None:
            monthdate = self.monthdate

        if Entname is not None:
            self.get_ent(Entname)
            EntId = self.entid
        else:
            EntId = None

        if Operator is None:
            Operator = self.Name

        if agentname is None:
            SrceSpId = -9999
        else:
            SrceSpId = self.get_agent(agentname)

        req = self.login.create_api(MonthBill_select,
                                    BillRelatedMoStart='',
                                    BillRelatedMoEnd='',
                                    BillMonthlyBatchId=-9999,
                                    EntId=-9999,
                                    TrgtSpId=-9999,
                                    TrgtSpAuditSts=-9999,
                                    BillSrce=-9999,
                                    SalaryTyp=-9999,
                                    SalaryPayer=-9999,
                                    Operator='',
                                    RecordIndex=0,
                                    RecordSize=10)
        print(req)
        print(req.json())
        self.billid = req.json()['Data']['RecordList'][0]['BillMonthlyBatchId']
        return self.billid

    def audit_monthbill(self, agentname, status=1):
        """
        审核月薪订单
        :param agentname: 来源名称，必填
        :param status: 审核状态，可选，默认 1：审核通过，2：审核不通过
        :return:
        """
        req = {}
        billid = self.select_monthbill(agentname=agentname)
        if status == 1:
            req = self.login.create_api(
                MonthBill_Confirm, BillMonthlyBatchId=billid)
        elif status == 2:
            req = self.login.create_api(
                MonthBill_Confirm, BillMonthlyBatchId=billid)
        result = req.json()['Desc']
        return result
