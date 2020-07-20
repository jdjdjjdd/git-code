#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import random

from common.base_utils.comm_utils import create_phone, create_name
from common.venv.api_path_mb import GetEntBorrowList, GetCoopList, AddBlocUser, GetBlocUserList, UpdateBlocUser, \
    AddOrUpdateEntBorrow, CancelUserBloc, AddResidentFactoryStaff, GetResidentFactoryStaffList, \
    UpdateResidentFactoryStaff, CancelResidentFactoryStaff, AddCoopTag, ModCoopTag, AddCoop, UpdateCoop
from common.venv.api_path_zt import ModPaySalaryEntCoopSts, GetPaySalaryEntList, GetTenantEntListByName


class GroupManagement():

    def __init__(self, login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login

    def getEntBorrowList(self, EntShortName='', EntName='', BEntName='',
                         IsEnabled=-9999, RcrtType=-9999, RecordIndex=0, RecordSize=10):
        result = self.login.create_api(GetEntBorrowList,
                                       EntShortName=EntShortName,
                                       EntName=EntName,
                                       BEntName=BEntName,
                                       IsEnabled=IsEnabled,
                                       RcrtType=RcrtType,
                                       RecordIndex=RecordIndex,
                                       RecordSize=RecordSize)
        res = result.json()
        return res

    def getcooplist(self, NickName='', Principal='', Mobile='',
                    CooperationStatus=-9999, RspsUserId=-9999, RecordIndex=0, RecordSize=10):
        result = self.login.create_api(GetCoopList,
                                       NickName=NickName,
                                       Principal=Principal,
                                       Mobile=Mobile,
                                       CooperationStatus=CooperationStatus,
                                       RspsUserId=RspsUserId,
                                       RecordIndex=RecordIndex,
                                       RecordSize=RecordSize)
        res = result.json()
        return res

    def add_bloc_user(self, AdminSysRoleId=21, AdminSysGroupId=21,
                      Mobile='', RealName='', IsEnabled=1, SpId=22699):
        """
        员工账号管理
        添加员工账号
        默认添加派遣端老板角色
        """
        if Mobile == '':
            Mobile = create_phone()

        if RealName == '':
            RealName = create_name()

        result = self.login.create_api(AddBlocUser,
                                       AdminSysRoleId=AdminSysRoleId,
                                       AdminSysGroupId=AdminSysGroupId,
                                       Mobile=Mobile,
                                       RealName=RealName,
                                       IsEnabled=IsEnabled,
                                       SpId=SpId)

        res = result.json()
        return res

    def get_bloc_user_list(self, Name='', Mobile='',
                           RoleId=0, IsEnabled=-9999, RecordIndex=0, RecordSize=10):
        """
        员工账号管理
        查询员工账号
        """
        result = self.login.create_api(GetBlocUserList,
                                       Name=Name,
                                       Mobile=Mobile,
                                       RoleId=RoleId,
                                       IsEnabled=IsEnabled,
                                       RecordIndex=RecordIndex,
                                       RecordSize=RecordSize)

        res = result.json()
        return res

    def update_bloc_user(self, AdminSysRoleId: int, AdminSysGroupId: int,
                         Mobile: str, RealName: str, IsEnabled: int, BlocManagementId: int):
        """
        员工账号管理
        修改员工账号
        """
        result = self.login.create_api(UpdateBlocUser,
                                       AdminSysRoleId=AdminSysRoleId,
                                       AdminSysGroupId=AdminSysGroupId,
                                       Mobile=Mobile,
                                       RealName=RealName,
                                       IsEnabled=IsEnabled,
                                       BlocManagementId=BlocManagementId)

        res = result.json()
        return res

    def cancel_user_bloc(self, UserId: int, Mobile: int):
        """
        注销账号
        @param UserId: 要注销的账号id
        @param Mobile: 要注销的账号电话
        @return:
        """
        result = self.login.create_api(
            CancelUserBloc, UserId=UserId, Mobile=Mobile)
        res = result.json()
        return res

    def mod_pay_salary_ent_coop_sts(self, CoopSts: int, TEntId: int):
        """
        修改标准企业生效状态
        @param CoopSts:
        @param TEntId:
        @return:
        """
        result = self.login.create_api(ModPaySalaryEntCoopSts,
                                       CoopSts=CoopSts,
                                       TEntId=TEntId
                                       )
        res = result.json()
        return res

    def get_pay_salary_ent_list(self, RecordIndex=0, RecordSize=10, FromDate='', ToDate='', USCCNum='', EntShortName='',
                                EntFullName='', EntName='', CoopSts=0):
        """
        查询标准企业列表
        @param RecordIndex:开始索引
        @param RecordSize:结束索引
        @param FromDate:添加日期起始
        @param ToDate:添加日期结束
        @param USCCNum:统一社会信用代码
        @param EntShortName:
        @param EntFullName:
        @param EntName:
        @param CoopSts:合作状态，0全部，1合作种，2终止合作
        @return:
        """
        result = self.login.create_api(GetPaySalaryEntList,
                                       RecordIndex=RecordIndex,
                                       RecordSize=RecordSize,
                                       FromDate=FromDate,
                                       ToDate=ToDate,
                                       USCCNum=USCCNum,
                                       EntShortName=EntShortName,
                                       EntFullName=EntFullName,
                                       EntName=EntName,
                                       CoopSts=CoopSts)
        res = result.json()
        return res

    def add_or_update_ent_borrow(
            self, CoopEntName: str, EntId: int, CoopEntId=0, IsEnabled=1, RcrtType=2, Flag=1):
        """
        新增企业工种；修改企业工种
        @param EntId: 标准企业id
        @param CoopEntName: 工种名字
        @param CoopEntId:
        @param IsEnabled:
        @param RcrtType:
        @param Flag:
        @return:
        """
        result = self.login.create_api(AddOrUpdateEntBorrow,
                                       EntId=EntId,
                                       CoopEntName=CoopEntName,
                                       CoopEntId=CoopEntId,
                                       IsEnabled=IsEnabled,
                                       RcrtType=RcrtType,
                                       Flag=Flag)
        res = result.json()
        return res

    def get_ent_borrow_list(self, IsEnabled=-9999, RcrtType=-9999, EntName='',
                            BEntName='', EntShortName='', RecordIndex=0, RecordSize=10):
        """
        查询企业工种
        @param IsEnabled:
        @param RcrtType:
        @param EntName:
        @param BEntName:
        @param EntShortName:
        @param RecordIndex:
        @param RecordSize:
        @return:
        """
        result = self.login.create_api(GetEntBorrowList,
                                       IsEnabled=IsEnabled,
                                       RcrtType=RcrtType,
                                       EntName=EntName,
                                       BEntName=BEntName,
                                       EntShortName=EntShortName,
                                       RecordIndex=RecordIndex,
                                       RecordSize=RecordSize)
        res = result.json()
        return res

    def add_resident_factory_staff(self, Name: str, IdCardNum: str, Mobile: str,
                                   EntId: str, EntryDate: str,
                                   EntFullName: str, BankName='', BankCardNum='', ResignationDate=''):
        """
        新增驻场账号
        @param Name:驻场名字
        @param IdCardNum:省份证号
        @param Mobile:手机号
        @param BankName:银行名
        @param BankCardNum:银行卡号
        @param EntId:该驻场名下的标准企业id，多个用逗号分隔，ps："10012,10013"
        @param EntryDate:入职日期，ps："2020-06-18"
        @param ResignationDate:离职日期，ps："2020-06-18"
        @param EntFullName:该驻场名下的标准企业名，多个用逗号分隔，ps："丽宝广场12,富士康"
        @return:
        """
        result = self.login.create_api(AddResidentFactoryStaff,
                                       Name=Name,
                                       IdCardNum=IdCardNum,
                                       Mobile=Mobile,
                                       BankName=BankName,
                                       BankCardNum=BankCardNum,
                                       EntId=EntId,
                                       EntryDate=EntryDate,
                                       ResignationDate=ResignationDate,
                                       EntFullName=EntFullName)
        res = result.json()
        return res

    def get_resident_factory_staff_list(self, EntId: int=None, Name='', IdCardNum='', Mobile='', WorkStatus=-9999, IsCancel=-9999,
                                        BeginEntryDate='', EndEntryDate='', BeginResignationDate='', EndResignationDate='', RecordIndex=0, RecordSize=10):
        """
        查询驻场账号
        @param EntId:标准企业id
        @param Name: 驻场姓名
        @param IdCardNum: 身份证号
        @param Mobile:手机号
        @param WorkStatus:在职状态
        @param IsCancel:账号是否被注销
        @param BeginEntryDate:最早入职日期
        @param EndEntryDate:最晚入职日期
        @param BeginResignationDate:最早离职日期
        @param EndResignationDate:最晚离职日期
        @param RecordIndex:开头索引
        @param RecordSize:结束索引
        @return:
        """
        result = self.login.create_api(GetResidentFactoryStaffList,
                                       EntId=EntId,
                                       Name=Name,
                                       IdCardNum=IdCardNum,
                                       Mobile=Mobile,
                                       WorkStatus=WorkStatus,
                                       IsCancel=IsCancel,
                                       BeginEntryDate=BeginEntryDate,
                                       EndEntryDate=EndEntryDate,
                                       BeginResignationDate=BeginResignationDate,
                                       EndResignationDate=EndResignationDate,
                                       RecordIndex=RecordIndex,
                                       RecordSize=RecordSize)
        res = result.json()
        return res

    def update_resident_factory_staff(self, Name: str, IdCardNum: str, Mobile: str, BankName: str, BankCardNum: str,
                                      EntId: str, EntryDate: str, ResignationDate: str, ResidentFactoryStaffId: int, EntFullName: str):
        """
        修改驻场账号
        @param Name:名字
        @param IdCardNum:身份证号
        @param Mobile:手机号
        @param BankName:银行名
        @param BankCardNum:银行账号
        @param EntId:标准企业id
        @param EntryDate:入职日期
        @param ResignationDate:离职日期
        @param ResidentFactoryStaffId:驻场账号主键
        @param EntFullName:标准企业全称
        @return:
        """
        result = self.login.create_api(UpdateResidentFactoryStaff,
                                       Name=Name,
                                       IdCardNum=IdCardNum,
                                       Mobile=Mobile,
                                       BankName=BankName,
                                       BankCardNum=BankCardNum,
                                       EntId=EntId,
                                       EntryDate=EntryDate,
                                       ResignationDate=ResignationDate,
                                       ResidentFactoryStaffId=ResidentFactoryStaffId,
                                       EntFullName=EntFullName)
        res = result.json()
        return res

    def cancel_resident_factory_staff(
            self, Mobile: str, UserId: int, IdCardNum: str):
        """
        注销驻场账号
        @param Mobile: 手机号
        @param UserId: userid
        @param IdCardNum: 身份证号
        @return:
        """
        result = self.login.create_api(
            CancelResidentFactoryStaff,
            Mobile=Mobile,
            UserId=UserId,
            IdCardNum=IdCardNum)
        res = result.json()
        return res

    def add_coop_tag(self, TagName: str):
        """
        新增供应商标签
        @param TagName:标签名
        @return:
        """
        result = self.login.create_api(AddCoopTag, TagName=TagName)
        res = result.json()
        return res

    def mod_coop_tag(self, TagName: str, TagId: int):
        """
        修改供应商标签
        @param TagName:标签名
        @param TagId: 标签id
        @return:
        """
        result = self.login.create_api(
            ModCoopTag, TagName=TagName, TagId=TagId)
        res = result.json()
        return res

    def add_coop(self, CoopShortName:str, CoopTagId:int, CoopFullName:str, Uscc:str, BankName:str,
                 BankCardNum:str, CtctName:str, CtctMobile:str, IdCardNum:str,RspsUserId:int,
                 BusinessLicenseUrl:str,CooperationStatus=1):
        """
        新增供应商
        @param CoopShortName:供应商名称
        @param CoopTagId:供应商标签id
        @param CoopFullName:营业执照公司名称
        @param Uscc:统一社会信用代码
        @param BankName:银行名称
        @param BankCardNum:银行账号
        @param CtctName:联系人姓名
        @param CtctMobile:联系人电话
        @param IdCardNum:联系人身份号
        @param CooperationStatus:合作状态
        @param RspsUserId:联络人userid
        @param BusinessLicenseUrl:营业执照url
        @return:
        """
        result = self.login.create_api(AddCoop,
                                       CoopShortName=CoopShortName,
                                       CoopTagId=CoopTagId,
                                       CoopFullName=CoopFullName,
                                       Uscc=Uscc,
                                       BankName=BankName,
                                       BankCardNum=BankCardNum,
                                       CtctName=CtctName,
                                       CtctMobile=CtctMobile,
                                       IdCardNum=IdCardNum,
                                       CooperationStatus=CooperationStatus,
                                       RspsUserId=RspsUserId,
                                       BusinessLicenseUrl=BusinessLicenseUrl)
        res = result.json()
        return res

    def randow_ent(self):
        """集团管理随机获取标准企业"""
        res = self.get_pay_salary_ent_list(RecordSize=100)
        lst = res['Data']['RecordList']
        ent_dic = lst[random.randint(0, len(lst) - 1)]
        EntName = ent_dic['EntName']
        EntShortName = ent_dic['EntShortName']
        TEntId = ent_dic['TEntId']
        res_lst = [EntShortName, TEntId, EntName]
        return res_lst

    def randow_borrowent(self):
        """集团管理随机获取企业"""
        res = self.getEntBorrowList(RecordSize=100)
        lst = res['Data']['RecordList']
        entborrow_dic = lst[random.randint(0, len(lst) - 1)]
        EntBorrowId = entborrow_dic['EntBorrowId']
        EntBorrowName = entborrow_dic['EntBorrowName']
        EntId = entborrow_dic['EntId']
        EntName = entborrow_dic['EntName']
        res_lst = [EntBorrowId, EntBorrowName, EntId, EntName]
        return res_lst

    def getTenantEntListByName(self, Name, CoopSts=0, RecordIndex=0, RecordSize=9999, ):
        """
        标准企业查询项获取标准企业
        :param Name:
        :param CoopSts:
        :param RecordIndex:
        :param RecordSize:
        :return:
        """
        res = self.login.create_api(GetTenantEntListByName, Name=Name, CoopSts=CoopSts, RecordIndex=RecordIndex,
                                    RecordSize=RecordSize).json()
        return res

    def updateCoop(self, CoopId=None, CooperationStatus=None, CooperationStatusOnly=None, CoopShortName=None,
                   CoopFullName=None, Uscc=None, IdCardNum=None,
                   CtctName=None, CtctMobile=None, BankName=None, BankCardNum=None, BusinessLicenseUrl=None,
                   ZtSpId=None, CoopTagId=None, RspsUserId=None):
        """
        编辑供应商
        :param CoopId:主键
        :param CooperationStatus:合作状态
        :param CooperationStatusOnly:只改合作状态
        :param CoopShortName:简称
        :param CoopFullName:全称
        :param Uscc:社会统一信用代码
        :param IdCardNum:身份证
        :param CtctName:联系人姓名
        :param CtctMobile:联系人手机号
        :param BankName:开户行名称
        :param BankCardNum:收款账户
        :param BusinessLicenseUrl:图片地址
        :param ZtSpId:中台SpID
        :param CoopTagId:标签id选填
        :param RspsUserId:负责人
        :return:
        """
        res = self.login.create_api(UpdateCoop,
                                    CoopId=CoopId,
                                    CooperationStatus=CooperationStatus,
                                    CooperationStatusOnly=CooperationStatusOnly,
                                    CoopShortName=CoopShortName,
                                    CoopFullName=CoopFullName,
                                    Uscc=Uscc,
                                    IdCardNum=IdCardNum,
                                    CtctName=CtctName,
                                    CtctMobile=CtctMobile,
                                    BankName=BankName,
                                    BankCardNum=BankCardNum,
                                    BusinessLicenseUrl=BusinessLicenseUrl,
                                    ZtSpId=ZtSpId,
                                    CoopTagId=CoopTagId,
                                    RspsUserId=RspsUserId
                                    ).json()
        return res
