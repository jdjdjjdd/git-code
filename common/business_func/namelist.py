#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : namelist.py
# @Author   : yht
# @Date     : 2020/02/23
# @Update   : 日期加名称
# @Desc     : 公共方法


from common.base_utils.comm_utils import get_api_result, create_name, create_IDCard, create_phone
from common.base_utils.comm_utils import get_value
from common.venv.api_path_mb import *
from common.venv.api_path_zt import *
from common.venv.var import *


# from common.base_utils.comm_utils import
# from common.module_tools.LogHandler import logger


class NameList():
    """
    名单类，定义一些关于名单操作的函数，包括招聘端、派遣端
    """

    def __init__(self, login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login
        # 初始化一些重要变量
        self.newnameid_pq = None  # 派遣端新录入名单的namelistid
        self.newname_pq = ''  # 派遣端新录入名单姓名
        self.newidnum_pq = ''  # 派遣端新录入名单身份证号码
        self.newmobile_pq = ''  # 派遣端新录入名单手机号码
        self.entid_pq = None  # 派遣端标准企业id
        self.newnameid_zp = None  # 招聘端新录入名单的namelistid
        self.newnamelistperformanceid = None  # 招聘端新录入名单模板绩效名单主键id
        self.newname_zq = ''  # 招聘端新录入名单姓名
        self.newidnum_zp = ''  # 招聘端新录入名单身份证号码
        self.newmobile_zp = ''  # 招聘端新录入名单手机号码
        self.TargetSpId = None  # 去向id
        self.SpName = None  # 去向名称
        self.entbrorrowid = None  # 企业id
        self.FromSpID = None  # 来源id
        self.status_code = None  # 接口调用的状态码
        self.code = None  # 接口返回的状态码
        self.desc = ''  # 接口返回的描述

    def get_business_interview_list(self, membername='', memberidcardnum='', startdate=nowtime, enddate=nowtime,
                                    InterviewState=-999, IsBindOrder=-999):
        """
        # 获取招聘端面试名单（商务）名单列表
        :param membername: 会员姓名，可选，默认为空
        :param memberidcardnum: 会员身份证号，可选，默认为空
        :param startdate: 面试日期前区间，可选，默认当天日期
        :param enddate: 面试日期后区间，可选，默认为当天日期
        :param InterviewState: 面试状态，可选，默认为全部
        :param IsBindOrder: 是否绑单，可选，默认全部
        :return:
        """
        # 调用获取招聘端面试名单（商务）名单列表接口
        api_result = self.login.create_api(GetBusinessInterviewList, StartDate=startdate, EndDate=enddate,
                                           InterviewState=InterviewState,
                                           MemberName=membername, MemberIDCardNum=memberidcardnum,
                                           IsBindOrder=IsBindOrder,
                                           RecordIndex=0, RecordSize=999)

        namelists = api_result.json()['Data']['RecordList']
        # 返回名单列表
        return namelists

    def get_nameList(self, StartTime=nowtime, EndTime=nowtime, Name=None, IDCardNum=None, Mobile=None, Gender=None,
                     InterviewStatus=9999, RecordSize=10, RecordIndex=0,
                     FromBindStatus=-9999, SpEntName=None, RcrtTyp=-9999, agentname=None, ScannerMobile=None,
                     ScannerUserID=None, CheckType=None):
        """
        # 获取派遣端实接记录列表
        :param starttime: 面试日期前区间，可选，默认为当天日期
        :param endtime: 面试日期后区间，可选，默认为当天日期
        :param name: 会员名称，可选，默认为None
        :param idcardnum: 身份证号，可选，默认为None
        :param mobile: 手机号码，可选，默认为None
        :param Gender: 性别，可选，1 男，2 女，默认为None
        :param InterviewStatus:面试状态，可选，0:未处理，1：未面试，2：面试通过，3：面试不通过，4：放弃
        :param FromBindStatus:绑单状态，可选，1 未绑， 2 已绑
        :param SpEntName:企业名称，可选
        :param RcrtTyp:企业类型，可选，1 预支，2 返费
        :param agentname:来源名称，可选
        :param ScannerMobile:扫描人手机号码，可选
        :param ScannerUserID:扫描人guid，可选
        :return:
        """
        if agentname == None:
            FromSpId = None
        else:
            FromSpId = self.get_source(FromSpName=agentname)
        # 调用获取派遣端实接记录列表接口
        res = self.login.create_api(GetNameList,
                                    StartTime=StartTime,
                                    EndTime=EndTime,
                                    Name=Name,
                                    IDCardNum=IDCardNum,
                                    InterviewStatus=InterviewStatus,
                                    Gender=Gender,
                                    Mobile=Mobile,
                                    RcrtTyp=RcrtTyp,
                                    FromBindStatus=-FromBindStatus,
                                    ScannerMobile=ScannerMobile,
                                    ScannerUserID=ScannerUserID,
                                    CheckType=CheckType,
                                    RecordIndex=RecordIndex,
                                    RecordSize=RecordSize,
                                    SpEntName=SpEntName,
                                    FromSpId=FromSpId,
                                    SpIDs=[22699])
        res = res.json()
        self.getnamelists = res['Data']['RecordList']
        self.getnameidlist = get_api_result(res, 'NameID')
        self.getMobilelist = get_api_result(res, 'Mobile')
        self.getidcardlist = get_api_result(res, 'IDCardNum')
        self.getrealnamelist = get_api_result(res, 'Name')
        self.getentlist = get_api_result(res, 'EntShortName')
        # 打印日志
        # logger.info('查询名单，查询结果:{}'.format(res.json()))
        return res

    def get_ent(self, entname, CoopSts=1):
        """
        获取标准企业
        :param entname: 标准企业名称,必填
        :param CoopSts: 合作状态，0 全部，1 合作中，2 不合作
        :return:
        """
        res = self.login.create_api(GetPaySalaryEntList_Api, CoopSts=CoopSts, RecordIndex=0, RecordSize=9999).json()
        ents = res['Data']['RecordList']
        for ent in ents:
            if entname == ent['EntShortName']:
                self.entid_pq = ent['EntId']
                break
        return res

    def get_entbrorrow(self, entbrorrowname=None):
        """
        # 获取招聘、派遣端录名单时需要的企业
        :param entbrorrowname: 企业名称，可选，默认为空
        :return:
        """
        res = self.login.create_api(GetEntBorrowByUserType, RcrtType=2).json()
        entbrorrows = res['Data']['RecordList']
        # 遍历列表寻找指定名称的id，找到id后赋值给SpEntID，没找到传入的名称抛出异常
        for entbrorrow in entbrorrows:
            if entbrorrowname == entbrorrow['EntBorrowName']:
                self.entbrorrowid = entbrorrow['EntBorrowId']
                break
        return res

    def get_source(self, FromSpName=None):
        """
        # 获取派遣端录名单时需要的来源
        :param FromSpName: 来源，可选，默认为空
        :return:
        """
        # 获取谁送给我
        res = self.login.create_api(GetVAgentListAPI)
        res = res.json()
        # 来源不为空，获取来源列表
        agentlist = res['Data']['RecordList']
        # 遍历列表寻找指定名称的id
        for agent in agentlist:
            # 找到id后赋值给FromSpID
            if FromSpName == agent['SpShortName']:
                self.FromSpID = agent['SpId']
                break

        # 打印日志
        # if self.FromSpID:
        #     logger.info(f'获取到来源：{self.FromSpID}，{FromSpName}')
        # else:
        #     logger.error(f'没有来源{FromSpName},请检查')
        #     raise Exception
        return res

    def get_labor(self, url, LaborName=None):
        """
        # 获取招聘、派遣端录名单时需要的去向
        :param url: 调用获取去向劳务的接口地址，必填
        :param LaborName: 去向劳务，可选，默认为空
        :return:
        """
        res = self.login.create_api(url).json()
        if url == get_labor:
            self.TargetSpId = int(get_api_result(res, 'SpId')[0])
            self.SpName = get_api_result(res, 'SpShortName')[0]
        else:
            # 企业不为空，获取企业列表
            laborlist = res['Data']['RecordList']
            # 遍历列表寻找指定名称的id，找到id后赋值给SpEntID，没找到传入的名称抛出异常
            for labor in laborlist:
                if labor['SpShortName'] == LaborName:
                    self.TargetSpId = labor['SpId']
                    self.SpName = LaborName
                    break
        return res

    def add_name_pq(self, entname=None, entbrorrowname=None, mobile=None, idnum=None, name=None, gender=1,
                    InterviewDate=nowtime, FromSpName=None, Nation=None, IDCardExprDate=None, Addr=None, InterviewStatus=0,
                    Remark=None, InputType=2, InterviewStatusDCode=None, InterviewStatusRemark=None):
        """
        派遣端录名单
        :param entbrorrowname: 企业，必填
        :param InterviewDate: 面试日期，可选，默认当天日期
        :param FromSpName: 来源，可选，默认为空
        :return: namelistid（名单中台id）, name（名单姓名）, IDCardNum（身份证号）
        """
        entid = entbrorrowid = FromSpID = None
        if entname:
            res = self.get_ent(entname)
            entid = get_value(res, value=entname, param1='EntShortName', param2='EntId')
        # 加载企业
        if entbrorrowname:
            res = self.get_entbrorrow(entbrorrowname)
            entbrorrowid = get_value(res, value=entbrorrowname, param1='EntBorrowName', param2='EntBorrowId')
        # 加载来源
        if FromSpName:
            res = self.get_source(FromSpName)
            FromSpID = get_value(res, value=FromSpName, param1='SpShortName', param2='SpId')
        # 加载劳务
        self.get_labor(get_labor)
        # 生成姓名、身份证、手机号,如果未指定姓名、身份证、手机号，则系统自动生成
        if not name:
            name = self.newname_pq = create_name()
        if not idnum:
            idnum = self.newidnum_pq = create_IDCard()
        if not mobile:
            mobile = self.newmobile_pq = create_phone()
        # 录入名单

        res = self.login.create_api(
            AddNameForOpenAPI,
            InterviewDate=InterviewDate,
            Name=name,
            Gender=gender,
            IDCardNum=idnum,
            EntId=entid,
            Mobile=mobile,
            Nation=Nation,
            IDCardExprDate=IDCardExprDate,
            Addr=Addr,
            SpEntID=entbrorrowid,
            InterviewStatus=InterviewStatus,
            InterviewStatusDCode=InterviewStatusDCode,
            InterviewStatusRemark=InterviewStatusRemark,
            Remark=Remark,
            FromSpID=FromSpID,
            FromSpName=FromSpName,
            TargetSpId=self.TargetSpId,
            SpName=self.SpName,
            InputType=InputType
        )
        # 获取接口返回值
        self.status_code = res.status_code
        self.code = res.json()['Code']
        self.desc = res.json()['Desc']
        self.res_guid = res.json()['Data']['Guid']
        self.newnameid_pq = res.json()['Data']['NameListId']
        self.res_rcrttype = res.json()['Data']['RcrtTyp']
        self.res_uuid = res.json()['Data']['Uuid']
        res = res.json()

        # if res['Desc'] != '成功':
        #     logger.error(f'录入名单失败，{res}')
        return res

    def add_name_zp(self, entbrorrowname, InterviewDate=nowtime, gender=1, LaborName=None):
        """
        招聘端录名单
        :param entbrorrowname: 企业，必填
        :param InterviewDate: 面试日期，可选，默认当天日期
        :param LaborName: 名单去向，可选，默认为空
        :return: InterviewID（名单模板id）, name（名单姓名）, IDCardNum（身份证号）, JFFNameListId（名单中台id）
        """
        # 赋值BrokerUserID
        BrokerUserID = self.login.Guid
        # 加载企业
        self.get_entbrorrow(entbrorrowname)
        # 加载去向
        self.get_labor(GetVLaborList, LaborName)
        # 生成参数
        self.newname_zq = create_name()
        self.newidnum_zp = create_IDCard()
        self.newmobile_zp = create_phone()
        # 因招聘端录入名单LaborName和LaborID为空时调用接口不能带这两个参数，所以做判断
        res = self.login.create_api(AddInterview, InterviewDate=InterviewDate, RealName=self.newname_zq,
                                    Gender=gender,
                                    IDCardNum=self.newidnum_zp,
                                    IdCardExprDt='2030-02-11', RsdtAddr='测试地址', Nation='汉',
                                    Mobile=self.newmobile_zp,
                                    BrokerUserID=BrokerUserID, EntID=self.entbrorrowid,
                                    EntName=entbrorrowname, LaborID=self.TargetSpId,
                                    LaborName=LaborName, InputType=2)
        # 状态码
        self.status_code = res.status_code
        res = res.json()
        name_idnum_mobile = {'Name': self.newname_zq, 'Idnum': self.newidnum_zp, 'Mobile': self.newmobile_zp}
        res.update(name_idnum_mobile)
        # 获取名单ID
        self.newnamelistperformanceid = res['Data']['InterviewID']
        self.newnameid_zp = res['Data']['JFFNameListId']
        self.newnameid_zp_desc = res['Desc']
        # 方法返回名单ID，姓名，身份证号
        return res

    def set_source(self, FromSpName, NameListIds: list = None):
        """
        # 派遣端名单设置谁送给我
        :param FromSpName:来源名称，必选
        :return:result
        """
        # 加载来源
        self.get_source(FromSpName)

        if NameListIds == None: NameListIds = [self.newnameid_pq]

        # 调用接口名单设置来源
        api_result = self.login.create_api(SetSpForOpenAPI, NameListIds=NameListIds, SpCoopId=self.FromSpID,
                                           SpCoopName=FromSpName, SpGroupId=None)
        # 状态码
        self.status_code = api_result.status_code

        res = api_result.json()
        return res

    def set_interview_state(self, IntvSts, IntvStsCode=None, IntvRemark=None, NameIdList: list = None):
        """
        # 派遣端设置面试状态
        :param IntvSts: 面试状态，必选,0:未处理，1：未面试，2：面试通过，3：面试不通过，4：放弃
        :param IntvStsCode: 面试状态码，可选，默认为空,
        :param IntvRemark: 面试备注，可选，默认为空
        :param NameIdList: 名单id，可选，默认为空，为空时使用对象中创建的名单id，输入参考web端接口返回值
        :return:
        """
        # 为空时使用对象中创建的名单id
        if NameIdList is None:
            NameIdList = [self.newnameid_pq]
        # 调用接口设置面试状态
        res = self.login.create_api(SetIntvSts, NameIdList=NameIdList, IntvSts=IntvSts, IntvStsCode=IntvStsCode,
                                    IntvRemark=IntvRemark)
        # 状态码
        self.status_code = res.status_code

        res = res.json()
        return res

    def bind_order(self, orderid, namelist=None):
        """
        # 名单绑定订单
        :param orderid:
        :param NameIdList:
        :return:
        """
        if namelist is None:
            namelist = [self.newnameid_pq]
        res = self.login.create_api(Send_BindOrder, NameIdList=namelist, MainOrderId=orderid)
        # 状态码
        self.status_code = res.status_code

        res = res.json()
        return res

    def wait_synchronize_namelist(self, name=None):
        """
        # 待上传名单同步
        :param name: 待上传名单的姓名
        :return:
        """
        # 获取待同步名单id
        res_result = self.login.create_api(JFF_WaitSyncName_GetWaitSyncNameList, StartInterviewDate=nowtime,
                                           StopInterviewDate=nowtime, RecordIndex=0, RecordSize=10, Order=2)
        list_ = res_result.json()['Data']['RecordList']
        NameList2BSyncIDs = None
        for i in range(len(list_)):
            if name == list_[i]['RealName']:
                NameList2BSyncIDs = list_[i]['NameList2BSyncID']
        # 调用接口同步名单
        res_result = self.login.create_api(SyncNameList, NameList2BSyncIDs=[NameList2BSyncIDs])
        # 状态码
        self.status_code = res_result.status_code

        res = res_result.json()
        return res

    # 招聘端同步名单面试状态
    def Sync_InterviewStatus(self, inviewid_list):
        """
        # 同步名单面试状态
        :param inviewid_list: 名单的InterviewID列表
        :return:
        """
        res = self.login.create_api(SynchronizeInterviewState, InterviewIDList=inviewid_list)
        # 状态码
        self.status_code = res.status_code

        res = res.json()
        return res

    # 招聘端面试名单（商务）页面修改面试状态
    def Modfiy_Zp_InterviewStatus(self, intv_state, interviewid_list, interviewstscode=None):
        """
        # 面试名单（商务）页面修改面试状态
        :param intv_state: 面试状态id
               interviewid_list：名单id列表
               interviewstscode：面试状态原因code
        :return:
        """
        res = self.login.create_api(SetBusinessInterviewState, InterviewState=intv_state, InterviewID=interviewid_list,
                                    InterviewStateCode=interviewstscode)
        # 状态码
        self.status_code = res.status_code

        res = res.json()
        return res

    # 招聘端面试名单（商务）页面设置去向劳务
    def Set_Trgtlabour(self, LaborName, namelist):
        # 加载劳务列表，获取labor_id
        self.get_labor(GetVLaborList, LaborName)
        labor_id = self.TargetSpId
        if labor_id == None:
            raise Exception('获取labor_id失败')

        res = self.login.create_api(SetLabor, SpCoopId=labor_id, SpShortName=LaborName, NameListIds=namelist,
                                    SpGroupId=1000006)
        # 状态码
        self.status_code = res.status_code

        return res.json()

    # 招聘端绑定订单
    def zp_bind_order(self, namelistid_list, mainorderid, ordertyp):
        """
        # 招聘端绑定订单
        :param namelistid_list: 中台名单id列表
               mainorderid：main订单id
               ordertyp：绑单类型1为发单，2为收单
        :return:
        """
        # 调用招聘端绑单接口
        res = self.login.create_api(Recruit_BindOrder,
                                    NameIdList=namelistid_list,
                                    MainOrderId=mainorderid,
                                    OrderType=ordertyp)
        # 状态码
        self.status_code = res.status_code

        res = res.json()
        return res

    # 招聘端面试名单（商务）页面获取收单列表
    def zp_collect_orderlist(self, entname, orderdt, trsp_id, storeid):
        """
        # 招聘端面试名单（商务）页面获取收单列表
        :param entname: 工种名称
               orderdt：订单日期（名单的面试日期）
               trsp_id：劳务id
               storeid: 门店id
        :return:
        """
        res = self.login.create_api(LGetWaitToBindZXXOrderList_api,
                                    EntName=entname,
                                    OrderDt=orderdt,
                                    TrgtSpId=trsp_id,
                                    StoreId=storeid)
        # 状态码
        self.status_code = res.status_code

        res = res.json()['Data']['RecordList']
        if res == []:
            raise Exception('获取的订单列表为空')
        return res

    # 招聘端面试名单（商务）页面获取发单列表
    def zp_send_orderlist(self, entid, trgtspid, orderdt, storeid):
        """
        # 招聘端面试名单（商务）页面获取发单列表
        :param entid: 工种id
               trgtspid：劳务id
               orderdt：订单日期（名单的面试日期）
               storeid: 门店id
        :return:
        """
        res = self.login.create_api(LGetWaitToBindZXXOrderList_api,
                                    EntId=entid,
                                    TrgtSpId=trgtspid,
                                    OrderDt=orderdt,
                                    StoreId=storeid)
        # 状态码
        self.status_code = res.status_code

        res = res.json()['Data']['RecordList']
        if res == []:
            raise Exception('获取的订单列表为空')
        return res

    def get_waitbindorder_pq(self, EntId, NameListIds: list, FromSpId, StdEntID=None, OrderDt=nowtime):
        """
        获取待绑定订单
        :param names:要绑定订单的名单姓名，只接受list
        :param orderDt:面试日期
        :return:生成对象属性wait_bind_orderids，list类型
        """
        res = self.login.create_api(GetWaitToBindZXXOrderList,
                                    OrderDt=OrderDt,
                                    EntId=EntId,
                                    StdEntID=StdEntID,
                                    NameListIds=NameListIds,
                                    FromSpId=FromSpId)
        return res.json()

    def modified_remark(self, NameIdList: list, Remark):
        """
        实接记录设置备注
        :param NameIdList: 名单id，列表
        :param Remark: 备注信息
        :return:
        """
        res = self.login.create_api(ModifiedRemark, NameIdList=NameIdList, Remark=Remark).json()
        return res

    def decryptAPI(self, DesenData, Typ=1):
        """
        脱敏
        :param DesenData: 脱敏数据
        :param Typ: 类型1,手机号码，2身份证号码
        :return:
        """
        res = self.login.create_api(DecryptAPI, DesenData=DesenData, Typ=Typ).json()
        return res

    def getScanRecordFZT(self, NameID):
        """
        查询名单扫描记录
        :param NameID:
        :return:
        """
        res = self.login.create_api(GetScanRecordFZT, NameID=NameID).json()
        return res

    def modNameListMobile(self, Mobile, NameListId, OwnSpId=22699):
        """
        实接记录修改手机号码
        :param Mobile:
        :param NameListId:
        :param OwnSpId: 22699
        :return:
        """
        res = self.login.create_api(ModNameListMobile, Mobile=Mobile, NameListId=NameListId, OwnSpId=OwnSpId)
        res = res.json()
        return res

    def borrowent_for_namelist(self):
        """实接记录录名单随机获取企业"""
        res = self.get_entbrorrow()
        lst = res['Data']['RecordList']
        entborrow_dic = lst[random.randint(0, len(lst) - 1)]
        EntBorrowId = entborrow_dic['EntBorrowId']
        EntBorrowName = entborrow_dic['EntBorrowName']
        EntId = entborrow_dic['EntId']
        res_lst = [EntBorrowId, EntBorrowName, EntId]
        return res_lst

    def random_agent(self):
        """实接记录录名单随机获取供应商"""
        res = self.get_source()
        lst = res['Data']['RecordList']
        agent_dic = lst[random.randint(0, len(lst) - 1)]
        SpId = agent_dic['SpId']
        SpShortName = agent_dic['SpShortName']
        res_lst = [SpId, SpShortName]
        return res_lst
