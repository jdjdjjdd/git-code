#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : DJY_Name_Manager.py
# @Author   : yht
# @Date     : 2020/05/11
# @Update   :
# @Desc     : 名单服务


from common.venv.api_path_mb import *


class DJYNameManaer():

    def __init__(self,login=None):
        self.login = login

    def AddNameForOpenAPI(self, EntId=None, SpEntID=None, mobile=None, idnum=None, name=None, gender=None,
                          InterviewDate=None, FromSpID=None, FromSpName=None, TargetSpId=None, SpName=None, Nation=None,
                          IDCardExprDate=None, Addr=None, InterviewStatus=None, Remark=None, InputType=None):
        """
        派遣端录名单
        :param EntId: 标准企业ID
        :param SpEntID:企业ID
        :param mobile:会员手机号码
        :param idnum:会员身份证号码
        :param name:会员姓名
        :param gender:会员性别
        :param InterviewDate:会员面试日期
        :param FromSpID:来源ID
        :param FromSpName:来源名称
        :param TargetSpId:去向ID
        :param SpName:去向名称
        :param Nation:民族
        :param IDCardExprDate:身份证有效期
        :param Addr:户籍地址
        :param InterviewStatus:面试状态
        :param Remark:备注
        :param InputType:工种类型
        :return:
        """
        # 录入名单

        res = self.login.create_api(AddNameForOpenAPI,
                                    InterviewDate=InterviewDate,
                                    Name=name,
                                    Gender=gender,
                                    IDCardNum=idnum,
                                    EntId=EntId,
                                    Mobile=mobile,
                                    Nation=Nation,
                                    IDCardExprDate=IDCardExprDate,
                                    Addr=Addr,
                                    SpEntID=SpEntID,
                                    InterviewStatus=InterviewStatus,
                                    Remark=Remark,
                                    FromSpID=FromSpID,
                                    FromSpName=FromSpName,
                                    TargetSpId=TargetSpId,
                                    SpName=SpName,
                                    InputType=InputType)
        # 获取接口返回值
        return res

    def get_nameList(self, starttime=None, endtime=None, name=None, idcardnum=None, mobile=None, Gender=None,
                     InterviewStatus=None, RecordSize=None, RecordIndex=None, FromBindStatus=None, SpEntName=None,
                     RcrtTyp=None, FromSpId=None, ScannerMobile=None, ScannerUserID=None):
        """
        # 派遣端实接记录查询
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
        :param FromSpId:来源id，可选
        :param ScannerMobile:扫描人手机号码，可选
        :param ScannerUserID:扫描人guid，可选
        :return:
        """
        # 调用获取派遣端实接记录列表接口
        res = self.login.create_api(GetNameList,
                                    StartTime=starttime,
                                    EndTime=endtime,
                                    Name=name,
                                    IDCardNum=idcardnum,
                                    InterviewStatus=InterviewStatus,
                                    Gender=Gender,
                                    Mobile=mobile,
                                    RcrtTyp=RcrtTyp,
                                    FromBindStatus=-FromBindStatus,
                                    ScannerMobile=ScannerMobile,
                                    ScannerUserID=ScannerUserID,
                                    RecordIndex=RecordIndex,
                                    RecordSize=RecordSize,
                                    SpEntName=SpEntName,
                                    FromSpId=FromSpId,
                                    SpIDs=[22699])
        return res
