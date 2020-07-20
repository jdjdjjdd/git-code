#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : Present_Remit.py
# @Author   : yht
# @Date     : 2020/05/11
# @Update   :
# @Desc     : 通用服务


from common.lib.venv.api_path_zt import *


class PresentRemit:

    def __init__(self, login=None):
        self.login = login

    def RemitSettleList(self, prefix=None, StartDt=None, EndDt=None, BatchNum=None, EntId=None, SalaryTyp=None,
                        PayType=None, AuditSts=None, RecordIndex=None, RecordSize=None):
        """
        薪资结算单查询页面查询数据
        :param prefix:
        :param StartDt:string //开始日期
        :param EndDt:string //结束日期
        :param BatchNum:string //对账单批次号
        :param EntId: int64  // 标准企业Id
        :param EntName:string //标准企业全称
        :param EntShortName:string //新增企业名简称
        :param SalaryTyp:int64  //-9999全部1 月薪 2周薪 3返费
        :param PayType:int64  //-9999全部 提交申请状态，1：代发垫发 2：线下打款
        :param AuditSts:int64  //-9999全部 代发垫发状态，1:通过，2:不通过
        :param RecordIndex:int64  //分页
        :param RecordSize:int64  //第几页
        :return:
        """
        res = self.login.create_api(url=RemitSettleList,
                                    prefix=prefix,
                                    StartDt=StartDt,
                                    EndDt=EndDt,
                                    BatchNum=BatchNum,
                                    EntId=EntId,
                                    SalaryTyp=SalaryTyp,
                                    PayType=PayType,
                                    AuditSts=AuditSts,
                                    RecordIndex=RecordIndex,
                                    RecordSize=RecordSize
                                    )
        res = res.json()
        return res

    def SetPayType(self, PayType=None, RemitAppIds: list = None):
        """
        薪资结算单查询页面设置放款方式
        :param PayType:int64 //1：代发垫发 2：线下打款
        :param RemitAppIds:[]int64
        :return:
        """
        res = self.login.create_api(url=SetPayType, PayType=PayType, RemitAppIds=RemitAppIds)

        res = res.json
        return res

    def RemitSettleDetailListV2(self, RealName=None, IDCardNum=None, TransferSts=None, BillRelatedMo=None,
                                RecordIndex=None, RecordSize=None, BillBatchId=None, TransactionId=None, EntId=None,
                                BillBatchType=None, PayType=None, StartDt=None, EndDt=None, ):
        """
        薪资结算单明细查询
        :param RealName:string //姓名
        :param IDCardNum:string //身份证
        :param TransferSts:int64  //打款状态 0 未打款，1  打款成功  2 打款失败
        :param BillRelatedMo:string //归属月份
        :param RecordIndex:int64  //第几页
        :param RecordSize:int64  //分页
        :param BillBatchId:int64  //批次号
        :param TransactionId:string //业务id
        :param EntId:int64  //标准企业
        :param BillBatchType:int64  //薪资发放类型  全部-9999 1月批次2周批次3返费4周返费
        :param PayType:int64  //打款方式 -9999全部 1：代发垫发2：线下打款
        :param StartDt:string //开始日期
        :param EndDt:string //结束日期
        :return:
        """
        res = self.login.create_api(url=RemitSettleDetailListV2,
                                    RealName=RealName,
                                    IDCardNum=IDCardNum,
                                    TransferSts=TransferSts,
                                    BillRelatedMo=BillRelatedMo,
                                    RecordIndex=RecordIndex,
                                    RecordSize=RecordSize,
                                    BillBatchId=BillBatchId,
                                    TransactionId=TransactionId,
                                    EntId=EntId,
                                    BillBatchType=BillBatchType,
                                    PayType=PayType,
                                    StartDt=StartDt,
                                    EndDt=EndDt
                                    )
        res = res.json()
        return res

    def SetTransferSts(self, RemitAppDetailId: list = None, TransferSts=None, Reason=None):
        """
        设置打款状态
        :param RemitAppDetailId:
        :param TransferSts:
        :param Reason:
        :return:
        """
        res = self.login.create_api(url=SetTransferSts,
                                    RemitAppDetailId=RemitAppDetailId,
                                    TransferSts=TransferSts,
                                    Reason=Reason)
        res = res.json
        return res

    def ExportRemitSettleDetailListV2(self, RecordSize=None, RecordIndex=None, BillBatchId=None, TransactionId=None,
                                      RealName=None, IDCardNum=None, TransferSts=None, EntId=None, BillBatchType=None,
                                      PayType=None, StartDt=None, EndDt=None, BillRelatedMo=None, ):
        """
        薪资结算单明细查询导出V2
        :param RecordSize:int64  //分页
        :param RecordIndex:int64  //第几页
        :param BillBatchId:int64  //批次号
        :param TransactionId:string //业务id
        :param RealName:string //姓名
        :param IDCardNum:string //身份证
        :param TransferSts:int64  //打款状态 0 未打款，1  打款成功  2 打款失败
        :param EntId:int64  //标准企业
        :param BillBatchType:int64  //薪资发放类型  全部-9999 1月批次2周批次3返费4周返费
        :param PayType:int64  //打款方式 -9999全部 1：代发垫发2：线下打款
        :param StartDt:string //开始日期
        :param EndDt:string //结束日期
        :param BillRelatedMo:归属月份
        :return:
        """
        res = self.login.create_api(url=ExportRemitSettleDetailListV2,
                                    RecordSize=RecordSize,
                                    RecordIndex=RecordIndex,
                                    BillBatchId=BillBatchId,
                                    TransactionId=TransactionId,
                                    RealName=RealName,
                                    IDCardNum=IDCardNum,
                                    TransferSts=TransferSts,
                                    EntId=EntId,
                                    BillBatchType=BillBatchType,
                                    PayType=PayType,
                                    StartDt=StartDt,
                                    EndDt=EndDt,
                                    BillRelatedMo=BillRelatedMo
                                    )
        res = res.json()
        return res

    def RemitSettleDetailList(self, BillBatchId=None, TransactionId=None, RealName=None, IDCardNum=None,
                              TransferSts=None, RecordSize=None, RecordIndex=None):
        """
        发款明细
        :param BillBatchId:int64  //
        :param TransactionId:string //业务id
        :param RealName:string //姓名
        :param IDCardNum:string //身份证
        :param TransferSts:int64  //打款状态，1 未打款，2 打款中 3 打款成功 4 打款失败
        :param RecordSize:int64  //分页
        :param RecordIndex:int64  //第几页
        :return:
        """
        res = self.login.create_api(url=RemitSettleDetailList,
                               BillBatchId=BillBatchId,
                               TransactionId=TransactionId,
                               RealName=RealName,
                               IDCardNum=IDCardNum,
                               TransferSts=TransferSts,
                               RecordSize=RecordSize,
                               RecordIndex=RecordIndex
                               )
        res = res.json()
        return res

    def GetUserTradeList(self,RecordIndex=None,RcrtOrderReturnFeeId=None,RecordSize=None):
        """
        到账明细
        :param RecordIndex:int64 //第几页
        :param RcrtOrderReturnFeeId:int64 //详情主键ID
        :param RecordSize:int64 //分页
        :return:
        """
        res = self.login.create_api(url=GetUserTradeList,
                               RecordIndex=RecordIndex,
                               RcrtOrderReturnFeeId=RcrtOrderReturnFeeId,
                               RecordSize=RecordSize
                               )
        res = res.json()
        return res

    def GetUserTradeDetail(self,RecordID=None):
        """
        到账明细详情
        :param RecordID:int64
        :return:
        """
        res = self.login.create_api(url=GetUserTradeDetail,RecordID=RecordID)
        res = res.json()
        return res
