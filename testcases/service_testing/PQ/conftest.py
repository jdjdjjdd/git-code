# 获取根路径
import os
import sys
import time

import jsonpath
import pytest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)
from config.Config import Config
from common.venv.var import *

cf = Config()


@pytest.fixture(scope='function')
def add_name_interview(name_manage, borrow_randow_fuction, random_agent):
    """
    预置条件：录入名单
    :param weblogin:登陆信息
    :return: nameid，idnum，mobile
    """
    name_manage.add_name_pq(entbrorrowname=borrow_randow_fuction[1], FromSpName=random_agent[1])
    nameid = name_manage.newnameid_pq
    idnum = name_manage.newidnum_pq
    mobile = name_manage.newmobile_pq
    name = name_manage.newname_pq
    agentid = random_agent[0]
    agentname = random_agent[1]
    borrowid = borrow_randow_fuction[0]
    borrowname = borrow_randow_fuction[1]
    lst = [nameid, idnum, mobile, name, borrowid, borrowname, agentid, agentname]
    return lst


@pytest.fixture(scope='function')
def ent(group_manage):
    """集团管理随机获取标准企业"""
    res = group_manage.get_pay_salary_ent_list(RecordSize=100)
    lst = res['Data']['RecordList']
    ent_dic = lst[random.randint(0, len(lst) - 1)]
    EntName = ent_dic['EntName']
    EntShortName = ent_dic['EntShortName']
    TEntId = ent_dic['TEntId']
    EntId = ent_dic['EntId']
    res_lst = [EntShortName, TEntId, EntName, EntId]
    return res_lst


@pytest.fixture(scope='function')
def borrowent(group_manage):
    """集团管理随机获取企业"""
    res = group_manage.getEntBorrowList(RecordSize=100, RcrtType=2)
    lst = res['Data']['RecordList']
    entborrow_dic = lst[random.randint(0, len(lst) - 1)]
    EntBorrowId = entborrow_dic['EntBorrowId']
    EntBorrowName = entborrow_dic['EntBorrowName']
    EntId = entborrow_dic['EntId']
    EntName = entborrow_dic['EntName']
    res_lst = [EntBorrowId, EntBorrowName, EntId, EntName]
    return res_lst

@pytest.fixture(scope='function')
def borrow_randow_fuction(name_manage):
    """实接记录录名单随机获取企业"""
    res = name_manage.get_entbrorrow()
    lst = res['Data']['RecordList']
    entborrow_dic = lst[random.randint(0, len(lst) - 1)]
    EntBorrowId = entborrow_dic['EntBorrowId']
    EntBorrowName = entborrow_dic['EntBorrowName']
    EntId = entborrow_dic['EntId']
    res_lst = [EntBorrowId, EntBorrowName, EntId]
    return res_lst

@pytest.fixture(scope='function')
def random_agent(name_manage):
    """实接记录录名单随机获取供应商"""
    res = name_manage.get_source()
    lst = res['Data']['RecordList']
    SpId = SpShortName = None
    for i in range(10):
        agent_dic = lst[random.randint(0, len(lst) - 1)]
        SpId = agent_dic['SpId']
        SpShortName = agent_dic['SpShortName']
        if SpShortName != '奇迹招聘':
            break
    res_lst = [SpId, SpShortName]
    return res_lst

@pytest.fixture()
def name_bind_order(name_manage, order_manage, borrow_randow_fuction, random_agent):
    """名单绑定订单"""
    borrowname = borrow_randow_fuction[1]
    agentname = random_agent[1]
    # 录入名单
    name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=agentname)
    # 创建订单
    order_manage.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
    # 审核订单
    order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
    # 分配订单
    order_manage.publishOrderToSupplier(agentname=agentname, OrderId=order_manage.orderid)
    # 名单绑定订单
    name_manage.bind_order(orderid=order_manage.orderid, namelist=[name_manage.newnameid_pq])
    res = name_manage.get_nameList(IDCardNum=name_manage.newidnum_pq)
    order_no = res['Data']['RecordList'][0]['OrderNo']
    nameid = name_manage.newnameid_pq
    lst = [order_no, nameid, name_manage.newidnum_pq, name_manage.newmobile_pq, name_manage.newname_pq, borrowname,
           agentname]
    return lst


@pytest.fixture(scope='class')
def borrow_random_class(name_manage):
    """实接记录录名单随机获取企业"""
    res = name_manage.get_entbrorrow()
    lst = res['Data']['RecordList']
    entborrow_dic = lst[random.randint(0, len(lst) - 1)]
    EntBorrowId = entborrow_dic['EntBorrowId']
    EntBorrowName = entborrow_dic['EntBorrowName']
    EntId = entborrow_dic['EntId']
    res_lst = [EntBorrowId, EntBorrowName, EntId]
    return res_lst


@pytest.fixture(scope='class')
def hundred_name(name_manage, borrow_random_class):
    """录入100个名单"""
    nameid_100 = []
    nameid_101 = []
    for i in range(100):
        borrowname = borrow_random_class[1]
        name_manage.add_name_pq(entbrorrowname=borrowname)
        nameid = name_manage.newnameid_pq
        nameid_100.append(nameid)
        nameid_101.append(nameid)
    # 再录入一条
    name_manage.add_name_pq(entbrorrowname=borrow_random_class[1])
    nameid_101.append(name_manage.newnameid_pq)
    result = [nameid_100, nameid_101]
    return result


@pytest.fixture(scope='class')
def hundred_settle_name(name_manage, borrow_random_class, order_manage, advance_manage):
    """录入100个名单"""
    res = name_manage.get_source()
    lst = res['Data']['RecordList']
    agentname = None
    for i in range(100):
        agent_dic = lst[random.randint(0, len(lst) - 1)]
        agentname = agent_dic['SpShortName']
        if agentname != '奇迹招聘':
            break

    nameid_100 = []
    idnum_100 = []
    borrowname = borrow_random_class[1]
    for i in range(100):
        name_manage.add_name_pq(entbrorrowname=borrowname, FromSpName=agentname)
        nameid = name_manage.newnameid_pq
        nameid_100.append(nameid)
        idnum_100.append(name_manage.newidnum_pq)
    # 创建订单
    order_manage.create_order_pq_mult(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1)
    # 审核订单
    order_manage.Judge_Order(auditsts=2, orderid=order_manage.orderid)
    # 分配订单
    order_manage.publishOrderToSupplier(agentname=agentname, OrderId=order_manage.orderid)
    # 名单绑定订单
    name_manage.bind_order(orderid=order_manage.orderid, namelist=nameid_100)
    time.sleep(60)
    NameIstIds = []
    for idnum in idnum_100:
        res = advance_manage.zxx_getNameList(IdCardNum=idnum)
        NameIstId = jsonpath.jsonpath(res, '$..NameIstId')[0]
        NameIstIds.append(NameIstId)
    result = [NameIstIds, idnum_100]
    return result
