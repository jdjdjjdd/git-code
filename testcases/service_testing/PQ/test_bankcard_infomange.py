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

class Testbankcardinfo:

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
    @allure.story('银行卡信息查询')
    @allure.title('身份证未审核状态银行卡信息记录检查')
    @allure.severity('blocker')
    def test_bankcardinfo_0001(self):
        """
                身份证未审核状态银行卡信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0001.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            bankcardaudit_id=upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step2:查看上传的银行卡记录信息"):
            # {"SequenceUploadTime":1,"RecordIndex":0,"RecordSize":10,"AuditSts":-9999,"Mobile":"17236738937"}
            res=upthreecard.weblogin.create_api(BankCardInfoList_Api,
                                                SequenceUploadTime=1,
                                                RecordIndex=0,
                                                RecordSize=10,
                                                AuditSts=-9999,
                                                Mobile=upthreecard.mobile)
            result=res.json()
        with allure.step("预期结果:接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt'] == 0)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 1)
            pytest.assume(result['Data']['UnPassCnt'] == 0)
            #获取待审核银行卡数量
            UnAuditRecordCount_sql=f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(UnAuditRecordCount_sql)
            UnAuditRecordCount=res[0][0]
            pytest.assume(result['Data']['UnAuditRecordCount'] == UnAuditRecordCount)
            #获取会员上传的银行卡member_user_bank_card_audit表数据
            bankcardaudit_sql=f'select ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id from member_user_bank_card_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res1=self.db.selectsql(bankcardaudit_sql)
            #获取会员上传的身份证member_user_idcard_audit表数据
            idcardaudit_sql=f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id} order by audit_tm,created_tm desc limit 1'
            res2=self.db.selectsql(idcardaudit_sql)

            pytest.assume(len(res1)==1)

            #构造对比数据
            dict={'AliBucket':res1[0][0],
                  'AreaName':'',
                  'AuditBy':'',
                  'AuditRemark':res1[0][2],
                  'AuditSts':res1[0][3],
                  'AuditTm':res1[0][4],
                  'BankCardNum':res1[0][5],
                  'BankCardUrl':res1[0][6],
                  'BankName':res1[0][7],
                  'CityName':'',
                  'IdCardAuditSts':res2[0][0],
                  'IdCardNum':res2[0][1],
                  'IdcardFrontUrl':res2[0][2],
                  'Mobile':upthreecard.mobile,
                  'ProvinceName':'',
                  'RealName':res2[0][3],
                  'UploadTime':res1[0][8].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserBankCardAuditId':res1[0][9],
                  'UserIdcardAuditId':res2[0][4]
            }
            pytest.assume(result['Data']['RecordList'][0]==dict)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('身份证审核不通过状态银行卡信息记录检查')
    @allure.severity('blocker')
    def test_bankcardinfo_0002(self):
        """
                身份证审核不通过状态银行卡信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0002.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传银行卡
            bankcardaudit_id=upthreecard.upload_bankcard(fakerbankcardpicture)
            #审核不通过身份证
            upthreecard.idcard_auditnopass(idcardaudit_id)

        with allure.step("step2:查看上传的银行卡记录信息"):
            # {"SequenceUploadTime":1,"RecordIndex":0,"RecordSize":10,"AuditSts":-9999,"Mobile":"17236738937"}
            res=upthreecard.weblogin.create_api(BankCardInfoList_Api,
                                                SequenceUploadTime=1,
                                                RecordIndex=0,
                                                RecordSize=10,
                                                AuditSts=-9999,
                                                Mobile=upthreecard.mobile)
            result=res.json()
        with allure.step("预期结果:接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt'] == 0)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 1)
            pytest.assume(result['Data']['UnPassCnt'] == 0)
            #获取待审核银行卡数量
            UnAuditRecordCount_sql=f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(UnAuditRecordCount_sql)
            UnAuditRecordCount=res[0][0]
            pytest.assume(result['Data']['UnAuditRecordCount'] == UnAuditRecordCount)
            #获取会员上传的银行卡member_user_bank_card_audit表数据
            bankcardaudit_sql=f'select ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id from member_user_bank_card_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res1=self.db.selectsql(bankcardaudit_sql)
            #获取会员上传的身份证member_user_idcard_audit表数据
            idcardaudit_sql=f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id} order by audit_tm,created_tm desc limit 1'
            res2=self.db.selectsql(idcardaudit_sql)

            pytest.assume(len(res1)==1)

            #构造对比数据
            dict={'AliBucket':res1[0][0],
                  'AreaName':'',
                  'AuditBy':'',
                  'AuditRemark':res1[0][2],
                  'AuditSts':res1[0][3],
                  'AuditTm':res1[0][4],
                  'BankCardNum':res1[0][5],
                  'BankCardUrl':res1[0][6],
                  'BankName':res1[0][7],
                  'CityName':'',
                  'IdCardAuditSts':res2[0][0],
                  'IdCardNum':res2[0][1],
                  'IdcardFrontUrl':'',
                  'Mobile':upthreecard.mobile,
                  'ProvinceName':'',
                  'RealName':res2[0][3],
                  'UploadTime':res1[0][8].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserBankCardAuditId':res1[0][9],
                  'UserIdcardAuditId':0
            }
            pytest.assume(result['Data']['RecordList'][0]==dict)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('身份证审核通过状态，未审核状态的银行信息记录检查')
    @allure.severity('blocker')
    def test_bankcardinfo_0003(self):
        """
                身份证审核通过状态，未审核状态的银行信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0003.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传银行卡
            bankcardaudit_id=upthreecard.upload_bankcard(fakerbankcardpicture)
            #审核不通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)

        with allure.step("step2:查看上传的银行卡记录信息"):
            # {"SequenceUploadTime":1,"RecordIndex":0,"RecordSize":10,"AuditSts":-9999,"Mobile":"17236738937"}
            res=upthreecard.weblogin.create_api(BankCardInfoList_Api,
                                                SequenceUploadTime=1,
                                                RecordIndex=0,
                                                RecordSize=10,
                                                AuditSts=-9999,
                                                Mobile=upthreecard.mobile)
            result=res.json()
        with allure.step("预期结果:接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt'] == 0)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 1)
            pytest.assume(result['Data']['UnPassCnt'] == 0)
            #获取待审核银行卡数量
            UnAuditRecordCount_sql=f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(UnAuditRecordCount_sql)
            UnAuditRecordCount=res[0][0]
            pytest.assume(result['Data']['UnAuditRecordCount'] == UnAuditRecordCount)
            #获取会员上传的银行卡member_user_bank_card_audit表数据
            bankcardaudit_sql=f'select ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id from member_user_bank_card_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res1=self.db.selectsql(bankcardaudit_sql)
            #获取会员上传的身份证member_user_idcard_audit表数据
            idcardaudit_sql=f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id} order by audit_tm,created_tm desc limit 1'
            res2=self.db.selectsql(idcardaudit_sql)

            pytest.assume(len(res1)==1)

            #构造对比数据
            dict={'AliBucket':res1[0][0],
                  'AreaName':'',
                  'AuditBy':'',
                  'AuditRemark':res1[0][2],
                  'AuditSts':res1[0][3],
                  'AuditTm':res1[0][4],
                  'BankCardNum':res1[0][5],
                  'BankCardUrl':res1[0][6],
                  'BankName':res1[0][7],
                  'CityName':'',
                  'IdCardAuditSts':res2[0][0],
                  'IdCardNum':res2[0][1],
                  'IdcardFrontUrl':'',
                  'Mobile':upthreecard.mobile,
                  'ProvinceName':'',
                  'RealName':res2[0][3],
                  'UploadTime':res1[0][8].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserBankCardAuditId':res1[0][9],
                  'UserIdcardAuditId':0
            }
            pytest.assume(result['Data']['RecordList'][0]==dict)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('身份证审核通过状态，审核通过银行卡信息记录检查')
    @allure.severity('blocker')
    def test_bankcardinfo_0004(self):
        """
                身份证审核通过状态，审核通过银行卡信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0004.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传银行卡
            bankcardaudit_id=upthreecard.upload_bankcard(fakerbankcardpicture)
            #审核不通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)
            #审核通过银行卡
            upthreecard.bankcard_auditpass(bankcardaudit_id)

        with allure.step("step2:查看上传的银行卡记录信息"):
            # {"SequenceUploadTime":1,"RecordIndex":0,"RecordSize":10,"AuditSts":-9999,"Mobile":"17236738937"}
            res=upthreecard.weblogin.create_api(BankCardInfoList_Api,
                                                SequenceUploadTime=1,
                                                RecordIndex=0,
                                                RecordSize=10,
                                                AuditSts=-9999,
                                                Mobile=upthreecard.mobile)
            result=res.json()
        with allure.step("预期结果:接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt'] == 1)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 0)
            pytest.assume(result['Data']['UnPassCnt'] == 0)
            #获取待审核银行卡数量
            UnAuditRecordCount_sql=f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(UnAuditRecordCount_sql)
            UnAuditRecordCount=res[0][0]
            pytest.assume(result['Data']['UnAuditRecordCount'] == UnAuditRecordCount)
            #获取会员上传的银行卡member_user_bank_card_audit表数据
            bankcardaudit_sql=f'select ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id from member_user_bank_card_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res1=self.db.selectsql(bankcardaudit_sql)
            #获取会员上传的身份证member_user_idcard_audit表数据
            idcardaudit_sql=f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id} order by audit_tm,created_tm desc limit 1'
            res2=self.db.selectsql(idcardaudit_sql)

            pytest.assume(len(res1)==1)
            # 获取AuditBy
            tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={res1[0][1]} and t_id={pq_tenant_id} and is_deleted=0'
            auditbyres = self.db.selectsql(tenant_user_sql)
            auditby = auditbyres[0][0]

            #构造对比数据
            dict={'AliBucket':res1[0][0],
                  'AreaName':'',
                  'AuditBy':auditby,
                  'AuditRemark':res1[0][2],
                  'AuditSts':res1[0][3],
                  'AuditTm':res1[0][4].__format__('%Y-%m-%d %H:%M:%S'),
                  'BankCardNum':res1[0][5],
                  'BankCardUrl':res1[0][6],
                  'BankName':res1[0][7],
                  'CityName':'',
                  'IdCardAuditSts':res2[0][0],
                  'IdCardNum':res2[0][1],
                  'IdcardFrontUrl':'',
                  'Mobile':upthreecard.mobile,
                  'ProvinceName':'',
                  'RealName':res2[0][3],
                  'UploadTime':res1[0][8].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserBankCardAuditId':res1[0][9],
                  'UserIdcardAuditId':0
            }
            pytest.assume(result['Data']['RecordList'][0]==dict)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('身份证审核通过状态，审核不通过银行卡信息记录检查')
    @allure.severity('blocker')
    def test_bankcardinfo_0005(self):
        """
                身份证审核通过状态，审核不通过银行卡信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0005.__name__))
        with allure.step("step1:前置条件准备"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传银行卡
            bankcardaudit_id=upthreecard.upload_bankcard(fakerbankcardpicture)
            #审核不通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)
            #审核通过银行卡
            upthreecard.bankcard_auditnopass(bankcardaudit_id)

        with allure.step("step2:查看上传的银行卡记录信息"):
            # {"SequenceUploadTime":1,"RecordIndex":0,"RecordSize":10,"AuditSts":-9999,"Mobile":"17236738937"}
            res=upthreecard.weblogin.create_api(BankCardInfoList_Api,
                                                SequenceUploadTime=1,
                                                RecordIndex=0,
                                                RecordSize=10,
                                                AuditSts=-9999,
                                                Mobile=upthreecard.mobile)
            result=res.json()
        with allure.step("预期结果:接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['NeedDesen']==0)
            pytest.assume(result['Data']['PassCnt'] == 0)
            pytest.assume(result['Data']['RecordCount'] == 1)
            pytest.assume(result['Data']['UnAuditCnt'] == 0)
            pytest.assume(result['Data']['UnPassCnt'] == 1)
            #获取待审核银行卡数量
            UnAuditRecordCount_sql=f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(UnAuditRecordCount_sql)
            UnAuditRecordCount=res[0][0]
            pytest.assume(result['Data']['UnAuditRecordCount'] == UnAuditRecordCount)
            #获取会员上传的银行卡member_user_bank_card_audit表数据
            bankcardaudit_sql=f'select ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id from member_user_bank_card_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}'
            res1=self.db.selectsql(bankcardaudit_sql)
            #获取会员上传的身份证member_user_idcard_audit表数据
            idcardaudit_sql=f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id} order by audit_tm,created_tm desc limit 1'
            res2=self.db.selectsql(idcardaudit_sql)

            pytest.assume(len(res1)==1)
            # 获取AuditBy
            tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={res1[0][1]} and t_id={pq_tenant_id} and is_deleted=0'
            auditbyres = self.db.selectsql(tenant_user_sql)
            auditby = auditbyres[0][0]

            #构造对比数据
            dict={'AliBucket':res1[0][0],
                  'AreaName':'',
                  'AuditBy':auditby,
                  'AuditRemark':res1[0][2],
                  'AuditSts':res1[0][3],
                  'AuditTm':res1[0][4].__format__('%Y-%m-%d %H:%M:%S'),
                  'BankCardNum':res1[0][5],
                  'BankCardUrl':res1[0][6],
                  'BankName':res1[0][7],
                  'CityName':'',
                  'IdCardAuditSts':res2[0][0],
                  'IdCardNum':res2[0][1],
                  'IdcardFrontUrl':'',
                  'Mobile':upthreecard.mobile,
                  'ProvinceName':'',
                  'RealName':res2[0][3],
                  'UploadTime':res1[0][8].__format__('%Y-%m-%d %H:%M:%S.%f'),
                  'UserBankCardAuditId':res1[0][9],
                  'UserIdcardAuditId':0
            }
            pytest.assume(result['Data']['RecordList'][0]==dict)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('统计信息数据检查')
    @allure.severity('blocker')
    def test_bankcardinfo_0006(self):
        """
                统计信息数据检查

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0006.__name__))
        with allure.step("step1:查询全部的银行卡记录"):
            #登录
            self.weblogin.login(pq_boss_user)
            #获取全部的银行卡记录
            res=self.weblogin.create_api(BankCardInfoList_Api,
                                     SequenceUploadTime=1,
                                     RecordIndex=0,
                                     RecordSize=10,
                                     AuditSts=-9999,
                                     IsUserDelete=-9999,
                                     Bank3keyAvlSts=-9999,
                                     Bank3keyCheckResult=-9999)
            res_data=res.json()['Data']
        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code']==0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):
            # 获取待审核数量
            unanditcnt_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcnt_sql)
            unanditcnt = res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=2 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=3 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f'select count(*) from member_user_bank_card_audit where is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcnt)
            pytest.assume(res_data['RecordCount'] == RecordCount)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('银行卡信息列表查看未脱敏手机号、未脱敏身份证号码、未脱敏银行卡号')
    @allure.severity('blocker')
    def test_bankcardinfo_0007(self):
        """
                银行卡信息列表查看未脱敏手机号、未脱敏身份证号码、未脱敏银行卡号

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0007.__name__))
        with allure.step("step1:查询审核通过的银行卡审核记录并随机获取一个银行卡记录"):
            #登录
            self.weblogin.login(pq_boss_user)
            #获取审核通过状态的银行卡审核记录列表
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=2)
            bankcardlist = res.json()['Data']['RecordList']
            #随机获取一条银行卡审核记录
            bankcardinfo=random.choice(bankcardlist)
            #获取脱敏的手机号码
            desenmobile=bankcardinfo['Mobile']
            #获取脱敏的身份证号码
            desenidcardnum = bankcardinfo['IdCardNum']
            #获取脱敏的银行卡号
            desenbankcardnum=bankcardinfo['BankCardNum']
            #获取银行卡审核记录的audit_id
            audit_id=bankcardinfo['UserBankCardAuditId']
            # 获取guid
            guid_sql=f'select guid from member_user_bank_card_audit where user_bank_card_audit_id={audit_id} and ec_id={ec_id} and is_deleted=0'
            res=self.db.selectsql(guid_sql)
            guid=res[0][0]
        with allure.step("step2:获取选择的银行记录的未脱敏的银行卡号、身份证号码、手机号码"):
            #获取数据库未脱敏的银行卡号、身份证号码、手机号码
            bankcardcardaudit_sql=f'select bank_card_num from member_user_bank_card_audit where user_bank_card_audit_id={audit_id} and ec_id={ec_id}'
            res=self.db.selectsql(bankcardcardaudit_sql)
            bankcardnum=res[0][0]
            # 获取数据库未脱敏的身份证号码
            idcardnum_sql=f'select id_card_num from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
            res = self.db.selectsql(idcardnum_sql)
            idcardnum = res[0][0]
            # 获取数据库未脱敏的手机号码
            member_user_sql=f'select mobile from member_user where guid={guid} and ec_id={ec_id}'
            res = self.db.selectsql(member_user_sql)
            mobile = res[0][0]

        with allure.step("step3:查看未脱敏的手机号码并校验返回值"):
            #查看未脱敏的手机号码
            res=self.weblogin.create_api(DecryptAPI,Typ=1,DesenData=desenmobile)
            result=res.json()
        with allure.step("预期结果:接口返回的数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['DesenData']==desenmobile)
            pytest.assume(result['Data']['OriData'] == mobile)
            pytest.assume(result['Data']['Typ'] == 1)

        with allure.step("step5:查看未脱敏的身份证号码并校验返回值"):
            # 查看未脱敏的身份证号码
            res = self.weblogin.create_api(DecryptAPI, Typ=2, DesenData=desenidcardnum)
            result = res.json()
        with allure.step("预期结果:接口返回的数据正确"):
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['DesenData'] == desenidcardnum)
            pytest.assume(result['Data']['OriData'] == idcardnum)
            pytest.assume(result['Data']['Typ'] == 2)

        with allure.step("step6:查看未脱敏的银行卡号并校验返回值"):
            # 查看未脱敏的身份证号码
            res = self.weblogin.create_api(DecryptAPI, Typ=3, DesenData=desenbankcardnum)
            result = res.json()
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
        with allure.step("预期结果:接口返回的数据正确"):
            pytest.assume(result['Data']['DesenData'] == desenbankcardnum)
            pytest.assume(result['Data']['OriData'] == bankcardnum)
            pytest.assume(result['Data']['Typ'] == 3)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('默认查询项查询')
    @allure.severity('blocker')
    def test_bankcardinfo_0008(self):
        """
                默认查询项查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0008.__name__))
        with allure.step("step1:默认查询项查询银行卡信息记录"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 获取全部的银行卡记录
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):
            # 获取待审核数量
            unanditcnt_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcnt_sql)
            unanditcnt = res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=2 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=3 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f'select count(*) from member_user_bank_card_audit where is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcnt)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f'SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0'
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                if bankcardlist[one]['BankCardNum']=='':
                    pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=3,
                                                   DesenData=bankcardlist[one]['BankCardNum'])
                    realbankcardnum = res.json()['Data']['OriData']
                    pytest.assume(realbankcardnum == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])

                if bankcardlist[one]['IdCardNum']=='':
                    pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                                   DesenData=bankcardlist[one]['IdCardNum'])
                    realidcardnum = res.json()['Data']['OriData']
                    pytest.assume(realidcardnum==idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]

                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=bankcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('身份证号码查询')
    @allure.severity('blocker')
    def test_bankcardinfo_0009(self):
        """
                身份证号码查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0009.__name__))
        with allure.step("step1:输入已存在的身份证号码，查询银行卡信息"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在银行卡审核记录的身份证号码
            idcardnum_sql=f'select id_card_num from member_user_unique where uuid in (select b.uuid from member_user_bank_card_audit as a left join member_user as b on a.guid=b.guid where b.uuid>0 and a.ec_id=1)'
            res=self.db.selectsql(idcardnum_sql)
            idcardnum = random.choice(res)[0]
            # 已存在银行卡审核记录的身份证号码查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           IdCardNum=idcardnum)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):
            #获取身份证号码对应的guid
            allguid_sql=f"select guid from member_user_unique as a left join member_user as b on a.uuid=b.uuid where a.id_card_num='{idcardnum}' and b.ec_id={ec_id}"
            res=self.db.selectsql(allguid_sql)
            allguid=''
            for one in res:
                allguid = allguid + str(one[0]) + ','
            allguid = allguid[:-1]

            # 获取待审核总数量
            unanditcntcont_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcntcont_sql)
            unanditcntcont = res[0][0]
            #获取查询结果中待审核数量
            unanditcnt_sql=f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 1) AND (ec_id = {ec_id})'
            res=self.db.selectsql(unanditcnt_sql)
            unanditcnt=res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 2) AND (ec_id = {ec_id})'
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 3) AND (ec_id = {ec_id})'
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (ec_id = {ec_id})'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcntcont)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f'SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and guid in ({allguid}) AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0'
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]
                pytest.assume(bankcardlist[one]['Mobile'] == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)

        with allure.step("step3:输入不存在的身份证号码，查询银行卡信息"):
            #随机生成不存在银行卡审核记录的身份证号码
            while True:
                # 生成身份证号码
                noneidcardnum = create_IDCard()
                # 校验身份证号码是否存在
                unique_sql = f"select id_card_num from member_user_unique where id_card_num={noneidcardnum}"
                res = self.db.selectsql(unique_sql)
                if res == ():
                    break

            # 不存在银行卡审核记录的身份证号码查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           IdCardNum=noneidcardnum)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('姓名查询')
    @allure.severity('blocker')
    def test_bankcardinfo_0010(self):
        """
                身份证号码查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0010.__name__))
        with allure.step("step1:输入已存在银行卡记录的姓名，查询银行卡信息"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在银行卡审核记录的姓名
            realname_sql=f'select real_name from member_user_unique where uuid in (select b.uuid from member_user_bank_card_audit as a left join member_user as b on a.guid=b.guid where b.uuid>0 and a.ec_id={ec_id})'
            res=self.db.selectsql(realname_sql)
            realname = random.choice(res)[0]
            # 已存在银行卡审核记录的姓名查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           RealName=realname)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):
            #获取身份证号码对应的guid
            allguid_sql=f"select guid from member_user_unique as a left join member_user as b on a.uuid=b.uuid where a.real_name='{realname}' and b.ec_id={ec_id}"
            res=self.db.selectsql(allguid_sql)
            allguid=''
            for one in res:
                allguid = allguid + str(one[0]) + ','
            allguid = allguid[:-1]

            # 获取待审核总数量
            unanditcntcont_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcntcont_sql)
            unanditcntcont = res[0][0]
            #获取查询结果中待审核数量
            unanditcnt_sql=f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 1) AND (ec_id = {ec_id})'
            res=self.db.selectsql(unanditcnt_sql)
            unanditcnt=res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 2) AND (ec_id = {ec_id})'
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 3) AND (ec_id = {ec_id})'
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (ec_id = {ec_id})'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcntcont)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f'SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and guid in ({allguid}) AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0'
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]
                pytest.assume(bankcardlist[one]['Mobile'] == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)

        with allure.step("step3:输入不已存在银行卡记录的姓名，查询银行卡信息"):
            #随机生成不存在银行卡审核记录的姓名
            while True:
                # 生成姓名
                nonerealname = create_name()
                # 校验姓名是否存在
                unique_sql = f"select id_card_num from member_user_unique where real_name='{nonerealname}'"
                res = self.db.selectsql(unique_sql)
                if res == ():
                    break

            # 不存在银行卡审核记录的姓名查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           RealName=nonerealname)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('手机号码查询')
    @allure.severity('blocker')
    def test_bankcardinfo_0011(self):
        """
                手机号码查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0011.__name__))
        with allure.step("step1:输入已存在银行卡记录的手机号码，查询银行卡信息"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在银行卡审核记录的手机号码
            mobile_sql=f'select b.mobile from member_user_bank_card_audit as a left join member_user as b on a.guid=b.guid where b.uuid>0 and a.ec_id={ec_id}'
            res=self.db.selectsql(mobile_sql)
            mobile = random.choice(res)[0]
            # 已存在银行卡审核记录的手机号码查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           Mobile=mobile)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):
            #获取手机号码对应的guid
            allguid_sql=f"select guid from member_user where mobile={mobile} and ec_id={ec_id}"
            res=self.db.selectsql(allguid_sql)
            allguid=res[0][0]

            # 获取待审核总数量
            unanditcntcont_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcntcont_sql)
            unanditcntcont = res[0][0]
            #获取查询结果中待审核数量
            unanditcnt_sql=f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 1) AND (ec_id = {ec_id})'
            res=self.db.selectsql(unanditcnt_sql)
            unanditcnt=res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 2) AND (ec_id = {ec_id})'
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 3) AND (ec_id = {ec_id})'
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (ec_id = {ec_id})'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcntcont)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f'SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and guid in ({allguid}) AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0'
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]
                pytest.assume(bankcardlist[one]['Mobile'] == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)

        with allure.step("step3:输入不已存在银行卡记录的手机号码，查询银行卡信息"):
            #随机生成不存在银行卡审核记录的手机号码
            while True:
                # 生成手机号码
                nonemobile = create_phone()
                # 校验手机号码是否存在
                unique_sql = f"select mobile from member_user where mobile='{nonemobile}' and ec_id={ec_id}"
                res = self.db.selectsql(unique_sql)
                if res == ():
                    break

            # 不存在银行卡审核记录的手机号码查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           Mobile=nonemobile)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('银行名称查询')
    @allure.severity('blocker')
    def test_bankcardinfo_0012(self):
        """
                银行名称查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0012.__name__))
        with allure.step("step1:输入已存在银行卡记录的银行名称，查询银行卡信息"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在银行卡审核记录的银行名称
            bankname_sql=f"select bank_name from member_user_bank_card_audit where is_deleted=0 and ec_id={ec_id} and bank_name<>''"
            res=self.db.selectsql(bankname_sql)
            bankname = random.choice(res)[0]
            # 已存在银行卡审核记录的银行名称查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           BankName=bankname)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):

            # 获取待审核总数量
            unanditcntcont_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcntcont_sql)
            unanditcntcont = res[0][0]
            #获取查询结果中待审核数量
            unanditcnt_sql=f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_name = '{bankname}') AND (audit_sts = 1) AND (ec_id = {ec_id})"
            res=self.db.selectsql(unanditcnt_sql)
            unanditcnt=res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_name = '{bankname}') AND (audit_sts = 2) AND (ec_id = {ec_id})"
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_name = '{bankname}') AND (audit_sts = 3) AND (ec_id = {ec_id})"
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_name = '{bankname}') AND (ec_id = {ec_id})"
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcntcont)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f"SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and (bank_name = '{bankname}') AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                if bankcardlist[one]['BankCardNum']=='':
                    pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=3,
                                                   DesenData=bankcardlist[one]['BankCardNum'])
                    realbankcardnum = res.json()['Data']['OriData']
                    pytest.assume(realbankcardnum == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                if bankcardlist[one]['IdCardNum']=='':
                    pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                                   DesenData=bankcardlist[one]['IdCardNum'])
                    realidcardnum = res.json()['Data']['OriData']
                    pytest.assume(realidcardnum==idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]

                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=bankcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)

        with allure.step("step3:输入不已存在银行卡记录的银行名称，查询银行卡信息"):
            #随机获取不存在银行卡记录的银行名称
            nonebankname_sql = f"SELECT bank_name FROM cfg_bank where bank_name not in(select bank_name from member_user_bank_card_audit where is_deleted=0 and ec_id={ec_id} and bank_name<>'')"
            res = self.db.selectsql(nonebankname_sql)
            nonebankname=random.choice(res)[0]

            # 不存在银行卡审核记录的银行名称查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           BankName=nonebankname)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('银行卡号查询')
    @allure.severity('blocker')
    def test_bankcardinfo_0013(self):
        """
                银行卡号查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0013.__name__))
        with allure.step("step1:输入已存在银行卡记录的银行卡号，查询银行卡信息"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在银行卡审核记录的银行卡号
            bankcardnum_sql=f'select bank_card_num from member_user_bank_card_audit where audit_sts=2 and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(bankcardnum_sql)
            bankcardnum = random.choice(res)[0]
            # 已存在银行卡审核记录的银行卡号查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           BankCardNum=bankcardnum)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):

            # 获取待审核总数量
            unanditcntcont_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcntcont_sql)
            unanditcntcont = res[0][0]
            # 获取查询结果中待审核数量
            unanditcnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_card_num = '{bankcardnum}') AND (audit_sts = 1) AND (ec_id = {ec_id})"
            res = self.db.selectsql(unanditcnt_sql)
            unanditcnt = res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_card_num = '{bankcardnum}') AND (audit_sts = 2) AND (ec_id = {ec_id})"
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_card_num = '{bankcardnum}') AND (audit_sts = 3) AND (ec_id = {ec_id})"
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (bank_card_num = '{bankcardnum}') AND (ec_id = {ec_id})"
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]

        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcntcont)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f"SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and (bank_card_num = '{bankcardnum}') AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]
                pytest.assume(bankcardlist[one]['Mobile'] == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)

        with allure.step("step3:输入不已存在银行卡记录的银行卡号，查询银行卡信息"):
            #随机生成不存在银行卡审核记录的银行卡号
            while True:
                # 生成银行卡号
                nonebankcardnum = create_bankcard()
                # 校验银行卡号是否存在
                unique_sql = f"select * from member_user_bank_card_audit where bank_card_num='{nonebankcardnum}' and ec_id={ec_id}"
                res = self.db.selectsql(unique_sql)
                if res == ():
                    break

            # 不存在银行卡审核记录的手机号码查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=-9999,
                                           BankCardNum=nonebankcardnum)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])



    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('审核状态查询')
    @pytest.mark.parametrize('AuditSts', [2, 3, 1])
    @allure.severity('blocker')
    def test_bankcardinfo_0014(self,AuditSts):
        """
                审核状态查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0014.__name__))
        with allure.step("step1:选择待审核、审核通过、审核不通过，查询银行卡信息"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 选择待审核、审核通过、审核不通过状态查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=AuditSts)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):

            # 获取待审核总数量
            unanditcntcont_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcntcont_sql)
            unanditcntcont = res[0][0]
            #获取查询结果中待审核数量
            unanditcnt_sql=f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (audit_sts = {AuditSts}) AND (audit_sts = 1) AND (ec_id = {ec_id})"
            res=self.db.selectsql(unanditcnt_sql)
            unanditcnt=res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (audit_sts = {AuditSts}) AND (audit_sts = 2) AND (ec_id = {ec_id})"
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (audit_sts = {AuditSts}) AND (audit_sts = 3) AND (ec_id = {ec_id})"
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (audit_sts = {AuditSts}) AND (ec_id = {ec_id})"
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcntcont)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f"SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and (audit_sts = {AuditSts}) AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                if bankcardlist[one]['BankCardNum']=='':
                    pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=3,
                                                   DesenData=bankcardlist[one]['BankCardNum'])
                    realbankcardnum = res.json()['Data']['OriData']
                    pytest.assume(realbankcardnum == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                if bankcardlist[one]['IdCardNum']=='':
                    pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])
                else:
                    res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                                   DesenData=bankcardlist[one]['IdCardNum'])
                    realidcardnum = res.json()['Data']['OriData']
                    pytest.assume(realidcardnum==idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]

                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=bankcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)



    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('上传日期查询')
    @allure.severity('blocker')
    @pytest.mark.parametrize('RegTimeBegin,RegTimeEnd',[(nowtime,None),
                                                        (None,nowtime),
                                                        (nowtime,nowtime)])
    def test_bankcardinfo_0015(self,RegTimeBegin,RegTimeEnd):
        """
                上传日期查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0015.__name__))
        with allure.step("step1:只选择开始时间、只选择结束时间、选择正确的时间区间，查询银行卡记录"):
            # 登录
            self.weblogin.login(pq_boss_user)

            # 只选择开始时间、只选择结束时间、选择正确的时间区间，查询银行卡记录
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           UploadTimeBegin=RegTimeBegin,
                                           UploadTimeEnd=RegTimeEnd)
            res_data = res.json()['Data']
        with allure.step("预期结果:接口调用成功,接口返回数据正确"):

            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')

            if RegTimeBegin==None:
                RegTimeEnd = RegTimeEnd + ' 23:59:59.000000'
            elif RegTimeEnd==None:
                RegTimeBegin = RegTimeBegin + ' 00:00:00.000000'
            else:
                RegTimeBegin=RegTimeBegin+' 00:00:00.000000'
                RegTimeEnd=RegTimeEnd+' 23:59:59.000000'
            # 获取总条数
            if RegTimeBegin==None:
                RecordCount_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (created_tm <= '{RegTimeEnd}') AND (ec_id = {ec_id})"
            elif RegTimeEnd==None:
                RecordCount_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (created_tm >= '{RegTimeBegin}') AND (ec_id = {ec_id})"
            else:
                RecordCount_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (created_tm >= '{RegTimeBegin}') AND (created_tm <= '{RegTimeEnd}') AND (ec_id = {ec_id})"

            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
            # 校验接口返回数据
            pytest.assume(res_data['RecordCount'] == RecordCount)

            # 获取数据库数据
            if RegTimeBegin==None:
                memberidcardaudit_sql=f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.created_tm<='{RegTimeEnd}' ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            elif RegTimeEnd==None:
                memberidcardaudit_sql=f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.created_tm>='{RegTimeBegin}' ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"
            else:
                memberidcardaudit_sql = f"SELECT a.audit_by,a.audit_remark,a.audit_sts,a.audit_tm,a.guid,a.id_card_num,a.idcard_front_url,a.real_name,a.created_tm,a.user_idcard_audit_id,b.mobile FROM member_user_idcard_audit AS a LEFT JOIN member_user AS b ON a.guid = b.guid WHERE( a.is_deleted = 0 ) AND ( a.ec_id = {ec_id} ) and a.created_tm>='{RegTimeBegin}' and a.created_tm<='{RegTimeEnd}' ORDER BY a.audit_sts ASC,a.created_tm DESC,a.audit_tm DESC LIMIT 10 OFFSET 0"

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            if RegTimeBegin==None:
                bankaudit_sql = f"SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and created_tm<='{RegTimeEnd}' AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            elif RegTimeEnd==None:
                bankaudit_sql = f"SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and created_tm>='{RegTimeBegin}' AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            else:
                bankaudit_sql = f"SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and created_tm>='{RegTimeBegin}' and created_tm<='{RegTimeEnd}' AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
                db_res = self.db.selectsql(bankaudit_sql)
                # 获取接口返回的RecordList列表
                bankcardlist = res_data['RecordList']
                for one in range(len(bankcardlist)):
                    pytest.assume(bankcardlist[one]['AliBucket'] == db_res[one][0])
                    pytest.assume(bankcardlist[one]['AreaName'] == '')
                    if db_res[one][1] != 0:
                        # 获取AuditBy
                        tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                        auditbyres = self.db.selectsql(tenant_user_sql)
                        auditby = auditbyres[0][0]
                    else:
                        auditby = ''
                    pytest.assume(bankcardlist[one]['AuditBy'] == auditby)
                    pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                    pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                    if db_res[one][4] == '0000-00-00 00:00:00':
                        audit_tm = '0000-00-00 00:00:00'
                    else:
                        audit_tm = db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                    pytest.assume(bankcardlist[one]['AuditTm'] == audit_tm)
                    if bankcardlist[one]['BankCardNum'] == '':
                        pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])
                    else:
                        res = self.weblogin.create_api(DecryptAPI, Typ=3,
                                                       DesenData=bankcardlist[one]['BankCardNum'])
                        realbankcardnum = res.json()['Data']['OriData']
                        pytest.assume(realbankcardnum == db_res[one][5])

                    pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                    pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                    pytest.assume(bankcardlist[one]['CityName'] == '')
                    # 获取银行卡记录的guid
                    guid = db_res[one][10]
                    # 获取guid对应的member_user_idcard_audit表数据
                    idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                    idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                    pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                    if bankcardlist[one]['IdCardNum'] == '':
                        pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])
                    else:
                        res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                                       DesenData=bankcardlist[one]['IdCardNum'])
                        realidcardnum = res.json()['Data']['OriData']
                        pytest.assume(realidcardnum == idcardauditinfo[0][1])

                    if idcardauditinfo[0][0] == 1:
                        IdcardFrontUrl = idcardauditinfo[0][2]
                        UserIdcardAuditId = idcardauditinfo[0][4]
                    else:
                        IdcardFrontUrl = ''
                        UserIdcardAuditId = 0

                    pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                    # 获取mobile
                    mobile_sql = f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                    res = self.db.selectsql(mobile_sql)
                    mobile = res[0][0]

                    res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=bankcardlist[one]['Mobile'])
                    realmobile = res.json()['Data']['OriData']
                    pytest.assume(realmobile == mobile)

                    pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                    if bankcardlist[one]['RealName'] == '':
                        realname = ''
                    else:
                        realname_sql = f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                        res = self.db.selectsql(realname_sql)
                        realname = res[0][0]

                    pytest.assume(bankcardlist[one]['RealName'] == realname)
                    pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                    pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                    pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)



    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('组合查询')
    @allure.severity('blocker')
    def test_bankcardinfo_0016(self):
        """
                填写身份证号码、姓名、手机号码、银行名称、银行卡号、审核状态、上传日期查询

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0016.__name__))
        with allure.step("step1:填写身份证号码、姓名、手机号码、银行名称、银行卡号、审核状态、上传日期查询"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 随机获取已存在银行卡审核记录的身份证号码、姓名、手机号码、银行名称、银行卡号、审核状态、上传日期
            bankaudit_sql=f'select bank_name,bank_card_num,audit_sts,created_tm,guid from member_user_bank_card_audit where audit_sts=2 and is_deleted=0 and ec_id=1'
            res=self.db.selectsql(bankaudit_sql)
            res1 = random.choice(res)
            #获取银行名称
            bankname=res1[0]
            # 获取银行卡号
            bankcardnum=res1[1]
            # 获取审核状态
            auditsts=res1[2]
            # 获取上传时间
            uploadtime=res1[3].__format__('%Y-%m-%d')
            # 构造UploadTimeBegin和UploadTimend
            UploadTimeBegin = uploadtime + ' 00:00:00.000000'
            UploadTimend = uploadtime + ' 23:59:59.000000'
            # 获取guid
            guid=res1[4]
            user_sql=f'select a.mobile,b.real_name,b.id_card_num from member_user as a left join member_user_unique as b on a.uuid=b.uuid where a.guid={guid} and a.ec_id={ec_id}'
            res = self.db.selectsql(user_sql)
            mobile=res[0][0]
            realname=res[0][1]
            idcardnum=res[0][2]

            # 填写身份证号码、姓名、手机号码、银行名称、银行卡号、审核状态、上传日期查询
            res = self.weblogin.create_api(BankCardInfoList_Api,
                                           SequenceUploadTime=1,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           AuditSts=auditsts,
                                           BankCardNum=bankcardnum,
                                           BankName=bankname,
                                           IdCardNum=idcardnum,
                                           Mobile=mobile,
                                           RealName=realname,
                                           UploadTimeBegin=UploadTimeBegin,
                                           UploadTimeEnd=UploadTimend)
            res_data=res.json()['Data']

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
        with allure.step("step2:获取待审核、审核通过、审核不通过数量"):
            #获取手机号码对应的guid
            allguid_sql=f"select guid from member_user where mobile={mobile} and ec_id={ec_id}"
            res=self.db.selectsql(allguid_sql)
            allguid=res[0][0]

            # 获取待审核总数量
            unanditcntcont_sql = f'select count(*) from member_user_bank_card_audit where audit_sts=1 and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(unanditcntcont_sql)
            unanditcntcont = res[0][0]
            #获取查询结果中待审核数量
            unanditcnt_sql=f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND(audit_sts = 1) AND (bank_name = '{bankname}') AND (bank_card_num = '{bankcardnum}') AND (created_tm >= '{UploadTimeBegin}') AND (created_tm <= '{UploadTimend}') AND (ec_id = {ec_id})"
            res=self.db.selectsql(unanditcnt_sql)
            unanditcnt=res[0][0]
            # 获取审核通过数量
            PassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 2) AND (bank_name = '{bankname}') AND (bank_card_num = '{bankcardnum}') AND (created_tm >= '{UploadTimeBegin}') AND (created_tm <= '{UploadTimend}') AND (ec_id = {ec_id})"
            res = self.db.selectsql(PassCnt_sql)
            PassCnt = res[0][0]
            # 获取审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (audit_sts = 3) AND (bank_name = '{bankname}') AND (bank_card_num = '{bankcardnum}') AND (created_tm >= '{UploadTimeBegin}') AND (created_tm <= '{UploadTimend}') AND (ec_id = {ec_id})"
            res = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = res[0][0]
            # 获取记录总数量
            RecordCount_sql = f'SELECT count(*) FROM `member_user_bank_card_audit`  WHERE (is_deleted = 0) AND (guid in ({allguid})) AND (ec_id = {ec_id})'
            res = self.db.selectsql(RecordCount_sql)
            RecordCount = res[0][0]
        with allure.step("预期结果:待审核、审核通过、审核不通过数量与接口返回的一致"):
            # 校验接口返回的待审核通过数量、审核通过数量、审核不通过数量、总记录数量
            pytest.assume(res_data['PassCnt'] == PassCnt)
            pytest.assume(res_data['UnAuditCnt'] == unanditcnt)
            pytest.assume(res_data['UnPassCnt'] == UnPassCnt)
            pytest.assume(res_data['UnAuditRecordCount'] == unanditcntcont)
            pytest.assume(res_data['RecordCount'] == RecordCount)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            bankaudit_sql=f"SELECT ali_bucket,audit_by,audit_remark,audit_sts,audit_tm,bank_card_num,bank_card_url,bank_name,created_tm,user_bank_card_audit_id,guid FROM member_user_bank_card_audit  WHERE (is_deleted = 0) and guid in ({allguid}) AND (audit_sts = {auditsts}) AND (bank_name = '{bankname}') AND (bank_card_num = '{bankcardnum}') AND (created_tm >= '{UploadTimeBegin}') AND (created_tm <= '{UploadTimend}') AND (ec_id = {ec_id}) ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(bankaudit_sql)
            #获取接口返回的RecordList列表
            bankcardlist=res_data['RecordList']
            for one in range(len(bankcardlist)):
                pytest.assume(bankcardlist[one]['AliBucket']==db_res[one][0])
                pytest.assume(bankcardlist[one]['AreaName']=='')
                if db_res[one][1] !=0:
                    # 获取AuditBy
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][1]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                else:
                    auditby=''
                pytest.assume(bankcardlist[one]['AuditBy']==auditby)
                pytest.assume(bankcardlist[one]['AuditRemark'] == db_res[one][2])
                pytest.assume(bankcardlist[one]['AuditSts'] == db_res[one][3])
                if db_res[one][4]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][4].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(bankcardlist[one]['AuditTm'] ==audit_tm)
                pytest.assume(bankcardlist[one]['BankCardNum'] == db_res[one][5])

                pytest.assume(bankcardlist[one]['BankCardUrl'] == db_res[one][6])
                pytest.assume(bankcardlist[one]['BankName'] == db_res[one][7])
                pytest.assume(bankcardlist[one]['CityName'] == '')
                #获取银行卡记录的guid
                guid=db_res[one][10]
                # 获取guid对应的member_user_idcard_audit表数据
                idcardaudit_sql = f'select audit_sts,id_card_num,idcard_front_url,real_name,user_idcard_audit_id from member_user_idcard_audit where guid={guid} and is_deleted=0 and ec_id={ec_id} order by updated_tm desc limit 1'
                idcardauditinfo = self.db.selectsql(idcardaudit_sql)
                pytest.assume(bankcardlist[one]['IdCardAuditSts'] == idcardauditinfo[0][0])
                pytest.assume(bankcardlist[one]['IdCardNum'] == idcardauditinfo[0][1])

                if idcardauditinfo[0][0]==1:
                    IdcardFrontUrl = idcardauditinfo[0][2]
                    UserIdcardAuditId = idcardauditinfo[0][4]
                else:
                    IdcardFrontUrl = ''
                    UserIdcardAuditId = 0

                pytest.assume(bankcardlist[one]['IdcardFrontUrl'] == IdcardFrontUrl)
                #获取mobile
                mobile_sql=f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
                res=self.db.selectsql(mobile_sql)
                mobile=res[0][0]
                pytest.assume(bankcardlist[one]['Mobile'] == mobile)

                pytest.assume(bankcardlist[one]['ProvinceName'] == '')
                if bankcardlist[one]['RealName']=='':
                    realname=''
                else:
                    realname_sql=f'select real_name from member_user_unique where uuid in(select uuid from member_user where guid={guid})'
                    res=self.db.selectsql(realname_sql)
                    realname=res[0][0]

                pytest.assume(bankcardlist[one]['RealName'] == realname)
                pytest.assume(bankcardlist[one]['UploadTime'] == db_res[one][8].__format__('%Y-%m-%d %H:%M:%S.%f'))
                pytest.assume(bankcardlist[one]['UserBankCardAuditId'] == db_res[one][9])
                pytest.assume(bankcardlist[one]['UserIdcardAuditId'] == UserIdcardAuditId)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('刷新待审核状态的银行卡')
    @allure.severity('blocker')
    def test_bankcardinfo_0017(self):
        """
                刷新待审核状态的银行卡

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0017.__name__))
        with allure.step("step1:前置条件准备：小程序上传身份证和银行卡,审核通过身份证"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #审核通过身份证
            idcardnum=create_IDCard()
            realname=create_name()
            upthreecard.weblogin.create_api(AuditIDCard_Api,
                                            IdCardNum=idcardnum,
                                            RealName=realname,
                                            UserIdcardAuditId=idcardaudit_id)
            # 上传银行卡
            bankcardaudit_id = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step2:刷新银行卡审核记录"):
            res=upthreecard.weblogin.create_api(ZXX_CmsBankCardQuery_Api,UserBankCardAuditId=bankcardaudit_id)
            result=res.json()

        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(result['Code']==0)
            pytest.assume(result['Desc'] == '')

        with allure.step("预期结果:校验银行审核记录审核状态仍为待审核状态"):
            bankcardaudit_sql=f'select audit_sts from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id} and ec_id={ec_id}'
            res=self.db.selectsql(bankcardaudit_sql)
            audit_sts=res[0][0]
            pytest.assume(audit_sts==1)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('待审核状态银行卡手动审核成功')
    @allure.severity('blocker')
    def test_bankcardinfo_0018(self):
        """
                待审核状态银行卡手动审核成功

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0018.__name__))
        with allure.step("step1:前置条件准备：小程序上传身份证和银行卡,审核通过身份证"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            idcardnum = create_IDCard()
            realname = create_name()
            upthreecard.weblogin.create_api(AuditIDCard_Api,
                                            IdCardNum=idcardnum,
                                            RealName=realname,
                                            UserIdcardAuditId=idcardaudit_id)
            # 上传银行卡
            bankcardaudit_id = upthreecard.upload_bankcard(fakerbankcardpicture)
        with allure.step("预期结果:会员上传的银行卡member_user_bank_card_audit表audit_sts为1，member_user_bank_card表无数据"):
            bankcardaudit_sql=f'select audit_sts,bank_name,bank_card_num from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res=self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==1)
            pytest.assume(res[0][1] == '')
            pytest.assume(res[0][2] == '')
            bankcard_sql=f'select * from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res = self.db.selectsql(bankcard_sql)
            pytest.assume(res == ())

        with allure.step("step2:手动审核银行卡"):
            #随机获取银行卡名称
            res=upthreecard.weblogin.create_api(GetBankList_Api)
            bankname=random.choice(res.json()['Data']['RecordList'])['BankName']
            #生成银行卡号
            bankcardnum=create_bankcard()
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                BankCardNum=bankcardnum,
                                                BankName=bankname,
                                                UserBankCardAuditId=bankcardaudit_id)
            res_data=res.json()

        with allure.step("预期结果:审核银行卡成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')

        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card表数据更新正确"):
            #校验member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==2)
            pytest.assume(res[0][1] == bankname)
            pytest.assume(res[0][2] == bankcardnum)
            auditby_sql=f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1=self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验member_user_bank_card表数据
            bankcard_sql=f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0'
            res=self.db.selectsql(bankcard_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==bankcardaudit_id)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)
            #获取uuid
            uuid_sql=f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            uuidres=self.db.selectsql(uuid_sql)
            uuid=uuidres[0][0]
            pytest.assume(res[0][2] == uuid)
            pytest.assume(res[0][3] == bankname)
            pytest.assume(res[0][4] == bankname)
            pytest.assume(res[0][5] == bankcardnum)
            pytest.assume(res[0][6] == 1)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('待审核状态银行卡手动审核不通过')
    @allure.severity('blocker')
    def test_bankcardinfo_0019(self):
        """
                待审核状态银行卡手动审核不通过

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0019.__name__))
        with allure.step("step1:前置条件准备：小程序上传身份证和银行卡,审核通过身份证"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            idcardnum = create_IDCard()
            realname = create_name()
            upthreecard.weblogin.create_api(AuditIDCard_Api,
                                            IdCardNum=idcardnum,
                                            RealName=realname,
                                            UserIdcardAuditId=idcardaudit_id)
            # 上传银行卡
            bankcardaudit_id = upthreecard.upload_bankcard(fakerbankcardpicture)
        with allure.step("预期结果:会员上传的银行卡member_user_bank_card_audit表audit_sts为1，member_user_bank_card表无数据"):
            bankcardaudit_sql=f'select audit_sts,bank_name,bank_card_num from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res=self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==1)
            pytest.assume(res[0][1] == '')
            pytest.assume(res[0][2] == '')
            bankcard_sql=f'select * from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            res = self.db.selectsql(bankcard_sql)
            pytest.assume(res == ())

        with allure.step("step2:手动审核不通过银行卡"):
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(ZXX_GetNextBankCardPic_Api,
                                                UserBankCardAuditId=bankcardaudit_id)
            res_data=res.json()

        with allure.step("预期结果:审核不通过银行卡成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')

        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card表数据更新正确"):
            #校验member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==3)
            pytest.assume(res[0][1] == '')
            pytest.assume(res[0][2] == '')
            auditby_sql=f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1=self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验member_user_bank_card表数据
            bankcard_sql=f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0'
            res=self.db.selectsql(bankcard_sql)
            pytest.assume(res==())


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('会员已有审核通过银行卡再次上传新的银行卡审核通过')
    @allure.severity('blocker')
    def test_bankcardinfo_0020(self):
        """
                会员已有审核通过银行卡再次上传新的银行卡审核通过

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0020.__name__))
        with allure.step("step1:前置条件准备：小程序上传身份证和银行卡,审核通过身份证"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            idcardnum = create_IDCard()
            realname = create_name()
            upthreecard.weblogin.create_api(AuditIDCard_Api,
                                            IdCardNum=idcardnum,
                                            RealName=realname,
                                            UserIdcardAuditId=idcardaudit_id)
            # 上传银行卡
            bankcardaudit_id = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step2:手动审核第一张银行卡"):
            #随机获取银行卡名称
            res=upthreecard.weblogin.create_api(GetBankList_Api)
            bankname=random.choice(res.json()['Data']['RecordList'])['BankName']
            #生成银行卡号
            bankcardnum=create_bankcard()
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                BankCardNum=bankcardnum,
                                                BankName=bankname,
                                                UserBankCardAuditId=bankcardaudit_id)
            res_data=res.json()

        with allure.step("预期结果:审核银行卡成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')

        with allure.step("step3:再次上传银行卡"):
            bankcardaudit_id2 = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step4:手动审核第二张银行卡"):
            #随机获取银行卡名称
            res=upthreecard.weblogin.create_api(GetBankList_Api)
            bankname2=random.choice(res.json()['Data']['RecordList'])['BankName']
            #生成银行卡号
            bankcardnum2=create_bankcard()
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                BankCardNum=bankcardnum2,
                                                BankName=bankname2,
                                                UserBankCardAuditId=bankcardaudit_id2)
            res_data2=res.json()

        with allure.step("预期结果:审核银行卡成功，接口返回数据正确"):
            pytest.assume(res_data2['Code']==0)
            pytest.assume(res_data2['Data'] == None)
            pytest.assume(res_data2['Desc'] == '成功')

        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card表数据更新正确"):
            #校验第一次上传的银行卡的member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==2)
            pytest.assume(res[0][1] == bankname)
            pytest.assume(res[0][2] == bankcardnum)
            auditby_sql=f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1=self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验第二次上传的银行卡的member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id2}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0] == 2)
            pytest.assume(res[0][1] == bankname2)
            pytest.assume(res[0][2] == bankcardnum2)
            auditby_sql = f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1 = self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验member_user_bank_card表数据
            # 获取uuid
            uuid_sql = f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            uuidres = self.db.selectsql(uuid_sql)
            uuid = uuidres[0][0]
            bankcard_sql=f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0 order by updated_tm desc'
            res=self.db.selectsql(bankcard_sql)
            pytest.assume(len(res)==2)
            #校验第二次审核成功的银行卡member_user_bank_card表数据
            pytest.assume(res[0][0]==bankcardaudit_id2)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)
            pytest.assume(res[0][2] == uuid)
            pytest.assume(res[0][3] == bankname2)
            pytest.assume(res[0][4] == bankname2)
            pytest.assume(res[0][5] == bankcardnum2)
            pytest.assume(res[0][6] == 1)
            # 校验第一次审核成功的银行卡member_user_bank_card表数据
            pytest.assume(res[1][0] == bankcardaudit_id)
            pytest.assume(res[1][1] == upthreecard.minilogin.Guid)
            pytest.assume(res[1][2] == uuid)
            pytest.assume(res[1][3] == bankname)
            pytest.assume(res[1][4] == bankname)
            pytest.assume(res[1][5] == bankcardnum)
            pytest.assume(res[1][6] == 1)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('会员在其他ec下存在审核通过的银行卡，审核通过会员的银行卡')
    @allure.severity('blocker')
    def test_bankcardinfo_0021(self):
        """
                会员在其他ec下存在审核通过的银行卡，审核通过会员的银行卡

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0021.__name__))
        with allure.step("step1:前置条件准备：小程序上传身份证和银行卡,审核通过身份证"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            idcardnum = create_IDCard()
            realname = create_name()
            upthreecard.weblogin.create_api(AuditIDCard_Api,
                                            IdCardNum=idcardnum,
                                            RealName=realname,
                                            UserIdcardAuditId=idcardaudit_id)
            # 上传银行卡
            bankcardaudit_id = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step2:手动审核银行卡，并更新member_user_bank_card_audit、member_user_bank_card表的ec_id"):
            #随机获取银行卡名称
            res=upthreecard.weblogin.create_api(GetBankList_Api)
            bankname=random.choice(res.json()['Data']['RecordList'])['BankName']
            #生成银行卡号
            bankcardnum=create_bankcard()
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                BankCardNum=bankcardnum,
                                                BankName=bankname,
                                                UserBankCardAuditId=bankcardaudit_id)
            res_data=res.json()
            #校验接口返回的结果
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')
            #更新member_user_bank_card_audit表ec_id
            update_bankaudit_sql=f'update member_user_bank_card_audit set ec_id=2 where user_bank_card_audit_id={bankcardaudit_id}'
            self.db.updatesql(update_bankaudit_sql)
            # 更新member_user_bank_card表的ec_id
            update_bankcard_sql=f'update member_user_bank_card set ec_id=2 where user_bank_card_audit_id={bankcardaudit_id}'
            self.db.updatesql(update_bankcard_sql)

        with allure.step("step3:再次上传银行卡，并填写相同银行卡号和银行名称审核通过银行卡"):
            # 上传银行卡
            bankcardaudit_id2 = upthreecard.upload_bankcard(fakerbankcardpicture)
            #填写相同的银行名称和银行卡号审核通过银行卡号
            # 调用审核银行卡接口
            res = upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                  BankCardNum=bankcardnum,
                                                  BankName=bankname,
                                                  UserBankCardAuditId=bankcardaudit_id2)
            res_data = res.json()
            # 校验接口返回的结果
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')


        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card表数据更新正确"):
            #校验其他ec_id下的该会员的银行卡的member_user_bank_card_audit表数据
            otherec_bankcardaudit_sql = f'select * from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id} and ec_id=2'
            res = self.db.selectsql(otherec_bankcardaudit_sql)
            pytest.assume(len(res)==1)
            #校验第二次审核的银行卡的member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id2}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==2)
            pytest.assume(res[0][1] == bankname)
            pytest.assume(res[0][2] == bankcardnum)
            auditby_sql=f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1=self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验其他ec_id下的该会员的银行卡的member_user_bank_card表数据
            otherbankcard_sql = f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id=2 and is_deleted=0'
            res = self.db.selectsql(otherbankcard_sql)
            pytest.assume(len(res) == 1)
            # 校验第二次member_user_bank_card表数据
            bankcard_sql=f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0'
            res=self.db.selectsql(bankcard_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==bankcardaudit_id2)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)
            #获取uuid
            uuid_sql=f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            uuidres=self.db.selectsql(uuid_sql)
            uuid=uuidres[0][0]
            pytest.assume(res[0][2] == uuid)
            pytest.assume(res[0][3] == bankname)
            pytest.assume(res[0][4] == bankname)
            pytest.assume(res[0][5] == bankcardnum)
            pytest.assume(res[0][6] == 1)


    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('会员已有审核通过的银行卡再次审核通过相同银行卡号的银行卡')
    @allure.severity('blocker')
    def test_bankcardinfo_0022(self):
        """
                会员已有审核通过的银行卡再次审核通过相同银行卡号的银行卡

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0020.__name__))
        with allure.step("step1:前置条件准备：小程序上传身份证和银行卡,审核通过身份证"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            idcardnum = create_IDCard()
            realname = create_name()
            upthreecard.weblogin.create_api(AuditIDCard_Api,
                                            IdCardNum=idcardnum,
                                            RealName=realname,
                                            UserIdcardAuditId=idcardaudit_id)
            # 上传银行卡
            bankcardaudit_id = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step2:手动审核第一张银行卡"):
            #随机获取银行卡名称
            res=upthreecard.weblogin.create_api(GetBankList_Api)
            bankname=random.choice(res.json()['Data']['RecordList'])['BankName']
            #生成银行卡号
            bankcardnum=create_bankcard()
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                BankCardNum=bankcardnum,
                                                BankName=bankname,
                                                UserBankCardAuditId=bankcardaudit_id)
            res_data=res.json()

        with allure.step("预期结果:审核银行卡成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')


        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card表数据更新正确"):
            #校验第一次上传的银行卡的member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==2)
            pytest.assume(res[0][1] == bankname)
            pytest.assume(res[0][2] == bankcardnum)
            auditby_sql=f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1=self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验member_user_bank_card表数据
            bankcard_sql=f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0'
            res=self.db.selectsql(bankcard_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==bankcardaudit_id)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)
            #获取uuid
            uuid_sql=f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            uuidres=self.db.selectsql(uuid_sql)
            uuid=uuidres[0][0]
            pytest.assume(res[0][2] == uuid)
            pytest.assume(res[0][3] == bankname)
            pytest.assume(res[0][4] == bankname)
            pytest.assume(res[0][5] == bankcardnum)
            pytest.assume(res[0][6] == 1)

        with allure.step("step3:再次上传银行卡"):
            bankcardaudit_id2 = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step4:填写相同的银行卡号，手动审核第二张银行卡"):
            #随机获取银行卡名称
            res=upthreecard.weblogin.create_api(GetBankList_Api)
            bankname2=random.choice(res.json()['Data']['RecordList'])['BankName']
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                BankCardNum=bankcardnum,
                                                BankName=bankname2,
                                                UserBankCardAuditId=bankcardaudit_id2)
            res_data2=res.json()

        with allure.step("预期结果:审核银行卡成功，接口返回数据正确"):
            pytest.assume(res_data2['Code']==0)
            pytest.assume(res_data2['Data'] == None)
            pytest.assume(res_data2['Desc'] == '成功')

        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card表数据更新正确"):
            # 校验第二次上传的银行卡的member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id2}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0] == 2)
            pytest.assume(res[0][1] == bankname2)
            pytest.assume(res[0][2] == bankcardnum)
            auditby_sql = f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1 = self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验member_user_bank_card表数据
            # 获取uuid
            uuid_sql = f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            uuidres = self.db.selectsql(uuid_sql)
            uuid = uuidres[0][0]
            bankcard_sql=f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0 order by updated_tm desc'
            res=self.db.selectsql(bankcard_sql)
            pytest.assume(len(res)==1)
            #校验第二次审核成功的银行卡member_user_bank_card表数据
            pytest.assume(res[0][0]==bankcardaudit_id2)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)
            pytest.assume(res[0][2] == uuid)
            pytest.assume(res[0][3] == bankname2)
            pytest.assume(res[0][4] == bankname2)
            pytest.assume(res[0][5] == bankcardnum)
            pytest.assume(res[0][6] == 1)



    @allure.feature('会员信息管理')
    @allure.story('银行卡信息查询')
    @allure.title('修改审核通过会员银行卡号')
    @allure.severity('blocker')
    def test_bankcardinfo_0023(self):
        """
                修改审核通过会员银行卡号

        """
        print('\n{}测试开始\n'.format(self.test_bankcardinfo_0020.__name__))
        with allure.step("step1:前置条件准备：小程序上传身份证和银行卡,审核通过身份证"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 审核通过身份证
            idcardnum = create_IDCard()
            realname = create_name()
            upthreecard.weblogin.create_api(AuditIDCard_Api,
                                            IdCardNum=idcardnum,
                                            RealName=realname,
                                            UserIdcardAuditId=idcardaudit_id)
            # 上传银行卡
            bankcardaudit_id = upthreecard.upload_bankcard(fakerbankcardpicture)

        with allure.step("step2:手动审核通过银行卡"):
            #随机获取银行卡名称
            res=upthreecard.weblogin.create_api(GetBankList_Api)
            bankname=random.choice(res.json()['Data']['RecordList'])['BankName']
            #生成银行卡号
            bankcardnum=create_bankcard()
            #调用审核银行卡接口
            res=upthreecard.weblogin.create_api(AuditBankCard_Api,
                                                BankCardNum=bankcardnum,
                                                BankName=bankname,
                                                UserBankCardAuditId=bankcardaudit_id)
            res_data=res.json()

        with allure.step("预期结果:审核银行卡成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')


        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card表数据更新正确"):
            #校验上传的银行卡的member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select audit_sts,bank_name,bank_card_num,audit_by,audit_name from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0]==2)
            pytest.assume(res[0][1] == bankname)
            pytest.assume(res[0][2] == bankcardnum)
            auditby_sql=f'select guid,user_name from tenant_user where mobile={pq_boss_user} and t_id={pq_tenant_id}'
            res1=self.db.selectsql(auditby_sql)
            pytest.assume(res[0][3] == res1[0][0])
            pytest.assume(res[0][4] == res1[0][1])
            # 校验member_user_bank_card表数据
            bankcard_sql=f'select user_bank_card_audit_id,guid,uuid,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0'
            res=self.db.selectsql(bankcard_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==bankcardaudit_id)
            pytest.assume(res[0][1] == upthreecard.minilogin.Guid)
            #获取uuid
            uuid_sql=f'select uuid from member_user where guid={upthreecard.minilogin.Guid} and ec_id={ec_id}'
            uuidres=self.db.selectsql(uuid_sql)
            uuid=uuidres[0][0]
            pytest.assume(res[0][2] == uuid)
            pytest.assume(res[0][3] == bankname)
            pytest.assume(res[0][4] == bankname)
            pytest.assume(res[0][5] == bankcardnum)
            pytest.assume(res[0][6] == 1)

        with allure.step("step3:修改审核通过的银行卡的银行卡号和银行名称"):
            # 随机获取银行卡名称
            res = upthreecard.weblogin.create_api(GetBankList_Api)
            bankname2 = random.choice(res.json()['Data']['RecordList'])['BankName']
            # 生成银行卡号
            bankcardnum2 = create_bankcard()
            #调用修改银行卡号接口
            res = upthreecard.weblogin.create_api(ZXX_ModifyBankCardParam_Api,
                                                  BankCardNum=bankcardnum2,
                                                  BankName=bankname2,
                                                  UserBankCardAuditId=bankcardaudit_id)


        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Data'] == None)
            pytest.assume(res_data['Desc'] == '成功')

        with allure.step("预期结果:member_user_bank_card_audit、member_user_bank_card数据更新正确"):
            # 校验member_user_bank_card_audit表数据
            bankcardaudit_sql = f'select bank_name,accnt_bank,bank_card_num from member_user_bank_card_audit where user_bank_card_audit_id={bankcardaudit_id}'
            res = self.db.selectsql(bankcardaudit_sql)
            pytest.assume(res[0][0] == bankname2)
            pytest.assume(res[0][1] == bankname2)
            pytest.assume(res[0][2] == bankcardnum2)
            # 校验member_user_bank_card表数据
            bankcard_sql = f'select user_bank_card_audit_id,bank_name,accnt_bank,bank_card_num,user_delete from member_user_bank_card where guid={upthreecard.minilogin.Guid} and ec_id={ec_id} and is_deleted=0'
            res = self.db.selectsql(bankcard_sql)
            pytest.assume(len(res) == 1)
            pytest.assume(res[0][0] == bankcardaudit_id)
            pytest.assume(res[0][1] == bankname2)
            pytest.assume(res[0][2] == bankname2)
            pytest.assume(res[0][3] == bankcardnum2)
            pytest.assume(res[0][4] == 1)









