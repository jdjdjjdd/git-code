from common.base_utils.comm_utils import create_bankcard
from common.business_func.applet_func import Applet_func
from common.business_func.namelist import NameList
from common.business_func.mem_information_manag_func import Member_information_management_func
from common.login.web_login import Web_Login
from common.login.applet_login import Applet_Login
from common.venv.var import *
from common.base_utils.comm_param import *
from common.business_func.orders import Order


# 配置项
n = 1 # 录名单数量
entborrows = ['协和小时工1']  # 企业
ents = ['昆山协和']  # 标准企业
interviewdt = '2020-07-01' # 面试日期
OrderDt = '2020-07-01' # 订单报价日期
BeginDt = '2020-07-01' # 订单生效开始日期
repairclockdt = '2020-07-01' # 补卡开始日期
agentnames = ['殷海涛供应商'] #供应商列表
username_name = '13340000001'
username_order = '15995627659'
username_mem = '15995627659'
username_advance = '15995627659'
bankname = '兴业银行'
SettleBeginDate='2020-07-01'
SettleEndDate = '2020-07-01'
workdate = '2020-07-01' # 入职日期






login = Web_Login()

login.login(username_name)

name_manage = NameList(login)

# 录名单

mobiles = []
membernames = []
idcardnums = []
nameids = []
for i in range(n):
    mobile = create_phone()
    idnum = create_IDCard()
    name = create_name()
    name_manage.add_name_pq(entbrorrowname=entborrows[0],InterviewDate=interviewdt,FromSpName=agentnames[0],name=name)
    mobiles.append(mobile)
    membernames.append(name)
    idcardnums.append(idnum)
    nameids.append(name_manage.newnameid_pq)
    print(i)
# 建订单
order_manage = Order(login)
order_manage.create_order_pq(ReceiverType=2,entbrorrowname=entborrows[0],OrderDt=OrderDt,BeginDt=OrderDt,PriceUnit=1)
order_manage.Judge_Order(auditsts=2,orderid=order_manage.orderid)
order_manage.publishOrderToSupplier(agentname=agentnames[0])

# 名单绑订单
name_manage.bind_order(orderid=order_manage.orderid,namelist=nameids)


# 上传身份证
workcardnos = []
for i in range(n):
    applogin = Applet_Login()
    applogin.applogin(tenantype=2, phone=mobiles[i])
    member = Applet_func(applogin)
    mem_manage = Member_information_management_func(login)

    member.upload_idcard(fakeridcardpicture)
    # 审核身份证
    mem_manage.audit_idcard(idcardnum=idcardnums[i],rname=membernames[i],phone=mobiles[i])

    # 上传银行卡
    member.upload_bankcard(bankname=bankname,bankCardFile=fakerbankcardpicture)
    # 审核银行卡
    bankcardnum = create_bankcard()
    mem_manage.audit_bankcard(bankcardnum=bankcardnum,bankname=bankname,phone=mobiles[i])

    # 上传工牌
    member.upload_workcard(entname=ents[0],workCardFile=workCardpicture)
    # 审核工牌
    workcardno = create_workcardno()
    mem_manage.audit_workcard(entshortname=ents[0],workcardno=workcardno,phone=mobiles[i])
    # workcardnos.append(workcardno)
