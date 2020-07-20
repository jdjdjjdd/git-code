# 获取根路径
import os,sys
import pytest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)

from common.login.web_login import *
from common.business_func.mem_information_manag_func import *
from common.business_func.namelist import *
from common.business_func.orders import *
from common.base_utils.comm_utils import *
from common.venv.var import *

class Name_list_settle:
    def __init__(self):
        self.weblogin=Web_Login()
        self.weblogin.login(pq_boss_user)
        self.namelistcs=NameList(self.weblogin)
        self.ordercs=Order(self.weblogin)
        # 创建OperateMDdb实例对象
        self.db = OperateMDdb()

    def add_namelist_settle(self,idcardnum,name,date,ent_id=None):
        # 随机获取来源
        res = self.namelistcs.get_source()
        lst = res['Data']['RecordList']
        agent_dic = lst[random.randint(0, len(lst) - 1)]
        SpId = agent_dic['SpId']
        SpShortName = agent_dic['SpShortName']
        if ent_id==None:
            # 随机获取工种
            res=self.namelistcs.get_entbrorrow()
            res1=random.choice(res['Data']['RecordList'])
            borrowname=res1['EntBorrowName']
            brorrowid=res1['EntBorrowId']
        else:
            #随机获取标准企业下工种
            sp_ent_sql=f"select sp_ent_name from sp_ent where tenant_id={pq_tenant_id} and ent_id={ent_id} and is_deleted=0 and rcrt_typ=2"
            sp_entres=self.db.selectsql(sp_ent_sql)
            borrowname=random.choice(sp_entres)[0]
        #录入名单
        self.namelistcs.add_name_pq(entbrorrowname=borrowname, FromSpName=SpShortName,idnum=idcardnum, name=name,InterviewDate=date)
        # 创建订单
        res=self.ordercs.create_order_pq(entbrorrowname=borrowname, ReceiverType=2, PriceUnit=1,OrderDt=date)
        # 审核订单
        self.ordercs.Judge_Order(auditsts=2, orderid=self.ordercs.orderid)
        # 分配订单
        self.ordercs.publishOrderToSupplier(agentname=SpShortName, OrderId=self.ordercs.orderid)
        # 名单绑定订单
        self.namelistcs.bind_order(orderid=self.ordercs.orderid, namelist=[self.namelistcs.newnameid_pq])

        return self.namelistcs.newnameid_pq