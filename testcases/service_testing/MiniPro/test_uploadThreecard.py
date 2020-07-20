# 获取根路径
import os, sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)

from common.base_utils.comm_utils import *
from common.data_operation.mysql_db import OperateMDdb
from common.venv.var import *
from common.login.applet_login import *
from common.login.web_login import *
from common.business_func.mem_information_manag_func import *
from common.business_func.applet_func import *
from testcases.service_testing.MiniPro.config_data import *
import pytest, allure
import random
from common.venv.api_path_mb import *

class TestThreecard():

    def setup_class(self):
        # 创建小程序登陆实例对象
        self.Minilogin = Applet_Login()
        #创建web登录对象
        self.weblogin=Web_Login()
        #创建Member_information_management_func对象
        self.management_func=Member_information_management_func(self.weblogin)
        #创建Applet_func实例对象
        self.appletfunc=Applet_func(self.Minilogin)
        #初始化数据库实例对象
        self.db = OperateMDdb()

    def setup_method(self):
        # 定义每个用例变量
        self.name = create_name()
        self.idnum = create_IDCard()
        self.mobile = create_phone()


    @allure.feature('上传三卡')
    @allure.story('上传身份证')
    @allure.title('选择身份证图片，上传身份证')
    @allure.severity('blocker')
    def test_uploadidcard_0001(self):
        """
                选择身份证图片，上传身份证

        """
        print('\n{}测试开始\n'.format(self.test_uploadidcard_0001.__name__))
        with allure.step("step1:上传身份证"):
            #登录小程序
            self.Minilogin.applogin(2,self.mobile)
            guid=self.Minilogin.Guid
            #上传身份证
            res=self.appletfunc.upload_idcard(fakeridcardpicture)
        with allure.step("step2:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']=='')

        with allure.step("step3:校验数据库数据"):
            idcard_audit_sql=f"SELECT audit_sts FROM member_user_idcard_audit where guid={guid} limit 1"
            res=self.db.selectsql(idcard_audit_sql)
            pytest.assume(res[0][0] == 1)


    @allure.feature('上传三卡')
    @allure.story('上传身份证')
    @allure.title('会员已上传身份证，再次上传身份证')
    @allure.severity('blocker')
    def test_uploadidcard_0002(self):
        """
                会员已上传身份证，再次上传身份证

        """
        print('\n{}测试开始\n'.format(self.test_uploadidcard_0001.__name__))
        #生成系统中不存在的手机号码
        while True:
                # 生成手机号码
                mobile = create_phone()
                # 校验手机号码是否存在
                mobilesql = f"select guid from center_user where login_name={mobile}"
                res = self.db.selectsql(mobilesql)
                if res == ():
                    break
        with allure.step("step1:上传身份证"):
            # 登录小程序
            self.Minilogin.applogin(2, mobile)
            guid = self.Minilogin.Guid
            # 上传身份证
            res = self.appletfunc.upload_idcard(fakeridcardpicture)
        with allure.step("step2:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == '')

        with allure.step("step3:校验数据库数据"):
            idcard_audit_sql = f"SELECT audit_sts,user_idcard_audit_id FROM member_user_idcard_audit where guid={guid} limit 1"
            res = self.db.selectsql(idcard_audit_sql)
            #获取user_idcard_audit_id
            user_idcard_audit_id=res[0][1]
            pytest.assume(res[0][0] == 1)
        with allure.step("step4:审核不通过身份证"):
            self.weblogin.login(pq_boss_user)
            res=self.management_func.IDCardPic(user_idcard_audit_id)
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
        with allure.step("step5:再次上传身份证"):
            # 再次上传身份证
            res = self.appletfunc.upload_idcard(fakeridcardpicture)
        with allure.step("step6:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == '')

        with allure.step("step7:校验数据库数据"):
            idcard_audit_sql = f"SELECT audit_sts FROM member_user_idcard_audit where guid={guid} order by created_tm desc limit 1"
            res = self.db.selectsql(idcard_audit_sql)
            pytest.assume(res[0][0] == 1)

    @allure.feature('上传三卡')
    @allure.story('上传银行卡')
    @allure.title('会员上传银行卡')
    @allure.severity('blocker')
    def test_uploadbankcard_0003(self):
        """
                        会员上传银行卡

        """
        print('\n{}测试开始\n'.format(self.test_uploadbankcard_0003.__name__))
        with allure.step("step1:上传银行卡"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            #随机获取一个银行名称
            res=upthreecard.minilogin.create_api(GetBankList_Api)
            banklist = res.json()['Data']['RecordList']
            bank=random.choice(banklist)
            bankname=bank['BankName']
            #上传银行卡
            res=upthreecard.appletfunc.upload_bankcard(bankname,fakerbankcardpicture)
        with allure.step("step2:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)
        with allure.step("step3:校验数据库数据"):
            bankcardaudit_sql=f'select guid,bank_name_self,audit_sts from member_user_bank_card_audit where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} order by created_tm desc limit 1'
            res=self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==upthreecard.minilogin.Guid)
            pytest.assume(res[0][1]==bankname)
            pytest.assume(res[0][2]==1)

    @allure.feature('上传三卡')
    @allure.story('上传银行卡')
    @allure.title('银行卡列表数据查看')
    @allure.severity('blocker')
    def test_uploadbankcard_0004(self):
        """
           会员存在待审核、审核通过、审核不通过银行卡，查看小程序银行卡列表

        """
        print('\n{}测试开始\n'.format(self.test_uploadbankcard_0004.__name__))
        with allure.step("step1:前置条件"):
            #创建upload_threecard对象
            upthreecard=upload_threecard()
            #上传身份证
            idcardaudit_id=upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)
            #上传银行卡
            bankaudit_id_01=upthreecard.upload_bankcard(fakerbankcardpicture)
            #审核不通过银行卡
            upthreecard.bankcard_auditnopass(bankaudit_id_01)
            #上传第二张银行卡
            bankaudit_id_02 = upthreecard.upload_bankcard(fakerbankcardpicture)
            #审核通过银行卡
            upthreecard.bankcard_auditpass(bankaudit_id_02)
            #上传第三银行卡
            bankaudit_id_03 = upthreecard.upload_bankcard(fakerbankcardpicture)
            #上传第四张银行卡
            bankaudit_id_04 = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step2:查询银行卡列表"):
            res=upthreecard.minilogin.create_api(ZXX_QueryBankCard_Api)
            response=res.json()

        with allure.step("step3:校验接口返回的数据"):
            pytest.assume(response['Code']==0)
            pytest.assume(response['Desc']=='成功')
            pytest.assume(response['Data']['RecordCount']==3)
            recordlist=response['Data']['RecordList']
            #获取数据库银行卡信息并构造对比参数
            bankaudit_id_01_sql=f'select audit_sts,bank_card_num,bank_name,user_bank_card_audit_id from member_user_bank_card_audit where user_bank_card_audit_id={bankaudit_id_01}'
            res = self.db.selectsql(bankaudit_id_01_sql)
            bankaudit_id_01_message=res[0]
            bankaudit_id_02_sql = f'select audit_sts,bank_card_num,bank_name,user_bank_card_audit_id from member_user_bank_card_audit where user_bank_card_audit_id={bankaudit_id_02}'
            res = self.db.selectsql(bankaudit_id_02_sql)
            bankaudit_id_02_message = res[0]
            bankaudit_id_03_sql = f'select audit_sts,bank_card_num,bank_name,user_bank_card_audit_id from member_user_bank_card_audit where user_bank_card_audit_id={bankaudit_id_03}'
            res = self.db.selectsql(bankaudit_id_03_sql)
            bankaudit_id_03_message = res[0]
            bankaudit_id_04_sql = f'select audit_sts,bank_card_num,bank_name,user_bank_card_audit_id from member_user_bank_card_audit where user_bank_card_audit_id={bankaudit_id_04}'
            res = self.db.selectsql(bankaudit_id_04_sql)
            bankaudit_id_04_message = res[0]
            #校验接口返回的data参数
            bankauditid_list=[]
            for one in recordlist:
                bankauditid_list.append(one['UserBankCardAuditId'])

            pytest.assume(bankaudit_id_01_message[3] not in bankauditid_list)
            #校验bankaudit_id_02_message
            for one in recordlist:
                if one['UserBankCardAuditId']==bankaudit_id_02_message[3]:
                    pytest.assume(one['AuditSts']==bankaudit_id_02_message[0])
                    pytest.assume(one['BankCardNum'] == bankaudit_id_02_message[1])
                    pytest.assume(one['BankName'] == bankaudit_id_02_message[2])
                    pytest.assume(one['UserBankCardAuditId'] == bankaudit_id_02_message[3])
            # 校验bankaudit_id_03_message
            for one in recordlist:
                if one['UserBankCardAuditId']==bankaudit_id_03_message[3]:
                    pytest.assume(one['AuditSts']==bankaudit_id_03_message[0])
                    pytest.assume(one['BankCardNum'] == bankaudit_id_03_message[1])
                    pytest.assume(one['BankName'] == bankaudit_id_03_message[2])
                    pytest.assume(one['UserBankCardAuditId'] == bankaudit_id_03_message[3])

            # 校验bankaudit_id_04_message
            for one in recordlist:
                if one['UserBankCardAuditId'] == bankaudit_id_04_message[3]:
                    pytest.assume(one['AuditSts'] == bankaudit_id_04_message[0])
                    pytest.assume(one['BankCardNum'] == bankaudit_id_04_message[1])
                    pytest.assume(one['BankName'] == bankaudit_id_04_message[2])
                    pytest.assume(one['UserBankCardAuditId'] == bankaudit_id_04_message[3])

    @allure.feature('上传三卡')
    @allure.story('上传工牌')
    @allure.title('会员身份证未审核通过上传工牌')
    @allure.severity('blocker')
    def test_uploadworkcard_0005(self):
        """
            会员身份证未审核通过上传工牌

        """
        print('\n{}测试开始\n'.format(self.test_uploadworkcard_0005.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #获取随机的标准企业名称
            entname_sql=f'select ent_short_name,ent_id from tenant_ent where is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(entname_sql)
            ent=random.choice(res)
            entshortname=ent[0]
            ent_id=ent[1]

        with allure.step("step2:上传工牌"):
            res=upthreecard.appletfunc.upload_workcard(entshortname,workCardpicture)

        with allure.step("step3:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data']==None)

        with allure.step("step4:校验数据库数据"):
            workcardaudit_sql=f'select guid,uuid,ent_id,audit_sts,is_canceled from member_user_work_card_audit where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} order by created_tm limit 1'
            res=self.db.selectsql(workcardaudit_sql)
            pytest.assume(res[0][0]==upthreecard.minilogin.Guid)
            pytest.assume(res[0][1]==0)
            pytest.assume(res[0][2] == ent_id)
            pytest.assume(res[0][3] == 1)
            pytest.assume(res[0][4] == 0)

    @allure.feature('上传三卡')
    @allure.story('上传工牌')
    @allure.title('会员身份证已审核通过上传工牌')
    @allure.severity('blocker')
    def test_uploadworkcard_0006(self):
        """
            会员身份证已审核通过上传工牌

        """
        print('\n{}测试开始\n'.format(self.test_uploadworkcard_0006.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)
            #获取uuid
            uuid_sql=f'select uuid from member_user where guid={upthreecard.minilogin.Guid}'
            res = self.db.selectsql(uuid_sql)
            uuid=res[0][0]
            # 获取随机的标准企业名称
            entname_sql = f'select ent_short_name,ent_id from tenant_ent where is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(entname_sql)
            ent = random.choice(res)
            entshortname = ent[0]
            ent_id = ent[1]

        with allure.step("step2:上传工牌"):
            res = upthreecard.appletfunc.upload_workcard(entshortname, workCardpicture)

        with allure.step("step3:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)

        with allure.step("step4:校验数据库数据"):
            workcardaudit_sql = f'select guid,uuid,ent_id,audit_sts,is_canceled from member_user_work_card_audit where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} order by created_tm limit 1'
            res = self.db.selectsql(workcardaudit_sql)
            pytest.assume(res[0][0] == upthreecard.minilogin.Guid)
            pytest.assume(res[0][1] == uuid)
            pytest.assume(res[0][2] == ent_id)
            pytest.assume(res[0][3] == 1)
            pytest.assume(res[0][4] == 0)

    @allure.feature('上传三卡')
    @allure.story('上传工牌')
    @allure.title('会员已上传待审核状态的工牌再次上传工牌')
    @allure.severity('blocker')
    def test_uploadworkcard_0007(self):
        """
            会员已上传待审核状态的工牌再次上传工牌

        """
        print('\n{}测试开始\n'.format(self.test_uploadworkcard_0007.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)
            # 获取uuid
            uuid_sql = f'select uuid from member_user where guid={upthreecard.minilogin.Guid}'
            res = self.db.selectsql(uuid_sql)
            uuid = res[0][0]
            # 获取随机的标准企业名称
            entname_sql = f'select ent_short_name,ent_id from tenant_ent where is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(entname_sql)
            ent = random.choice(res)
            entshortname = ent[0]
            ent_id = ent[1]

        with allure.step("step2:上传工牌"):
            res = upthreecard.appletfunc.upload_workcard(entshortname, workCardpicture)

        with allure.step("step3:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)

        with allure.step("step4:校验数据库数据"):
            workcardaudit_sql = f'select guid,uuid,ent_id,audit_sts,is_canceled,user_work_card_audit_id from member_user_work_card_audit where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} order by created_tm limit 1'
            res = self.db.selectsql(workcardaudit_sql)
            workcardaudit_id=res[0][5]
            pytest.assume(res[0][0] == upthreecard.minilogin.Guid)
            pytest.assume(res[0][1] == uuid)
            pytest.assume(res[0][2] == ent_id)
            pytest.assume(res[0][3] == 1)
            pytest.assume(res[0][4] == 0)

        with allure.step("step5:再次上传工牌"):
            res = upthreecard.appletfunc.upload_workcard(entshortname, workCardpicture)

        with allure.step("step6:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)

        with allure.step("step7:校验数据库之前上传的工牌记录的is_canceled"):
            workcardaudit_sql = f'select is_canceled from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id}'
            res = self.db.selectsql(workcardaudit_sql)
            pytest.assume(res[0][0] == 1)

    @allure.feature('上传三卡')
    @allure.story('上传工牌')
    @allure.title('会员工牌列表检查')
    @allure.severity('blocker')
    def test_uploadworkcard_0008(self):
        """
            会员存在待审核、审核通过、审核不通过工牌，查看小程序工牌列表

        """
        print('\n{}测试开始\n'.format(self.test_uploadworkcard_0008.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)
            # 获取uuid
            uuid_sql = f'select uuid from member_user where guid={upthreecard.minilogin.Guid}'
            res = self.db.selectsql(uuid_sql)
            uuid = res[0][0]
            # 获取随机的标准企业名称
            entname_sql = f'select ent_short_name,ent_id from tenant_ent where is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(entname_sql)
            ent = random.choice(res)
            entshortname = ent[0]
            ent_id = ent[1]

        with allure.step("step2:上传工牌"):
            #上传第一张工牌
            workcardauditid_01 = upthreecard.upload_workcard(workCardpicture)
            #审核不通过工牌
            res=upthreecard.weblogin.create_api(ZXX_GetNextWorkCardPic_Api,UserWorkCardAuditId=workcardauditid_01)
            pytest.assume(res.json()['Code']==0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res.json()['Data'] == None)

            #上传第二张工牌
            workcardauditid_02 = upthreecard.upload_workcard(workCardpicture)
            # 获取随机的标准企业名称
            entname_sql = f'select ent_short_name,ent_id from tenant_ent where is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(entname_sql)
            ent = random.choice(res)
            entshortname = ent[0]
            ent_id = ent[1]
            #生成随机工牌号码
            workcard_num=str(random.randint(1, 10000))

            # 审核第二张工牌
            res = upthreecard.memberuser_managefunc.audit_workcard(entshortname, workcard_num,
                                                                   userworkcardauditid=workcardauditid_02)
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)

            #上传第三张工牌
            workcardauditid_03 = upthreecard.upload_workcard(workCardpicture)
            # 获取随机的标准企业名称
            entname_sql = f'select ent_short_name,ent_id from tenant_ent where is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(entname_sql)
            ent = random.choice(res)
            second_entshortname = ent[0]
            second_ent_id = ent[1]
            # 生成随机工牌号码
            second_workcard_num = str(random.randint(1, 10000))

            #审核第三张工牌
            res = upthreecard.memberuser_managefunc.audit_workcard(second_entshortname, second_workcard_num,userworkcardauditid=workcardauditid_03)
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == None)

            #上传第四张工牌
            workcardauditid_04 = upthreecard.upload_workcard(workCardpicture)

            #上传第五张工牌
            workcardauditid_05 = upthreecard.upload_workcard(workCardpicture)

        with allure.step("step3:获取工牌列表"):
            res=upthreecard.minilogin.create_api(ZXX_QueryWorkCard_Api)

        with allure.step("step4:校验接口返回数据"):
            pytest.assume(res.json()['Code']==0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res.json()['Data']['RecordCount']==2)
            RecordList=res.json()['Data']['RecordList']
            #获取第三张工牌数据库信息
            workcardauditid_03_sql=f'SELECT a.audit_sts,b.ent_short_name,a.work_card_no,a.user_work_card_audit_id FROM member_user_work_card_audit as a left join tenant_ent as b on a.ent_id=b.ent_id where a.user_work_card_audit_id={workcardauditid_03} and b.ec_id={ec_id}'
            res=self.db.selectsql(workcardauditid_03_sql)
            workcardauditid03_message=res[0]
            # 获取第五张工牌数据库信息
            workcardauditid_05_sql = f'SELECT a.audit_sts,b.ent_short_name,a.work_card_no,a.user_work_card_audit_id FROM member_user_work_card_audit as a left join tenant_ent as b on a.ent_id=b.ent_id where a.user_work_card_audit_id={workcardauditid_05} and b.ec_id={ec_id}'
            res = self.db.selectsql(workcardauditid_05_sql)
            workcardauditid05_message = res[0]

            # 校验接口返回的data参数
            workcardauditid_list = []
            for one in RecordList:
                workcardauditid_list.append(one['UserWorkCardAuditId'])

            pytest.assume(workcardauditid_01 not in workcardauditid_list)
            pytest.assume(workcardauditid_02 not in workcardauditid_list)
            pytest.assume(workcardauditid_04 not in workcardauditid_list)

            #校验workcardauditid02_message
            for one in RecordList:
                if one['UserWorkCardAuditId']==workcardauditid03_message[3]:
                    pytest.assume(one['AuditSts']==workcardauditid03_message[0])
                    pytest.assume(one['EntName']==workcardauditid03_message[1])
                    pytest.assume(one['UserWorkCardAuditId'] == workcardauditid03_message[3])
                    pytest.assume(one['WorkCardNo'] == workcardauditid03_message[2])

            # 校验workcardauditid02_message
            for one in RecordList:
                if one['UserWorkCardAuditId'] == workcardauditid05_message[3]:
                    pytest.assume(one['AuditSts'] == workcardauditid05_message[0])
                    pytest.assume(one['EntName'] == workcardauditid05_message[1])
                    pytest.assume(one['UserWorkCardAuditId'] == workcardauditid05_message[3])
                    pytest.assume(one['WorkCardNo'] == workcardauditid05_message[2])


    @allure.feature('上传三卡')
    @allure.story('上传身份证')
    @allure.title('会员已上传待审核状态身份证，再次上传身份证')
    @allure.severity('blocker')
    def test_uploadidcard_0009(self):
        """
                会员已上传待审核状态身份证，再次上传身份证

        """
        print('\n{}测试开始\n'.format(self.test_uploadidcard_0009.__name__))
        #生成系统中不存在的手机号码
        while True:
                # 生成手机号码
                mobile = create_phone()
                # 校验手机号码是否存在
                mobilesql = f"select guid from center_user where login_name={mobile}"
                res = self.db.selectsql(mobilesql)
                if res == ():
                    break
        with allure.step("step1:上传身份证"):
            # 登录小程序
            self.Minilogin.applogin(2, mobile)
            guid = self.Minilogin.Guid
            # 上传身份证
            res = self.appletfunc.upload_idcard(fakeridcardpicture)
        with allure.step("step2:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == '')

        with allure.step("step3:校验数据库数据"):
            idcard_audit_sql = f"SELECT audit_sts,user_idcard_audit_id FROM member_user_idcard_audit where guid={guid} limit 1"
            res = self.db.selectsql(idcard_audit_sql)
            #获取user_idcard_audit_id
            user_idcard_audit_id=res[0][1]
            pytest.assume(res[0][0] == 1)
        with allure.step("step4:再次上传身份证"):
            # 再次上传身份证
            res = self.appletfunc.upload_idcard(fakeridcardpicture)
        with allure.step("step6:校验接口返回数据"):
            pytest.assume(res['Code'] == 62224)
            pytest.assume(res['Desc'] == '上传身份证图片失败')
            pytest.assume(res['Data'] == '')


    @allure.feature('上传三卡')
    @allure.story('上传身份证')
    @allure.title('会员已上传审核通过的身份证，再次上传身份证')
    @allure.severity('blocker')
    def test_uploadidcard_0010(self):
        """
                会员已上传身份证，再次上传身份证

        """
        print('\n{}测试开始\n'.format(self.test_uploadidcard_0010.__name__))
        #生成系统中不存在的手机号码
        while True:
                # 生成手机号码
                mobile = create_phone()
                # 校验手机号码是否存在
                mobilesql = f"select guid from center_user where login_name={mobile}"
                res = self.db.selectsql(mobilesql)
                if res == ():
                    break
        with allure.step("step1:上传身份证"):
            # 登录小程序
            self.Minilogin.applogin(2, mobile)
            guid = self.Minilogin.Guid
            # 上传身份证
            res = self.appletfunc.upload_idcard(fakeridcardpicture)
        with allure.step("step2:校验接口返回数据"):
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
            pytest.assume(res['Data'] == '')

        with allure.step("step3:校验数据库数据"):
            idcard_audit_sql = f"SELECT audit_sts,user_idcard_audit_id FROM member_user_idcard_audit where guid={guid} limit 1"
            res = self.db.selectsql(idcard_audit_sql)
            #获取user_idcard_audit_id
            user_idcard_audit_id=res[0][1]
            pytest.assume(res[0][0] == 1)
        with allure.step("step4:审核不通过身份证"):
            self.weblogin.login(pq_boss_user)
            idcardnum = create_IDCard()
            name = create_name()
            res=self.management_func.audit_idcard(idcardnum,name,useridcardauditid=user_idcard_audit_id)
            pytest.assume(res['Code'] == 0)
            pytest.assume(res['Desc'] == '成功')
        with allure.step("step5:再次上传身份证"):
            # 再次上传身份证
            res = self.appletfunc.upload_idcard(fakeridcardpicture)
        with allure.step("step6:校验接口返回数据"):
            pytest.assume(res['Code'] == 62224)
            pytest.assume(res['Desc'] == '')
            pytest.assume(res['Data'] == '上传身份证图片失败')































