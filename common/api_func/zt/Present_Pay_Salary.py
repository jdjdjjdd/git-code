#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : Present_Comm.py
# @Author   : yht
# @Date     : 2020/05/12
# @Update   :
# @Desc     : 通用服务


from common.lib.venv.api_path_zt import *


class PresentPaySalary:

    def __init__(self, login=None):
        self.login = login

    def GetPayAuditListV2(
            self,
            PaymentNum=None,
            EntId=None,
            SalaryType=None,
            RecordSize=None,
            RecordIndex=None,
            CreatedStartTm=None,
            CreatedEndTm=None,
            AuditSts=None):
        """
        发薪审核列表V2
        :param PaymentNum:string
        :param EntId:int64 //标准企业ID
        :param SalaryType:int64 //0全部 1日薪 2周薪 3月薪
        :param RecordSize:int64 //分页
        :param RecordIndex:int64 //第几页
        :param CreatedStartTm:string //发起发款审核时间
        :param CreatedEndTm:string //发起发款审核时间
        :param AuditSts:int64 //0全部 1未审核  2已通过  3已拒绝
        :return:
        """
        res = self.login.create_api(url=GetPayAuditListV2,
                                    PaymentNum=PaymentNum,
                                    EntId=EntId,
                                    SalaryType=SalaryType,
                                    RecordSize=RecordSize,
                                    RecordIndex=RecordIndex,
                                    CreatedStartTm=CreatedStartTm,
                                    CreatedEndTm=CreatedEndTm,
                                    AuditSts=AuditSts
                                    )
        return res

    # 已作废
    def AuditPaySalary(
            self,
            SettleIds: list = None,
            AuditSts=None,
            Remark=None):
        """
        发款审核
        :param SettleIds:[]int64
        :param AuditSts:int64 //1通过 2不通过
        :param Remark:string
        :return:
        """
        res = self.login.create_api(url=AuditPaySalary,
                                    SettleIds=SettleIds,
                                    AuditSts=AuditSts,
                                    Remark=Remark
                                    )
        return res

    def GetSettleHandleListV2(
            self,
            SettleBatchNum=None,
            ApplySts=None,
            EntId=None,
            CreatedStartTm=None,
            CreatedEndTm=None,
            SalaryType=None,
            SettleType=None,
            AuditSts=None,
            AuditStartTm=None,
            AuditEndTm=None,
            RecordSize=None,
            RecordIndex=None):
        """
        发款处理V2
        :param SettleBatchNum:string
        :param ApplySts:int64
        :param EntId:int64
        :param CreatedStartTm:string
        :param CreatedEndTm:string
        :param SalaryType:int64 //薪资类型 1月薪 2周薪 3日薪 4返费 5保险 6其他
        :param SettleType:int64 //1代发 2垫发
        :param AuditSts:int64 //审核状态筛选 -9999 全部  审核状态，1未审核  2已通过  3已拒绝
        :param AuditStartTm:string
        :param AuditEndTm:string
        :param RecordSize:int64
        :param RecordIndex:int64
        :return:
        """
        res = self.login.create_api(url=GetSettleHandleListV2,
                                    SettleBatchNum=SettleBatchNum,
                                    ApplySts=ApplySts,
                                    EntId=EntId,
                                    CreatedStartTm=CreatedStartTm,
                                    CreatedEndTm=CreatedEndTm,
                                    SalaryType=SalaryType,
                                    SettleType=SettleType,
                                    AuditSts=AuditSts,
                                    AuditStartTm=AuditStartTm,
                                    AuditEndTm=AuditEndTm,
                                    RecordSize=RecordSize,
                                    RecordIndex=RecordIndex
                                    )
        return res

    # 已作废
    def CommitPaySalary(self, SettleIds: list = None):
        """
        一键代发
        :param SettleIds:[]int64
        :return:
        """
        res = self.login.create_api(url=CommitPaySalary, SettleIds=SettleIds)
        return res

    # 已作废
    def CommitPayPad(self, SettleId=None, EntPayDate=None, PadAmt=None):
        """
        申请垫发
        :param SettleId:int64
        :param EntPayDate:string
        :param PadAmt:int64 //垫发金额（分）
        :return:
        """
        res = self.login.create_api(
            url=CommitPayPad,
            SettleId=SettleId,
            EntPayDate=EntPayDate,
            PadAmt=PadAmt)
        return res

    def AuditPaySalaryV2(
            self,
            SettleIds: list = None,
            AuditSts=None,
            Remark=None):
        """
        发款审核V2
        :param SettleIds:[]int64
        :param AuditSts:int64 //1通过 2不通过
        :param Remark:string
        :return:
        """
        res = self.login.create_api(
            url=AuditPaySalaryV2,
            SettleIds=SettleIds,
            AuditSts=AuditSts,
            Remark=Remark)
        return res

    def CommitPaySalaryV2(self, SettleIds: list = None):
        """
        一键代发V2
        :param SettleIds:[]int64
        :return:
        """
        res = self.login.create_api(url=CommitPaySalaryV2, SettleIds=SettleIds)
        return res

    def CommitPayPadV2(self, SettleId=None, EntPayDate=None, PadAmt=None):
        """
        申请垫发V2
        :param SettleId:int64
        :param EntPayDate:string
        :param PadAmt:int64 //垫发金额（分）
        :return:
        """
        res = self.login.create_api(
            url=CommitPayPadV2,
            SettleId=SettleId,
            EntPayDate=EntPayDate,
            PadAmt=PadAmt)
        return res

    def GetLaborBalance(self, TId=None):
        """
        劳务余额
        :param TId:string
        :return:
        """
        res = self.login.create_api(url=GetLaborBalance, TId=TId)
        return res

    # 已作废
    def GetAuthPayList(
            self,
            PaymentNum=None,
            TenantName=None,
            EntName=None,
            SalaryType=None,
            AuthSts=None,
            RecordSize=None,
            RecordIndex=None):
        """
        授权列表
        :param PaymentNum:string //批次号
        :param TenantName:string //劳务公司
        :param EntName:string //企业名
        :param SalaryType:int64  //薪资类型
        :param AuthSts:int64  //授权类型
        :param RecordSize:int64
        :param RecordIndex:int64
        :return:
        """
        res = self.login.create_api(url=GetAuthPayList,
                                    PaymentNum=PaymentNum,
                                    TenantName=TenantName,
                                    EntName=EntName,
                                    SalaryType=SalaryType,
                                    AuthSts=AuthSts,
                                    RecordSize=RecordSize,
                                    RecordIndex=RecordIndex
                                    )
        return res

    def GetAuthPayListV2(
            self,
            PaymentNum=None,
            TenantName=None,
            EntName=None,
            SalaryType=None,
            AuthSts=None,
            RecordSize=None,
            RecordIndex=None):
        """
        授权列表V2
        :param PaymentNum:string //批次号
        :param TenantName:string //劳务公司
        :param EntName:string //企业名
        :param SalaryType:int64  //薪资类型
        :param AuthSts:int64  //授权类型
        :param RecordSize:int64
        :param RecordIndex:int64
        :return:
        """
        res = self.login.create_api(url=GetAuthPayListV2,
                                    PaymentNum=PaymentNum,
                                    TenantName=TenantName,
                                    EntName=EntName,
                                    SalaryType=SalaryType,
                                    AuthSts=AuthSts,
                                    RecordSize=RecordSize,
                                    RecordIndex=RecordIndex
                                    )
        return res

    def CommitAuthPay(self, RecvSettleId=None, AuthSts=None, TId=None):
        """
        授权打款
        :param RecvSettleId:int64 //批次号
        :param AuthSts:int64 //1未授权  2已授权  3已拒绝
        :param TId:string
        :return:
        """
        res = self.login.create_api(url=CommitAuthPay,
                                    RecvSettleId=RecvSettleId,
                                    AuthSts=AuthSts,
                                    TId=TId
                                    )
        return res