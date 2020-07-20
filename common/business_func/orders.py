#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : orders.py
# @Author   : yht
# @Date     : 2020/02/23
# @Desc     : 公共方法


from common.base_utils.comm_utils import get_api_result
from common.venv.api_path_mb import *
from common.venv.api_path_zt import *
from common.venv.var import *


class Order():

    def __init__(self,login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login
        self.orderid = None
        self.entbrorrowname = None
        self.entbrorrowid = None
        self.TargetSpId = None
        self.SpName = ''
        self.SettlementTyp = 2

    def get_query_agent(self):
        """获取可预支订单供应商查询项数据"""
        res = self.login.create_api(GetCoopListWithDirection, Direction=1)
        return res

    def get_entbrorrow(self, entbrorrowname=''):
        """
        # 获取招聘、派遣端创建时需要的企业
        :param entbrorrowname: 企业名称，可选，默认为空
        :return:
        """
        res = self.login.create_api(GetEntBorrowByUserType).json()
        entbrorrows = res['Data']['RecordList']
        # 遍历列表寻找指定名称的id，找到id后赋值给SpEntID，没找到传入的名称抛出异常
        for entbrorrow in entbrorrows:
            if entbrorrowname == entbrorrow['EntBorrowName']:
                self.entbrorrowid = entbrorrow['EntBorrowId']
                self.entbrorrowname = entbrorrowname
                break
        # if self.entbrorrowid:
        #     logger.info(f'获取企业：{self.entbrorrowname},{self.entbrorrowid}')
        # else:
        #     logger.error(f'没有找到企业{entbrorrowname}')
        #     raise Exception

    def get_labor(self, LaborName=''):
        """
        # 获取招聘、派遣端创建订单时需要的去向
        :param url: 调用获取去向劳务的接口地址，必填
        :param LaborName: 去向劳务，可选，默认为空
        :return:
        """
        api_result = self.login.create_api(get_vlabor)
        labors = api_result.json()['Data']['RecordList']
        # 遍历列表寻找指定名称的id，找到id后赋值给TargetSpId，没找到传入的名称抛出异常
        for labor in labors:
            if LaborName in labor['SpShortName']:
                self.TargetSpId = labor['SpId']
                self.SpName = LaborName
                break

    def get_agent(self, agentname=None, orderid=None):
        """
        获取派遣端订单分配的供应商列表
        :param agentname:
        :param orderid:
        :return:
        """
        if agentname:
            res = self.login.create_api(GetZXXOrderReceiveCoop, OrderId=orderid)
            tags = res.json()['Data']['RecordList']
            for tag in tags:
                agents = tag['CoopList']
                for agent in agents:
                    if agentname == agent['CoopName']:
                        self.CoopId = agent['CoopId']
                        self.ZtVSpId = agent['ZtVSpId']
                        self.status = agent['Status']
                        break
        else:
            res = self.login.create_api(GetZXXOrderReceiveCoop, OrderId=orderid).json()
            return res

    def create_order_pq(self, entbrorrowname, ReceiverType=1, SettlementTyp=None, OrderTyp=2, OrderChargeTyp=6,
                        OrderDt=nowtime, BeginDt=nowtime,
                        EndDt='', PriceUnit=None):
        """
        派遣端创建订单
        :param entbrorrowname: 企业，必选
        :param ReceiverType:订单发单类型，1 门店订单，2 供应商订单
        :param OrderTyp:订单类型 1 返费订单，2 周薪订单
        :param SettlementTyp: 订单结算方式 1:ZX结算方式 2:Z结算方式 3:ZA结算方式 4：ZX-A
        :param OrderChargeTyp:订单类型 默认6  5 一周收费5天 6 一周收费6天
        :param OrderDt:订单时间（报价日期）
        :param BeginDt:订单有效期限开始日期
        :param EndDt:订单有效期限结束日期
        :param PriceUnit:供应商订单参数，1 按天算服务费，2 按小时算服务费
        :return:
        """
        # 加载企业
        self.get_entbrorrow(entbrorrowname)
        if SettlementTyp:
            self.SettlementTyp = SettlementTyp
        # 会员相关费用
        OrderWeekFeeList = [
            {"BeginDt": BeginDt, 'EndDt': EndDt, 'TerminateTyp': 2, 'AdvancePayAmt': 10000, 'Remark': '工资说明',
             'AcpHourlyWorkAmt': 2000, 'AcpLeavedHourlyWorkAmt': 2000, 'HourlyWorkAmt': 2000,
             'LeavedHourlyWorkAmt': 2000}]
        # 中介费
        if PriceUnit==2:  # 供应商政策按小时结算
            OrderAgencyFee = [
                {'AgentFee': 1000, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        else:
            OrderAgencyFee = [
                {'MinDays': 1, 'MaxDays': 0, 'AgentFee': 1000, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''},
                {'DaysNoMoney': 7, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        # 服务费
        OrderServiceFee = [{'PlatformSrvcFee': 0, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        # 返费
        OrderReturnFee = [{'Days': 10, 'FeeTyp': 3, 'ReturnTyp': 2, 'ReturnFee': 5000},
                          {'Days': 20, 'FeeTyp': 3, 'ReturnTyp': 1, 'ReturnFee': 1000}]
        # 获取劳务ID、name
        res = self.login.create_api(get_vlabor).json()
        TargetSpId = int(get_api_result(res, 'SpId')[0])
        SpName = get_api_result(res, 'SpShortName')[0]
        # 调用接口创建订单
        res = self.login.create_api(CreateZXXNewOrder, OrderTyp=OrderTyp, HasReturnFee=0, SettlementTyp=SettlementTyp,
                                     EmploymentTyp=1,
                                     ReceiverType=ReceiverType, SpQuota=20, InsideRemark='企业政策', OrderDt=OrderDt,
                                     EntId=self.entbrorrowid,
                                     SpEntName=entbrorrowname, TrgtSpId=TargetSpId, TrgtSpName=SpName,
                                     OrderChargeTyp=OrderChargeTyp, OrderWeekFeeList=OrderWeekFeeList,
                                     OrderAgencyFee=OrderAgencyFee, OrderServiceFee=OrderServiceFee,
                                     OrderReturnFee=OrderReturnFee, Remark='供应商备注', PriceUnit=PriceUnit)
        self.orderid = res.json()['Data']
        return res.json()

    def create_order_pq_mult(self, entbrorrowname, HasReturnFee=0, ReceiverType=2, EmploymentTyp=1, SettlementTyp=2,
                             OrderTyp=2, OrderChargeTyp=None, OrderDt=nowtime, BeginDt=nowtime,
                             HasDiffPrice=0, DiffPriceIssueDt=None, AdditionalSubsidy=0, SubsidyMoney=None,
                             EnjoyStart=None, EnjoyEnd=None, InWorkDay=None, IssueDay=None,
                             EndDt='', PriceUnit=None):
        """
        派遣端创建多模式订单
        :param entbrorrowname: 企业，必选
        :param HasReturnFee:是否有会员返费，0 无返费，1 劳务返费，2 平台返费
        :param ReceiverType:订单发单类型，1 门店订单，2 供应商订单
        :param EmploymentTyp: 用工方式，1 劳务用工，2 灵活用工
        :param OrderTyp:订单类型 1 返费订单，2 周薪订单
        :param SettlementTyp: 订单结算方式 1:ZX结算方式 2:Z结算方式 3:ZA结算方式 4：ZX-A
        :param OrderChargeTyp:订单类型 默认6  5 一周收费5天 6 一周收费6天
        :param OrderDt:订单时间（报价日期）
        :param BeginDt:订单有效期限开始日期
        :param EndDt:订单有效期限结束日期
        :param HasDiffPrice:是否有差价，1 无差价，2 有差价
        :param DiffPriceIssueDt:差价发放日期，限制整形
        :param AdditionalSubsidy:是否有补贴，0 无补贴，1 有补贴
        :param SubsidyMoney:补贴金额(元/小时) 限制整形
        :param EnjoyStart：享受周期开始时间
        :param EnjoyEnd：享受周期结束时间
        :param IssueDay：补贴发放会员的日期
        :param InWorkDay：补贴发放要求会员在职日期
        :param PriceUnit:供应商订单参数，1 按天算服务费，2 按小时算服务费
        :return:
        """
        # 加载企业
        self.get_entbrorrow(entbrorrowname)
        # 周薪天数
        orderChargeTyp = 6 if SettlementTyp in (1, 2) else OrderChargeTyp

        # 会员相关费用
        if SettlementTyp in (1, 2):
            OrderWeekFeeList = [
                {"BeginDt": BeginDt, 'EndDt': EndDt, 'TerminateTyp': 2, 'AdvancePayAmt': 10000, 'Remark': '工资说明',
                 'AcpHourlyWorkAmt': 2000, 'AcpLeavedHourlyWorkAmt': 2000, 'HourlyWorkAmt': 2000,
                 'LeavedHourlyWorkAmt': 2000}]
        elif SettlementTyp in (3, 6):
            OrderWeekFeeList = [
                {"BeginDt": BeginDt, 'EndDt': EndDt, 'TerminateTyp': 2, 'Remark': '工资说明',
                 'AcpHourlyWorkAmt': 2000, 'AcpLeavedHourlyWorkAmt': 2000, 'HourlyWorkAmt': 2000,
                 'LeavedHourlyWorkAmt': 2000}]
        # 中介费
        if PriceUnit==2:  # 供应商政策按小时结算
            OrderAgencyFee = [
                {'AgentFee': 1000, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        else:
            OrderAgencyFee = [
                {'MinDays': 1, 'MaxDays': 0, 'AgentFee': 1000, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''},
                {'DaysNoMoney': 7, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        # 服务费
        OrderServiceFee = [{'PlatformSrvcFee': 0, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        # 返费
        if HasReturnFee: # 有会员返费
            OrderReturnFee = [{'Days': 10, 'FeeTyp': 3, 'ReturnTyp': 2, 'ReturnFee': 5000},
                            {'Days': 20, 'FeeTyp': 3, 'ReturnTyp': 1, 'ReturnFee': 10000},
                              {'Days': 30, 'FeeTyp': 3, 'ReturnTyp': 3, 'ReturnFee': 10000}
                              ]
        else:# 无会员返费，只有供应商返费
            OrderReturnFee = [
                              {'Days': 30, 'FeeTyp': 3, 'ReturnTyp': 3, 'ReturnFee': 10000}
                              ]
        # 获取劳务ID、name
        res = self.login.create_api(get_vlabor).json()
        TargetSpId = int(get_api_result(res, 'SpId')[0])
        SpName = get_api_result(res, 'SpShortName')[0]
        # 调用接口创建订单
        res = self.login.create_api(add_order_mult,
                                    OrderTyp=OrderTyp,
                                    HasReturnFee=HasReturnFee,
                                    SettlementTyp=SettlementTyp,
                                    EmploymentTyp=EmploymentTyp,
                                    ReceiverType=ReceiverType,
                                    SpQuota=20,
                                    InsideRemark='企业政策',
                                    OrderDt=OrderDt,
                                    EntId=self.entbrorrowid,
                                    HasDiffPrice=HasDiffPrice,
                                    DiffPriceIssueDt=DiffPriceIssueDt,
                                    AdditionalSubsidy=AdditionalSubsidy,
                                    SubsidyMoney=SubsidyMoney,
                                    EnjoyStart=EnjoyStart,
                                    EnjoyEnd=EnjoyEnd,
                                    InWorkDay=InWorkDay,
                                    IssueDay=IssueDay,
                                    SpEntName=entbrorrowname,
                                    TrgtSpId=TargetSpId,
                                    TrgtSpName=SpName,
                                    OrderChargeTyp=orderChargeTyp,
                                    OrderWeekFeeList=OrderWeekFeeList,
                                    OrderAgencyFee=OrderAgencyFee,
                                    OrderServiceFee=OrderServiceFee,
                                    OrderReturnFee=OrderReturnFee,
                                    Remark='供应商备注',
                                    PriceUnit=PriceUnit)
        self.orderid = res.json()['Data']
        return res.json()

    def create_order_zp(self, entbrorrowname, OrderDt=nowtime, LaborName='', BeginDt=nowtime, EndDt='',
                        OrderChargeTyp=6):
        # 加载企业
        self.get_entbrorrow(entbrorrowname)
        # 加载劳务
        self.get_labor(LaborName)
        # 会员相关费用
        OrderWeekFeeList = [
            {"BeginDt": BeginDt, 'EndDt': EndDt, 'TerminateTyp': 2, 'AdvancePayAmt': 10000, 'Remark': '工资说明',
             'AcpHourlyWorkAmt': 2000, 'AcpLeavedHourlyWorkAmt': 2000, 'HourlyWorkAmt': 2000,
             'LeavedHourlyWorkAmt': 2000}]
        # 中介费
        OrderAgencyFee = [
            {'MinDays': 1, 'MaxDays': 0, 'AgentFee': 1000, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''},
            {'DaysNoMoney': 7, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        # 服务费
        OrderServiceFee = [{'PlatformSrvcFee': 0, 'TerminateTyp': 2, 'BeginDt': BeginDt, 'EndDt': ''}]
        # 返费
        OrderReturnFee = [{'Days': 10, 'FeeTyp': 3, 'ReturnTyp': 2, 'ReturnFee': 5000},
                          {'Days': 20, 'FeeTyp': 3, 'ReturnTyp': 1, 'ReturnFee': 1000}]
        # 调用接口创建订单
        api_result = self.login.create_api(CreateZXXNewOrder,
                                     OrderTyp=2,
                                     HasReturnFee=0,
                                     SettlementTyp=1,
                                     EmploymentTyp=1,
                                     SpQuota=233,
                                     InsideRemark='企业政策',
                                     OrderDt=OrderDt,
                                     EntId=self.entbrorrowid,
                                     SpEntName=entbrorrowname,
                                     TrgtSpId=self.TargetSpId,
                                     TrgtSpName=LaborName,
                                     OrderChargeTyp=OrderChargeTyp,
                                     OrderWeekFeeList=OrderWeekFeeList,
                                     OrderAgencyFee=OrderAgencyFee,
                                     OrderServiceFee=OrderServiceFee,
                                     OrderReturnFee=OrderReturnFee,
                                     Remark='备注')
        orderid = api_result.json()['Data']
        return orderid

    # 审核订单
    def Judge_Order(self, auditsts, orderid=None, remark=None, ordertyp=2):
        """
        审核订单
        :param auditsts: 审核状态，2为审核通过，3为审核不通过
        :param orderid: 审核的订单id
        :param remark:  审核备注，默认为空
        :param ordertyp:  订单类型1为返费，2为周薪
        :return:
        """
        # 调用审核订单接口
        res = self.login.create_api(JudgeOrder,
                              JudgeStatus=auditsts,
                              Remark=remark,
                              OrderId=orderid,
                              OrderTyp=ordertyp)
        response = res.json()
        return response

    # 订单分配门店
    def Edit_Order_Store(self, mainorderid, tenanttyp, storeidlist, shopmgrfee=3, shopuserfee=35):
        """
        招聘端订单分配门店
        :param mainorderid: 订单main_id
        :param tenanttyp: 订单类型1为招聘，2为派遣
        :param storeidlist:  门店id列表
        :param shopmgrfee:  店长提成比例
        :param shopuserfee:  店员提成比例
        :return:
        """
        res = self.login.create_api(Edit_OrderStoreList_api,
                              TenantType=tenanttyp,
                              RcrtMainOrderId=mainorderid,
                              StoreInfos=[{"ShopMgrFeeRate": shopmgrfee, "ShopUsrFeeRate": shopuserfee,
                                           "DistributedStoreIds": storeidlist}])
        response = res.json()
        return response

    def publishOrderToSupplier(self, agentname, OrderId=None, *args):
        """
        派遣端订单分配
        :param agentname:来源名称
        :param OrderId:订单编号
        :param args:
        :return:
        """
        SpIds = []
        self.get_agent(agentname=agentname, orderid=OrderId)
        SpIds.append(self.ZtVSpId)
        if not OrderId:
            OrderId = self.orderid
        res = self.login.create_api(PublishOrderToSupplier, OrderId=OrderId, SpIds=SpIds)
        return res.json()

    def get_orders(self, StartDate=nowtime, EndDate=nowtime, OrderStatus=-9999, CreatedBy=-9999, agentname=None,
                   EntName=None,RecordSize=10):
        """
        获取派遣端订单列表
        :param StartDate:
        :param EndDate:
        :param OrderStatus:
        :param CreatedBy:
        :param agentname:
        :param EntName:
        :param RecordSize:
        :return:
        """
        agentid = None
        if agentname:
            res_ = self.get_query_agent()
            agents = res_.json()['Data']['RecordList']
            for agent in agents:
                if agentname == agent['SpShortName']:
                    agentid = agent['ZtVspId']
        else:
            agentid = -9999

        result = self.login.create_api(QuerySendZXXOrderList, StartDate=StartDate, EndDate=EndDate, OrderStatus=OrderStatus,
                              SettlementTyp=2, EmploymentTyp=1,
                              CreatedBy=CreatedBy, SuppierId=agentid, EntName=EntName, RecordIndex=0, RecordSize=RecordSize)
        res = result.json()
        return res


