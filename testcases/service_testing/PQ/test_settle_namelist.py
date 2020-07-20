#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 获取根路径
import os
import sys
import time


curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)
from common.business_func.applet_func import Applet_func
from common.login.applet_login import Applet_Login
from common.venv.var import *
from common.data_operation.mysql_db import OperateMDdb
from common.base_utils.comm_utils import *
from common.venv.api_path_zt import *
from common.venv.api_path_mb import *
import pytest, allure
import warnings

warnings.filterwarnings('ignore')


class TestSettleNameList:

    def setup_class(self):
        self.db = OperateMDdb()

    def setup_method(self):
        self.mobile = create_phone()
        self.login = Applet_Login()
        self.login.applogin(tenantype=2, phone=self.mobile)
        self.applet = Applet_func(self.login)

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('生成预支名单1')
    @allure.severity('blocker')
    def test_settle_namelist_0001(self, member_manage, ent, name_manage, order_manage, group_manage, random_agent,
                                  advance_manage):
        """生成预支名单1"""
        with allure.step("预置条件：1、会员三卡认证 2、工牌认证时间大于等于面试日期"):
            # 上传身份证
            self.applet.upload_idcard(fakeridcardpicture)
            idnum = create_IDCard()
            name = create_name()
            # 审核身份证
            member_manage.audit_idcard(phone=self.mobile, idcardnum=idnum, rname=name)

            # 获取工种
            res = group_manage.get_ent_borrow_list(IsEnabled=1, RcrtType=2, EntShortName=ent[0])
            if res['Data']['RecordCount'] != 0:
                lst = res['Data']['RecordList']
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowname = entborrow_dic['EntBorrowName']
            else:
                borrowname = ent[0] + '周薪薪'
                group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=0, EntId=ent[3], IsEnabled=1,
                                                      RcrtType=2, Flag=1)
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1], mobile=self.mobile,
                                    idnum=idnum, name=name)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_manage.orderid)

            # 上传工牌
            self.applet.upload_workcard(workCardFile=workCardpicture, entname=ent[0])
            # 审核工牌
            cardno = create_workcardno()
            member_manage.audit_workcard(entshortname=ent[0], workcardno=cardno, phone=self.mobile)

        with allure.step("step1：名单绑定订单，检查预支名单列表"):
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
        with allure.step("预期结果：生成一条预支名单记录"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == cardno)
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['EntShortName'] == ent[0])
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_manage.newnameid_pq)
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_manage.orderid)
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)

        with allure.step("step2：检查name_list_settle表"):
            name_list_settle_sql = "SELECT * FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            name_list_settle_res = self.db.selectsql(name_list_settle_sql)
            member_user_sql = "SELECT uuid FROM member_user ORDER BY user_id desc limit 1"
            uuid = self.db.selectsql(member_user_sql)[0][0]
        with allure.step(
                "预期结果：name_list_id、id_card_num、real_name、uuid、agent_tenant_coop_id、rcrt_order_id、sp_ent_id、work_card_no等字段正确"):
            pytest.assume(name_list_settle_res[0][1] == name_manage.newnameid_pq)
            pytest.assume(name_list_settle_res[0][2] == idnum)
            pytest.assume(name_list_settle_res[0][3] == name)
            pytest.assume(name_list_settle_res[0][4] == self.mobile)
            pytest.assume(name_list_settle_res[0][5] == uuid)
            pytest.assume(name_list_settle_res[0][14] == borrowname)
            pytest.assume(name_list_settle_res[0][20] == order_manage.orderid)
            pytest.assume(name_list_settle_res[0][21] == 5)
            pytest.assume(name_list_settle_res[0][24] == 1)
            pytest.assume(name_list_settle_res[0][27] == cardno)

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('生成预支名单2')
    @allure.severity('blocker')
    def test_settle_namelist_0002(self, member_manage, ent, name_manage, order_manage, group_manage, random_agent,
                                  advance_manage):
        """生成预支名单2"""
        with allure.step("预置条件：1、会员三卡认证 2、工牌认证时间小于面试日期"):
            # 上传身份证
            self.applet.upload_idcard(fakeridcardpicture)
            idnum = create_IDCard()
            name = create_name()
            # 审核身份证
            member_manage.audit_idcard(phone=self.mobile, idcardnum=idnum, rname=name)
            # 获取工种
            res = group_manage.get_ent_borrow_list(IsEnabled=1, RcrtType=2, EntShortName=ent[0])
            if res['Data']['RecordCount'] != 0:
                lst = res['Data']['RecordList']
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowname = entborrow_dic['EntBorrowName']
            else:
                borrowname = ent[0] + '周薪薪'
                group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=0, EntId=ent[3], IsEnabled=1,
                                                      RcrtType=2, Flag=1)
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1], mobile=self.mobile,
                                    idnum=idnum, name=name, InterviewDate=tomorrow)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1, OrderDt=tomorrow,
                                         BeginDt=tomorrow)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_manage.orderid)

            # 上传工牌
            self.applet.upload_workcard(workCardFile=workCardpicture, entname=ent[0])
            # 审核工牌
            cardno = create_workcardno()
            member_manage.audit_workcard(entshortname=ent[0], workcardno=cardno, phone=self.mobile)

        with allure.step("step1：名单绑定订单，检查预支名单列表"):
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
        with allure.step("预期结果：生成一条预支名单记录"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum, StartDate=tomorrow, EndDate=tomorrow)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['EntShortName'] == ent[0])
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_manage.newnameid_pq)
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_manage.orderid)
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)

        with allure.step("step2：检查name_list_settle表"):
            name_list_settle_sql = "SELECT * FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            name_list_settle_res = self.db.selectsql(name_list_settle_sql)
            member_user_sql = "SELECT uuid FROM member_user ORDER BY user_id desc limit 1"
            uuid = self.db.selectsql(member_user_sql)[0][0]
        with allure.step(
                "预期结果：name_list_id、id_card_num、real_name、uuid、agent_tenant_coop_id、rcrt_order_id、sp_ent_id、work_card_no等字段正确，work_card_no字为空"):
            pytest.assume(name_list_settle_res[0][1] == name_manage.newnameid_pq)
            pytest.assume(name_list_settle_res[0][2] == idnum)
            pytest.assume(name_list_settle_res[0][3] == name)
            pytest.assume(name_list_settle_res[0][4] == self.mobile)
            pytest.assume(name_list_settle_res[0][5] == uuid)
            pytest.assume(name_list_settle_res[0][14] == borrowname)
            pytest.assume(name_list_settle_res[0][20] == order_manage.orderid)
            pytest.assume(name_list_settle_res[0][21] == 5)
            pytest.assume(name_list_settle_res[0][24] == 1)
            pytest.assume(name_list_settle_res[0][27] == '')

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('生成预支名单3')
    @allure.severity('blocker')
    def test_settle_namelist_0003(self, member_manage, ent, name_manage, order_manage, group_manage, random_agent,
                                  advance_manage):
        """生成预支名单3"""
        with allure.step("预置条件：1、会员三卡认证2、工牌认证时间大于等于面试日期3、工牌标准企业和名单企业不对应"):
            # 上传身份证
            self.applet.upload_idcard(fakeridcardpicture)
            idnum = create_IDCard()
            name = create_name()
            # 审核身份证
            member_manage.audit_idcard(phone=self.mobile, idcardnum=idnum, rname=name)
            # 获取工种
            res = group_manage.get_ent_borrow_list(IsEnabled=1, RcrtType=2, EntShortName=ent[0])
            if res['Data']['RecordCount'] != 0:
                lst = res['Data']['RecordList']
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowname = entborrow_dic['EntBorrowName']
            else:
                borrowname = ent[0] + '周薪薪'
                group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=0, EntId=ent[3], IsEnabled=1,
                                                      RcrtType=2, Flag=1)
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1], mobile=self.mobile,
                                    idnum=idnum, name=name)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_manage.orderid)

            # 上传工牌
            self.applet.upload_workcard(workCardFile=workCardpicture, entname=ent[0])
            # 获取和名单不同的标准企业
            res = group_manage.get_pay_salary_ent_list(RecordSize=100)
            lst = res['Data']['RecordList']
            for i in range(100):
                ent_dic = lst[random.randint(0, len(lst) - 1)]
                EntShortName = ent_dic['EntShortName']
                if EntShortName != ent[0]:
                    break
            # 审核工牌
            cardno = create_workcardno()
            member_manage.audit_workcard(entshortname=EntShortName, workcardno=cardno, phone=self.mobile)

        with allure.step("step1：名单绑定订单，检查预支名单列表"):
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
        with allure.step("预期结果：生成一条预支名单记录"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['EntShortName'] == ent[0])
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_manage.newnameid_pq)
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_manage.orderid)
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)

        with allure.step("step2：检查name_list_settle表"):
            name_list_settle_sql = "SELECT * FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            name_list_settle_res = self.db.selectsql(name_list_settle_sql)
            member_user_sql = "SELECT uuid FROM member_user ORDER BY user_id desc limit 1"
            uuid = self.db.selectsql(member_user_sql)[0][0]
        with allure.step(
                "预期结果：name_list_id、id_card_num、real_name、uuid、agent_tenant_coop_id、rcrt_order_id、sp_ent_id、work_card_no等字段正确，work_card_no字为空"):
            pytest.assume(name_list_settle_res[0][1] == name_manage.newnameid_pq)
            pytest.assume(name_list_settle_res[0][2] == idnum)
            pytest.assume(name_list_settle_res[0][3] == name)
            pytest.assume(name_list_settle_res[0][4] == self.mobile)
            pytest.assume(name_list_settle_res[0][5] == uuid)
            pytest.assume(name_list_settle_res[0][14] == borrowname)
            pytest.assume(name_list_settle_res[0][20] == order_manage.orderid)
            pytest.assume(name_list_settle_res[0][21] == 5)
            pytest.assume(name_list_settle_res[0][24] == 1)
            pytest.assume(name_list_settle_res[0][27] == '')

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('生成预支名单4')
    @allure.severity('blocker')
    def test_settle_namelist_0004(self, member_manage, ent, name_manage, order_manage, group_manage, random_agent,
                                  advance_manage):
        """生成预支名单4"""
        with allure.step("预置条件：会员三卡未认证"):
            # 生成未认证过的身份证号码
            for i in range(100):
                idnum = create_IDCard()
                res = member_manage.get_idcardlist(auditsts=2, IdCardNum=idnum)
                if res['Data']['RecordCount'] == 0:
                    break
            name = create_name()
            # 审核身份证
            member_manage.audit_idcard(phone=self.mobile, idcardnum=idnum, rname=name)
            # 获取工种
            res = group_manage.get_ent_borrow_list(IsEnabled=1, RcrtType=2, EntShortName=ent[0])
            if res['Data']['RecordCount'] != 0:
                lst = res['Data']['RecordList']
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowname = entborrow_dic['EntBorrowName']
            else:
                borrowname = ent[0] + '周薪薪'
                group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=0, EntId=ent[3], IsEnabled=1,
                                                      RcrtType=2, Flag=1)
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1], mobile=self.mobile,
                                    idnum=idnum, name=name)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_manage.orderid)

        with allure.step("step1：名单绑定订单，检查预支名单列表"):
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
        with allure.step("预期结果：生成一条预支名单记录"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['EntShortName'] == ent[0])
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_manage.newnameid_pq)
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_manage.orderid)
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)

        with allure.step("step2：检查name_list_settle表"):
            name_list_settle_sql = "SELECT * FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            name_list_settle_res = self.db.selectsql(name_list_settle_sql)
        with allure.step(
                "预期结果：name_list_id、id_card_num、real_name、uuid、agent_tenant_coop_id、rcrt_order_id、sp_ent_id、work_card_no等字段正确，work_card_no字为空"):
            pytest.assume(name_list_settle_res[0][1] == name_manage.newnameid_pq)
            pytest.assume(name_list_settle_res[0][2] == idnum)
            pytest.assume(name_list_settle_res[0][3] == name)
            pytest.assume(name_list_settle_res[0][4] == self.mobile)
            pytest.assume(name_list_settle_res[0][5] == 0)
            pytest.assume(name_list_settle_res[0][14] == borrowname)
            pytest.assume(name_list_settle_res[0][20] == order_manage.orderid)
            pytest.assume(name_list_settle_res[0][21] == 5)
            pytest.assume(name_list_settle_res[0][24] == 1)
            pytest.assume(name_list_settle_res[0][27] == '')

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('生成预支名单5')
    @allure.severity('blocker')
    def test_settle_namelist_0005(self, member_manage, ent, name_manage, order_manage, group_manage, random_agent,
                                  advance_manage):
        """生成预支名单5"""
        with allure.step("预置条件：会员三卡仅认证身份证"):
            # 上传身份证
            self.applet.upload_idcard(fakeridcardpicture)
            # 生成未认证过的身份证号码
            for i in range(100):
                idnum = create_IDCard()
                res = member_manage.get_idcardlist(auditsts=2, IdCardNum=idnum)
                if res['Data']['RecordCount'] == 0:
                    break
            name = create_name()
            # 审核身份证
            member_manage.audit_idcard(phone=self.mobile, idcardnum=idnum, rname=name)
            # 获取工种
            res = group_manage.get_ent_borrow_list(IsEnabled=1, RcrtType=2, EntShortName=ent[0])
            if res['Data']['RecordCount'] != 0:
                lst = res['Data']['RecordList']
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowname = entborrow_dic['EntBorrowName']
            else:
                borrowname = ent[0] + '周薪薪'
                group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=0, EntId=ent[3], IsEnabled=1,
                                                      RcrtType=2, Flag=1)
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1], mobile=self.mobile,
                                    idnum=idnum, name=name)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_manage.orderid)

            # 上传工牌
            self.applet.upload_workcard(workCardFile=workCardpicture, entname=ent[0])

        with allure.step("step1：名单绑定订单，检查预支名单列表"):
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
        with allure.step("预期结果：生成一条预支名单记录"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['EntShortName'] == ent[0])
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_manage.newnameid_pq)
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_manage.orderid)
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)

        with allure.step("step2：检查name_list_settle表"):
            name_list_settle_sql = "SELECT * FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            name_list_settle_res = self.db.selectsql(name_list_settle_sql)
            member_user_sql = "SELECT uuid FROM member_user ORDER BY user_id desc limit 1"
            uuid = self.db.selectsql(member_user_sql)[0][0]
        with allure.step(
                "预期结果：name_list_id、id_card_num、real_name、uuid、agent_tenant_coop_id、rcrt_order_id、sp_ent_id、work_card_no等字段正确，work_card_no字为空"):
            pytest.assume(name_list_settle_res[0][1] == name_manage.newnameid_pq)
            pytest.assume(name_list_settle_res[0][2] == idnum)
            pytest.assume(name_list_settle_res[0][3] == name)
            pytest.assume(name_list_settle_res[0][4] == self.mobile)
            pytest.assume(name_list_settle_res[0][5] == uuid)
            pytest.assume(name_list_settle_res[0][14] == borrowname)
            pytest.assume(name_list_settle_res[0][20] == order_manage.orderid)
            pytest.assume(name_list_settle_res[0][21] == 5)
            pytest.assume(name_list_settle_res[0][24] == 1)
            pytest.assume(name_list_settle_res[0][27] == '')

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('订单模式不同的预支名单')
    @allure.severity('blocker')
    @pytest.mark.parametrize('SettlementTyp', [1, 2, 3, 6])
    def test_settle_namelist_0006(self, member_manage, ent, name_manage, order_manage, group_manage, random_agent,
                                  advance_manage, SettlementTyp, borrow_randow_fuction):
        """订单模式不同的预支名单"""
        with allure.step("预置条件：会员三卡仅认证身份证"):
            idnum = create_IDCard()
            name = create_name()
            # 获取工种
            borrowname = borrow_randow_fuction[1]
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1], mobile=self.mobile,
                                    idnum=idnum, name=name)
            # 创建订单
            order_manage.create_order_pq_mult(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1,
                                              SettlementTyp=SettlementTyp)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_manage.orderid)

        with allure.step("step1：名单绑定订单，检查预支名单列表"):
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
        with allure.step("预期结果：生成一条预支名单记录"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_manage.newnameid_pq)
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_manage.orderid)
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)
            pytest.assume(res['Data']['RecordList'][0]['SettlementType'] == SettlementTyp)

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('订单模式不同的预支名单')
    @allure.severity('blocker')
    def test_settle_namelist_0007(self, member_manage, ent, name_manage, order_manage, random_agent,
                                  advance_manage, borrow_randow_fuction):
        """相同身份证不同面试日期的预支名单"""
        with allure.step("预置条件：录入两条身份证信息相同，面试日期不同的名单"):
            idnum = create_IDCard()
            name = create_name()
            # 获取工种
            borrowname = borrow_randow_fuction[1]
            # 录入名单
            name_res1 = name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1],
                                                mobile=self.mobile,
                                                idnum=idnum, name=name, InterviewDate=yesterday)
            name_res2 = name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1],
                                                mobile=self.mobile,
                                                idnum=idnum, name=name, InterviewDate=nowtime)

            # 创建订单
            order_res1 = order_manage.create_order_pq_mult(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1,
                                                           OrderDt=yesterday, BeginDt=yesterday)
            order_res2 = order_manage.create_order_pq_mult(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1,
                                                           OrderDt=nowtime, BeginDt=nowtime)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_res1['Data'])
            order_manage.Judge_Order(auditsts=2, orderid=order_res2['Data'])
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_res1['Data'])
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_res2['Data'])

        with allure.step("step1：名单绑定订单，检查预支名单列表"):
            # 名单绑定订单
            name_manage.bind_order(orderid=order_res1['Data'], namelist=[name_res1['Data']['NameListId']])
            name_manage.bind_order(orderid=order_res2['Data'], namelist=[name_res2['Data']['NameListId']])
        with allure.step("预期结果：生成两条可预支名单"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum, StartDate=yesterday, EndDate=nowtime)
            pytest.assume(res['Data']['RecordCount'] == 2)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][0]['IntvDt'] == nowtime)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_res2['Data']['NameListId'])
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_res2['Data'])
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)
            pytest.assume(res['Data']['RecordList'][1]['Mobile'] == self.mobile)
            pytest.assume(res['Data']['RecordList'][1]['IntvDt'] == yesterday)
            pytest.assume(res['Data']['RecordList'][1]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][1]['WorkName'] == borrowname)
            pytest.assume(res['Data']['RecordList'][1]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][1]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][1]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][1]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][1]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][1]['NameListId'] == name_res1['Data']['NameListId'])
            pytest.assume(res['Data']['RecordList'][1]['RcrtOrderId'] == order_res1['Data'])
            pytest.assume(res['Data']['RecordList'][1]['Realname'] == name)

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('名单未绑定订单，检查预支名单')
    @allure.severity('blocker')
    def test_settle_namelist_0008(self, member_manage, ent, name_manage, order_manage, random_agent,
                                  advance_manage, borrow_randow_fuction):
        """名单未绑定订单，检查预支名单"""
        with allure.step("step1：录入名单"):
            idnum = create_IDCard()
            name = create_name()
            # 获取工种
            borrowname = borrow_randow_fuction[1]
            # 录入名单
            name_res1 = name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=random_agent[1],
                                                mobile=self.mobile,
                                                idnum=idnum, name=name, InterviewDate=yesterday)

        with allure.step("预期结果：录入成功单"):
            pytest.assume(name_res1['Code'] == 0)
            pytest.assume(name_res1['Desc'] == '成功')


        with allure.step("step2:检查可预支名单"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
        with allure.step("预期结果：生成两条可预支名单"):
            pytest.assume(res['Data']['RecordCount'] == 0)

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('预支名单更换工种重新绑单')
    @allure.severity('blocker')
    def test_settle_namelist_0009(self, ent, name_manage, order_manage, random_agent,
                                  advance_manage, borrow_randow_fuction, name_bind_order):
        """预支名单更换工种重新绑单"""
        # 等待30s预置条件名单绑订单生产可预支名单
        time.sleep(30)

        with allure.step("step1：录入名单"):
            borrowname1 = name_bind_order[5]
            idnum = name_bind_order[2]
            mobile = name_bind_order[3]
            name = name_bind_order[4]
            agentname = name_bind_order[6]
            # 获取和上次录入不一致的工种
            res = name_manage.get_entbrorrow()
            lst = res['Data']['RecordList']
            for i in range(100):
                entborrow_dic = lst[random.randint(0, len(lst) - 1)]
                borrowname2 = entborrow_dic['EntBorrowName']
                if borrowname2 != borrowname1:
                    break
            # 录入名单
            name_res = name_manage.add_name_pq(entbrorrowname=borrowname2, FromSpName=agentname, mobile=mobile,
                                               idnum=idnum, name=name)
            # 创建订单
            order_res = order_manage.create_order_pq_mult(entbrorrowname=borrowname2, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_res['Data'])
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=random_agent[1], OrderId=order_res['Data'])
            # 名单绑定订单
            name_manage.bind_order(orderid=order_res['Data'], namelist=[name_res['Data']['NameListId']])

        with allure.step("预期结果：绑定成功，修改原预支名单"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == mobile)
            pytest.assume(res['Data']['RecordList'][0]['IntvDt'] == nowtime)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname2)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_res['Data']['NameListId'])
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_res['Data'])
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)

        with allure.step("step2:检查name_list_settle表"):
            name_list_settle_sql = "SELECT * FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            name_list_settle_res = self.db.selectsql(name_list_settle_sql)
        with allure.step("预期结果：生成两条可预支名单"):
            pytest.assume(name_list_settle_res[0][1] == name_manage.newnameid_pq)
            pytest.assume(name_list_settle_res[0][2] == idnum)
            pytest.assume(name_list_settle_res[0][3] == name)
            pytest.assume(name_list_settle_res[0][4] == mobile)
            pytest.assume(name_list_settle_res[0][14] == borrowname2)
            pytest.assume(name_list_settle_res[0][20] == order_res['Data'])
            pytest.assume(name_list_settle_res[0][21] == 5)
            pytest.assume(name_list_settle_res[0][24] == 1)
            pytest.assume(name_list_settle_res[0][27] == '')

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('预支名单更换来源重新绑单')
    @allure.severity('blocker')
    def test_settle_namelist_0010(self, ent, name_manage, order_manage, random_agent,
                                  advance_manage, borrow_randow_fuction, name_bind_order):
        """预支名单更换来源重新绑单"""
        # 等待30s预置条件名单绑订单生产可预支名单
        time.sleep(30)

        with allure.step("step1：录入名单"):
            borrowname1 = name_bind_order[5]
            idnum = name_bind_order[2]
            mobile = name_bind_order[3]
            name = name_bind_order[4]
            agentname1 = name_bind_order[6]
            # 获取和上次录入不一致的工种
            res = name_manage.get_source()
            lst = res['Data']['RecordList']
            for i in range(100):
                agent_dic = lst[random.randint(0, len(lst) - 1)]
                agentname2 = agent_dic['SpShortName']
                agentid2 = agent_dic['SpId']
                if agentname2 != agentname1:
                    break
            # 录入名单
            name_res = name_manage.add_name_pq(entbrorrowname=borrowname1, FromSpName=agentname2, mobile=mobile,
                                               idnum=idnum, name=name)
            # 创建订单
            order_res = order_manage.create_order_pq_mult(entbrorrowname=borrowname1, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_res['Data'])
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=agentname2, OrderId=order_res['Data'])
            # 名单绑定订单
            name_manage.bind_order(orderid=order_res['Data'], namelist=[name_res['Data']['NameListId']])

        with allure.step("预期结果：绑定成功，修改原预支名单"):
            # 等待30s
            time.sleep(30)
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            pytest.assume(res['Data']['RecordCount'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['Mobile'] == mobile)
            pytest.assume(res['Data']['RecordList'][0]['IntvDt'] == nowtime)
            pytest.assume(res['Data']['RecordList'][0]['WorkCardNo'] == '')
            pytest.assume(res['Data']['RecordList'][0]['WorkName'] == borrowname1)
            pytest.assume(res['Data']['RecordList'][0]['WorkSts'] == 5)
            pytest.assume(res['Data']['RecordList'][0]['IdCardNum'] == idnum)
            pytest.assume(res['Data']['RecordList'][0]['IsBindOrder'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['IsValid'] == 1)
            pytest.assume(res['Data']['RecordList'][0]['NameListId'] == name_res['Data']['NameListId'])
            pytest.assume(res['Data']['RecordList'][0]['RcrtOrderId'] == order_res['Data'])
            pytest.assume(res['Data']['RecordList'][0]['Realname'] == name)
            pytest.assume(res['Data']['RecordList'][0]['SrceSpName'] == agentname2)

        with allure.step("step2:检查name_list_settle表"):
            name_list_settle_sql = "SELECT * FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            name_list_settle_res = self.db.selectsql(name_list_settle_sql)
        with allure.step("预期结果：生成两条可预支名单"):
            pytest.assume(name_list_settle_res[0][1] == name_manage.newnameid_pq)
            pytest.assume(name_list_settle_res[0][2] == idnum)
            pytest.assume(name_list_settle_res[0][3] == name)
            pytest.assume(name_list_settle_res[0][4] == mobile)
            pytest.assume(name_list_settle_res[0][14] == borrowname1)
            pytest.assume(name_list_settle_res[0][17] == agentid2)
            pytest.assume(name_list_settle_res[0][20] == order_res['Data'])
            pytest.assume(name_list_settle_res[0][21] == 5)
            pytest.assume(name_list_settle_res[0][24] == 1)
            pytest.assume(name_list_settle_res[0][27] == '')

    @allure.feature('可预支名单')
    @allure.story('生成预支名单')
    @allure.title('作废/恢复可预支名单')
    @allure.severity('blocker')
    def test_settle_namelist_0011(self, weblogin, name_manage, order_manage, hundred_settle_name,
                                  advance_manage):
        """作废/恢复可预支名单"""
        with allure.step("step1:作废单条预支名单"):
            delete_res = weblogin.create_api(ZXX_DeleteNameByIdList,
                                             NameIdList=[hundred_settle_name[0][0]],
                                             IsValid=2).json()
            query_res = advance_manage.zxx_getNameList(IdCardNum=hundred_settle_name[1][0])
        with allure.step("预期结果：作废成功，name_list_settle中is_valid被更新为2"):
            pytest.assume(delete_res['Code'] == 0)
            pytest.assume(delete_res['Desc'] == '成功')
            pytest.assume(delete_res['Data'] == {})
            IsValid = jsonpath.jsonpath(query_res, '$..IsValid')[0]
            pytest.assume(IsValid == 2)
            namelist_settle_sql = f"SELECT is_valid from name_list_settle WHERE id_card_num={hundred_settle_name[1][0]}"
            db_res = self.db.selectsql(namelist_settle_sql)
            pytest.assume(db_res[0][0] == 2)

        with allure.step("step1:恢复单条预支名单"):
            delete_res = weblogin.create_api(ZXX_DeleteNameByIdList,
                                             NameIdList=[hundred_settle_name[0][0]],
                                             IsValid=1).json()
            query_res = advance_manage.zxx_getNameList(IdCardNum=hundred_settle_name[1][0])
        with allure.step("预期结果：作废成功，name_list_settle中is_valid被更新为1"):
            pytest.assume(delete_res['Code'] == 0)
            pytest.assume(delete_res['Desc'] == '成功')
            pytest.assume(delete_res['Data'] == {})
            IsValid = jsonpath.jsonpath(query_res, '$..IsValid')[0]
            pytest.assume(IsValid == 1)
            namelist_settle_sql = f"SELECT is_valid from name_list_settle WHERE id_card_num={hundred_settle_name[1][0]}"
            db_res = self.db.selectsql(namelist_settle_sql)
            pytest.assume(db_res[0][0] == 1)

        with allure.step("step1:批量作废预支名单"):
            delete_res = weblogin.create_api(ZXX_DeleteNameByIdList,
                                             NameIdList=hundred_settle_name[0],
                                             IsValid=2).json()

        with allure.step("预期结果：作废成功，name_list_settle中is_valid被更新为2"):
            pytest.assume(delete_res['Code'] == 0)
            pytest.assume(delete_res['Desc'] == '成功')
            pytest.assume(delete_res['Data'] == {})
            for idnum in hundred_settle_name[1]:
                query_res = advance_manage.zxx_getNameList(IdCardNum=idnum)
                IsValid = jsonpath.jsonpath(query_res, '$..IsValid')[0]
                pytest.assume(IsValid == 2)
            namelist_settle_sql = f"SELECT is_valid from name_list_settle WHERE id_card_num in {tuple(hundred_settle_name[1])}"
            db_res = self.db.selectsql(namelist_settle_sql)
            for i in range(len(db_res)):
                pytest.assume(db_res[i][0] == 2)

        with allure.step("step1:批量恢复预支名单"):
            delete_res = weblogin.create_api(ZXX_DeleteNameByIdList,
                                             NameIdList=hundred_settle_name[0],
                                             IsValid=1).json()

        with allure.step("预期结果：作废成功，name_list_settle中is_valid被更新为1"):
            pytest.assume(delete_res['Code'] == 0)
            pytest.assume(delete_res['Desc'] == '成功')
            pytest.assume(delete_res['Data'] == {})
            for idnum in hundred_settle_name[1]:
                query_res = advance_manage.zxx_getNameList(IdCardNum=idnum)
                IsValid = jsonpath.jsonpath(query_res, '$..IsValid')[0]
                pytest.assume(IsValid == 1)
            namelist_settle_sql = f"SELECT is_valid from name_list_settle WHERE id_card_num in {tuple(hundred_settle_name[1])}"
            db_res = self.db.selectsql(namelist_settle_sql)
            for i in range(len(db_res)):
                pytest.assume(db_res[i][0] == 1)

    @allure.feature('可预支名单')
    @allure.story('功能按钮')
    @allure.title('身份证脱敏')
    @allure.severity('critical')
    def test_settle_namelist_0040(self, name_bind_order, name_manage, advance_manage):
        """身份证脱敏"""
        name = name_bind_order[4]
        idnum = name_bind_order[2]
        # 等待30s
        time.sleep(30)
        # 查询预支名单
        res = advance_manage.zxx_getNameList(Realname=name)
        encrypt_idnum = jsonpath.jsonpath(res, '$..IdCardNum')[0]

        with allure.step("step1:点击列表身份证字段"):
            res = name_manage.decryptAPI(DesenData=encrypt_idnum, Typ=2)
        with allure.step("预期结果：身份证信息正确"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['OriData'] == idnum)
            pytest.assume(res['Data']['DesenData'] == encrypt_idnum)
            pytest.assume(res['Data']['Typ'] == 2)

    @allure.feature('可预支名单')
    @allure.story('功能按钮')
    @allure.title('在职状态')
    @allure.severity('critical')
    def test_settle_namelist_0041(self, name_bind_order, name_manage, advance_manage):
        """在职状态"""
        with allure.step("step1:检查可预支名单默认在职状态"):
            # 等待30s
            time.sleep(30)
            idnum = name_bind_order[2]
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
        with allure.step("预期结果：默认在职状态为未知"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(jsonpath.jsonpath(res, '$..WorkSts')[0] == 5)

        with allure.step("step2：检查name_list_settle表"):
            settle_sql1 = "SELECT work_sts FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql2 = "SELECT entry_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql3 = "SELECT leave_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            db_work_sts = self.db.selectsql(settle_sql1)[0][0]
            db_entry_dt = self.db.selectsql(settle_sql2)[0][0]
            db_leave_dt = self.db.selectsql(settle_sql3)[0][0]
        with allure.step("预期结果：work_sts为5，entry_dt和leave_dt字段值为空"):
            pytest.assume(db_work_sts == 5)
            pytest.assume(db_entry_dt == '0000-00-00')
            pytest.assume(db_leave_dt == '0000-00-00')

    @allure.feature('可预支名单')
    @allure.story('功能按钮')
    @allure.title('在职状态-在职')
    @allure.severity('critical')
    def test_settle_namelist_0042(self, name_bind_order, name_manage, advance_manage, weblogin):
        """在职状态-在职"""
        with allure.step("step1:选择在职，填入入职日期，点击确定"):
            # 等待30s
            time.sleep(30)
            idnum = name_bind_order[2]
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt='0000-00-00',
                                             WorkSts=1,
                                             NameListId=NameListId).json()
            resed = advance_manage.zxx_getNameList(IdCardNum=idnum)

        with allure.step("预期结果：确定成功，页面展示入职日期和在职状态"):
            pytest.assume(update_res['Code'] == 0)
            pytest.assume(update_res['Desc'] == '成功')
            pytest.assume(jsonpath.jsonpath(resed, '$..WorkSts')[0] == 1)

        with allure.step("step2：检查name_list_settle表"):
            settle_sql1 = "SELECT work_sts FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql2 = "SELECT entry_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql3 = "SELECT leave_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            db_work_sts = self.db.selectsql(settle_sql1)[0][0]
            db_entry_dt = self.db.selectsql(settle_sql2)[0][0]
            db_leave_dt = self.db.selectsql(settle_sql3)[0][0]
        with allure.step("预期结果：work_sts为1，entry_dt和leave_dt字段值为空"):
            pytest.assume(db_work_sts == 1)
            pytest.assume(db_entry_dt.strftime('%Y-%m-%d') == nowtime)
            pytest.assume(db_leave_dt == '0000-00-00')

    @allure.feature('可预支名单')
    @allure.story('功能按钮')
    @allure.title('在职状态-离职')
    @allure.severity('critical')
    def test_settle_namelist_0043(self, name_bind_order, name_manage, advance_manage, weblogin):
        """在职状态-离职"""
        with allure.step("step1:选择离职，填入在职日期和离职日期，点击确定"):
            # 等待30s
            time.sleep(30)
            idnum = name_bind_order[2]
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt=tomorrow,
                                             WorkSts=2,
                                             NameListId=NameListId).json()
            resed = advance_manage.zxx_getNameList(IdCardNum=idnum)

        with allure.step("预期结果：确定成功，页面展示入职日期、离职日期和离职状态"):
            pytest.assume(update_res['Code'] == 0)
            pytest.assume(update_res['Desc'] == '成功')
            pytest.assume(jsonpath.jsonpath(resed, '$..WorkSts')[0] == 2)

        with allure.step("step2：检查name_list_settle表"):
            settle_sql1 = "SELECT work_sts FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql2 = "SELECT entry_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql3 = "SELECT leave_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            db_work_sts = self.db.selectsql(settle_sql1)[0][0]
            db_entry_dt = self.db.selectsql(settle_sql2)[0][0]
            db_leave_dt = self.db.selectsql(settle_sql3)[0][0]
        with allure.step("预期结果：work_sts为2，entry_dt和leave_dt字段值正确"):
            pytest.assume(db_work_sts == 2)
            pytest.assume(db_entry_dt.strftime('%Y-%m-%d') == nowtime)
            pytest.assume(db_leave_dt.strftime('%Y-%m-%d') == tomorrow)

        with allure.step("step3:只选择离职日期，不填在职日期，点击确定"):
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt='0000-00-00',
                                             LeaveDt=tomorrow,
                                             WorkSts=2,
                                             NameListId=NameListId).json()
        with allure.step("预期结果：提示在职状态和入离职日期不匹配"):
            pytest.assume(update_res['Code'] == 60475)
            pytest.assume(update_res['Desc'] == '在职状态和入离职日期不匹配')

        with allure.step("step4:只填在职日期，不填离职日期，点击确定"):
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt='0000-00-00',
                                             WorkSts=2,
                                             NameListId=NameListId).json()
        with allure.step("预期结果：提示在职状态和入离职日期不匹配"):
            pytest.assume(update_res['Code'] == 60475)
            pytest.assume(update_res['Desc'] == '在职状态和入离职日期不匹配')

        with allure.step("step5:填入离职日期小于在职日期，点击确定"):
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt=yesterday,
                                             WorkSts=2,
                                             NameListId=NameListId).json()
        with allure.step("预期结果：输入参数错误"):
            pytest.assume(update_res['Code'] == 50001)
            pytest.assume(update_res['Desc'] == '输入参数错误')

    @allure.feature('可预支名单')
    @allure.story('功能按钮')
    @allure.title('在职状态-转正')
    @allure.severity('critical')
    def test_settle_namelist_0044(self, name_bind_order, name_manage, advance_manage, weblogin):
        """在职状态-转正"""
        with allure.step("step1:选择转正，填入在职日期，点击确定"):
            # 等待30s
            time.sleep(30)
            idnum = name_bind_order[2]
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt='0000-00-00',
                                             WorkSts=3,
                                             NameListId=NameListId).json()
            resed = advance_manage.zxx_getNameList(IdCardNum=idnum)

        with allure.step("预期结果：确定成功，页面展示入职日期、离职日期和离职状态"):
            pytest.assume(update_res['Code'] == 0)
            pytest.assume(update_res['Desc'] == '成功')
            pytest.assume(jsonpath.jsonpath(resed, '$..WorkSts')[0] == 3)

        with allure.step("step2：检查name_list_settle表"):
            settle_sql1 = "SELECT work_sts FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql2 = "SELECT entry_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql3 = "SELECT leave_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            db_work_sts = self.db.selectsql(settle_sql1)[0][0]
            db_entry_dt = self.db.selectsql(settle_sql2)[0][0]
            db_leave_dt = self.db.selectsql(settle_sql3)[0][0]
        with allure.step("预期结果：wwork_sts为3，entry_dt正确，leave_dt为空"):
            pytest.assume(db_work_sts == 3)
            pytest.assume(db_entry_dt.strftime('%Y-%m-%d') == nowtime)
            pytest.assume(db_leave_dt == '0000-00-00')

        with allure.step("step3:不填入职日期，选择转正，点击确定"):
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt='0000-00-00',
                                             LeaveDt='0000-00-00',
                                             WorkSts=3,
                                             NameListId=NameListId).json()
        with allure.step("预期结果：提示在职状态和入离职日期不匹配"):
            pytest.assume(update_res['Code'] == 60475)
            pytest.assume(update_res['Desc'] == '在职状态和入离职日期不匹配')

    @allure.feature('可预支名单')
    @allure.story('功能按钮')
    @allure.title('在职状态-未处理')
    @allure.severity('critical')
    def test_settle_namelist_0045(self, name_bind_order, name_manage, advance_manage, weblogin):
        """在职状态-未处理"""
        with allure.step("step1:选择未处理，填入在职日期，点击确定"):
            # 等待30s
            time.sleep(30)
            idnum = name_bind_order[2]
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt='0000-00-00',
                                             LeaveDt='0000-00-00',
                                             WorkSts=4,
                                             NameListId=NameListId).json()
            resed = advance_manage.zxx_getNameList(IdCardNum=idnum)

        with allure.step("预期结果：确定成功，页面展示入职日期和未处理状态"):
            pytest.assume(update_res['Code'] == 0)
            pytest.assume(update_res['Desc'] == '成功')
            pytest.assume(jsonpath.jsonpath(resed, '$..WorkSts')[0] == 4)

        with allure.step("step2：检查name_list_settle表"):
            settle_sql1 = "SELECT work_sts FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql2 = "SELECT entry_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql3 = "SELECT leave_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            db_work_sts = self.db.selectsql(settle_sql1)[0][0]
            db_entry_dt = self.db.selectsql(settle_sql2)[0][0]
            db_leave_dt = self.db.selectsql(settle_sql3)[0][0]
        with allure.step("预期结果：wwork_sts为4，entry_dt为空，leave_dt为空"):
            pytest.assume(db_work_sts == 4)
            pytest.assume(db_entry_dt == '0000-00-00')
            pytest.assume(db_leave_dt == '0000-00-00')

    @allure.feature('可预支名单')
    @allure.story('功能按钮')
    @allure.title('在职状态-自离')
    @allure.severity('critical')
    def test_settle_namelist_0046(self, name_bind_order, name_manage, advance_manage, weblogin):
        """在职状态-自离"""
        with allure.step("step1:选择自离，填入在职日期和离职日期，点击确定"):
            # 等待30s
            time.sleep(30)
            idnum = name_bind_order[2]
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt=tomorrow,
                                             WorkSts=6,
                                             NameListId=NameListId).json()
            resed = advance_manage.zxx_getNameList(IdCardNum=idnum)

        with allure.step("预期结果：确定成功，页面展示入职日期、离职日期和离职状态"):
            pytest.assume(update_res['Code'] == 0)
            pytest.assume(update_res['Desc'] == '成功')
            pytest.assume(jsonpath.jsonpath(resed, '$..WorkSts')[0] == 6)

        with allure.step("step2：检查name_list_settle表"):
            settle_sql1 = "SELECT work_sts FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql2 = "SELECT entry_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            settle_sql3 = "SELECT leave_dt FROM name_list_settle ORDER BY name_list_settle_id desc limit 1"
            db_work_sts = self.db.selectsql(settle_sql1)[0][0]
            db_entry_dt = self.db.selectsql(settle_sql2)[0][0]
            db_leave_dt = self.db.selectsql(settle_sql3)[0][0]
        with allure.step("预期结果：work_sts为6，entry_dt和leave_dt字段值正确"):
            pytest.assume(db_work_sts == 6)
            pytest.assume(db_entry_dt.strftime('%Y-%m-%d') == nowtime)
            pytest.assume(db_leave_dt.strftime('%Y-%m-%d') == tomorrow)

        with allure.step("step3:只选择离职日期，不填在职日期，点击确定"):
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt='0000-00-00',
                                             LeaveDt=tomorrow,
                                             WorkSts=6,
                                             NameListId=NameListId).json()
        with allure.step("预期结果：提示在职状态和入离职日期不匹配"):
            pytest.assume(update_res['Code'] == 60475)
            pytest.assume(update_res['Desc'] == '在职状态和入离职日期不匹配')

        with allure.step("step4:只填在职日期，不填离职日期，点击确定"):
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt='0000-00-00',
                                             WorkSts=6,
                                             NameListId=NameListId).json()
        with allure.step("预期结果：提示在职状态和入离职日期不匹配"):
            pytest.assume(update_res['Code'] == 60475)
            pytest.assume(update_res['Desc'] == '在职状态和入离职日期不匹配')

        with allure.step("step5:填入离职日期小于在职日期，点击确定"):
            # 查询预支名单
            res = advance_manage.zxx_getNameList(IdCardNum=idnum)
            NameListId = jsonpath.jsonpath(res, '$..NameListId')[0]
            update_res = weblogin.create_api(UpdateUserMembsWorkStsForApp,
                                             EntryDt=nowtime,
                                             LeaveDt=yesterday,
                                             WorkSts=6,
                                             NameListId=NameListId).json()
        with allure.step("预期结果：输入参数错误"):
            pytest.assume(update_res['Code'] == 50001)
            pytest.assume(update_res['Desc'] == '输入参数错误')

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用面试日期查询')
    @allure.severity('critical')
    def test_settle_namelist_0047(self, weblogin):
        """使用面试日期查询"""
        with allure.step("step1:面试日期左右区间都不为空，点击查询"):
            # 查询
            res = weblogin.create_api(ZXX_GetNameList,
                                      StartDate=nowtime,
                                      EndDate=nowtime,
                                      IntvSts=-9999,
                                      RecordIndex=0,
                                      RecordSize=9999,
                                      ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：查询成功，查询到对应面试日期的数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['RecordCount'] == db_count)
            interv_dts = jsonpath.jsonpath(res, '$..IntvDt')
            for interv_dt in interv_dts:
                pytest.assume(interv_dt == nowtime)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用入职日期查询')
    @allure.severity('critical')
    def test_settle_namelist_0048(self, weblogin):
        """使用入职日期查询"""
        with allure.step("step1:入职日期左右区间都不为空，点击查询"):
            # 查询
            res = weblogin.create_api(ZXX_GetNameList,
                                      EntryDtBegin=nowtime,
                                      EntryDtEnd=nowtime,
                                      IntvSts=-9999,
                                      RecordIndex=0,
                                      RecordSize=9999,
                                      ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (entry_dt >= '{nowtime}') AND (entry_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：查询成功，查询到对应面试日期的数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['RecordCount'] == db_count)
            EntryDts = jsonpath.jsonpath(res, '$..EntryDt')
            for EntryDt in EntryDts:
                pytest.assume(EntryDt == nowtime)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用离职日期查询')
    @allure.severity('critical')
    def test_settle_namelist_0049(self, weblogin):
        """使用离职日期查询"""
        with allure.step("step1:入职日期左右区间都不为空，点击查询"):
            # 查询
            res = weblogin.create_api(ZXX_GetNameList,
                                      LeaveDtBegin=tomorrow,
                                      LeaveDtEnd=tomorrow,
                                      IntvSts=-9999,
                                      RecordIndex=0,
                                      RecordSize=9999,
                                      ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (leave_dt >= '{tomorrow}') AND (leave_dt <= '{tomorrow}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：查询成功，查询到对应面试日期的数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['RecordCount'] == db_count)
            leave_dts = jsonpath.jsonpath(res, '$..LeaveDt')
            for leave_dt in leave_dts:
                pytest.assume(leave_dt == tomorrow)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用供应商查询')
    @allure.severity('critical')
    def test_settle_namelist_0050(self, weblogin, group_manage):
        """使用供应商查询"""
        with allure.step("预支条件：获取供应商相关信息"):
            # 获取名单中存在的供应商
            res = weblogin.create_api(ZXX_GetNameList,
                                      StartDate=nowtime,
                                      EndDate=nowtime,
                                      IntvSts=-9999,
                                      RecordIndex=0,
                                      RecordSize=9999,
                                      ).json()
            agentname = jsonpath.jsonpath(res, '$..SrceSpName')[0]
            agentid = jsonpath.jsonpath(res, '$..SrceSpId')[0]
        with allure.step("step1:使用合作中的供应商查询"):
            # 查询
            res = weblogin.create_api(ZXX_GetNameList,
                                      StartDate=nowtime,
                                      EndDate=nowtime,
                                      SrceSpId=agentid,
                                      SrceSpName=agentname,
                                      IntvSts=-9999,
                                      RecordIndex=0,
                                      RecordSize=9999,
                                      ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE agent_sp_id in ('{agentid}') AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['RecordCount'] == db_count)
            SrceSpIds = jsonpath.jsonpath(res, '$..SrceSpId')
            SrceSpNames = jsonpath.jsonpath(res, '$..SrceSpName')
            for SrceSpId in SrceSpIds:
                pytest.assume(SrceSpId == agentid)
            for SrceSpName in SrceSpNames:
                pytest.assume(SrceSpName == agentname)
        with allure.step("step2:使用不合作的供应商查询"):
            # 供应商页面查询供应商
            res = group_manage.getcooplist(NickName=agentname)
            coopid = jsonpath.jsonpath(res, '$..SupplierId')[0]
            # 关闭供应商合作状态
            group_manage.updateCoop(CoopId=coopid, CooperationStatus=2, CooperationStatusOnly=1)
            # 查询
            res = weblogin.create_api(ZXX_GetNameList,
                                      StartDate=nowtime,
                                      EndDate=nowtime,
                                      SrceSpId=agentid,
                                      IntvSts=-9999,
                                      RecordIndex=0,
                                      RecordSize=9999,
                                      ).json()
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']['RecordCount'] == db_count)
            SrceSpIds = jsonpath.jsonpath(res, '$..SrceSpId')
            SrceSpNames = jsonpath.jsonpath(res, '$..SrceSpName')
            for SrceSpId in SrceSpIds:
                pytest.assume(SrceSpId == agentid)
            for SrceSpName in SrceSpNames:
                pytest.assume(SrceSpName == agentname)

        with allure.step("恢复环境：打开供应商合作状态"):
            group_manage.updateCoop(CoopId=coopid, CooperationStatus=1, CooperationStatusOnly=1)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用标准企业查询')
    @allure.severity('critical')
    def test_settle_namelist_0051(self, weblogin, group_manage):
        """使用标准企业查询"""
        with allure.step("预支条件：获取标准企业相关信息"):
            # 获取名单中存在的标准企业
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            ent_short_name = jsonpath.jsonpath(res1, '$..EntShortName')[0]
            res2 = weblogin.create_api(GetTenantEntListByName, Name=ent_short_name, CoopSts=0, RecordIndex=0,
                                       RecordSize=9999).json()
            ent_id = jsonpath.jsonpath(res2, '$..EntId')[0]
            TEntId = jsonpath.jsonpath(res2, '$..TEntId')[0]
        with allure.step("step1:使用合作中的标准企业查询"):
            # 查询
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       RealEntId=[ent_id],
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (ent_id in ('{ent_id}')) AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            EntShortNames = jsonpath.jsonpath(res3, '$..EntShortName')
            for EntShortName in EntShortNames:
                pytest.assume(EntShortName == ent_short_name)
        with allure.step("step2:使用不合作的标准企业查询"):
            # 关闭标准企业合作状态
            weblogin.create_api(ModPaySalaryEntCoopSts, CoopSts=2, TEntId=TEntId)
            # 查询
            res4 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       RealEntId=[ent_id],
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res4['Code'] == 0)
            pytest.assume(res4['Desc'] == '成功')
            pytest.assume(res4['Data']['RecordCount'] == db_count)
            EntShortNames = jsonpath.jsonpath(res4, '$..EntShortName')
            for EntShortName in EntShortNames:
                pytest.assume(EntShortName == ent_short_name)

        with allure.step("恢复环境：打开供应商合作状态"):
            weblogin.create_api(ModPaySalaryEntCoopSts, CoopSts=1, TEntId=TEntId)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用企业查询')
    @allure.severity('critical')
    def test_settle_namelist_0052(self, weblogin, group_manage):
        """使用企业查询"""
        with allure.step("预支条件：获取标准企业相关信息"):
            # 获取名单中存在的企业
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            borrowname = jsonpath.jsonpath(res1, '$..WorkName')[0]
            borrowid = jsonpath.jsonpath(res1, '$..WorkId')[0]
            ent_id = jsonpath.jsonpath(res1, '$..RealEntId')[0]

        with allure.step("step1:使用合作中的企业查询"):
            # 查询
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       SpEntName=borrowname,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (sp_ent_name like '%{borrowname}%') AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            WorkNames = jsonpath.jsonpath(res3, '$..WorkName')
            WorkIds = jsonpath.jsonpath(res3, '$..WorkId')
            for WorkName in WorkNames:
                pytest.assume(WorkName == borrowname)
            for WorkId in WorkIds:
                pytest.assume(WorkId == borrowid)

        with allure.step("step2:使用不合作的企业查询"):
            # 关闭企业合作状态
            group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=borrowid, IsEnabled=2, RcrtType=2,
                                                  Flag=1, EntId=ent_id)
            # 查询
            res4 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       SpEntName=borrowname,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res4['Code'] == 0)
            pytest.assume(res4['Desc'] == '成功')
            pytest.assume(res4['Data']['RecordCount'] == db_count)
            WorkNames = jsonpath.jsonpath(res3, '$..WorkName')
            WorkIds = jsonpath.jsonpath(res3, '$..WorkId')
            for WorkName in WorkNames:
                pytest.assume(WorkName == borrowname)
            for WorkId in WorkIds:
                pytest.assume(WorkId == borrowid)

        with allure.step("恢复环境：打开供应商合作状态"):
            group_manage.add_or_update_ent_borrow(CoopEntName=borrowname, CoopEntId=borrowid, IsEnabled=1, RcrtType=2,
                                                  Flag=1, EntId=ent_id)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用企业查询')
    @allure.severity('critical')
    @pytest.mark.parametrize("IntvSts,IntvStsCode,IntvRemark", [(0, None, None),
                                                                (1, None, None),
                                                                (2, None, None),
                                                                (3, 3, None),
                                                                (3, 0, 'test'),
                                                                (4, 3, None)])
    def test_settle_namelist_0052(self, weblogin, group_manage, borrow_randow_fuction, random_agent, name_manage,
                                  order_manage, IntvSts, IntvStsCode, IntvRemark):
        """使用企业查询"""
        dic = {0: '未处理', 1: '未面试', 2: '面试通过', 3: '面试不通过', 4: '放弃'}
        with allure.step(f"预支条件：构造面试状态为{dic[IntvSts]}的可预支名单"):
            """名单绑定订单"""
            borrowname = borrow_randow_fuction[1]
            agentname = random_agent[1]
            # 录入名单
            name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=agentname, InterviewStatus=IntvSts,
                                    InterviewStatusDCode=IntvStsCode,
                                    InterviewStatusRemark=IntvRemark)
            # 创建订单
            order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
            # 审核订单
            order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
            # 分配订单
            order_manage.publishOrderToSupplier(agentname=agentname, OrderId=order_manage.orderid)
            # 名单绑定订单
            name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
            # 等待30s
            time.sleep(30)
        with allure.step("step1:使用合作中的企业查询"):
            # 查询
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=IntvSts,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_sts in ('{IntvSts}')) AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            intvstss = jsonpath.jsonpath(res3, '$..IntvSts')
            for intvsts in intvstss:
                pytest.assume(intvsts == IntvSts)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用身份证号码查询')
    @allure.severity('critical')
    def test_settle_namelist_0054(self, weblogin, group_manage):
        """使用身份证号码查询"""
        with allure.step("预支条件：获取身份证相关信息"):
            # 获取名单中存在的身份证
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            decryp_idnum = jsonpath.jsonpath(res1, '$..IdCardNum')[0]
            res2 = weblogin.create_api(DecryptAPI, Typ=2, DesenData=decryp_idnum).json()
            idnum = jsonpath.jsonpath(res2, '$..OriData')[0]

        with allure.step("step1:使用格式正确的身份证号码查询"):
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IdCardNum=idnum,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (id_card_num = '{idnum}') AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            IdCardNums = jsonpath.jsonpath(res3, '$..IdCardNum')
            for IdCardNum in IdCardNums:
                pytest.assume(IdCardNum == idnum)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用姓名查询')
    @allure.severity('critical')
    def test_settle_namelist_0055(self, weblogin, group_manage):
        """使用身份证号码查询"""
        with allure.step("预支条件：获取姓名相关信息"):
            # 获取名单中存在的姓名
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            name = jsonpath.jsonpath(res1, '$..Realname')[0]

        with allure.step("step1:使用存在的姓名查询"):
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       Realname=name,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (real_name = '{name}') AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            Realnames = jsonpath.jsonpath(res3, '$..Realname')
            for Realname in Realnames:
                pytest.assume(Realname == name)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用在职状态查询')
    @allure.severity('critical')
    @pytest.mark.parametrize('WorkSts', (1, 2, 3, 4, 5, 6))
    def test_settle_namelist_0056(self, weblogin, group_manage, WorkSts):
        """使用在职状态查询"""
        dic = {1: '在职', 2: '离职', 3: '转正', 4: '未处理', 5: '未知', 6: '自离'}
        with allure.step(f"step1:使用状态为{dic[WorkSts]}查询"):
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       WorkSts=WorkSts,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (work_sts in ('{WorkSts}')) AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            WorkStss = jsonpath.jsonpath(res3, '$..WorkSts')
            for workSts in WorkStss:
                pytest.assume(workSts == WorkSts)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用名单是否作废查询')
    @allure.severity('critical')
    def test_settle_namelist_0057(self, weblogin, group_manage):
        """使用名单是否作废查询"""
        with allure.step(f"step1:使用状态为正常查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IsValid=1,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (is_valid = '1') AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res1['Code'] == 0)
            pytest.assume(res1['Desc'] == '成功')
            pytest.assume(res1['Data']['RecordCount'] == db_count)
            IsValids = jsonpath.jsonpath(res1, '$..IsValid')
            for IsValid in IsValids:
                pytest.assume(IsValid == 1)

        with allure.step(f"step1:使用状态为已作废查询"):
            # 先作废部分名单
            res2 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            NameIdList = jsonpath.jsonpath(res2, '$..NameIstId')[0:3]
            weblogin.create_api(ZXX_DeleteNameByIdList, NameIdList=NameIdList, IsValid=2)
            # 查询已作废的名单
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IsValid=2,
                                       IntvSts=-9999,
                                       WorkSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (is_valid = '2') AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            IsValids = jsonpath.jsonpath(res3, '$..IsValid')
            for IsValid in IsValids:
                pytest.assume(IsValid == 2)

        with allure.step("恢复环境：恢复被作废的名单"):
            weblogin.create_api(ZXX_DeleteNameByIdList, NameIdList=NameIdList, IsValid=1)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('使用订单编号查询')
    @allure.severity('critical')
    def test_settle_namelist_0058(self, weblogin, group_manage):
        """使用订单编号查询"""
        with allure.step("预支条件：获取订单相关信息"):
            # 获取名单中存在的订单号
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            orderno = jsonpath.jsonpath(res1, '$..OrderNo')[0]

        with allure.step("step1:使用存在的姓名查询"):
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       OrderNo=orderno,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            orderid_sql = f"SELECT rcrt_main_order_id FROM `rcrt_zxx_order`  WHERE (order_no = '{orderno}') AND (is_deleted = 0) AND (tenant_id = '{weblogin.zt_tid}')"
            orderid = self.db.selectsql(orderid_sql)[0][0]
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (rcrt_order_id in ('{orderid}')) AND (intv_dt = '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ({weblogin.zt_tid})) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            OrderNos = jsonpath.jsonpath(res3, '$..OrderNo')
            for OrderNo in OrderNos:
                pytest.assume(OrderNo == orderno)

    @allure.feature('可预支名单')
    @allure.story('查询')
    @allure.title('组合查询')
    @allure.severity('critical')
    def test_settle_namelist_0059(self, weblogin, group_manage):
        """组合查询"""
        with allure.step("预支条件：获取组合查询相关信息"):
            # 获取名单中存在的身份证
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            decryp_idnum = jsonpath.jsonpath(res1, '$..IdCardNum')[0]
            res2 = weblogin.create_api(DecryptAPI, Typ=2, DesenData=decryp_idnum).json()
            idnum = jsonpath.jsonpath(res2, '$..OriData')[0]
            # 获取入职日期
            entryDt = jsonpath.jsonpath(res1, '$..EntryDt')[0]
            entrydt = '' if entryDt == '0000-00-00' else entryDt
            # 获取离职日期
            leaveDt = jsonpath.jsonpath(res1, '$..LeaveDt')[0]
            leavedt = '' if leaveDt == '0000-00-00' else leaveDt
            # 获取供应商
            agentname = jsonpath.jsonpath(res1, '$..SrceSpName')[0]
            agentid = jsonpath.jsonpath(res1, '$..SrceSpId')[0]
            # 获取标准企业
            ent_name = jsonpath.jsonpath(res1, '$..EntShortName')[0]
            ent_id = jsonpath.jsonpath(res1, '$..RealEntId')[0]
            # 获取企业
            borrowname = jsonpath.jsonpath(res1, '$..WorkName')[0]
            borrowid = jsonpath.jsonpath(res1, '$..WorkId')[0]
            # 获取面试状态
            IntvSts = jsonpath.jsonpath(res1, '$..IntvSts')[0]
            # 获取姓名
            name = jsonpath.jsonpath(res1, '$..Realname')[0]
            # 获取在职状态
            worksts = jsonpath.jsonpath(res1, '$..WorkSts')[0]
            # 获取名单是否作废状态
            is_valid = jsonpath.jsonpath(res1, '$..IsValid')[0]
            # 获取订单编号
            orderno = jsonpath.jsonpath(res1, '$..OrderNo')[0]

        with allure.step("step1:正确填写每一项，点击查询"):
            res3 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IdCardNum=idnum,
                                       SrceSpId=agentid,
                                       RealEntId=[ent_id],
                                       SpEntName=borrowname,
                                       IntvSts=IntvSts,
                                       Realname=name,
                                       WorkSts=worksts,
                                       OrderNo=orderno,
                                       EntryDtBegin=entrydt,
                                       EntryDtEnd=entrydt,
                                       LeaveDtBegin=leavedt,
                                       LeaveDtEnd=leavedt,
                                       RcrtTyp=2,
                                       RecordIndex=0,
                                       RecordSize=9999,
                                       ).json()
            # 查询数据库
            orderid_sql = f"SELECT rcrt_main_order_id FROM `rcrt_zxx_order`  WHERE (order_no = '{orderno}') AND (is_deleted = 0) AND (tenant_id = '{weblogin.zt_tid}')"
            orderid = self.db.selectsql(orderid_sql)[0][0]
            count_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (id_card_num = '{idnum}') AND (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (ent_id in ('{ent_id}')) AND (agent_sp_id in ('{agentid}')) AND (rcrt_order_id in ('{orderid}')) AND (work_sts in ('{worksts}')) AND (intv_sts in ('{IntvSts}')) AND (settle_typ = '1') AND (real_name = '{name}') AND (sp_ent_name like '%{borrowname}%') AND (is_valid = '{is_valid}') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"
            db_count = self.db.selectsql(count_sql)[0][0]
        with allure.step("预期结果：可以查询到对应的可预支名单"):
            pytest.assume(res3['Code'] == 0)
            pytest.assume(res3['Desc'] == '成功')
            pytest.assume(res3['Data']['RecordCount'] == db_count)
            IdCardNum = jsonpath.jsonpath(res3, '$..IdCardNum')[0]
            IntvDt = jsonpath.jsonpath(res3, '$..IntvDt')[0]
            SrceSpId = jsonpath.jsonpath(res3, '$..SrceSpId')[0]
            RealEntId = jsonpath.jsonpath(res3, '$..RealEntId')[0]
            intvsts = jsonpath.jsonpath(res3, '$..IntvSts')[0]
            WorkName = jsonpath.jsonpath(res3, '$..WorkName')[0]
            Realname = jsonpath.jsonpath(res3, '$..Realname')[0]
            WorkSts = jsonpath.jsonpath(res3, '$..WorkSts')[0]
            OrderNo = jsonpath.jsonpath(res3, '$..OrderNo')[0]
            EntryDt = jsonpath.jsonpath(res3, '$..EntryDt')[0]
            LeaveDt = jsonpath.jsonpath(res3, '$..LeaveDt')[0]
            pytest.assume(IdCardNum == idnum)
            pytest.assume(IntvDt == nowtime)
            pytest.assume(SrceSpId == agentid)
            pytest.assume(RealEntId == ent_id)
            pytest.assume(intvsts == IntvSts)
            pytest.assume(WorkName == borrowname)
            pytest.assume(Realname == name)
            pytest.assume(WorkSts == worksts)
            pytest.assume(OrderNo == orderno)
            pytest.assume(EntryDt == entryDt)
            pytest.assume(LeaveDt == leaveDt)

    @allure.feature('可预支名单')
    @allure.story('分页')
    @allure.title('分页数据量检查')
    @allure.severity('critical')
    def test_settle_namelist_0061(self, weblogin, group_manage):
        """分页数据量检查"""
        with allure.step("step1:每页为10条数据查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=10,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            count10_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 10 OFFSET 0"
            count = len(self.db.selectsql(count10_sql))
        with allure.step("预期结果：每页展示选定数量的数据"):
            pytest.assume(len(RecordList) == count)

        with allure.step("step1:每页为20条数据查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=20,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            count10_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 20 OFFSET 0"
            count = len(self.db.selectsql(count10_sql))
        with allure.step("预期结果：每页展示选定数量的数据"):
            pytest.assume(len(RecordList) == count)

        with allure.step("step1:每页为20条数据查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=30,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            count10_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 30 OFFSET 0"
            count = len(self.db.selectsql(count10_sql))
        with allure.step("预期结果：每页展示选定数量的数据"):
            pytest.assume(len(RecordList) == count)

        with allure.step("step1:每页为20条数据查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=50,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            count10_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 50 OFFSET 0"
            count = len(self.db.selectsql(count10_sql))
        with allure.step("预期结果：每页展示选定数量的数据"):
            pytest.assume(len(RecordList) == count)

        with allure.step("step1:每页为20条数据查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=100,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            count10_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 100 OFFSET 0"
            count = len(self.db.selectsql(count10_sql))
        with allure.step("预期结果：每页展示选定数量的数据"):
            pytest.assume(len(RecordList) == count)

        with allure.step("step1:每页为20条数据查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=200,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            count10_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 200 OFFSET 0"
            count = len(self.db.selectsql(count10_sql))
        with allure.step("预期结果：每页展示选定数量的数据"):
            pytest.assume(len(RecordList) == count)

    @allure.feature('可预支名单')
    @allure.story('分页')
    @allure.title('分页数据量检查')
    @allure.severity('critical')
    def test_settle_namelist_0062(self, weblogin, group_manage):
        """分页数据量检查"""
        with allure.step("step1:切换到第二页"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=10,
                                       RecordSize=10,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            db_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 10 OFFSET 10"
            db_res = self.db.selectsql(db_sql)
            count = len(db_res)
        with allure.step("预期结果：正确显示每页数据"):
            pytest.assume(len(RecordList) == count)
            for i in range(count):
                pytest.assume(RecordList[i]['NameIstId'] == db_res[i][0])
                pytest.assume(RecordList[i]['NameListId'] == db_res[i][1])

        with allure.step("step1:切换到第三页"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=20,
                                       RecordSize=10,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            db_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 10 OFFSET 20"
            db_res = self.db.selectsql(db_sql)
            count = len(db_res)
        with allure.step("预期结果：正确显示每页数据"):
            pytest.assume(len(RecordList) == count)
            for i in range(count):
                pytest.assume(RecordList[i]['NameIstId'] == db_res[i][0])
                pytest.assume(RecordList[i]['NameListId'] == db_res[i][1])

        with allure.step("step1:切换到第三页"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       IntvSts=-9999,
                                       RecordIndex=0,
                                       RecordSize=10,
                                       ).json()
            RecordList = jsonpath.jsonpath(res1, '$..RecordList')[0]
            db_sql = f"SELECT * FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0) ORDER BY intv_dt desc LIMIT 10 OFFSET 0"
            db_res = self.db.selectsql(db_sql)
            count = len(db_res)
        with allure.step("预期结果：正确显示每页数据"):
            pytest.assume(len(RecordList) == count)
            for i in range(count):
                pytest.assume(RecordList[i]['NameIstId'] == db_res[i][0])
                pytest.assume(RecordList[i]['NameListId'] == db_res[i][1])

    @allure.feature('可预支名单')
    @allure.story('分页')
    @allure.title('概要检查')
    @allure.severity('critical')
    def test_settle_namelist_0063(self, weblogin, group_manage):
        """分页数据量检查"""
        with allure.step("step1:查询"):
            res1 = weblogin.create_api(ZXX_GetNameList,
                                       StartDate=nowtime,
                                       EndDate=nowtime,
                                       EntryDtBegin='',
                                       EntryDtEnd='',
                                       LeaveDtBegin='',
                                       LeaveDtEnd='',
                                       RealEntId=[],
                                       IntvSts=-9999,
                                       WorkSts=-9999,
                                       IsValid=-9999,
                                       RcrtTyp=2,
                                       RecordIndex=0,
                                       RecordSize=10,
                                       ).json()
            TotalLeaveCnt = jsonpath.jsonpath(res1, '$..TotalLeaveCnt')[0]
            TotalSelfLeaveCnt = jsonpath.jsonpath(res1, '$..TotalSelfLeaveCnt')[0]
            TotalStandCnt = jsonpath.jsonpath(res1, '$..TotalStandCnt')[0]
            TotalStayCnt = jsonpath.jsonpath(res1, '$..TotalStayCnt')[0]
            TotalUnHandleCnt = jsonpath.jsonpath(res1, '$..TotalUnHandleCnt')[0]
            TotalUnKnowCnt = jsonpath.jsonpath(res1, '$..TotalUnKnowCnt')[0]
            TotalValidCnt = jsonpath.jsonpath(res1, '$..TotalValidCnt')[0]
            # sql
            totalvalidcnt_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (settle_typ = '1') AND (is_valid = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"
            totalstaycnt_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (work_sts in ('1')) AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"
            totalleavecnt_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (work_sts in ('2')) AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"
            totalselfleavecnt_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (work_sts in ('6')) AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"
            totalstandcnt_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (work_sts in ('3')) AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"
            totalunhandlecnt_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (work_sts in ('4')) AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"
            totalunknowcnt_sql = f"SELECT count(*) FROM `name_list_settle`  WHERE (intv_dt >= '{nowtime}') AND (intv_dt <= '{nowtime}') AND (work_sts in ('5')) AND (settle_typ = '1') AND (tenant_id in ('{weblogin.zt_tid}')) AND (is_deleted = 0)"

            totalvalidcnt = self.db.selectsql(totalvalidcnt_sql)[0][0]
            totalstaycnt = self.db.selectsql(totalstaycnt_sql)[0][0]
            totalleavecnt = self.db.selectsql(totalleavecnt_sql)[0][0]
            totalselfleavecnt = self.db.selectsql(totalselfleavecnt_sql)[0][0]
            totalstandcnt = self.db.selectsql(totalstandcnt_sql)[0][0]
            totalunhandlecnt = self.db.selectsql(totalunhandlecnt_sql)[0][0]
            totalunknowcnt = self.db.selectsql(totalunknowcnt_sql)[0][0]
        with allure.step("预期结果：每页展示选定数量的数据"):
            pytest.assume(totalvalidcnt == TotalValidCnt)
            pytest.assume(totalstaycnt == TotalStayCnt)
            pytest.assume(totalleavecnt == TotalLeaveCnt)
            pytest.assume(totalselfleavecnt == TotalSelfLeaveCnt)
            pytest.assume(totalstandcnt == TotalStandCnt)
            pytest.assume(totalunhandlecnt == TotalUnHandleCnt)
            pytest.assume(totalunknowcnt == TotalUnKnowCnt)
