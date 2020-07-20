#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 获取根路径
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)
from common.base_utils.Log import MyLog
from common.base_utils.Assert import Assertions
from common.venv.var import *
from config.Config import Config
from common.business_func.namelist import NameList
from common.data_operation.mysql_db import OperateMDdb
from common.venv.api_path_mb import *
from common.login.web_login import Web_Login
from common.base_utils.comm_utils import *
import pytest, allure
import warnings

warnings.filterwarnings('ignore')


class TestNameList:


    def setup_class(self):
        # 创建配置实例
        self.cf = Config()
        self.db = OperateMDdb()
        self.name_global = create_name()
        self.idnum_global = create_IDCard()
        self.mobile_global = create_phone()
        self.assert_equal = Assertions().assert_equal
        self.log = MyLog().error

    def setup_method(self):
        # 定义每个用例变量
        self.name = create_name()
        self.idnum = create_IDCard()
        self.mobile = create_phone()


    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('手动录入-不填选填信息')
    @allure.severity('blocker')
    def test_namelist_0002(self, weblogin, name_manage, borrow_randow_fuction):
        """
        手动录入-不填选填信息

        """
        print('\n{}测试开始\n'.format(self.test_namelist_0002.__name__))
        borrowid1 = borrow_randow_fuction[0]
        borrowname1 = borrow_randow_fuction[1]
        entid = borrow_randow_fuction[2]


        with allure.step("step1:填入姓名、身份证号，选择工种、面试日期，点击确定"):
            # 录入名单
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               InterviewDate=nowtime,
                                               Name=self.name,
                                               IDCardNum=self.idnum,
                                               Gender=1,
                                               TargetSpId=22699,
                                               SpEntID=borrowid1
                                               )
        with allure.step("预期结果：提示保存成功，接口返回数据正确"):
            # 接口返回
            status = add_name_res.status_code
            code = add_name_res.json()['Code']
            desc = add_name_res.json()['Desc']
            guid = add_name_res.json()['Data']['Guid']
            nameid = add_name_res.json()['Data']['NameListId']
            rcrttype = add_name_res.json()['Data']['RcrtTyp']
            uuid = add_name_res.json()['Data']['Uuid']
            # 断言
            pytest.assume(status==200,f'{status},200')
            pytest.assume(code==0)
            pytest.assume(guid==0)
            pytest.assume(desc=='成功')
            pytest.assume(rcrttype==2)
            pytest.assume(uuid==0)

        with allure.step("step2:检查列表数据"):
            query_res = name_manage.get_nameList(StartTime=nowtime, EndTime=nowtime, IDCardNum=self.idnum,
                                                 Name=self.name)
        with allure.step("预期结果：列表生成一条新的名单记录，数据和刚才录入一致"):
            pytest.assume(get_api_result(query_res,'NameID')[0] == nameid,(get_api_result(query_res,'NameID'),nameid))
            pytest.assume(get_api_result(query_res,'IDCardNum')[0] == self.idnum)
            pytest.assume(get_api_result(query_res,'Name')[0] == self.name)
            pytest.assume(get_api_result(query_res, 'SpEntName')[0] == borrowname1)
            pytest.assume(get_api_result(query_res,'RcrtTyp')[0] == 2)

        with allure.step("step3:检查数据库落表"):
            # 构造sql
            sql1 = "select * from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, self.idnum)
            sql2 = "select * from name_list_flow where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, self.idnum)
            # 查询数据库
            db_name_list_res = self.db.selectsql(sql1)
            db_name_list_flow_res = self.db.selectsql(sql2)
        with allure.step("预期结果1：name_list生成一条新的数据，与录入的数据一致"):
            name_list_nameid = db_name_list_res[0][0]
            name_list_idnum = db_name_list_res[0][3]
            name_list_name = db_name_list_res[0][4]
            name_list_spid = db_name_list_res[0][11]
            name_list_entid = db_name_list_res[0][12]
            name_list_entborrowid = db_name_list_res[0][13]
            name_list_entborrowname = db_name_list_res[0][14]
            name_list_rcrt_type = db_name_list_res[0][15]
            name_list_srce_tenant_coop_id = db_name_list_res[0][17]
            name_list_srce_sp_short_name = db_name_list_res[0][18]
            # 断言
            pytest.assume(name_list_nameid == nameid)
            pytest.assume(name_list_idnum == self.idnum)
            pytest.assume(name_list_name == self.name)
            pytest.assume(name_list_spid == 22699)
            pytest.assume(name_list_entid == entid)
            pytest.assume(name_list_entborrowid == borrowid1)
            pytest.assume(name_list_entborrowname == borrowname1)
            pytest.assume(name_list_rcrt_type == 2)
            pytest.assume(name_list_srce_tenant_coop_id == 0)
            pytest.assume(name_list_srce_sp_short_name == '')
        with allure.step("预期结果2：name_list_flow生成一条新的数据，与录入的数据一致"):
            name_list_flow_nameid = db_name_list_flow_res[0][1]
            name_list_flow_idnum = db_name_list_flow_res[0][3]
            name_list_flow_name = db_name_list_flow_res[0][4]
            name_list_flow_spid = db_name_list_flow_res[0][11]
            name_list_flow_entid = db_name_list_flow_res[0][12]
            name_list_flow_entborrowid = db_name_list_flow_res[0][13]
            name_list_flow_entborrowname = db_name_list_flow_res[0][14]
            name_list_flow_srce_tenant_coop_id = db_name_list_flow_res[0][16]
            name_list_flow_srce_sp_short_name = db_name_list_flow_res[0][17]
            # 断言
            pytest.assume(name_list_flow_nameid == nameid)
            pytest.assume(name_list_flow_idnum == self.idnum)
            pytest.assume(name_list_flow_name == self.name)
            pytest.assume(name_list_flow_spid == 22699)
            pytest.assume(name_list_flow_entid == entid)
            pytest.assume(name_list_flow_entborrowid == borrowid1)
            pytest.assume(name_list_flow_entborrowname == borrowname1)
            pytest.assume(name_list_flow_srce_tenant_coop_id == 0)
            pytest.assume(name_list_flow_srce_sp_short_name == None)


    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('手动录入-带所有选填项信息')
    @allure.severity('critical')
    def test_namelist_0003(self, weblogin, name_manage, random_agent, borrow_randow_fuction):
        """手动录入-带所有选填项信息"""
        print('\n{}测试开始\n'.format(self.test_namelist_0003.__name__))
        borrowid1 = borrow_randow_fuction[0]
        borrowname1 = borrow_randow_fuction[1]
        entid = borrow_randow_fuction[2]
        from_sp_id1 = random_agent[0]
        from_sp_name1 = random_agent[1]

        with allure.step("step1:填入姓名、身份证号、手机号码、证件有效期、户籍地址、民族、备注，选择工种、面试日期、来源，点击确定"):
            # 录入名单
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               SpEntID=borrowid1,
                                               # SpEntName=self.entborrowname,
                                               FromSpID=from_sp_id1,
                                               FromSpName=from_sp_name1,
                                               # ToSpID=22699,
                                               # ToSpName='奇迹劳务',
                                               TargetSpId=22699,
                                               SpName='奇迹劳务',
                                               InputType=2,
                                               InterviewStatus=0,
                                               InterviewStatusDCode=None,
                                               InterviewStatusRemark=None,
                                               InterviewDate=nowtime,
                                               Name=self.name,
                                               Mobile=self.mobile,
                                               IDCardNum=self.idnum,
                                               Nation='汉',
                                               Addr='测试地址',
                                               Gender=1,
                                               Remark='测试备注',
                                               IDCardExprDate='2030-06-01',
                                               ContactMobile=self.mobile,
                                               # NameListLaborBackId=None,
                                               )
        with allure.step("预期结果：提示保存成功，接口返回数据正确"):
            # 接口返回
            status = add_name_res.status_code
            code = add_name_res.json()['Code']
            desc = add_name_res.json()['Desc']
            guid = add_name_res.json()['Data']['Guid']
            nameid = add_name_res.json()['Data']['NameListId']
            rcrttype = add_name_res.json()['Data']['RcrtTyp']
            uuid = add_name_res.json()['Data']['Uuid']
            # 断言
            pytest.assume(status == 200)
            pytest.assume(code == 0)
            pytest.assume(guid == 0)
            pytest.assume(desc == '成功')
            pytest.assume(rcrttype == 2)
            pytest.assume(uuid == 0)

        with allure.step("step2:检查列表数据"):
            query_res = name_manage.get_nameList(StartTime=nowtime, EndTime=nowtime, IDCardNum=self.idnum,
                                                 Name=self.name)
        with allure.step("预期结果：列表生成一条新的名单记录，数据和刚才录入一致"):
            pytest.assume(get_api_result(query_res,'NameID'),nameid)
            pytest.assume(get_api_result(query_res,'IDCardNum'),self.idnum)
            pytest.assume(get_api_result(query_res,'Name'),self.name)
            pytest.assume(get_api_result(query_res, 'SpEntName'), borrowname1)
            pytest.assume(get_api_result(query_res,'RcrtTyp'),2)

        with allure.step("step3:检查数据库落表"):
            # 构造sql
            sql1 = "select * from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, self.idnum)
            sql2 = "select * from name_list_flow where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, self.idnum)
            sql3 = "select * from name_list_sync where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, self.idnum)
            # 查询数据库
            db_name_list_res = self.db.selectsql(sql1)
            db_name_list_flow_res = self.db.selectsql(sql2)
            db_name_list_sync_res = self.db.selectsql(sql3)
        with allure.step("预期结果1：name_list生成一条新的数据，与录入的数据一致"):
            name_list_nameid = db_name_list_res[0][0]
            name_list_idnum = db_name_list_res[0][3]
            name_list_name = db_name_list_res[0][4]
            name_list_spid = db_name_list_res[0][11]
            name_list_entid = db_name_list_res[0][12]
            name_list_entborrowid = db_name_list_res[0][13]
            name_list_entborrowname = db_name_list_res[0][14]
            name_list_rcrt_type = db_name_list_res[0][15]
            name_list_srce_tenant_coop_id = db_name_list_res[0][17]
            name_list_srce_sp_short_name = db_name_list_res[0][18]
            # 断言
            pytest.assume(name_list_nameid == nameid)
            pytest.assume(name_list_idnum == self.idnum)
            pytest.assume(name_list_name == self.name)
            pytest.assume(name_list_spid == 22699)
            pytest.assume(name_list_entid == entid)
            pytest.assume(name_list_entborrowid == borrowid1)
            pytest.assume(name_list_entborrowname == borrowname1)
            pytest.assume(name_list_rcrt_type == 2)
            pytest.assume(name_list_srce_tenant_coop_id == from_sp_id1)
            pytest.assume(name_list_srce_sp_short_name == from_sp_name1)
        with allure.step("预期结果2：name_list_flow生成一条新的数据，与录入的数据一致"):
            name_list_flow_nameid = db_name_list_flow_res[0][1]
            name_list_flow_idnum = db_name_list_flow_res[0][3]
            name_list_flow_name = db_name_list_flow_res[0][4]
            name_list_flow_spid = db_name_list_flow_res[0][11]
            name_list_flow_entid = db_name_list_flow_res[0][12]
            name_list_flow_entborrowid = db_name_list_flow_res[0][13]
            name_list_flow_entborrowname = db_name_list_flow_res[0][14]
            name_list_flow_srce_tenant_coop_id = db_name_list_flow_res[0][16]
            name_list_flow_srce_sp_short_name = db_name_list_flow_res[0][17]
            # 断言
            pytest.assume(name_list_flow_nameid == nameid)
            pytest.assume(name_list_flow_idnum == self.idnum)
            pytest.assume(name_list_flow_name == self.name)
            pytest.assume(name_list_flow_spid == 22699)
            pytest.assume(name_list_flow_entid == entid)
            pytest.assume(name_list_flow_entborrowid == borrowid1)
            pytest.assume(name_list_flow_entborrowname == borrowname1)
            pytest.assume(name_list_flow_srce_tenant_coop_id == from_sp_id1)
            pytest.assume(name_list_flow_srce_sp_short_name == from_sp_name1)
        with allure.step("预期结果3：name_list_sync生成一条新的数据，与录入的数据一致"):
            name_list_sync_nameid = db_name_list_sync_res[0][1]
            name_list_sync_idnum = db_name_list_sync_res[0][3]
            name_list_sync_name = db_name_list_sync_res[0][4]
            name_list_sync_spid = db_name_list_sync_res[0][9]
            name_list_sync_entid = db_name_list_sync_res[0][10]
            name_list_sync_entborrowid = db_name_list_sync_res[0][11]
            name_list_sync_entborrowname = db_name_list_sync_res[0][12]
            # 断言
            pytest.assume(name_list_sync_nameid == nameid)
            pytest.assume(name_list_sync_idnum == self.idnum)
            pytest.assume(name_list_sync_name == self.name)
            pytest.assume(name_list_sync_entid == entid)
            pytest.assume(name_list_sync_entborrowid == borrowid1)
            pytest.assume(name_list_sync_entborrowname == borrowname1)

    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('手动录入-不同面试状态录入：面试状态为{InterviewStatus}')
    @allure.severity('critical')
    @pytest.mark.parametrize('InterviewStatus', [0, 1, 2, 3, 4])
    def test_namelist_0004(self, InterviewStatus, weblogin, name_manage, borrow_randow_fuction, random_agent):
        """手动录入-不同面试状态录入"""
        print('\n{}测试开始\n'.format(self.test_namelist_0004.__name__))
        status = {0: '未处理', 1: '未面试', 2: '面试通过', 3: '面试不通过', 4: '放弃'}
        borrowid1 = borrow_randow_fuction[0]
        borrowname1 = borrow_randow_fuction[1]
        entid = borrow_randow_fuction[2]
        from_sp_id1 = random_agent[0]
        from_sp_name1 = random_agent[1]

        with allure.step("step1:录入面试状态为{}的名单，检查列表数据，检查数据库落表".format(status[InterviewStatus])):
            idnum = create_IDCard()
            mobile = create_phone()
            name = create_name()
            # 录入名单
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               SpEntID=borrowid1,
                                               # SpEntName=self.entborrowname,
                                               FromSpID=from_sp_id1,
                                               FromSpName=from_sp_name1,
                                               # ToSpID=22699,
                                               # ToSpName='奇迹劳务',
                                               TargetSpId=22699,
                                               SpName='奇迹劳务',
                                               InputType=2,
                                               InterviewStatus=InterviewStatus,
                                               InterviewStatusDCode=None,
                                               InterviewStatusRemark=None,
                                               InterviewDate=nowtime,
                                               Name=name,
                                               Mobile=mobile,
                                               IDCardNum=idnum,
                                               Nation='汉',
                                               Addr='测试地址',
                                               Gender=1,
                                               Remark='测试备注',
                                               IDCardExprDate='2030-06-01',
                                               ContactMobile=mobile,
                                               )
            # 查询名单
            query_res = name_manage.get_nameList(StartTime=nowtime, EndTime=nowtime, IDCardNum=idnum, Name=name)
            # 构造sql
            sql1 = "select intv_sts from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            sql2 = "select intv_sts from name_list_flow where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            sql3 = "select intv_sts from name_list_sync where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            # 查询数据库
            db_name_list_res = self.db.selectsql(sql1)
            db_name_list_flow_res = self.db.selectsql(sql2)
            db_name_list_sync_res = self.db.selectsql(sql3)
        with allure.step("预期结果1：提示保存成功，接口返回数据正确"):
            # 接口返回
            status = add_name_res.status_code
            code = add_name_res.json()['Code']
            desc = add_name_res.json()['Desc']
            guid = add_name_res.json()['Data']['Guid']
            nameid = add_name_res.json()['Data']['NameListId']
            rcrttype = add_name_res.json()['Data']['RcrtTyp']
            uuid = add_name_res.json()['Data']['Uuid']
            # 断言
            pytest.assume(status == 200)
            pytest.assume(code == 0)
            pytest.assume(guid == 0)
            pytest.assume(desc == '成功')
            pytest.assume(rcrttype == 2)
            pytest.assume(uuid == 0)
        with allure.step("预期结果2：列表生成名单记录面试状态为未处理"):
            # 断言-检查面试状态
            pytest.assume(get_api_result(query_res, 'InterviewStatus'), InterviewStatus)
        with allure.step("预期结果3：name_list表intv_sts字段为{}".format(InterviewStatus)):
            name_list_intv_sts = db_name_list_res[0][0]
            # 断言
            pytest.assume(name_list_intv_sts == InterviewStatus)
        with allure.step("预期结果4：name_list_flow表intv_sts字段为{}".format(InterviewStatus)):
            name_list_flow_intv_sts = db_name_list_flow_res[0][0]
            # 断言
            pytest.assume(name_list_flow_intv_sts == InterviewStatus)
        with allure.step("预期结果5：name_list_sync表intv_sts字段为{}".format(InterviewStatus)):
            name_list_sync_intv_sts = db_name_list_sync_res[0][0]
            # 断言
            pytest.assume(name_list_sync_intv_sts == InterviewStatus)


    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('手动录入-不同性别录入:性别为{Gender}')
    @allure.severity('critical')
    @pytest.mark.parametrize('Gender', [1, 2])
    def test_namelist_0005(self, Gender, weblogin, name_manage, borrow_randow_fuction, random_agent):
        """手动录入-不同性别录入"""
        print('\n{}测试开始\n'.format(self.test_namelist_0005.__name__))
        borrowid1 = borrow_randow_fuction[0]
        borrowname1 = borrow_randow_fuction[1]
        entid = borrow_randow_fuction[2]
        from_sp_id1 = random_agent[0]
        from_sp_name1 = random_agent[1]

        with allure.step("step1:录入性别为男的名单，检查列表数据，检查数据库落表"):
            idnum = create_IDCard()
            mobile = create_phone()
            name = create_name()
            # 录入名单
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               SpEntID=borrowid1,
                                               FromSpID=from_sp_id1,
                                               FromSpName=from_sp_name1,
                                               TargetSpId=22699,
                                               SpName='奇迹劳务',
                                               InputType=2,
                                               InterviewStatus=0,
                                               InterviewStatusDCode=None,
                                               InterviewStatusRemark=None,
                                               InterviewDate=nowtime,
                                               Name=name,
                                               Mobile=mobile,
                                               IDCardNum=idnum,
                                               Nation='汉',
                                               Addr='测试地址',
                                               Gender=Gender,
                                               Remark='测试备注',
                                               IDCardExprDate='2030-06-01',
                                               ContactMobile=mobile,
                                               )
            # 查询名单
            query_res = name_manage.get_nameList(StartTime=nowtime, EndTime=nowtime, IDCardNum=idnum, Name=name)
            # 构造sql
            sql1 = "select gender from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            sql2 = "select gender from name_list_flow where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            sql3 = "select gender from name_list_sync where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            # 查询数据库
            db_name_list_res = self.db.selectsql(sql1)
            db_name_list_flow_res = self.db.selectsql(sql2)
            db_name_list_sync_res = self.db.selectsql(sql3)
        with allure.step("预期结果1：提示保存成功，接口返回数据正确"):
            # 接口返回
            status = add_name_res.status_code
            code = add_name_res.json()['Code']
            desc = add_name_res.json()['Desc']
            guid = add_name_res.json()['Data']['Guid']
            nameid = add_name_res.json()['Data']['NameListId']
            rcrttype = add_name_res.json()['Data']['RcrtTyp']
            uuid = add_name_res.json()['Data']['Uuid']
            # 断言
            pytest.assume(status == 200)
            pytest.assume(code == 0)
            pytest.assume(guid == 0)
            pytest.assume(desc == '成功')
            pytest.assume(rcrttype == 2)
            pytest.assume(uuid == 0)
        with allure.step("预期结果2：列表生成名单记录性别为男"):
            # 断言-检查面试状态
            pytest.assume(get_api_result(query_res, 'Gender'), Gender)
        with allure.step("预期结果3：name_list表gender字段为{}".format(Gender)):
            name_list_gender = db_name_list_res[0][0]
            # 断言
            pytest.assume(name_list_gender == Gender)
        with allure.step("预期结果4：name_list_flow表gender字段为{}".format(Gender)):
            name_list_flow_gender = db_name_list_flow_res[0][0]
            # 断言
            pytest.assume(name_list_flow_gender == Gender)
        with allure.step("预期结果5：name_list_sync表gender字段为{}".format(Gender)):
            name_list_sync_gender = db_name_list_sync_res[0][0]
            # 断言
            pytest.assume(name_list_sync_gender == Gender)


    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('手工录入-关闭企业')
    @allure.severity('critical')
    def test_namelist_0006(self, name_manage, group_manage, weblogin, borrowent, borrow_randow_fuction):
        """手工录入-关闭企业"""
        print('\n{}测试开始\n'.format(self.test_namelist_0006.__name__))
        borrowname2 = borrowent[1]
        with allure.step("step1:关闭企业A"):
            res1 = group_manage.getEntBorrowList(BEntName=borrowname2)
            coop_borrow_id = get_value(res=res1, value=borrowname2, param1='EntBorrowName', param2='EntBorrowId')
            entid = get_value(res=res1, value=borrowname2, param1='EntBorrowName', param2='EntId')
            group_manage.add_or_update_ent_borrow(CoopEntId=coop_borrow_id, CoopEntName=borrowname2, IsEnabled=2,
                                                EntId=entid, RcrtType=2, Flag=0)
        with allure.step("预期结果：关闭企业A成功"):
            entborrow_res = group_manage.getEntBorrowList(BEntName=borrowname2)
            isenable = get_api_result(entborrow_res, 'IsEnabled')[0]
            pytest.assume(isenable == 2)

        with allure.step("step2:点击录入名单，选择企业A"):
            res = name_manage.get_entbrorrow()
        with allure.step("预期结果：选择不到企业A"):
            entbrorrowid = get_value(res=res, value=borrowname2, param1='EntBorrowName', param2='EntBorrowId')
            pytest.assume(entbrorrowid == None)

        with allure.step("step3:打开企业A，点击录入名单，选择企业A，填入其他信息，点击确定"):
            group_manage.add_or_update_ent_borrow(CoopEntId=coop_borrow_id, CoopEntName=borrowname2, IsEnabled=1,
                                                  EntId=entid, RcrtType=2, Flag=0)
            res = name_manage.get_entbrorrow()
        with allure.step("预期结果：可以选择到企业A"):
            entbrorrowid = get_value(res=res, value=borrowname2, param1='EntBorrowName', param2='EntBorrowId')
            pytest.assume(entbrorrowid is not None)

        with allure.step("step4:使用企业A录入名单"):
            # 录入名单
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               InterviewDate=nowtime,
                                               Name=self.name,
                                               IDCardNum=self.idnum,
                                               Gender=1,
                                               TargetSpId=22699,
                                               SpEntID=entbrorrowid
                                               )
        with allure.step("预期结果：提示保存成功，接口返回数据正确"):
            # 接口返回
            status = add_name_res.status_code
            code = add_name_res.json()['Code']
            desc = add_name_res.json()['Desc']
            guid = add_name_res.json()['Data']['Guid']
            nameid = add_name_res.json()['Data']['NameListId']
            rcrttype = add_name_res.json()['Data']['RcrtTyp']
            uuid = add_name_res.json()['Data']['Uuid']
            # 断言
            pytest.assume(status == 200)
            pytest.assume(code == 0)
            pytest.assume(guid == 0)
            pytest.assume(desc == '成功')
            pytest.assume(rcrttype == 2)
            pytest.assume(uuid == 0)

    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('手工录入-关闭标准企业')
    @allure.severity('critical')
    def test_namelist_0007(self, group_manage, name_manage, weblogin, borrowent):
        """手工录入-关闭标准企业"""
        print('\n{}测试开始\n'.format(self.test_namelist_0007.__name__))
        borrowname3 = borrowent[1]
        res = group_manage.getEntBorrowList(BEntName=borrowname3)
        ent_full_name = res['Data']['RecordList'][0]['EntName']
        res = group_manage.get_pay_salary_ent_list(EntFullName=ent_full_name)
        t_ent_id3 = res['Data']['RecordList'][0]['TEntId']
        ent_name3 = res['Data']['RecordList'][0]['EntShortName']
        with allure.step("step1:关闭标准企业A"):
            group_manage.mod_pay_salary_ent_coop_sts(CoopSts=2, TEntId=t_ent_id3)
        with allure.step("预期结果：关闭成功"):
            res = name_manage.get_ent(entname=ent_name3, CoopSts=0)
            CoopSts = get_value(res, ent_name3, 'EntShortName', 'CoopSts')
            pytest.assume(CoopSts == 2)

        with allure.step("step2:点击录入名单，选择标准企业A下的企业"):
            res2 = name_manage.get_entbrorrow()
        with allure.step("预期结果：查询不到标准企业A下的企业"):
            entbrorrowid = get_value(res=res2, value=borrowname3, param1='EntBorrowName', param2='EntBorrowName')
            pytest.assume(entbrorrowid == None)

        with allure.step("step3:打开标准企业A"):
            group_manage.mod_pay_salary_ent_coop_sts(CoopSts=1, TEntId=t_ent_id3)
        with allure.step("预期结果：打开成功"):
            res = name_manage.get_ent(entname=ent_name3, CoopSts=0)
            CoopSts = get_api_result(res, 'CoopSts')[0]
            pytest.assume(CoopSts == 1)

        with allure.step("step4:使用企业A录入名单"):
            res = name_manage.get_entbrorrow()
            entbrorrowid = get_value(res=res, value=borrowname3, param1='EntBorrowName', param2='EntBorrowId')
            # 录入名单
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               InterviewDate=nowtime,
                                               Name=self.name,
                                               IDCardNum=self.idnum,
                                               Gender=1,
                                               TargetSpId=22699,
                                               SpEntID=entbrorrowid
                                               )
        with allure.step("预期结果：提示保存成功，接口返回数据正确"):
            # 接口返回
            status = add_name_res.status_code
            code = add_name_res.json()['Code']
            desc = add_name_res.json()['Desc']
            guid = add_name_res.json()['Data']['Guid']
            rcrttype = add_name_res.json()['Data']['RcrtTyp']
            uuid = add_name_res.json()['Data']['Uuid']
            # 断言
            pytest.assume(status == 200)
            pytest.assume(code == 0)
            pytest.assume(guid == 0)
            pytest.assume(desc == '成功')
            pytest.assume(rcrttype == 2)
            pytest.assume(uuid == 0)

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('名单设置来源')
    @allure.severity('critical')
    def test_namelist_0016(self, weblogin, name_manage, borrow_randow_fuction, random_agent):
        """
        名单设置来源
        """
        borrowid1 = borrow_randow_fuction[0]
        from_sp_name1 = random_agent[1]
        print('\n{}测试开始\n'.format(self.test_namelist_0016.__name__))

        with allure.step("step1:录入一个不带来源的名单"):
            # 录入名单
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               InterviewDate=nowtime,
                                               Name=self.name,
                                               IDCardNum=self.idnum,
                                               Gender=1,
                                               TargetSpId=22699,
                                               SpEntID=borrowid1
                                               )
        with allure.step("预期结果：录入成功"):
            # 接口返回
            status = add_name_res.status_code
            code = add_name_res.json()['Code']
            desc = add_name_res.json()['Desc']
            guid = add_name_res.json()['Data']['Guid']
            nameid = add_name_res.json()['Data']['NameListId']
            rcrttype = add_name_res.json()['Data']['RcrtTyp']
            uuid = add_name_res.json()['Data']['Uuid']
            # 断言
            pytest.assume(status == 200)
            pytest.assume(code == 0)
            pytest.assume(guid == 0)
            pytest.assume(desc == '成功')
            pytest.assume(rcrttype == 2)
            pytest.assume(uuid == 0)

        with allure.step("step2: 选择该条名单，设置来源"):
            lst_nameid = []
            lst_nameid.append(nameid)
            res = name_manage.set_source(from_sp_name1, lst_nameid)
        with allure.step("预期结果1：设置来源成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['ResultList'][0]['IsOk'] == 1)
            pytest.assume(res['Data']['ResultList'][0]['NameListId'] == nameid)
        with allure.step("预期结果2：数据库落name_list表成功，srce_sp_id、srce_tenant_coop_id、srce_sp_short_name字段正确"):
            # 构造sql
            sql1 = "select srce_sp_short_name from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(
                nowtime, self.idnum)
            # 查询数据库
            db_name_list_res = self.db.selectsql(sql1)
            name_list_srce_sp_short_name = db_name_list_res[0][0]
            # 断言
            pytest.assume(name_list_srce_sp_short_name == from_sp_name1)

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('名单设置来源')
    @allure.severity('critical')
    def test_namelist_0016_2(self, weblogin, name_manage, random_agent, add_name_interview):
        """
        名单设置来源

        """
        from_sp_name1 = random_agent[1]
        nameid = add_name_interview[0]
        idnum = add_name_interview[1]
        lst_nameid = [nameid]
        print('\n{}测试开始\n'.format(self.test_namelist_0016.__name__))

        with allure.step("step3: 选择该条名单，修改来源"):
            res = name_manage.set_source(from_sp_name1, lst_nameid)
        with allure.step("预期结果1：修改来源成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['ResultList'][0]['IsOk'] == 1)
            pytest.assume(res['Data']['ResultList'][0]['NameListId'] == nameid)
        with allure.step("预期结果2：数据库落name_list表成功，srce_sp_id、srce_tenant_coop_id、srce_sp_short_name字段正确"):
            # 构造sql
            sql1 = "select srce_sp_short_name from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(
                nowtime, idnum)
            # 查询数据库
            db_name_list_res = self.db.selectsql(sql1)
            name_list_srce_sp_short_name = db_name_list_res[0][0]
            # 断言
            pytest.assume(name_list_srce_sp_short_name == from_sp_name1)


    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('名单设置面试状态')
    @allure.severity('critical')
    @pytest.mark.parametrize("IntvSts,IntvStsCode,IntvRemark", [(0, None, None),
                                                                (1, None, None),
                                                                (2, None, None),
                                                                (3, 3, None),
                                                                (3, 0, 'test'),
                                                                (4, 3, None)])
    def test_namelist_0017(self, add_name_interview, IntvSts, IntvStsCode, IntvRemark, name_manage):
        """名单设置面试状态"""
        print('\n{}测试开始\n'.format(self.test_namelist_0016.__name__))
        nameid = add_name_interview[0]
        idnum = add_name_interview[1]
        with allure.step("step2:设置面试状态为{}".format(IntvSts)):
            namelist = [nameid]
            res = name_manage.set_interview_state(IntvSts=IntvSts, NameIdList=namelist, IntvStsCode=IntvStsCode,
                                                  IntvRemark=IntvRemark)
        with allure.step("预期结果1：面试状态设置成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['SuccCount'] == 1)
        with allure.step("预期结果2：数据库落表成功"):
            # 构造sql
            sql1 = "select * from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            # 查询数据库
            db_name_list_res = self.db.selectsql(sql1)
            intv_sts = db_name_list_res[0][26]
            intv_remark = db_name_list_res[0][27]
            intv_sts_code = db_name_list_res[0][28]
            # 断言
            if not IntvRemark:
                IntvRemark = ''
            if not IntvStsCode:
                IntvStsCode = 0
            pytest.assume(intv_sts == IntvSts)
            pytest.assume(intv_remark == IntvRemark)
            pytest.assume(intv_sts_code == IntvStsCode)

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('名单修改备注')
    @allure.severity('critical')
    def test_namelist_0018(self, add_name_interview, name_manage):
        """名单修改备注"""
        print('\n{}测试开始\n'.format(self.test_namelist_0018.__name__))
        nameid = add_name_interview[0]
        idnum = add_name_interview[1]
        with allure.step("step1:选择一条名单，点击修改备注，点击确定"):
            namelist = [nameid]
            res = name_manage.modified_remark(NameIdList=namelist, Remark='test1')
        with allure.step("预期结果1：修改成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['FailureList'] == [])
            pytest.assume(res['Data']['SuccessList'] == namelist)
        with allure.step("预期结果2：数据库name_list表remark字段的值和输入的一致"):
            # 构造sql
            sql1 = "select remark from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            # 查询数据库
            db = self.db.selectsql(sql1)
            pytest.assume(db[0][0] == 'test1')

        with allure.step("step2:再次修改该条名单备注"):
            namelist = [nameid]
            res = name_manage.modified_remark(NameIdList=namelist, Remark='test2')
        with allure.step("预期结果1：修改成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['FailureList'] == [])
            pytest.assume(res['Data']['SuccessList'] == namelist)
        with allure.step("预期结果2：数据库name_list表remark字段的值和输入的一致"):
            # 构造sql
            sql1 = "select remark from name_list where intv_dt='{0}' and mbr_id_card_num='{1}'".format(nowtime, idnum)
            # 查询数据库
            db = self.db.selectsql(sql1)
            pytest.assume(db[0][0] == 'test2')

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('查看列表不脱敏信息')
    @allure.severity('critical')
    def test_namelist_0022(self, add_name_interview, name_manage):
        """查看列表不脱敏信息"""
        print('\n{}测试开始\n'.format(self.test_namelist_0022.__name__))
        idnum = add_name_interview[1]
        mobile = add_name_interview[2]
        res1 = name_manage.get_nameList()
        encrypt_idnum = get_api_result(res1, 'IDCardNum')[0]
        encrypt_mobile = get_api_result(res1, 'Mobile')[0]
        with allure.step("step1:点击列表手机号码字段"):
            res2 = name_manage.decryptAPI(DesenData=encrypt_mobile, Typ=1)
        with allure.step("预期结果：展示不脱敏信息，信息正确"):
            pytest.assume(res2['Code'] == 0)
            pytest.assume(res2['Desc'] == '成功')
            pytest.assume(res2['Data']['OriData'] == mobile)
            pytest.assume(res2['Data']['DesenData'] == encrypt_mobile)
            pytest.assume(res2['Data']['Typ'] == 1)

        with allure.step("step2:点击列表身份证信息字段"):
            res = name_manage.decryptAPI(DesenData=encrypt_idnum, Typ=2)
        with allure.step("预期结果：展示不脱敏信息，信息正确"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['OriData'] == idnum)
            pytest.assume(res['Data']['DesenData'] == encrypt_idnum)
            pytest.assume(res['Data']['Typ'] == 2)

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('检查扫描记录')
    @allure.severity('critical')
    def test_namelist_0023(self, add_name_interview, weblogin, name_manage, borrow_randow_fuction, random_agent):
        """检查扫描记录"""
        print('\n{}测试开始\n'.format(self.test_namelist_0023.__name__))
        with allure.step("step1:点击列表扫描人字段"):
            nameid = add_name_interview[0]
            idnum = add_name_interview[1]
            mobile = add_name_interview[2]
            name = add_name_interview[3]
            borrowname = add_name_interview[5]
            agentid = add_name_interview[6]
            agentname = add_name_interview[7]
            res = name_manage.getScanRecordFZT(nameid)
        with allure.step("预期结果：弹出扫描记录弹窗，扫描记录正确"):
            data = res['Data']['RecordList']
            pytest.assume(mobile == data[0]['Mobile'])
            pytest.assume(agentname == data[0]['FromSpName'])
            pytest.assume(weblogin.zt_guid == data[0]['ScannerId'])
            pytest.assume(weblogin.Name == data[0]['ScannerName'])
            pytest.assume(borrowname == data[0]['SpEntName'])

        with allure.step("step2:重新录入名单，更换工种"):
            borrowname2 = borrow_randow_fuction[1]
            borrowid2 = borrow_randow_fuction[0]
            # 录名单
            weblogin.create_api(url=AddNameForOpenAPI,
                                SpEntID=borrowid2,
                                FromSpID=agentid,
                                FromSpName=agentname,
                                TargetSpId=22699,
                                SpName='奇迹劳务',
                                InputType=2,
                                InterviewStatus=0,
                                InterviewStatusDCode=None,
                                InterviewStatusRemark=None,
                                InterviewDate=nowtime,
                                Name=name,
                                Mobile=mobile,
                                IDCardNum=idnum,
                                Nation='汉',
                                Addr='测试地址',
                                Gender=1,
                                Remark='测试备注',
                                IDCardExprDate='2030-06-01',
                                ContactMobile=mobile,
                                )
            # 检查扫描记录
            res = name_manage.getScanRecordFZT(nameid)
        with allure.step("预期结果：扫描记录新增一条"):
            data = res['Data']['RecordList']
            pytest.assume(mobile == data[0]['Mobile'])
            pytest.assume(agentname == data[0]['FromSpName'])
            pytest.assume(weblogin.zt_guid == data[0]['ScannerId'])
            pytest.assume(weblogin.Name == data[0]['ScannerName'])
            pytest.assume(borrowname == data[0]['SpEntName'])
            pytest.assume(mobile == data[1]['Mobile'])
            pytest.assume(agentname == data[1]['FromSpName'])
            pytest.assume(weblogin.zt_guid == data[1]['ScannerId'])
            pytest.assume(weblogin.Name == data[1]['ScannerName'])
            pytest.assume(borrowname2 == data[1]['SpEntName'])

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('检查名单绑订单')
    @allure.severity('critical')
    def test_namelist_0025(self, name_manage, order_manage, borrow_randow_fuction, random_agent):
        """检查名单绑订单"""
        print('\n{}测试开始\n'.format(self.test_namelist_0025.__name__))
        with allure.step("预置条件：名单和订单日期、来源、企业一致"):
            # 定义参数
            borrowid = borrow_randow_fuction[0]
            borrowname = borrow_randow_fuction[1]
            agentid = random_agent[0]
            agentname = random_agent[1]
            # 录名单
            name_res = name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=agentname)
            nameid = name_res['Data']['NameListId']
            # 创建订单
            order_res = order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            order_manage.publishOrderToSupplier(agentname=agentname, OrderId=order_manage.orderid)
            # 查询订单
            res = order_manage.get_orders(EntName=borrowname, agentname=agentname, OrderStatus=2)
            OrderAgencyFee = res['Data']['RecordList'][0]['OrderAgencyFee']
            OrderServiceFee = res['Data']['RecordList'][0]['OrderServiceFee']
            OrderWeekFeeList = res['Data']['RecordList'][0]['OrderWeekFeeList']
            OrderNo = res['Data']['RecordList'][0]['OrderNo']
            QuotaCount = res['Data']['RecordList'][0]['QuotaCount']
            Remark = res['Data']['RecordList'][0]['Remark']
        with allure.step("step1:选择名单，点击绑定可预支订单"):
            res = name_manage.get_waitbindorder_pq(EntId=borrowid, FromSpId=agentid, NameListIds=[nameid])
        with allure.step("预期结果：弹出绑定窗口，有可预支订单"):
            data = res['Data']['RecordList']
            pytest.assume(len(data) > 0)
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(data[0]['MainOrderId'] == order_manage.orderid)
            pytest.assume(data[0]['OrderAgencyFee'] == OrderAgencyFee)
            pytest.assume(data[0]['OrderServiceFee'] == OrderServiceFee)
            pytest.assume(data[0]['OrderWeekFeeList'] == OrderWeekFeeList)
            pytest.assume(data[0]['OrderNo'] == OrderNo)
            pytest.assume(data[0]['QuotaCount'] == QuotaCount)
            pytest.assume(data[0]['Remark'] == Remark)
            pytest.assume(data[0]['SpEntName'] == borrowname)

        with allure.step("step2:选择一条订单记录，点击确定"):
            res = name_manage.bind_order(orderid=order_manage.orderid, namelist=[nameid])
        with allure.step("预期结果：绑定成功，页面显示订单编号和信息，name_list表中orderid落表成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == '成功1人,失败0人')
        with allure.step("预期结果2：检查namelist表srce_rcrt_order_id字段"):
            sql = "SELECT srce_rcrt_order_id FROM name_list WHERE mbr_id_card_num = '{0}' and intv_dt = '{1}'".format(
                name_manage.newidnum_pq, nowtime)
            db_res = self.db.selectsql(sql)
            pytest.assume(db_res[0][0] == order_manage.orderid)

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('名单没有来源绑定订单')
    @allure.severity('critical')
    def test_namelist_0026(self, name_manage, order_manage, borrow_randow_fuction, random_agent):
        """名单没有来源绑定订单"""
        print('\n{}测试开始\n'.format(self.test_namelist_0026.__name__))
        with allure.step("预置条件:名单和订单日期、企业一致,名单没有来源"):
            # 定义参数
            borrowid = borrow_randow_fuction[0]
            borrowname = borrow_randow_fuction[1]
            agentid = random_agent[0]
            agentname = random_agent[1]
            # 录名单
            name_res = name_manage.add_name_pq(entbrorrowname=borrowname)
            nameid = name_res['Data']['NameListId']
            # 创建订单
            order_res = order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            order_manage.publishOrderToSupplier(agentname=agentname, OrderId=order_manage.orderid)

        with allure.step("step1:选择名单，点击绑定可预支订单"):
            res = name_manage.get_waitbindorder_pq(EntId=borrowid, FromSpId=0, NameListIds=[nameid])
        with allure.step("预期结果：提示请先设置来源"):
            pytest.assume(res['Code'] == 65043)
            pytest.assume(res['Desc'] == '请设置名单来源再绑定订单')
            pytest.assume(res['Data'] == {"RecordList": []})

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('名单和订单企业不一致')
    @allure.severity('critical')
    def test_namelist_0027(self, name_manage, order_manage, borrow_randow_fuction, random_agent):
        """名单和订单企业不一致"""
        print('\n{}测试开始\n'.format(self.test_namelist_0027.__name__))
        with allure.step("预置条件:录入名单，创建订单，名单和订单企业不一致"):

            # 定义参数
            borrowid1 = borrow_randow_fuction[0]
            borrowname1 = borrow_randow_fuction[1]
            agentid = random_agent[0]
            agentname = random_agent[1]
            # 随机获取工种
            for i in range(10):
                res = name_manage.get_entbrorrow()
                lst = res['Data']['RecordList']
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowid2 = entborrow_dic['EntBorrowId']
                borrowname2 = entborrow_dic['EntBorrowName']
                if borrowid1 != borrowid2:
                    break

            # 录名单
            name_res = name_manage.add_name_pq(entbrorrowname=borrowname1, FromSpName=agentname)
            nameid = name_res['Data']['NameListId']
            # 创建订单
            order_res = order_manage.create_order_pq(entbrorrowname=borrowname2, ReceiverType=2, PriceUnit=1)
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            order_manage.publishOrderToSupplier(agentname=agentname, OrderId=order_manage.orderid)

        with allure.step("step1:选择名单，点击绑定可预支订单"):
            res = name_manage.get_waitbindorder_pq(EntId=borrowid1, FromSpId=agentid, NameListIds=[nameid])
        with allure.step("预期结果：提示请先设置来源"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == {"RecordList": []})

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('补录及修改手机号码')
    @allure.severity('critical')
    def test_namelist_0028(self, name_manage, borrow_randow_fuction, weblogin):
        """补录及修改手机号码"""
        print('\n{}测试开始\n'.format(self.test_namelist_0028.__name__))
        with allure.step("step1:点击名单记录的手机号码字段,输入手机号码，点击确定"):
            # 录入没有手机号码的名单
            borrowid = borrow_randow_fuction[0]
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               InterviewDate=nowtime,
                                               Name=self.name,
                                               IDCardNum=self.idnum,
                                               Gender=1,
                                               TargetSpId=22699,
                                               SpEntID=borrowid
                                               )
            nameid = add_name_res.json()['Data']['NameListId']
            res = name_manage.modNameListMobile(NameListId=nameid, Mobile=self.mobile)
        with allure.step("预期结果1：补录成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)
        with allure.step("预期结果2：name_list落表成功"):
            sql = "SELECT mobile FROM name_list WHERE mbr_id_card_num = '{0}' and intv_dt = '{1}'".format(self.idnum,
                                                                                                          nowtime)
            db_res = self.db.selectsql(sql)
            pytest.assume(db_res[0][0] == self.mobile)

        with allure.step("step2:修改手机号码，点击确定"):
            new_mobile = create_phone()
            res = name_manage.modNameListMobile(NameListId=nameid, Mobile=new_mobile)
        with allure.step("预期结果1：修改成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)
        with allure.step("预期结果2：name_list落表成功"):
            sql = "SELECT mobile FROM name_list WHERE mbr_id_card_num = '{0}' and intv_dt = '{1}'".format(self.idnum,
                                                                                                          nowtime)
            db_res = self.db.selectsql(sql)
            pytest.assume(db_res[0][0] == new_mobile)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用面试日期查询')
    @allure.severity('critical')
    def test_namelist_0030(self, weblogin, name_manage):
        """使用面试日期查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0030.__name__))
        with allure.step("step1:左右区间为空，点击查询"):
            res1 = weblogin.create_api(GetNameList, RecordIndex=0, RecordSize=10).json()
        with allure.step("预期结果：面试日期为必填项，提示面试日期不为空"):
            pytest.assume(res1['Code'] == 50001)
            pytest.assume(res1['Desc'] == '输入参数错误')
            pytest.assume(res1['Data'] == None)

        with allure.step("step2:左区间不为空，右区间为空，点击查询"):
            res2 = weblogin.create_api(GetNameList, StartTime=nowtime, RecordIndex=0, RecordSize=10).json()
        with allure.step("预期结果：面试日期为必填项，提示面试日期不为空"):
            pytest.assume(res2['Code'] == 50001)
            pytest.assume(res2['Desc'] == '输入参数错误')
            pytest.assume(res2['Data'] == None)

        with allure.step("step3:左区间为空，右区间不为空，点击查询"):
            res3 = weblogin.create_api(GetNameList, EndTime=nowtime, RecordIndex=0, RecordSize=10).json()
        with allure.step("预期结果：面试日期为必填项，提示面试日期不为空"):
            pytest.assume(res3['Code'] == 50001)
            pytest.assume(res3['Desc'] == '输入参数错误')
            pytest.assume(res3['Data'] == None)

        with allure.step("step4:左右区间都不为空，点击查询"):
            res4 = weblogin.create_api(GetNameList, StartTime=nowtime, EndTime=nowtime, InterviewStatus=9999,
                                       RcrtTyp=-9999, RecordIndex=0, RecordSize=10, SpIds=[22699]).json()
        with allure.step("预期结果：查询到对应数据，无数据返回空列表"):
            sql0 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (intv_sts = '0') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            sql2 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (intv_sts = '2') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            sql3 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (intv_sts = '3') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            sql4 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (intv_sts = '4') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            sql5 = "SELECT * FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (is_deleted = 0) AND (tenant_id = '1000005') ORDER BY intv_dt DESC,created_tm DESC LIMIT 10 OFFSET 0".format(
                nowtime)
            db_res0 = self.db.selectsql(sql0)
            db_res1 = self.db.selectsql(sql1)
            db_res2 = self.db.selectsql(sql2)
            db_res3 = self.db.selectsql(sql3)
            db_res4 = self.db.selectsql(sql4)
            db_res5 = self.db.selectsql(sql5)
            pytest.assume(res4['Code'] == 0)
            pytest.assume(res4['Desc'] == '成功')
            pytest.assume(res4['Data']['RecordCount'] == db_res0[0][0])
            pytest.assume(res4['Data']['UnHandleCnt'] == db_res1[0][0])
            pytest.assume(res4['Data']['PassCnt'] == db_res2[0][0])
            pytest.assume(res4['Data']['AbandonCnt'] == db_res4[0][0])
            data = res4['Data']['RecordList']
            for i in range(len(data)):
                pytest.assume(data[i]['FromSpID'] == db_res5[i][17])
                pytest.assume(data[i]['FromSpName'] == db_res5[i][18])
                pytest.assume(data[i]['Gender'] == db_res5[i][6])
                pytest.assume(data[i]['InterviewStatus'] == db_res5[i][26])
                if db_res5[i][27] and data[i]['InterviewStatusRemark']: pytest.assume(
                    data[i]['InterviewStatusRemark'] == db_res5[i][27])
                if db_res5[i][28] and data[i]['InterviewStatusDCode']: pytest.assume(
                    data[i]['InterviewStatusDCode'] == db_res5[i][28])
                pytest.assume(data[i]['Name'] == db_res5[i][4])
                pytest.assume(data[i]['NameID'] == db_res5[i][0])
                if db_res5[i][20] and data[i]['FromOrderSeq']: pytest.assume(data[i]['FromOrderSeq'] == db_res5[i][20])
                pytest.assume(data[i]['SpEntID'] == db_res5[i][13])
                pytest.assume(data[i]['SpEntName'] == db_res5[i][14])
                # 解码身份证和手机号码
                idnum = name_manage.decryptAPI(DesenData=data[i]['IDCardNum'], Typ=2)['Data']['OriData']
                mobile = name_manage.decryptAPI(DesenData=data[i]['Mobile'], Typ=1)['Data']['OriData'] if data[i][
                    'Mobile'] else None
                pytest.assume(idnum == db_res5[i][3])
                pytest.assume(mobile == db_res5[i][5])

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用标准企业查询')
    @allure.severity('critical')
    def test_namelist_0031(self, borrow_randow_fuction, name_manage, group_manage, weblogin):
        """使用标准企业查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0031.__name__))
        with allure.step("预置条件"):
            # 录入名单
            borrowname = borrow_randow_fuction[1]
            name_manage.add_name_pq(entbrorrowname=borrowname)
            entfullname = group_manage.get_ent_borrow_list(BEntName=borrowname)['Data']['RecordList'][0]['EntName']
            TEntId = group_manage.get_pay_salary_ent_list(EntFullName=entfullname)['Data']['RecordList'][0]['TEntId']
            entshortname = group_manage.get_pay_salary_ent_list(EntFullName=entfullname)['Data']['RecordList'][0][
                'EntShortName']
            entid = group_manage.getTenantEntListByName(CoopSts=0, Name=entshortname)['Data']['RecordList'][0]['EntId']

        with allure.step("step1:使用启用的标准企业查询"):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       EntIds=[entid],
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到对应标准企业的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (ent_id in ('{1}')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, entid)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = res1['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res1['Data']['RecordList'][i]['EntShortName'] == entshortname)

        with allure.step("step2:使用未开启的标准企业查询"):
            # 关闭标准企业
            group_manage.mod_pay_salary_ent_coop_sts(CoopSts=2, TEntId=TEntId)
            res2 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       EntIds=[entid],
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到对应标准企业的名单"):
            sql2 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (ent_id in ('{1}')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, entid)
            db_res2 = self.db.selectsql(sql2)
            pytest.assume(db_res2[0][0] == res2['Data']['RecordCount'])
            pytest.assume(res2['Code'] == 0)
            pytest.assume(res2['Desc'] == '成功')
            n = res2['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res2['Data']['RecordList'][i]['EntShortName'] == entshortname)

        with allure.step("恢复环境：打开标准企业"):
            group_manage.mod_pay_salary_ent_coop_sts(CoopSts=1, TEntId=TEntId)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用企业查询')
    @allure.severity('critical')
    def test_namelist_0032(self, weblogin, borrow_randow_fuction, name_manage, group_manage):
        """使用企业查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0032.__name__))
        with allure.step("预置条件："):
            borrowid = borrow_randow_fuction[0]
            borrowname = borrow_randow_fuction[1]
            res1 = group_manage.get_ent_borrow_list(BEntName=borrowname)
            coop_entid = res1['Data']['RecordList'][0]['EntBorrowId']

            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname)

        with allure.step("step1：使用启用的企业查询"):
            res2 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       SpEntName=borrowname,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()

        with allure.step("预期结果：查询到对应企业的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (sp_ent_name like '%{1}%') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, borrowname)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res2['Data']['RecordCount'])
            pytest.assume(res2['Code'] == 0)
            pytest.assume(res2['Desc'] == '成功')
            n = res2['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res2['Data']['RecordList'][i]['SpEntName'] == borrowname)

        with allure.step("step2:使用未开启的企业查询"):
            # 关闭标准企业
            group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=coop_entid, EntId=borrowid,
                                                  IsEnabled=2, RcrtType=2)
            res3 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       SpEntName=borrowname,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到对应企业的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (sp_ent_name like '%{1}%') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, borrowname)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res3['Data']['RecordCount'])
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            n = res3['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res3['Data']['RecordList'][i]['SpEntName'] == borrowname)

        with allure.step("step3:使用企业部分关键字查询"):
            res3 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       SpEntName=borrowname[0:2],
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到对应企业的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (sp_ent_name like '%{1}%') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, borrowname[0:2])
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res3['Data']['RecordCount'])
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            n = res3['Data']['RecordCount']
            for i in range(n):
                pytest.assume(borrowname[0:2] in res3['Data']['RecordList'][i]['SpEntName'])

        with allure.step("恢复环境：打开企业"):
            group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=coop_entid, EntId=borrowid,
                                                  IsEnabled=1, RcrtType=2)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用谁送给我查询')
    @allure.severity('critical')
    def test_namelist_0033(self, weblogin, group_manage, borrow_randow_fuction, random_agent, name_manage):
        """使用谁送给我查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0033.__name__))
        with allure.step("预置条件："):
            agentname = random_agent[1]
            agentid = random_agent[0]
            borrowname = borrow_randow_fuction[1]
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=agentname)

        with allure.step("step1：使用合作中的来源查询"):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       FromSpId=agentid,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：可以查询到对应的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (srce_tenant_coop_id in ('{1}')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, agentid)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = res1['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res1['Data']['RecordList'][i]['FromSpName'] == agentname)

        with allure.step("step2：使用不合作的来源查询"):
            coop_res = group_manage.getcooplist(NickName=agentname)
            coop_id = coop_res['Data']['RecordList'][0]['SupplierId']
            group_manage.updateCoop(CoopId=coop_id, CooperationStatus=2, CooperationStatusOnly=1)
        with allure.step("预期结果：可以查询到对应的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (srce_tenant_coop_id in ('{1}')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, agentid)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = res1['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res1['Data']['RecordList'][i]['FromSpName'] == agentname)

        with allure.step("恢复环境：打开供应商合作关系"):
            group_manage.updateCoop(CoopId=coop_id, CooperationStatus=1, CooperationStatusOnly=1)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用姓名查询')
    @allure.severity('critical')
    def test_namelist_0034(self, weblogin, add_name_interview, name_manage):
        """使用姓名查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0034.__name__))
        with allure.step("step1：使用存在的姓名查询"):
            name = add_name_interview[3]
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       Name=name,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：可以查询到对应的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (real_name = '{1}') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, name)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = res1['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res1['Data']['RecordList'][i]['Name'] == name)

        with allure.step("step1：使用不存在的姓名查询"):
            res2 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       Name='123@#',
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("查询不到对应名单"):
            pytest.assume(res2['Data']['RecordCount'] == 0)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用身份证号查询')
    @allure.severity('critical')
    def test_namelist_0035(self, weblogin, add_name_interview):
        """使用身份证号查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0035.__name__))
        with allure.step("step1:使用存在的身份证号码查询"):
            idnum = add_name_interview[1]
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       IDCardNum=idnum,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果:查询到对应名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (mbr_id_card_num like '{1}%') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, idnum)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            pytest.assume(res1['Data']['RecordList'][0]['IDCardNum'] == idnum)

        with allure.step("step2：使用不存在的身份证号码查询"):
            res2 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       IDCardNum='1233211231233212',
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询不到名单"):
            pytest.assume(res2['Data']['RecordCount'] == 0)

        with allure.step("使用身份证号码部分字段查询"):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       IDCardNum=idnum[0:-3],
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果:查询到对应名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (mbr_id_card_num like '{1}%') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, idnum)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            pytest.assume(res1['Data']['RecordList'][0]['IDCardNum'] == idnum)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用手机号码查询')
    @allure.severity('critical')
    def test_namelist_0036(self, weblogin, add_name_interview):
        """使用手机号码查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0036.__name__))
        with allure.step("step1：使用存在的手机号码查询"):
            mobile = add_name_interview[2]
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       Mobile=mobile,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("查询到对应名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (mobile = '{1}') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, mobile)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            pytest.assume(res1['Data']['RecordList'][0]['Mobile'] == mobile)

        with allure.step("step2：使用不存在的手机号码查询"):
            res2 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       Mobile='10000000000',
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("查询到对应名单"):
            pytest.assume(res2['Data']['RecordCount'] == 0)

        with allure.step("step3：使用手机号码部分字段查询"):
            res3 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       Mobile=mobile[0:-2],
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("查询到对应名单"):
            pytest.assume(res3['Data']['RecordCount'] == 0)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用扫描人查询')
    @allure.severity('critical')
    def test_namelist_0037(self, weblogin, add_name_interview):
        """使用扫描人查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0037.__name__))
        with allure.step("step1：使用在职状态扫描人查询"):
            res = weblogin.create_api(GetNameList,
                                      StartTime=nowtime,
                                      EndTime=nowtime,
                                      ScannerUserID=weblogin.zt_guid,
                                      InterviewStatus=9999,
                                      RcrtTyp=-9999,
                                      RecordIndex=0,
                                      RecordSize=9999,
                                      SpIds=[22699]).json()
        with allure.step("预期结果：可以查询到对应的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (scanner_id in ('{1}')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, weblogin.zt_guid)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res['Data']['RecordCount'])
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            n = res['Data']['RecordCount']
            for i in range(n):
                pytest.assume(res['Data']['RecordList'][i]['ScannerName'] == weblogin.Name)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用设置检查查询')
    @allure.severity('critical')
    def test_namelist_0038(self, weblogin):
        """使用设置检查查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0038.__name__))
        """使用扫描人查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0037.__name__))
        with allure.step("step1：使用未设置来源查询"):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       CheckType=1,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：可以查询到对应的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (srce_sp_id in ('0')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = len(res1['Data']['RecordList'])
            if n > 0:
                for i in range(n):
                    pytest.assume(res1['Data']['RecordList'][i]['FromSpID'] == 0)

        with allure.step("step2：使用未绑单查询"):
            res2 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       CheckType=3,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：可以查询到对应的名单"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (srce_rcrt_order_id in ('0')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res2['Data']['RecordCount'])
            pytest.assume(res2['Code'] == 0)
            pytest.assume(res2['Desc'] == '成功')
            lst = res2['Data']['RecordList']
            n2 = len(lst)
            if n2 > 0:
                for i in range(n2):
                    pytest.assume(lst[i]['FromOrderSeq'] == '')

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用性别查询')
    @allure.severity('critical')
    @pytest.mark.parametrize('Gender', [1, 2])
    def test_namelist_0039(self, weblogin, Gender):
        """使用性别查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0039.__name__))
        dic = {1: '男', 2: '女'}
        with allure.step("step1：使用性别{}查询".format(dic[Gender])):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       Gender=Gender,
                                       InterviewStatus=9999,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到性别为{}的名单".format(dic[Gender])):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (gender = '{1}') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, Gender)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = len(res1['Data']['RecordList'])
            if n > 0:
                for i in range(n):
                    pytest.assume(res1['Data']['RecordList'][i]['Gender'] == Gender)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用面试状态查询')
    @allure.severity('critical')
    @pytest.mark.parametrize('InterviewStatus', [0, 1, 2, 3, 4])
    def test_namelist_0040(self, weblogin, InterviewStatus):
        """使用面试状态查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0040.__name__))
        dic = {0: '未处理', 1: '未面试', 2: '面试通过', 3: '面试不通过', 4: '放弃'}
        with allure.step("step1：使用面试状态{}查询".format(dic[InterviewStatus])):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       InterviewStatus=InterviewStatus,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到面试状态为{}的名单".format(dic[InterviewStatus])):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (intv_sts = '{1}') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, InterviewStatus)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = len(res1['Data']['RecordList'])
            if n > 0:
                for i in range(n):
                    pytest.assume(res1['Data']['RecordList'][i]['InterviewStatus'] == InterviewStatus)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用企业类型查询')
    @allure.severity('critical')
    @pytest.mark.parametrize('RcrtTyp', [2, 0])
    def test_namelist_0041(self, weblogin, RcrtTyp):
        """使用企业类型查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0041.__name__))
        dic = {2: '预支', 0: '范围'}
        with allure.step("step1：使用{}查询".format(dic[RcrtTyp])):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       InterviewStatus=9999,
                                       RcrtTyp=RcrtTyp,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到{}数据".format(dic[RcrtTyp])):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (rcrt_typ = '{1}') AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, RcrtTyp)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = len(res1['Data']['RecordList'])
            if n > 0:
                for i in range(n):
                    pytest.assume(res1['Data']['RecordList'][i]['RcrtTyp'] == RcrtTyp)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用订单编号查询')
    @allure.severity('critical')
    def test_namelist_0042(self, weblogin, name_bind_order):
        """使用订单编号查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0042.__name__))
        with allure.step("step1：使用存在的订单编号查询"):
            OrderNo = name_bind_order[0]
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       InterviewStatus=9999,
                                       OrderNo=OrderNo,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到对应的数据"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (srce_rcrt_order_id in ('100{1}')) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime, OrderNo[-4:])
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = len(res1['Data']['RecordList'])
            if n > 0:
                for i in range(n):
                    pytest.assume(res1['Data']['RecordList'][i]['OrderNo'] == OrderNo)

        with allure.step("step2：使用不存在的订单编号查询"):
            res2 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       InterviewStatus=9999,
                                       OrderNo='1234567',
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：返回空列表"):
            pytest.assume(res2['Data']['RecordCount'] == 0)

    @allure.feature('实接记录')
    @allure.story('查询')
    @allure.title('使用订单绑定状态查询')
    @allure.severity('critical')
    def test_namelist_0043(self, weblogin):
        """使用订单绑定状态查询"""
        print('\n{}测试开始\n'.format(self.test_namelist_0043.__name__))
        with allure.step("step1：使用已绑单查询"):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       InterviewStatus=9999,
                                       FromBindStatus=1,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到已绑单数据"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (srce_rcrt_order_id > 0) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = len(res1['Data']['RecordList'])
            if n > 0:
                for i in range(n):
                    print('i', i)
                    print('FromOrderSeq', res1['Data']['RecordList'][i]['FromOrderSeq'])
                    pytest.assume(res1['Data']['RecordList'][i]['FromOrderSeq'] != '')

        with allure.step("step1：使用未绑单查询"):
            res1 = weblogin.create_api(GetNameList,
                                       StartTime=nowtime,
                                       EndTime=nowtime,
                                       InterviewStatus=9999,
                                       FromBindStatus=2,
                                       RcrtTyp=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       SpIds=[22699]).json()
        with allure.step("预期结果：查询到未绑单数据"):
            sql1 = "SELECT count(*) FROM `name_list`  WHERE (intv_dt = '{0}') AND (sp_id in ('22699')) AND (srce_rcrt_order_id = 0) AND (is_deleted = 0) AND (tenant_id = '1000005')".format(
                nowtime)
            db_res = self.db.selectsql(sql1)
            pytest.assume(db_res[0][0] == res1['Data']['RecordCount'])
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            n = len(res1['Data']['RecordList'])
            if n > 0:
                for i in range(n):
                    pytest.assume(res1['Data']['RecordList'][i]['FromOrderSeq'] == '')

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('批量设置来源')
    @allure.severity('critical')
    def test_namelist_0044(self, weblogin, hundred_name, random_agent, name_manage):
        """批量设置来源"""
        print('\n{}测试开始\n'.format(self.test_namelist_0044.__name__))
        with allure.step("step1:选中100条数据，设置来源"):
            hundred_nameid = hundred_name[0]
            agentid = random_agent[0]
            agentname = random_agent[1]
            res1 = weblogin.create_api(SetSpForOpenAPI,
                                       NameListIds=hundred_nameid,
                                       SpCoopId=agentid,
                                       SpCoopName=agentname).json()
        with allure.step("预期结果：设置成功"):
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            for i in range(100):
                pytest.assume(res1['Data']['ResultList'][i]['IsOk'] == 1)
                pytest.assume(res1['Data']['ResultList'][i]['NameListId'] in hundred_nameid)

        with allure.step("step2:选中101条数据，设置来源"):
            hundred_nameid = hundred_name[1]
            res2 = weblogin.create_api(SetSpForOpenAPI,
                                       NameListIds=hundred_nameid,
                                       SpCoopId=agentid,
                                       SpCoopName=agentname).json()
        with allure.step("预期结果：设置失败，提示最大只能设置100条"):
            pytest.assume(res2['Code'] == 65086)
            pytest.assume(res2['Data']['ResultList'] == None)
            pytest.assume(res2['Desc'] == '抱歉，每次仅能操作最多100条数据')

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('批量设置面试状态')
    @allure.severity('critical')
    @pytest.mark.parametrize('IntvSts', [0, 1, 2, 3, 4])
    def test_namelist_0045(self, weblogin, hundred_name, IntvSts, name_manage):
        """批量设置面试状态"""
        print('\n{}测试开始\n'.format(self.test_namelist_0045.__name__))
        with allure.step("step1:选中100条数据，设置面试状态"):
            nameid_lst = hundred_name[0]
            res1 = weblogin.create_api(SetIntvSts, IntvSts=IntvSts, NameIdList=nameid_lst).json()
        with allure.step("预期结果：设置成功"):
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            pytest.assume(res1['Data']['SuccCount'] == 100)

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('批量修改备注')
    @allure.severity('critical')
    def test_namelist_0046(self, weblogin, hundred_name, name_manage):
        """批量修改备注"""
        print('\n{}测试开始\n'.format(self.test_namelist_0046.__name__))
        with allure.step("step1:选中100条数据，修改备注"):
            nameid_lst = hundred_name[0]
            res = weblogin.create_api(ModifiedRemark, NameIdList=nameid_lst, Remark='测试备注').json()
        with allure.step("预期结果：修改成功"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['FailureList'] == [])
            for i in res['Data']['SuccessList']:
                pytest.assume(i in nameid_lst)

    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('名单绑订单后重新录入-工种')
    @allure.severity('critical')
    def test_namelist_0047(self, weblogin, name_manage, order_manage, random_agent):
        """名单绑订单后重新录入-工种"""
        print('\n{}测试开始\n'.format(self.test_namelist_0047.__name__))
        with allure.step("预支条件：名单绑定订单"):
            # 随机获取工种
            res = name_manage.get_entbrorrow()
            lst = res['Data']['RecordList']
            entborrow_dic = lst[random.randint(0, len(lst) - 1)]
            EntBorrowName = entborrow_dic['EntBorrowName']
            agentname = random_agent[1]
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=EntBorrowName, FromSpName=agentname)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=EntBorrowName, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=agentname, OrderId=order_manage.orderid)
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])

        with allure.step("step1:更换工种，再次录入名单"):
            # 再次随机更换工种，和上次不一致
            for i in range(10):
                res = name_manage.get_entbrorrow()
                lst = res['Data']['RecordList']
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowname = entborrow_dic['EntBorrowName']
                borrowid = entborrow_dic['EntBorrowId']
                if borrowname != EntBorrowName:
                    break
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               InterviewDate=nowtime,
                                               Name=name_manage.newname_pq,
                                               IDCardNum=name_manage.newidnum_pq,
                                               Gender=1,
                                               TargetSpId=22699,
                                               SpEntID=borrowid
                                               ).json()
            res1 = name_manage.get_nameList(IDCardNum=name_manage.newidnum_pq, Name=name_manage.newname_pq)
        with allure.step("预期结果：录入成功，绑单状态为未绑单"):
            pytest.assume(add_name_res['Code'] == 0)
            pytest.assume(add_name_res['Desc'] == '成功')
            pytest.assume(res1['Data']['RecordList'][0]['FromOrderSeq'] == '')

    @allure.feature('实接记录')
    @allure.story('手工录入')
    @allure.title('名单绑订单后重新录入-来源')
    @allure.severity('critical')
    def test_namelist_0048(self, weblogin, name_manage, order_manage, borrow_randow_fuction):
        """名单绑订单后重新录入-来源"""
        print('\n{}测试开始\n'.format(self.test_namelist_0049.__name__))
        with allure.step("预支条件：名单绑定订单"):
            # 随机获取来源
            res = name_manage.get_source()
            lst = res['Data']['RecordList']
            agent_dic = lst[random.randint(0, len(lst) - 1)]
            SpId = agent_dic['SpId']
            SpShortName = agent_dic['SpShortName']
            borrowid = borrow_randow_fuction[0]
            borrowname = borrow_randow_fuction[0]
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=SpShortName)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=SpShortName, OrderId=order_manage.orderid)
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])

        with allure.step("step1:更换供应商，再次录入名单"):
            # 再次随机更换来源，和上次不一致
            for i in range(10):
                res = name_manage.get_source()
                lst = res['Data']['RecordList']
                agent_dic = lst[random.randint(0, len(lst) - 1)]
                agentid = agent_dic['SpId']
                agentname = agent_dic['SpShortName']
                if agentname != SpShortName:
                    break
            add_name_res = weblogin.create_api(url=AddNameForOpenAPI,
                                               InterviewDate=nowtime,
                                               Name=name_manage.newname_pq,
                                               IDCardNum=name_manage.newidnum_pq,
                                               Gender=1,
                                               TargetSpId=22699,
                                               SpEntID=borrowid,
                                               FromSpID=agentid,
                                               FromSpName=agentname
                                               ).json()
            res1 = name_manage.get_nameList(IDCardNum=name_manage.newidnum_pq, Name=name_manage.newname_pq)
        with allure.step("预期结果：录入成功，绑单状态为未绑单"):
            pytest.assume(add_name_res['Code'] == 0)
            pytest.assume(add_name_res['Desc'] == '成功')
            pytest.assume(res1['Data']['RecordList'][0]['FromOrderSeq'] == '')

    @allure.feature('实接记录')
    @allure.story('功能按钮')
    @allure.title('名单绑订单后修改来源')
    @allure.severity('critical')
    def test_namelist_0049(self, weblogin, name_manage, order_manage, borrow_randow_fuction):
        """名单绑订单后重新录入-来源"""
        print('\n{}测试开始\n'.format(self.test_namelist_0049.__name__))
        with allure.step("预支条件：名单绑定订单"):
            # 随机获取来源
            res = name_manage.get_source()
            lst = res['Data']['RecordList']
            agent_dic = lst[random.randint(0, len(lst) - 1)]
            SpId = agent_dic['SpId']
            SpShortName = agent_dic['SpShortName']
            borrowid = borrow_randow_fuction[0]
            borrowname = borrow_randow_fuction[0]
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=SpShortName)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=SpShortName, OrderId=order_manage.orderid)
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])

        with allure.step("step1:更换供应商"):
            # 再次随机更换来源，和上次不一致
            for i in range(10):
                res = name_manage.get_source()
                lst = res['Data']['RecordList']
                agent_dic = lst[random.randint(0, len(lst) - 1)]
                agentid = agent_dic['SpId']
                agentname = agent_dic['SpShortName']
                if agentname != SpShortName:
                    break
            res1 = weblogin.create_api(SetSpForOpenAPI,
                                       NameListIds=[name_manage.newnameid_pq],
                                       SpCoopId=agentid,
                                       SpCoopName=agentname).json()
            res2 = name_manage.get_nameList(IDCardNum=name_manage.newidnum_pq, Name=name_manage.newname_pq)
        with allure.step("预期结果：录入成功，绑单状态为未绑单"):
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            pytest.assume(res1['Data']['ResultList'][0]['IsOk'] == 1)
            pytest.assume(res2['Data']['RecordList'][0]['FromOrderSeq'] == '')

    @allure.feature('实接记录')
    @allure.story('权限')
    @allure.title('普通驻厂名单查看权限')
    @allure.severity('critical')
    def test_namelist_0050(self, weblogin, group_manage, borrow_randow_fuction):
        """普通驻厂名单查看权限"""
        with allure.step("预置条件：获取普通驻厂账号，并登陆"):
            res = group_manage.get_resident_factory_staff_list(IsCancel=0)
            mobiles = jsonpath.jsonpath(res,'$..Mobile')
            entids = jsonpath.jsonpath(res,'$..EntId')
            n = random.randint(0,len(mobiles))
            login = Web_Login()
            login.login(mobiles[n])
            namemanage = NameList(login)

        with allure.step("step1：检查列表展示的名单数据"):
            res1 = namemanage.get_nameList()