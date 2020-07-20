# 获取根路径
import os,sys
import pytest

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)
from common.login.applet_login import *
from common.login.web_login import *
from common.business_func.applet_func import *
from common.business_func.mem_information_manag_func import *
from common.base_utils.comm_utils import *


class upload_threecard():
    #初始化函数
    def __init__(self):
        #创建Applet_Login对象
        self.minilogin=Applet_Login()
        #创建Web_Login对象
        self.weblogin=Web_Login()
        # 创建OperateMDdb实例对象
        self.db = OperateMDdb()
        # 创建Applet_func实例对象
        self.appletfunc = Applet_func(self.minilogin)
        #创建Member_information_management_func对象
        self.memberuser_managefunc=Member_information_management_func(self.weblogin)
        # 生成系统中不存在的手机号码
        while True:
            # 生成手机号码
            self.mobile = create_phone()
            # 校验手机号码是否存在
            mobilesql = f"select guid from center_user where login_name={self.mobile}"
            res = self.db.selectsql(mobilesql)
            if res == ():
                break
        # 登录小程序
        self.minilogin.applogin(2, self.mobile)
        #登录web派遣端
        self.weblogin.login(pq_boss_user)


    #上传身份证
    def upload_idcard(self,idcardfile):
        # 上传身份证
        res = self.appletfunc.upload_idcard(idcardfile)
        assert (res['Code'] == 0)
        assert (res['Desc'] == '成功')
        assert (res['Data']=='')
        # 获取user_idcard_audit_id并return
        idcard_audit_sql = f"SELECT user_idcard_audit_id FROM member_user_idcard_audit where guid={self.minilogin.Guid} and ec_id={ec_id} order by created_tm desc limit 1"
        res = self.db.selectsql(idcard_audit_sql)
        idcard_audit_id=res[0][0]
        return idcard_audit_id

    #审核通过身份证
    def idcard_auditpass(self,idcard_audit_id):
        #生成身份证号码
        idcardnum=create_IDCard()
        #生成真实姓名
        realname=create_name()
        #审核通过身份证
        res=self.memberuser_managefunc.audit_idcard(idcardnum,realname,useridcardauditid=idcard_audit_id)
        assert (res['Code'] == 0)
        assert (res['Desc'] == '成功')
        assert (res['Data'] == None)

    #审核不通过身份证
    def idcard_auditnopass(self,idcard_audit_id):
        res=self.memberuser_managefunc.IDCardPic(idcard_audit_id)
        assert (res['Code'] == 0)
        assert (res['Desc'] == '成功')
        assert (res['Data'] == None)
    #上传银行卡
    def upload_bankcard(self,bankcardfile):
        #随机获取一个银行名称
        res = self.weblogin.create_api(GetBankList_Api)
        banklist = res.json()['Data']['RecordList']
        bank = random.choice(banklist)
        bankname = bank['BankName']
        #上传银行卡
        res=self.appletfunc.upload_bankcard(bankname,bankcardfile)
        assert (res['Code'] == 0)
        assert (res['Desc'] == '成功')
        assert (res['Data'] == None)
        #获取user_bank_card_audit_id并return
        bankcardaudit_sql=f'select user_bank_card_audit_id from member_user_bank_card_audit where guid={self.minilogin.Guid} and ec_id={ec_id} order by created_tm desc limit 1'
        res = self.db.selectsql(bankcardaudit_sql)
        bank_audit_id = res[0][0]
        return bank_audit_id
    #审核通过银行卡
    def bankcard_auditpass(self,bankaudit_id):
        # 随机获取一个银行名称
        res = self.weblogin.create_api(GetBankList_Api)
        banklist = res.json()['Data']['RecordList']
        bank = random.choice(banklist)
        bankname = bank['BankName']
        #生成银行卡号
        bankcardnum=create_bankcard()
        #审核通过银行卡
        res=self.memberuser_managefunc.audit_bankcard(bankcardnum,bankname,userbankcardauditid=bankaudit_id)
        assert (res['Code'] == 0)
        assert (res['Desc'] == '成功')
        assert (res['Data'] == None)
    # 审核不通过银行卡
    def bankcard_auditnopass(self,bankaudit_id):
        #审核不通过银行卡
        res=self.weblogin.create_api(ZXX_GetNextBankCardPic_Api,UserBankCardAuditId=bankaudit_id)
        assert (res.json()['Code'] == 0)
        assert (res.json()['Desc'] == '成功')
        assert (res.json()['Data'] == None)
    #上传工牌
    def upload_workcard(self,workcardfile):
        #随机获取一个ent_name
        tenant_ent_sql=f'SELECT ent_short_name FROM tenant_ent where is_deleted=0 and ec_id={ec_id} and is_enabled=1'
        res = self.db.selectsql(tenant_ent_sql)
        ent_name=random.choice(res)[0]
        #上传工牌
        res=self.appletfunc.upload_workcard(ent_name,workcardfile)
        assert (res['Code'] == 0)
        assert (res['Desc'] == '成功')
        assert (res['Data'] == None)
        # 获取user_work_card_audit_id并return
        workcardaudit_sql = f'SELECT user_work_card_audit_id FROM member_user_work_card_audit where guid={self.minilogin.Guid} and ec_id={ec_id} order by created_tm desc limit 1'
        res = self.db.selectsql(workcardaudit_sql)
        work_audit_id = res[0][0]
        return work_audit_id
    #打卡
    def clock(self,clocktype):
        #打卡
        self.appletfunc.colock_in(clocktype)

    #小程序补卡
    def repair_clock(self,clockdate,clocktm,clocktyp):
        #补卡
        self.appletfunc.repair_clock(clockdate,clocktm,clocktyp)












