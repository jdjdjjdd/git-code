# encoding=utf8
import os,sys
# 获取根路径
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
from testcases.service_testing.PQ.config_data import *
import pytest, allure
import random
import time
import datetime

class Testidcardinfo:

    def setup_class(self):
        # 创建小程序登陆实例对象
        self.Minilogin = Applet_Login()
        # 创建web登录对象
        self.weblogin = Web_Login()
        # 创建Member_information_management_func对象
        self.management_func = Member_information_management_func(self.weblogin)
        # 创建Applet_func实例对象
        self.appletfunc = Applet_func(self.Minilogin)
        # 初始化数据库实例对象
        self.db = OperateMDdb()

    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('待审核状态身份证信息记录检查')
    @allure.severity('blocker')
    def test_idcardinfo_0001(self):
        """
                待审核状态身份证信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0001.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)

        with allure.step("step2:查询上传的身份证记录"):
            result=upthreecard.memberuser_managefunc.get_idcardlist(phone=upthreecard.mobile)

        with allure.step("step2:校验接口返回的参数"):
            #校验接口返回的code和desc
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            #校验返回的数据只有一条
            pytest.assume(len(result['Data']['RecordList'])==1)
            #获取总待审核身份证记录数量
            idcardauditcount_sql=f'select count(*) from member_user_idcard_audit where audit_sts=1 and ec_id={ec_id} and is_deleted=0'
            res = self.db.selectsql(idcardauditcount_sql)
            idcardauditcount=res[0][0]
            #获取数据库上传的身份证记录的信息
            idcardaudit_sql=f'select audit_sts,guid,user_idcard_audit_id,idcard_front_url,created_tm from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} order by created_tm desc limit 1'
            db_res=self.db.selectsql(idcardaudit_sql)
            #校验Data返回数据
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt']==0)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 1)
            pytest.assume(result['Data']['UnPassCnt'] == 0)
            pytest.assume(result['Data']['UnAuditRecordCount'] == idcardauditcount)
            #构造对比数据
            dict={'AuditBy':'',
                  'AuditRemark':'',
                  'AuditSts':1,
                  'AuditTm':'',
                  'BankCardAuditSts':0,
                  'CreditScore':'',
                  'Guid':db_res[0][1],
                  'IdCardNum':'',
                  'IdcardFrontUrl':db_res[0][3],
                  'Mobile':upthreecard.mobile,
                  'RealName':'',
                  'RegTime':db_res[0][4].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserIdcardAuditId':db_res[0][2]}
            pytest.assume(result['Data']['RecordList'][0]==dict)

    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('审核通过状态身份证信息记录检查')
    @allure.severity('blocker')
    def test_idcardinfo_0002(self):
        """
                审核通过状态身份证信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0002.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #审核通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)

        with allure.step("step2:查询上传的身份证记录"):
            result = upthreecard.memberuser_managefunc.get_idcardlist(phone=upthreecard.mobile)

        with allure.step("step2:校验接口返回的参数"):
            #校验接口返回的code和desc
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            #校验返回的数据只有一条
            pytest.assume(len(result['Data']['RecordList'])==1)
            #获取总待审核身份证记录数量
            idcardauditcount_sql=f'select count(*) from member_user_idcard_audit where audit_sts=1 and ec_id={ec_id} and is_deleted=0'
            res = self.db.selectsql(idcardauditcount_sql)
            idcardauditcount=res[0][0]
            #获取数据库上传的身份证记录的信息
            idcardaudit_sql=f'select audit_by,audit_remark,audit_sts,audit_tm,guid,id_card_num,idcard_front_url,real_name,created_tm,user_idcard_audit_id from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} order by created_tm desc limit 1'
            db_res=self.db.selectsql(idcardaudit_sql)
            #校验Data返回数据
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt']==1)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 0)
            pytest.assume(result['Data']['UnPassCnt'] == 0)
            pytest.assume(result['Data']['UnAuditRecordCount'] == idcardauditcount)
            #获取AuditBy
            tenant_user_sql=f'SELECT user_name FROM tenant_user where guid={db_res[0][0]} and t_id={pq_tenant_id} and is_deleted=0'
            auditbyres = self.db.selectsql(tenant_user_sql)
            auditby=auditbyres[0][0]
            #构造对比数据
            dict={'AuditBy':auditby,
                  'AuditRemark':db_res[0][1],
                  'AuditSts':db_res[0][2],
                  'AuditTm':db_res[0][3].__format__('%Y-%m-%d %H:%M:%S'),
                  'BankCardAuditSts':0,
                  'CreditScore':'',
                  'Guid':db_res[0][4],
                  'IdCardNum':db_res[0][5],
                  'IdcardFrontUrl':db_res[0][6],
                  'Mobile':upthreecard.mobile,
                  'RealName':db_res[0][7],
                  'RegTime':db_res[0][8].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserIdcardAuditId':db_res[0][9]}
            pytest.assume(result['Data']['RecordList'][0]==dict)



    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('审核不通过状态身份证信息记录检查')
    @allure.severity('blocker')
    def test_idcardinfo_0003(self):
        """
                审核不通过状态身份证信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0003.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #审核通过身份证
            upthreecard.idcard_auditnopass(idcardaudit_id)

        with allure.step("step2:查询上传的身份证记录"):
            result = upthreecard.memberuser_managefunc.get_idcardlist(phone=upthreecard.mobile)

        with allure.step("step2:校验接口返回的参数"):
            #校验接口返回的code和desc
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            #校验返回的数据只有一条
            pytest.assume(len(result['Data']['RecordList'])==1)
            #获取总待审核身份证记录数量
            idcardauditcount_sql=f'select count(*) from member_user_idcard_audit where audit_sts=1 and ec_id={ec_id} and is_deleted=0'
            res = self.db.selectsql(idcardauditcount_sql)
            idcardauditcount=res[0][0]
            #获取数据库上传的身份证记录的信息
            idcardaudit_sql=f'select audit_by,audit_remark,audit_sts,audit_tm,guid,id_card_num,idcard_front_url,real_name,created_tm,user_idcard_audit_id from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} order by created_tm desc limit 1'
            db_res=self.db.selectsql(idcardaudit_sql)
            #校验Data返回数据
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt']==0)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 0)
            pytest.assume(result['Data']['UnPassCnt'] == 1)
            pytest.assume(result['Data']['UnAuditRecordCount'] == idcardauditcount)
            # 获取AuditBy
            tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[0][0]} and t_id={pq_tenant_id} and is_deleted=0'
            auditbyres = self.db.selectsql(tenant_user_sql)
            auditby = auditbyres[0][0]
            #构造对比数据
            dict={'AuditBy':auditby,
                  'AuditRemark':db_res[0][1],
                  'AuditSts':db_res[0][2],
                  'AuditTm':db_res[0][3].__format__('%Y-%m-%d %H:%M:%S'),
                  'BankCardAuditSts':0,
                  'CreditScore':'',
                  'Guid':db_res[0][4],
                  'IdCardNum':db_res[0][5],
                  'IdcardFrontUrl':db_res[0][6],
                  'Mobile':upthreecard.mobile,
                  'RealName':db_res[0][7],
                  'RegTime':db_res[0][8].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserIdcardAuditId':db_res[0][9]}
            pytest.assume(result['Data']['RecordList'][0]==dict)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('统计信息数据检查')
    @allure.severity('blocker')
    def test_idcardinfo_0004(self):
        """
                统计信息数据检查

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0004.__name__))
        with allure.step("step1:查询全部的身份证审核记录"):
            self.weblogin.login(pq_boss_user)
            res=self.management_func.get_idcardlist()
            res_data=res['Data']

        with allure.step("step2:校验接口返回的数据"):
            #获取待审核数量
            unanditcnt_sql=f'select count(*) from member_user_idcard_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(unanditcnt_sql)
            unanditcnt=res[0][0]
            #获取审核通过数量
            PassCnt_sql=f'select count(*) from member_user_idcard_audit where audit_sts=2 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            #获取审核不通过数量
            UnPassCnt_sql=f'select count(*) from member_user_idcard_audit where audit_sts=3 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            #获取记录总数量
            RecordCount_sql=f'select count(*) from member_user_idcard_audit where is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            #校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt']==PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcnt)
            pytest.assume(res_data['RecordCount'] == RecordCount)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('身份证信息列表查看未脱敏手机号和未脱敏身份证号码')
    @allure.severity('blocker')
    def test_idcardinfo_0005(self):
        """
                身份证信息列表查看未脱敏手机号和未脱敏身份证号码

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0005.__name__))
        with allure.step("step1:查询审核通过的身份证审核记录"):
            #登录
            self.weblogin.login(pq_boss_user)
            #获取审核通过状态的身份证审核记录列表
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=2)
            idcardlist = res.json()['Data']['RecordList']
            #随机获取一条身份证审核记录
            idcardinfo=random.choice(idcardlist)
            #获取脱敏的手机号码
            desenmobile=idcardinfo['Mobile']
            #获取脱敏的身份证号码
            desenidcardnum = idcardinfo['IdCardNum']
            #获取guid
            guid=idcardinfo['Guid']
            #获取身份证审核记录的audit_id
            audit_id=idcardinfo['UserIdcardAuditId']
            #获取数据库未脱敏的身份证号码和手机号码
            idcardaudit_sql=f'select id_card_num from member_user_idcard_audit where user_idcard_audit_id={audit_id} and ec_id={ec_id}'
            res=self.db.selectsql(idcardaudit_sql)
            idcardnum=res[0][0]
            member_user_sql=f'select mobile from member_user where guid={guid} and ec_id={ec_id}'
            res = self.db.selectsql(member_user_sql)
            mobile = res[0][0]

        with allure.step("step2:查看未脱敏的手机号码并校验返回值"):
            #查看未脱敏的手机号码
            res=self.weblogin.create_api(DecryptAPI,Typ=1,DesenData=desenmobile)
            result=res.json()
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['DesenData']==desenmobile)
            pytest.assume(result['Data']['OriData'] == mobile)
            pytest.assume(result['Data']['Typ'] == 1)

        with allure.step("step2:查看未脱敏的身份证号码并校验返回值"):
            # 查看未脱敏的身份证号码
            res = self.weblogin.create_api(DecryptAPI, Typ=2, DesenData=desenidcardnum)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['DesenData'] == desenidcardnum)
            pytest.assume(result['Data']['OriData'] == idcardnum)
            pytest.assume(result['Data']['Typ'] == 2)

    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('默认查询项查询')
    @allure.severity('blocker')
    def test_idcardinfo_0006(self):
        """
                默认查询项查询

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0006.__name__))
        with allure.step("step1:默认查询项查询查询并校验接口返回结果"):
            # 登录
            self.weblogin.login(pq_boss_user)
            # 身份证号码为空查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,)
            result=res.json()
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            #获取总条数
            RecordCount_sql=f'select count(*) from member_user_idcard_audit where is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            #校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == RecordCount)
            #获取数据库数据
            memberidcardaudit_sql=f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            idcardaudittuple=self.db.selectsql(memberidcardaudit_sql)
            for one in range(len(result['Data']['RecordList'])):
                if idcardaudittuple[one][0] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={idcardaudittuple[one][0]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''

                pytest.assume(result['Data']['RecordList'][one]['AuditBy']==auditby)
                pytest.assume(result['Data']['RecordList'][one]['AuditRemark'] == idcardaudittuple[one][1])
                pytest.assume(result['Data']['RecordList'][one]['AuditSts'] == idcardaudittuple[one][2])
                if idcardaudittuple[one][3]=='0000-00-00 00:00:00':
                    audit_tm=''
                else:
                    audit_tm=idcardaudittuple[one][3].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(result['Data']['RecordList'][one]['AuditTm'] == audit_tm)
                pytest.assume(result['Data']['RecordList'][one]['Guid'] == idcardaudittuple[one][4])
                if result['Data']['RecordList'][one]['IdCardNum'] == '':
                    pytest.assume(result['Data']['RecordList'][one]['IdCardNum'] == idcardaudittuple[one][5])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                                   DesenData=result['Data']['RecordList'][one]['IdCardNum'])
                    realidcardnum = res.json()['Data']['OriData']
                    pytest.assume(realidcardnum == idcardaudittuple[one][5])
                pytest.assume(result['Data']['RecordList'][one]['IdcardFrontUrl'] == idcardaudittuple[one][6])
                pytest.assume(result['Data']['RecordList'][one]['RealName'] == idcardaudittuple[one][7])
                pytest.assume(result['Data']['RecordList'][one]['RegTime'] == idcardaudittuple[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(result['Data']['RecordList'][one]['UserIdcardAuditId'] == idcardaudittuple[one][9])
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=result['Data']['RecordList'][one]['Mobile'])
                realmobile=res.json()['Data']['OriData']
                pytest.assume(realmobile==idcardaudittuple[one][10])

    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('身份证号码查询')
    @allure.severity('blocker')
    def test_idcardinfo_0007(self):
        """
                身份证号码查询

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0007.__name__))
        with allure.step("step1:已存在审核记录的身份证号码查询并校验返回结果"):
            # 登录
            self.weblogin.login(pq_boss_user)
            #随机获取已存在身份证审核记录的身份证号码
            idcardnum_sql=f'select id_card_num from member_user_idcard_audit where audit_sts=2 and is_deleted=0 and ec_id={ec_id}'
            idcardnumtuple=self.db.selectsql(idcardnum_sql)
            idcardnum=str(random.choice(idcardnumtuple)[0])
            # 已存在身份证审核记录的身份证号码查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           IdCardNum=idcardnum)
            result=res.json()
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            #获取总条数
            RecordCount_sql=f'SELECT count(*) FROM `member_user_idcard_audit`  WHERE (is_deleted = 0) AND (id_card_num in ({idcardnum})) AND (ec_id = {ec_id})'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            #校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == RecordCount)
            # 获取数据库数据
            memberidcardaudit_sql = f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.id_card_num={idcardnum} ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            idcardaudittuple = self.db.selectsql(memberidcardaudit_sql)
            for one in range(len(result['Data']['RecordList'])):
                if idcardaudittuple[one][0] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={idcardaudittuple[one][0]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(result['Data']['RecordList'][one]['AuditBy'] == auditby)
                pytest.assume(result['Data']['RecordList'][one]['AuditRemark'] == idcardaudittuple[one][1])
                pytest.assume(result['Data']['RecordList'][one]['AuditSts'] == idcardaudittuple[one][2])
                if idcardaudittuple[one][3]=='0000-00-00 00:00:00':
                    audit_tm=''
                else:
                    audit_tm=idcardaudittuple[one][3].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(result['Data']['RecordList'][one]['AuditTm'] == audit_tm)
                pytest.assume(result['Data']['RecordList'][one]['Guid'] == idcardaudittuple[one][4])
                pytest.assume(result['Data']['RecordList'][one]['IdCardNum'] == idcardaudittuple[one][5])
                pytest.assume(result['Data']['RecordList'][one]['IdcardFrontUrl'] == idcardaudittuple[one][6])
                pytest.assume(result['Data']['RecordList'][one]['RealName'] == idcardaudittuple[one][7])
                pytest.assume(result['Data']['RecordList'][one]['RegTime'] == idcardaudittuple[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(result['Data']['RecordList'][one]['UserIdcardAuditId'] == idcardaudittuple[one][9])
                pytest.assume(result['Data']['RecordList'][one]['Mobile'] == idcardaudittuple[one][10])

        with allure.step("step1:不存在审核记录的身份证号码查询并校验返回结果"):
            # 随机生成不存在身份证审核记录的身份证号码
            while True:
                # 生成身份证号码
                noneidcardnum = create_IDCard()
                # 校验身份证号码是否存在
                idcardaudit_sql = f"select id_card_num from member_user_idcard_audit where id_card_num={noneidcardnum}"
                res = self.db.selectsql(idcardaudit_sql)
                if res == ():
                    break
            # 不存在身份证审核记录的身份证号码查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           IdCardNum=noneidcardnum)
            result=res.json()
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            #校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == 0)
            pytest.assume(result['Data']['RecordList']==[])

    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('姓名查询')
    @allure.severity('blocker')
    def test_idcardinfo_0008(self):
        """
                姓名查询

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0008.__name__))
        with allure.step("step1:已存在审核记录的姓名名称查询并校验返回结果"):
            # 登录
            self.weblogin.login(pq_boss_user)
            #随机获取已存在身份证审核记录的会员姓名
            realname_sql=f'select real_name from member_user_idcard_audit where audit_sts=2 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(realname_sql)
            realname=random.choice(res)[0]
            #已存在身份证审核记录的姓名查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           RealName=realname)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            # 获取总条数
            RecordCount_sql = f"SELECT count(*) FROM member_user_idcard_audit WHERE is_deleted = 0 AND real_name = '{realname}' AND ec_id = {ec_id}"
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            # 校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == RecordCount)
            # 获取数据库数据
            memberidcardaudit_sql = f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.real_name='{realname}' ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            idcardaudittuple = self.db.selectsql(memberidcardaudit_sql)
            for one in range(len(result['Data']['RecordList'])):
                if idcardaudittuple[one][0] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={idcardaudittuple[one][0]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(result['Data']['RecordList'][one]['AuditBy'] == auditby)
                pytest.assume(result['Data']['RecordList'][one]['AuditRemark'] == idcardaudittuple[one][1])
                pytest.assume(result['Data']['RecordList'][one]['AuditSts'] == idcardaudittuple[one][2])
                if idcardaudittuple[one][3] == '0000-00-00 00:00:00':
                    audit_tm = ''
                else:
                    audit_tm = idcardaudittuple[one][3].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(result['Data']['RecordList'][one]['AuditTm'] == audit_tm)
                pytest.assume(result['Data']['RecordList'][one]['Guid'] == idcardaudittuple[one][4])
                pytest.assume(result['Data']['RecordList'][one]['IdCardNum'] == idcardaudittuple[one][5])
                pytest.assume(result['Data']['RecordList'][one]['IdcardFrontUrl'] == idcardaudittuple[one][6])
                pytest.assume(result['Data']['RecordList'][one]['RealName'] == idcardaudittuple[one][7])
                pytest.assume(result['Data']['RecordList'][one]['RegTime'] == idcardaudittuple[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(result['Data']['RecordList'][one]['UserIdcardAuditId'] == idcardaudittuple[one][9])
                pytest.assume(result['Data']['RecordList'][one]['Mobile'] == idcardaudittuple[one][10])

        with allure.step("step1:不存在审核记录的姓名名称查询并校验返回结果"):
            # 随机生成不存在身份证审核记录的姓名
            while True:
                # 生成姓名
                name = create_name()
                # 校验身份证号码是否存在
                name_sql = f"select id_card_num from member_user_idcard_audit where real_name='{name}'"
                res = self.db.selectsql(name_sql)
                if res == ():
                    break
            #已存在身份证审核记录的姓名查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           RealName=name)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            # 校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == 0)
            pytest.assume(result['Data']['RecordList'] == [])

    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('手机号码查询')
    @allure.severity('blocker')
    def test_idcardinfo_0009(self):
        """
                手机号码查询

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0009.__name__))
        with allure.step("step1:已存在审核记录的手机号码查询并校验返回结果"):
            # 登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在身份证审核记录的手机号码
            mobile_sql = f'select b.mobile,a.guid from member_user_idcard_audit as a left join member_user as b on a.guid=b.guid where  a.is_deleted=0 and a.ec_id={ec_id}'
            res = self.db.selectsql(mobile_sql)
            mobile = random.choice(res)[0]

            # 已存在身份证审核记录的手机号码查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           Mobile=mobile)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            # 获取总条数
            RecordCount_sql = f'SELECT count(*) FROM member_user_idcard_audit as a left join member_user as b on a.guid=b.guid  WHERE a.is_deleted = 0 AND b.mobile={mobile} AND a.ec_id = {ec_id}'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            # 校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == RecordCount)
            # 获取数据库数据
            memberidcardaudit_sql = f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and b.mobile={mobile} ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            idcardaudittuple = self.db.selectsql(memberidcardaudit_sql)
            for one in range(len(result['Data']['RecordList'])):
                if idcardaudittuple[one][0] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={idcardaudittuple[one][0]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(result['Data']['RecordList'][one]['AuditBy'] == auditby)
                pytest.assume(result['Data']['RecordList'][one]['AuditRemark'] == idcardaudittuple[one][1])
                pytest.assume(result['Data']['RecordList'][one]['AuditSts'] == idcardaudittuple[one][2])
                if idcardaudittuple[one][3] == '0000-00-00 00:00:00':
                    audit_tm = ''
                else:
                    audit_tm = idcardaudittuple[one][3].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(result['Data']['RecordList'][one]['AuditTm'] == audit_tm)
                pytest.assume(result['Data']['RecordList'][one]['Guid'] == idcardaudittuple[one][4])
                pytest.assume(result['Data']['RecordList'][one]['IdCardNum'] == idcardaudittuple[one][5])
                pytest.assume(result['Data']['RecordList'][one]['IdcardFrontUrl'] == idcardaudittuple[one][6])
                pytest.assume(result['Data']['RecordList'][one]['RealName'] == idcardaudittuple[one][7])
                pytest.assume(result['Data']['RecordList'][one]['RegTime'] == idcardaudittuple[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(result['Data']['RecordList'][one]['UserIdcardAuditId'] == idcardaudittuple[one][9])
                pytest.assume(result['Data']['RecordList'][one]['Mobile'] == idcardaudittuple[one][10])

        with allure.step("step1:不存在审核记录的手机号码查询并校验返回结果"):
            # 随机生成不存在身份证审核记录的手机号码
            while True:
                # 生成手机号码
                mobile = create_phone()
                # 校验手机号码是否存在
                mobilesql = f"select guid from center_user where login_name={mobile}"
                res = self.db.selectsql(mobilesql)
                if res == ():
                    break
            # 已存在身份证审核记录的姓名查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           Mobile=mobile)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            # 校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == 0)
            pytest.assume(result['Data']['RecordList'] == [])



    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('审核状态查询')
    @allure.severity('blocker')
    @pytest.mark.parametrize('AuditSts',[2,3,1])
    def test_idcardinfo_0010(self,AuditSts):
        """
                审核状态查询

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0009.__name__))
        with allure.step("step1:传入审核状态参数，查询身份证审核记录并校验"):
            # 登录
            self.weblogin.login(pq_boss_user)

            # 传入审核状态参数，查询身份证审核记录
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=AuditSts)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            # 获取总条数
            RecordCount_sql = f'SELECT count(*) FROM member_user_idcard_audit where audit_sts={AuditSts} and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            # 校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == RecordCount)
            # 获取数据库数据
            memberidcardaudit_sql = f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and audit_sts={AuditSts} ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            idcardaudittuple = self.db.selectsql(memberidcardaudit_sql)
            for one in range(len(result['Data']['RecordList'])):
                if idcardaudittuple[one][0] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={idcardaudittuple[one][0]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(result['Data']['RecordList'][one]['AuditBy'] == auditby)
                pytest.assume(result['Data']['RecordList'][one]['AuditRemark'] == idcardaudittuple[one][1])
                pytest.assume(result['Data']['RecordList'][one]['AuditSts'] == idcardaudittuple[one][2])
                if idcardaudittuple[one][3] == '0000-00-00 00:00:00':
                    audit_tm = ''
                else:
                    audit_tm = idcardaudittuple[one][3].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(result['Data']['RecordList'][one]['AuditTm'] == audit_tm)
                pytest.assume(result['Data']['RecordList'][one]['Guid'] == idcardaudittuple[one][4])
                if result['Data']['RecordList'][one]['IdCardNum']=='':
                    pytest.assume(result['Data']['RecordList'][one]['IdCardNum'] == idcardaudittuple[one][5])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                                   DesenData=result['Data']['RecordList'][one]['IdCardNum'])
                    realidcardnum = res.json()['Data']['OriData']
                    pytest.assume(realidcardnum==idcardaudittuple[one][5])
                pytest.assume(result['Data']['RecordList'][one]['IdcardFrontUrl'] == idcardaudittuple[one][6])
                pytest.assume(result['Data']['RecordList'][one]['RealName'] == idcardaudittuple[one][7])
                pytest.assume(result['Data']['RecordList'][one]['RegTime'] == idcardaudittuple[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(result['Data']['RecordList'][one]['UserIdcardAuditId'] == idcardaudittuple[one][9])
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=result['Data']['RecordList'][one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == idcardaudittuple[one][10])



    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('上传日期查询')
    @allure.severity('blocker')
    @pytest.mark.parametrize('RegTimeBegin,RegTimeEnd',[(nowtime,None),
                                                        (None,nowtime),
                                                        (nowtime,nowtime)])
    def test_idcardinfo_0011(self,RegTimeBegin,RegTimeEnd):
        """
                上传日期查询

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0011.__name__))
        with allure.step("step1:已存在审核记录的手机号码查询并校验返回结果"):
            # 登录
            self.weblogin.login(pq_boss_user)

            # 传入审核状态参数，查询身份证审核记录
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           RegTimeBegin=RegTimeBegin,
                                           RegTimeEnd=RegTimeEnd
                                           )
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            if RegTimeBegin==None:
                RegTimeEnd = RegTimeEnd + ' 23:59:59.000000'
            elif RegTimeEnd==None:
                RegTimeBegin = RegTimeBegin + ' 00:00:00.000000'
            else:
                RegTimeBegin=RegTimeBegin+' 00:00:00.000000'
                RegTimeEnd=RegTimeEnd+' 23:59:59.000000'
            # 获取总条数
            if RegTimeBegin==None:
                RecordCount_sql = f"SELECT count(*) FROM member_user_idcard_audit  WHERE (is_deleted = 0) AND (created_tm <= '{RegTimeEnd}') AND (ec_id = {ec_id})"
            elif RegTimeEnd==None:
                RecordCount_sql = f"SELECT count(*) FROM member_user_idcard_audit  WHERE (is_deleted = 0) AND (created_tm >= '{RegTimeBegin}') AND (ec_id = {ec_id})"
            else:
                RecordCount_sql = f"SELECT count(*) FROM member_user_idcard_audit  WHERE (is_deleted = 0) AND (created_tm >= '{RegTimeBegin}') AND (created_tm <= '{RegTimeEnd}') AND (ec_id = {ec_id})"

            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            # 校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == RecordCount)
            # 获取数据库数据
            if RegTimeBegin==None:
                memberidcardaudit_sql=f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.created_tm<='{RegTimeEnd}' ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            elif RegTimeEnd==None:
                memberidcardaudit_sql=f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.created_tm>='{RegTimeBegin}' ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            else:
                memberidcardaudit_sql = f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.created_tm>='{RegTimeBegin}' and a.created_tm<='{RegTimeEnd}' ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            idcardaudittuple = self.db.selectsql(memberidcardaudit_sql)
            for one in range(len(result['Data']['RecordList'])):
                if idcardaudittuple[one][0] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={idcardaudittuple[one][0]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(result['Data']['RecordList'][one]['AuditBy'] == auditby)
                pytest.assume(result['Data']['RecordList'][one]['AuditRemark'] == idcardaudittuple[one][1])
                pytest.assume(result['Data']['RecordList'][one]['AuditSts'] == idcardaudittuple[one][2])
                if idcardaudittuple[one][3] == '0000-00-00 00:00:00':
                    audit_tm = ''
                else:
                    audit_tm = idcardaudittuple[one][3].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(result['Data']['RecordList'][one]['AuditTm'] == audit_tm)
                pytest.assume(result['Data']['RecordList'][one]['Guid'] == idcardaudittuple[one][4])
                if result['Data']['RecordList'][one]['IdCardNum']=='':
                    pytest.assume(result['Data']['RecordList'][one]['IdCardNum'] == idcardaudittuple[one][5])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                                   DesenData=result['Data']['RecordList'][one]['IdCardNum'])
                    realidcardnum = res.json()['Data']['OriData']
                    pytest.assume(realidcardnum==idcardaudittuple[one][5])
                pytest.assume(result['Data']['RecordList'][one]['IdcardFrontUrl'] == idcardaudittuple[one][6])
                pytest.assume(result['Data']['RecordList'][one]['RealName'] == idcardaudittuple[one][7])
                pytest.assume(result['Data']['RecordList'][one]['RegTime'] == idcardaudittuple[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(result['Data']['RecordList'][one]['UserIdcardAuditId'] == idcardaudittuple[one][9])
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=result['Data']['RecordList'][one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == idcardaudittuple[one][10])


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('组合查询')
    @allure.severity('blocker')
    def test_idcardinfo_0012(self):
        """
                填写身份证号码、手机号码、姓名、审核状态、上传日期查询

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0012.__name__))
        with allure.step("step1:填写身份证号码、手机号码、姓名、审核状态、上传日期查询"):
            # 登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在身份证审核记录的身份证号码、手机号码、姓名、审核状态、上传日期
            idcardaudit_sql = f'select a.id_card_num,b.mobile,a.real_name,a.audit_sts,a.created_tm from member_user_idcard_audit as a left join member_user as b on a.guid=b.guid where a.audit_sts=2 and a.is_deleted=0 and a.ec_id={ec_id}'
            res = self.db.selectsql(idcardaudit_sql)
            res1 = random.choice(res)
            idcardnum=res1[0]
            mobile = res1[1]
            name = res1[2]
            auditsts = res1[3]
            create_tm = res1[4].__format__('%Y-%m-%d')
            #构造RegTimeBegin和RegTimeEnd
            RegTimeBegin=create_tm+' 00:00:00.000000'
            RegTimeEnd=create_tm+' 23:59:59.000000'
            # 身份证号码、手机号码、姓名、审核状态、上传日期查询
            res = self.weblogin.create_api(IDCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=auditsts,
                                           IdCardNum=idcardnum,
                                           Mobile=mobile,
                                           RealName=name,
                                           RegTimeBegin=RegTimeBegin,
                                           RegTimeEnd=RegTimeEnd)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            # 获取总条数
            RecordCount_sql = f"select count(*) from member_user_idcard_audit as a left join member_user as b on a.guid=b.guid where b.mobile={mobile} and a.is_deleted=0 and a.audit_sts={auditsts} and a.id_card_num='{idcardnum}' and a.real_name like '%{name}%' and a.created_tm >= '{RegTimeBegin}' and a.created_tm <= '{RegTimeEnd}' and a.ec_id = {ec_id}"
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            # 校验接口返回数据
            pytest.assume(result['Data']['RecordCount'] == RecordCount)
            # 获取数据库数据
            memberidcardaudit_sql = f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE b.mobile={mobile} and a.is_deleted=0 and a.audit_sts={auditsts} and a.id_card_num={idcardnum} and a.real_name like '%{name}%' and a.created_tm >= '{RegTimeBegin}' and a.created_tm <= '{RegTimeEnd}' and a.ec_id = {ec_id} ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            idcardaudittuple = self.db.selectsql(memberidcardaudit_sql)
            for one in range(len(result['Data']['RecordList'])):
                if idcardaudittuple[one][0] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={idcardaudittuple[one][0]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(result['Data']['RecordList'][one]['AuditBy'] == auditby)
                pytest.assume(result['Data']['RecordList'][one]['AuditRemark'] == idcardaudittuple[one][1])
                pytest.assume(result['Data']['RecordList'][one]['AuditSts'] == idcardaudittuple[one][2])
                if idcardaudittuple[one][3] == '0000-00-00 00:00:00':
                    audit_tm = ''
                else:
                    audit_tm = idcardaudittuple[one][3].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(result['Data']['RecordList'][one]['AuditTm'] == audit_tm)
                pytest.assume(result['Data']['RecordList'][one]['Guid'] == idcardaudittuple[one][4])
                pytest.assume(result['Data']['RecordList'][one]['IdCardNum'] == idcardaudittuple[one][5])
                pytest.assume(result['Data']['RecordList'][one]['IdcardFrontUrl'] == idcardaudittuple[one][6])
                pytest.assume(result['Data']['RecordList'][one]['RealName'] == idcardaudittuple[one][7])
                pytest.assume(result['Data']['RecordList'][one]['RegTime'] == idcardaudittuple[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(result['Data']['RecordList'][one]['UserIdcardAuditId'] == idcardaudittuple[one][9])
                pytest.assume(result['Data']['RecordList'][one]['Mobile'] == idcardaudittuple[one][10])




    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('刷新待审核状态的身份证')
    @allure.severity('blocker')
    def test_idcardinfo_0013(self):
        """
                刷新待审核状态的身份证

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0013.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)

        with allure.step("step2:刷新身份证审核记录"):
            res=upthreecard.weblogin.create_api(ZXX_CmsIdCardQuery_Api,UserIdcardAuditId=idcardaudit_id)
            result=res.json()

        with allure.step("step3:校验接口返回的结果"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data']==None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("step3:校验身份证审核记录审核状态仍为待审核状态"):
            idcardaudit_sql=f'select audit_sts from member_user_idcard_audit where user_idcard_audit_id={idcardaudit_id} and ec_id={ec_id}'
            res=self.db.selectsql(idcardaudit_sql)
            audit_sts=res[0][0]
            pytest.assume(audit_sts==1)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('手动审核身份证成功')
    @allure.severity('blocker')
    def test_idcardinfo_0014(self):
        """
                手动审核身份证成功

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0014.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)


        with allure.step("step2:手动审核通过身份证"):
            while True:
                idcardnum=create_IDCard()
                #校验身份证在member_user_unique表不存在
                unique_sql=f'select * from member_user_unique where id_card_num={idcardnum}'
                res=self.db.selectsql(unique_sql)
                if res==():
                    break

            name=create_name()
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("step3:校验接口返回数据"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("step4:校验member_user_idcardaudit表数据"):
            idcardaudit_sql=f'select real_name,id_card_num,gender,audit_sts,audit_by,audit_remark,audit_name from member_user_idcard_audit where user_idcard_audit_id={idcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(idcardaudit_sql)
            pytest.assume(res[0][0]==name)
            pytest.assume(res[0][1] == idcardnum)
            #校验身份证倒数第二位数是奇数还是偶数
            ge=int(idcardnum[-2])
            if (ge % 2) == 0:
                ge=2
            else:
                ge=1
            pytest.assume(res[0][2]==ge)
            pytest.assume(res[0][3] == 2)
            #获取审核人
            tenantuser_sql=f'SELECT guid,user_name FROM tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id} and is_deleted=0'
            res1=self.db.selectsql(tenantuser_sql)
            pytest.assume(res[0][4] == res1[0][0])
            pytest.assume(res[0][5] == '人工审核通过')
            pytest.assume(res[0][6] == res1[0][1])

        with allure.step("step4:校验member_user_idcard表数据"):
            idcard_sql=f'select guid,real_name,id_card_num,gender from member_user_idcard where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(idcard_sql)
            pytest.assume(res[0][0]==upthreecard.minilogin.Guid)
            pytest.assume(res[0][1] == name)
            pytest.assume(res[0][2] == idcardnum)
            pytest.assume(res[0][3] == ge)

        with allure.step("step5:校验member_user_unique表数据"):
            unique_sql=f'select uuid,id_card_num,real_name from member_user_unique where id_card_num={idcardnum}'
            res=self.db.selectsql(unique_sql)
            uuid=res[0][0]
            pytest.assume(res[0][1]==idcardnum)
            pytest.assume(res[0][2] == name)

        with allure.step("step6:校验member_user表数据"):
            memberuser_sql=f'select uuid,guid from member_user where guid={upthreecard.minilogin.Guid} and is_deleted=0 and is_enabled=1 and ec_id={ec_id}'
            res=self.db.selectsql(memberuser_sql)
            pytest.assume(res[0][0]==uuid)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('待审核状态身份证手动审核不通过')
    @allure.severity('blocker')
    def test_idcardinfo_0015(self):
        """
                待审核状态身份证手动审核不通过

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0015.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)


        with allure.step("step2:手动审核不通过身份证"):
            res=upthreecard.weblogin.create_api(ZXX_GetNextIDCardPic_Api,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("step3:校验接口返回数据"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("step4:校验member_user_idcardaudit表数据"):
            idcardaudit_sql=f'select real_name,id_card_num,gender,audit_sts,audit_by,audit_remark,audit_name from member_user_idcard_audit where user_idcard_audit_id={idcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(idcardaudit_sql)
            pytest.assume(res[0][0]=='')
            pytest.assume(res[0][1] == '')
            pytest.assume(res[0][2]==0)
            pytest.assume(res[0][3] == 3)
            #获取审核人
            tenantuser_sql=f'SELECT guid,user_name FROM tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id} and is_deleted=0'
            res1=self.db.selectsql(tenantuser_sql)
            pytest.assume(res[0][4] == res1[0][0])
            pytest.assume(res[0][5] == '看不清')
            pytest.assume(res[0][6] == res1[0][1])


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('填写已存在的身份证号码审核通过')
    @allure.severity('blocker')
    def test_idcardinfo_0016(self):
        """
                填写ec下已审核通过的身份证号码和姓名，审核通过身份证

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0016.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #获取已审核通过的身份证号码和姓名
            idcard_sql=f'select real_name,id_card_num from member_user_idcard where is_deleted=0 and ec_id={ec_id}'
            another_idcard=self.db.selectsql(idcard_sql)
            res1=random.choice(another_idcard)
            name=res1[0]
            idcardnum=res1[1]


        with allure.step("step2:手动审核通过身份证"):
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("step3:校验接口返回数据"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("step4:校验member_user_idcardaudit表数据"):
            idcardaudit_sql=f'select real_name,id_card_num,gender,audit_sts,audit_by,audit_remark,audit_name from member_user_idcard_audit where user_idcard_audit_id={idcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(idcardaudit_sql)
            pytest.assume(res[0][0]==name)
            pytest.assume(res[0][1] == idcardnum)
            #校验身份证倒数第二位数是奇数还是偶数
            ge=int(idcardnum[-2])
            if (ge % 2) == 0:
                ge=2
            else:
                ge=1
            pytest.assume(res[0][2]==ge)
            pytest.assume(res[0][3] == 2)
            #获取审核人
            tenantuser_sql=f'SELECT guid,user_name FROM tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id} and is_deleted=0'
            res1=self.db.selectsql(tenantuser_sql)
            pytest.assume(res[0][4] == res1[0][0])
            pytest.assume(res[0][5] == '人工审核通过')
            pytest.assume(res[0][6] == res1[0][1])


        with allure.step("step5:校验member_user_idcard表数据"):
            #校验相同身份证号码的原数据不变
            idcard_sql = f'select real_name,id_card_num from member_user_idcard where is_deleted=0 and ec_id={ec_id} and guid<>{upthreecard.minilogin.Guid}'
            another_idcard1 = self.db.selectsql(idcard_sql)
            pytest.assume(another_idcard==another_idcard1)
            #校验新增的数据
            idcard_sql=f'select guid,real_name,id_card_num,gender from member_user_idcard where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(idcard_sql)
            pytest.assume(res[0][0]==upthreecard.minilogin.Guid)
            pytest.assume(res[0][1] == name)
            pytest.assume(res[0][2] == idcardnum)
            pytest.assume(res[0][3] == ge)

        with allure.step("step6:校验member_user_unique表数据"):
            unique_sql=f'select uuid,id_card_num,real_name from member_user_unique where id_card_num={idcardnum}'
            res=self.db.selectsql(unique_sql)
            uuid=res[0][0]
            pytest.assume(res[0][1]==idcardnum)
            pytest.assume(res[0][2] == name)

        with allure.step("step7:校验member_user表数据"):
            memberuser_sql=f'select uuid,guid from member_user where guid={upthreecard.minilogin.Guid} and is_deleted=0 and is_enabled=1 and ec_id={ec_id}'
            res=self.db.selectsql(memberuser_sql)
            pytest.assume(res[0][0]==uuid)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('身份证最后一位为小写“x”，身份证审核通过')
    @allure.severity('blocker')
    def test_idcardinfo_0017(self):
        """
                身份证最后一位为小写“x”，身份证审核通过

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0017.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)


        with allure.step("step2:手动审核通过身份证"):
            #生成系统不存在的身份证号码
            while True:
                #生成最后一位为X的身份证号码
                idcardnum=create_IDCard()
                idcardnum=idcardnum[0:17]+'x'
                real_idcardnum=idcardnum[0:17]+'X'
                #校验身份证在member_user_unique表不存在
                unique_sql=f"select * from member_user_unique where id_card_num='{real_idcardnum}'"
                res=self.db.selectsql(unique_sql)
                if res==():
                    break

            name=create_name()
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("step3:校验接口返回数据"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("step4:校验member_user_idcardaudit表数据"):
            idcardaudit_sql=f'select real_name,id_card_num,gender,audit_sts,audit_by,audit_remark,audit_name from member_user_idcard_audit where user_idcard_audit_id={idcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(idcardaudit_sql)
            pytest.assume(res[0][0]==name)
            pytest.assume(res[0][1] == real_idcardnum)
            #校验身份证倒数第二位数是奇数还是偶数
            ge=int(real_idcardnum[-2])
            if (ge % 2) == 0:
                ge=2
            else:
                ge=1
            pytest.assume(res[0][2]==ge)
            pytest.assume(res[0][3] == 2)
            #获取审核人
            tenantuser_sql=f'SELECT guid,user_name FROM tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id} and is_deleted=0'
            res1=self.db.selectsql(tenantuser_sql)
            pytest.assume(res[0][4] == res1[0][0])
            pytest.assume(res[0][5] == '人工审核通过')
            pytest.assume(res[0][6] == res1[0][1])

        with allure.step("step4:校验member_user_idcard表数据"):
            idcard_sql=f'select guid,real_name,id_card_num,gender from member_user_idcard where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(idcard_sql)
            pytest.assume(res[0][0]==upthreecard.minilogin.Guid)
            pytest.assume(res[0][1] == name)
            pytest.assume(res[0][2] == real_idcardnum)
            pytest.assume(res[0][3] == ge)

        with allure.step("step5:校验member_user_unique表数据"):
            unique_sql=f"select uuid,id_card_num,real_name from member_user_unique where id_card_num='{real_idcardnum}'"
            res=self.db.selectsql(unique_sql)
            uuid=res[0][0]
            pytest.assume(res[0][1]==real_idcardnum)
            pytest.assume(res[0][2] == name)

        with allure.step("step6:校验member_user表数据"):
            memberuser_sql=f'select uuid,guid from member_user where guid={upthreecard.minilogin.Guid} and is_deleted=0 and is_enabled=1 and ec_id={ec_id}'
            res=self.db.selectsql(memberuser_sql)
            pytest.assume(res[0][0]==uuid)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('会员已有结算名单，审核身份证成功')
    @allure.severity('blocker')
    def test_idcardinfo_0018(self):
        """
                会员已有结算名单，审核身份证成功

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0018.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            #生成身份证号码
            idcardnum=create_IDCard()
            #生成姓名
            name=create_name()
            #创建可预支名单
            namelist_id=namelistsettle.add_namelist_settle(idcardnum,name,nowtime)
            while True:
                time.sleep(5)
                settle_sql=f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res=self.db.selectsql(settle_sql)
                if res!=():
                    break
            #校验name_list_settle表的uuid
            settle_uuid_sql=f'select uuid from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            res=self.db.selectsql(settle_uuid_sql)
            pytest.assume(res[0][0]==0)


        with allure.step("step2:手动审核通过身份证"):
            #审核通过身份证
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("step3:校验接口返回数据"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("step4:校验name_list_settle表的uuid"):
            #获取身份证审核生成的uuid
            member_user_sql=f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res=self.db.selectsql(member_user_sql)
            uuid=res[0][0]
            time.sleep(1)
            #获取可预支名单的uuid
            settle_uuid_sql = f'select uuid from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            res = self.db.selectsql(settle_uuid_sql)
            pytest.assume(res[0][0]==uuid)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('会员已有多条结算名单，审核身份证成功')
    @allure.severity('blocker')
    def test_idcardinfo_0019(self):
        """
                会员已有多条结算名单，审核身份证成功

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0019.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            #生成身份证号码
            idcardnum=create_IDCard()
            #生成姓名
            name=create_name()
            #创建可预支名单
            namelist_id=namelistsettle.add_namelist_settle(idcardnum,name,nowtime)
            while True:
                time.sleep(5)
                settle_sql=f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res=self.db.selectsql(settle_sql)
                if res!=():
                    break
            #校验name_list_settle表的uuid
            settle_uuid_sql=f'select uuid from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            res=self.db.selectsql(settle_uuid_sql)
            pytest.assume(res[0][0]==0)

            #再次创建可预支名单
            beforedate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            namelist_id1 = namelistsettle.add_namelist_settle(idcardnum, name, beforedate)
            while True:
                time.sleep(5)
                settle_sql = f'select * from name_list_settle where name_list_id={namelist_id1} and ec_id={ec_id}'
                res = self.db.selectsql(settle_sql)
                if res != ():
                    break
            # 校验name_list_settle表的uuid
            settle_uuid_sql = f'select uuid from name_list_settle where name_list_id={namelist_id1} and ec_id={ec_id}'
            res = self.db.selectsql(settle_uuid_sql)
            pytest.assume(res[0][0] == 0)



        with allure.step("step2:手动审核通过身份证"):
            #审核通过身份证
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("step3:校验接口返回数据"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("step4:校验name_list_settle表的uuid"):
            #获取身份证审核生成的uuid
            member_user_sql=f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res=self.db.selectsql(member_user_sql)
            uuid=res[0][0]
            #获取可预支名单的uuid
            settle_uuid_sql = f'select uuid from name_list_settle where name_list_id in ({namelist_id},{namelist_id1}) and ec_id={ec_id}'
            res = self.db.selectsql(settle_uuid_sql)
            pytest.assume(res[0][0]==uuid)
            pytest.assume(res[1][0] == uuid)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('会员已有打卡记录，审核身份证成功')
    @allure.severity('blocker')
    def test_idcardinfo_0020(self):
        """
                会员已有打卡记录，审核身份证成功

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0020.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #会员打卡生成上传打卡记录
            upthreecard.clock(1)

        with allure.step("预期结果:打卡记录表的uuid为0"):
            clock_rec_sql=f'SELECT uuid FROM member_user_clock_rec where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res=self.db.selectsql(clock_rec_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==0)


        with allure.step("step2:手动审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成姓名
            name = create_name()
            #审核通过身份证
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("预期结果:校验接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("预期结果:校验member_user_clock_rec表中uuid更新正确"):
            # 获取身份证审核生成的uuid
            member_user_sql = f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res = self.db.selectsql(member_user_sql)
            uuid = res[0][0]
            #校验member_user_clock_rec表中uuid是否正确
            clock_rec_sql = f'SELECT uuid FROM member_user_clock_rec where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res = self.db.selectsql(clock_rec_sql)
            pytest.assume(res[0][0]==uuid)


    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('会员已有小程序补卡记录，审核身份证成功')
    @allure.severity('blocker')
    def test_idcardinfo_0021(self):
        """
                会员已有小程序补卡记录，审核身份证成功

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0021.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #会员补卡
            date=(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            datetm = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")
            upthreecard.repair_clock(date,datetm,1)

        with allure.step("预期结果:member_user_repair_clock_rec表的uuid为0"):
            repairclock_rec_sql=f'SELECT uuid FROM member_user_repair_clock_rec where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res=self.db.selectsql(repairclock_rec_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==0)


        with allure.step("step2:手动审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成姓名
            name = create_name()
            #审核通过身份证
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("预期结果:校验接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("预期结果:校验member_user_repair_clock_rec表中uuid更新正确"):
            # 获取身份证审核生成的uuid
            member_user_sql = f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res = self.db.selectsql(member_user_sql)
            uuid = res[0][0]
            #校验member_user_clock_rec表中uuid是否正确
            repairclock_rec_sql = f'SELECT uuid FROM member_user_repair_clock_rec where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res = self.db.selectsql(repairclock_rec_sql)
            pytest.assume(res[0][0]==uuid)



    @allure.feature('会员信息管理')
    @allure.story('身份证信息查询')
    @allure.title('会员已上传工牌，审核身份证成功')
    @allure.severity('blocker')
    def test_idcardinfo_0022(self):
        """
                会员已上传工牌，审核身份证成功

        """
        print('\n{}测试开始\n'.format(self.test_idcardinfo_0022.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)


        with allure.step("预期结果:member_user_work_card_audit表的uuid为0"):
            workcardaudit_sql=f'SELECT uuid FROM member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and ec_id={ec_id}'
            res=self.db.selectsql(workcardaudit_sql)
            pytest.assume(res[0][0]==0)


        with allure.step("step2:手动审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成姓名
            name = create_name()
            #审核通过身份证
            res=upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                IdCardNum=idcardnum,
                                                RealName=name,
                                                UserIdcardAuditId=idcardaudit_id)
            result=res.json()
        with allure.step("预期结果:校验接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Data'] == None)
            pytest.assume(result['Desc'] == '成功')

        with allure.step("预期结果:校验member_user_work_card_audit表中uuid更新正确"):
            # 获取身份证审核生成的uuid
            member_user_sql = f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res = self.db.selectsql(member_user_sql)
            uuid = res[0][0]
            #校验member_user_clock_rec表中uuid是否正确
            workcardaudit_sql = f'SELECT uuid FROM member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and ec_id={ec_id}'
            res = self.db.selectsql(workcardaudit_sql)
            pytest.assume(res[0][0]==uuid)







