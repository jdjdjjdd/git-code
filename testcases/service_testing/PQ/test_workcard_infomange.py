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

class Testworkcardinfo:

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
    @allure.story('工牌信息查询')
    @allure.title('身份证未审核状态工牌信息记录检查')
    @allure.severity('blocker')
    def test_workcardinfo_0001(self):
        """
                身份证未审核状态工牌信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0001.__name__))
        with allure.step("step1:前置条件准备,会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)


        with allure.step("step2:工牌信息列表查询上传的工牌"):
            res=upthreecard.weblogin.create_api(WorkCardInfoList_Api,
                                            SequenceUploadTime=2,
                                            RecordIndex=0,
                                            RecordSize=10,
                                            EntId=-9999,
                                            AuditSts=-9999,
                                            Mobile=upthreecard.mobile)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功，查询结果为空"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            pytest.assume(res_data['Data']['PassCnt'] == 0)
            pytest.assume(res_data['Data']['RecordCount'] == 0)
            pytest.assume(res_data['Data']['RecordList'] == [])
            pytest.assume(res_data['Data']['UnAuditCnt'] == 0)
            #获取待审核总数量
            UnAuditRecordcount_sql=f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res=self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount=res[0][0]

            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            pytest.assume(res_data['Data']['UnPassCnt'] == 0)

        with allure.step("预期结果:member_user_work_card_audit表落表数据正确"):
            workaudit_sql=f'select guid,uuid,work_card_no,ent_id,audit_sts,audit_by,audit_remark,is_canceled from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(workaudit_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==upthreecard.minilogin.Guid)
            pytest.assume(res[0][1] == 0)
            pytest.assume(res[0][2] == '')
            pytest.assume(res[0][3] == upthreecard.appletfunc.entid)
            pytest.assume(res[0][4] == 1)
            pytest.assume(res[0][5] == 0)
            pytest.assume(res[0][6] == '')
            pytest.assume(res[0][7] == 0)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('身份证审核不通过状态工牌信息记录检查')
    @allure.severity('blocker')
    def test_workcardinfo_0002(self):
        """
                身份证审核不通过状态工牌信息记录检查

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0002.__name__))
        with allure.step("step1:前置条件准备,会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:审核不通过身份证"):
            upthreecard.idcard_auditnopass(idcardaudit_id)

        with allure.step("step3:工牌信息列表查询上传的工牌"):
            res=upthreecard.weblogin.create_api(WorkCardInfoList_Api,
                                            SequenceUploadTime=2,
                                            RecordIndex=0,
                                            RecordSize=10,
                                            EntId=-9999,
                                            AuditSts=-9999,
                                            Mobile=upthreecard.mobile)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功，查询结果为空"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            pytest.assume(res_data['Data']['PassCnt'] == 0)
            pytest.assume(res_data['Data']['RecordCount'] == 0)
            pytest.assume(res_data['Data']['RecordList'] == [])
            pytest.assume(res_data['Data']['UnAuditCnt'] == 0)
            #获取待审核总数量
            UnAuditRecordcount_sql=f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res=self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount=res[0][0]

            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            pytest.assume(res_data['Data']['UnPassCnt'] == 0)

        with allure.step("预期结果:member_user_work_card_audit表落表数据正确"):
            workaudit_sql=f'select guid,uuid,work_card_no,ent_id,audit_sts,audit_by,audit_remark,is_canceled from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res=self.db.selectsql(workaudit_sql)
            pytest.assume(len(res)==1)
            pytest.assume(res[0][0]==upthreecard.minilogin.Guid)
            pytest.assume(res[0][1] == 0)
            pytest.assume(res[0][2] == '')
            pytest.assume(res[0][3] == upthreecard.appletfunc.entid)
            pytest.assume(res[0][4] == 1)
            pytest.assume(res[0][5] == 0)
            pytest.assume(res[0][6] == '')
            pytest.assume(res[0][7] == 0)



    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('身份证审核通过状态，未审核状态的工牌信息检查')
    @allure.severity('blocker')
    def test_workcardinfo_0003(self):
        """
                身份证审核通过状态，未审核状态的工牌信息检查

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0003.__name__))
        with allure.step("step1:前置条件准备,会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:审核通过身份证"):
            upthreecard.idcard_auditpass(idcardaudit_id)

        with allure.step("step3:工牌信息列表查询上传的工牌"):
            res=upthreecard.weblogin.create_api(WorkCardInfoList_Api,
                                            SequenceUploadTime=2,
                                            RecordIndex=0,
                                            RecordSize=10,
                                            EntId=-9999,
                                            AuditSts=-9999,
                                            Mobile=upthreecard.mobile)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            pytest.assume(res_data['Data']['PassCnt'] == 0)
            pytest.assume(res_data['Data']['RecordCount'] == 1)
            pytest.assume(res_data['Data']['UnAuditCnt'] == 1)
            #获取待审核总数量
            UnAuditRecordcount_sql=f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res=self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount=res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            pytest.assume(res_data['Data']['UnPassCnt'] == 0)
            #校验RecordList数据
            workaudit_sql = f'select audit_by,audit_remark,audit_sts,audit_tm,ent_id,uuid,guid,created_tm,user_work_card_audit_id,work_card_no,work_card_url from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(workaudit_sql)
            ent_id=res[0][4]
            #获取EntFullName和entshortname
            entname_sql=f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            entname_res=self.db.selectsql(entname_sql)
            ent_fulll_name=entname_res[0][0]
            ent_short_name = entname_res[0][1]
            #获取idcardnum和real_name
            uuid=res[0][5]
            idcardnum_sql=f'select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0'
            idcardnumres=self.db.selectsql(idcardnum_sql)
            idcardnum=idcardnumres[0][0]
            real_name=idcardnumres[0][1]
            # 获取mobile
            guid = res[0][6]
            mobile_sql = f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
            mobileres = self.db.selectsql(mobile_sql)
            mobile = mobileres[0][0]
            # 构造对比数据
            dict ={'AuditBy':'',
                   'AuditRemark':'',
                   'AuditSts':1,
                   'AuditTm':res[0][3],
                   'EntFullName':ent_fulll_name,
                   'EntId':ent_id,
                   'EntShortName':ent_short_name,
                   'IdCardNum':idcardnum,
                   'IneterviewDate':'',
                   'InterViewEntId':0,
                   'InterViewEntShortNme':'',
                   'InterviewEntFullName':'',
                   'Mobile':mobile,
                   'RealName':real_name,
                   'UploadTime':res[0][7].__format__('%Y-%m-%d %H:%M:%S.%f'),
                   'UserWorkCardAuditId':res[0][8],
                   'WorkCardNo':res[0][9],
                   'WorkCardUrl':res[0][10]

            }
            pytest.assume(res_data['Data']['RecordList'][0] == dict)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('身份证审核通过状态，审核通过状态的工牌信息检查')
    @allure.severity('blocker')
    def test_workcardinfo_0004(self):
        """
                身份证审核通过状态，审核通过状态的工牌信息检查

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0004.__name__))
        with allure.step("step1:前置条件准备:会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:前置条件准备:审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成真实姓名
            realname = create_name()
            # 审核通过身份证
            res = upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                  IdCardNum=idcardnum,
                                                  RealName=realname,
                                                  UserIdcardAuditId=idcardaudit_id)
        with allure.step("step2:前置条件准备:生成可预支名单"):
            # 创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            # 创建可预支名单
            namelist_id = namelistsettle.add_namelist_settle(idcardnum, realname, nowtime)
            while True:
                time.sleep(5)
                settle_sql=f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res=self.db.selectsql(settle_sql)
                if res!=():
                    break

        with allure.step("step3:前置条件准备:审核通过工牌"):
            #生成随机工牌
            workCardnum='workcard'+str(random.randint(1,100000))
            #获取可预支名单的ent_id
            settle_ent_sql=f'select ent_id from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            settle_entres=self.db.selectsql(settle_ent_sql)
            namelist_ent_id=settle_entres[0][0]
            #审核通过工牌
            res=upthreecard.weblogin.create_api(AuditWorkCard_Api,
                                            UserWorkCardAuditId=workcardaudit_id,
                                            WorkCardNo=workCardnum,
                                            InterViewEntId=namelist_ent_id,
                                            SubmitEntId=namelist_ent_id,)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("step4:工牌信息列表查询上传的工牌"):
            res = upthreecard.weblogin.create_api(WorkCardInfoList_Api,
                                                  SequenceUploadTime=2,
                                                  RecordIndex=0,
                                                  RecordSize=10,
                                                  EntId=-9999,
                                                  AuditSts=-9999,
                                                  Mobile=upthreecard.mobile)
            res_data = res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            pytest.assume(res_data['Data']['PassCnt'] == 1)
            pytest.assume(res_data['Data']['RecordCount'] == 1)
            pytest.assume(res_data['Data']['UnAuditCnt'] == 0)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            pytest.assume(res_data['Data']['UnPassCnt'] == 0)
            # 校验RecordList数据
            workaudit_sql = f'select audit_by,audit_remark,audit_sts,audit_tm,ent_id,uuid,guid,created_tm,user_work_card_audit_id,work_card_no,work_card_url from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(workaudit_sql)
            ent_id = res[0][4]
            # 获取EntFullName和entshortname
            entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            entname_res = self.db.selectsql(entname_sql)
            ent_fulll_name = entname_res[0][0]
            ent_short_name = entname_res[0][1]
            #获取audit_by
            if res[0][0]==0:
                auditby=''
            else:
                tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={res[0][0]} and t_id={pq_tenant_id} and is_deleted=0'
                auditbyres = self.db.selectsql(tenant_user_sql)
                auditby = auditbyres[0][0]
            # 获取idcardnum和real_name
            uuid = res[0][5]
            idcardnum_sql = f'select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0'
            idcardnumres = self.db.selectsql(idcardnum_sql)
            idcardnum = idcardnumres[0][0]
            real_name = idcardnumres[0][1]
            # 获取mobile
            guid = res[0][6]
            mobile_sql = f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
            mobileres = self.db.selectsql(mobile_sql)
            mobile = mobileres[0][0]
            #获取IneterviewDate、InterViewEntId、InterViewEntShortNme、InterviewEntFullName
            settle_sql = f'select intv_dt,ent_id from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            settleres=self.db.selectsql(settle_sql)
            intv_dt=settleres[0][0].__format__('%Y-%m-%d')
            settle_ent_id=settleres[0][1]
            settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            settle_entname_res = self.db.selectsql(settle_entname_sql)
            settle_ent_fulll_name = settle_entname_res[0][0]
            settle_ent_short_name = settle_entname_res[0][1]
            # 构造对比数据
            dict = {'AuditBy': auditby,
                    'AuditRemark': '',
                    'AuditSts': 2,
                    'AuditTm': res[0][3].__format__('%Y-%m-%d %H:%M:%S'),
                    'EntFullName': ent_fulll_name,
                    'EntId': ent_id,
                    'EntShortName': ent_short_name,
                    'IdCardNum': idcardnum,
                    'IneterviewDate': intv_dt,
                    'InterViewEntId': settle_ent_id,
                    'InterViewEntShortNme': settle_ent_short_name,
                    'InterviewEntFullName': settle_ent_fulll_name,
                    'Mobile': mobile,
                    'RealName': real_name,
                    'UploadTime': res[0][7].__format__('%Y-%m-%d %H:%M:%S.%f'),
                    'UserWorkCardAuditId': res[0][8],
                    'WorkCardNo': res[0][9],
                    'WorkCardUrl': res[0][10]
                    }
            pytest.assume(res_data['Data']['RecordList'][0] == dict)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('身份证审核通过状态，审核不通过状态的工牌信息检查')
    @allure.severity('blocker')
    def test_workcardinfo_0005(self):
        """
                身份证审核通过状态，审核不通过状态的工牌信息检查

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0003.__name__))
        with allure.step("step1:前置条件准备:会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)
            #审核通过身份证
            upthreecard.idcard_auditpass(idcardaudit_id)

        with allure.step("step2:前置条件准备:审核不通过工牌"):
            res=upthreecard.weblogin.create_api(ZXX_GetNextWorkCardPic_Api,
                                                UserWorkCardAuditId=workcardaudit_id)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)
        with allure.step("step3:工牌信息列表查询上传的工牌"):
            res = upthreecard.weblogin.create_api(WorkCardInfoList_Api,
                                                  SequenceUploadTime=2,
                                                  RecordIndex=0,
                                                  RecordSize=10,
                                                  EntId=-9999,
                                                  AuditSts=-9999,
                                                  Mobile=upthreecard.mobile)
            res_data = res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            pytest.assume(res_data['Data']['PassCnt'] == 0)
            pytest.assume(res_data['Data']['RecordCount'] == 1)
            pytest.assume(res_data['Data']['UnAuditCnt'] == 0)
            #获取待审核总数量
            UnAuditRecordcount_sql=f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res=self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount=res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            pytest.assume(res_data['Data']['UnPassCnt'] == 1)

            #校验RecordList数据
            workaudit_sql = f'select audit_by,audit_remark,audit_sts,audit_tm,ent_id,uuid,guid,created_tm,user_work_card_audit_id,work_card_no,work_card_url from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(workaudit_sql)
            # 获取audit_by
            if res[0][0] == 0:
                auditby = ''
            else:
                tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={res[0][0]} and t_id={pq_tenant_id} and is_deleted=0'
                auditbyres = self.db.selectsql(tenant_user_sql)
                auditby = auditbyres[0][0]
            ent_id=res[0][4]
            #获取EntFullName和entshortname
            entname_sql=f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            entname_res=self.db.selectsql(entname_sql)
            ent_fulll_name=entname_res[0][0]
            ent_short_name = entname_res[0][1]
            #获取idcardnum和real_name
            uuid=res[0][5]
            idcardnum_sql=f'select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0'
            idcardnumres=self.db.selectsql(idcardnum_sql)
            idcardnum=idcardnumres[0][0]
            real_name=idcardnumres[0][1]
            # 获取mobile
            guid = res[0][6]
            mobile_sql = f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
            mobileres = self.db.selectsql(mobile_sql)
            mobile = mobileres[0][0]
            # 构造对比数据
            dict ={'AuditBy':auditby,
                   'AuditRemark':'',
                   'AuditSts':3,
                   'AuditTm':res[0][3].__format__('%Y-%m-%d %H:%M:%S'),
                   'EntFullName':ent_fulll_name,
                   'EntId':ent_id,
                   'EntShortName':ent_short_name,
                   'IdCardNum':idcardnum,
                   'IneterviewDate':'',
                   'InterViewEntId':0,
                   'InterViewEntShortNme':'',
                   'InterviewEntFullName':'',
                   'Mobile':mobile,
                   'RealName':real_name,
                   'UploadTime':res[0][7].__format__('%Y-%m-%d %H:%M:%S.%f'),
                   'UserWorkCardAuditId':res[0][8],
                   'WorkCardNo':res[0][9],
                   'WorkCardUrl':res[0][10]

            }
            pytest.assume(res_data['Data']['RecordList'][0] == dict)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('会员有多条结算名单，查询工牌信息接口返回数据检查')
    @allure.severity('blocker')
    def test_workcardinfo_0006(self):
        """
                会员有多条结算名单，查询工牌信息接口返回数据检查

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0006.__name__))
        with allure.step("step1:前置条件准备:会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:前置条件准备:审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成真实姓名
            realname = create_name()
            # 审核通过身份证
            res = upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                  IdCardNum=idcardnum,
                                                  RealName=realname,
                                                  UserIdcardAuditId=idcardaudit_id)
        with allure.step("step3:前置条件准备:生成可预支名单"):
            # 创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            # 创建第一条可预支名单
            namelist_id = namelistsettle.add_namelist_settle(idcardnum, realname, nowtime)
            while True:
                time.sleep(5)
                settle_sql=f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res=self.db.selectsql(settle_sql)
                if res!=():
                    break
            # 创建第二条可预支名单
            beforedate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            namelist_id1 = namelistsettle.add_namelist_settle(idcardnum, realname, beforedate)
            while True:
                time.sleep(5)
                settle_sql=f'select * from name_list_settle where name_list_id={namelist_id1} and ec_id={ec_id}'
                res=self.db.selectsql(settle_sql)
                if res!=():
                    break


        with allure.step("step4:工牌信息列表查询上传的工牌"):
            res = upthreecard.weblogin.create_api(WorkCardInfoList_Api,
                                                  SequenceUploadTime=2,
                                                  RecordIndex=0,
                                                  RecordSize=10,
                                                  EntId=-9999,
                                                  AuditSts=-9999,
                                                  Mobile=upthreecard.mobile)
            res_data = res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            pytest.assume(res_data['Data']['PassCnt'] == 0)
            pytest.assume(res_data['Data']['RecordCount'] == 1)
            pytest.assume(res_data['Data']['UnAuditCnt'] == 1)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            pytest.assume(res_data['Data']['UnPassCnt'] == 0)
            # 校验RecordList数据
            workaudit_sql = f'select audit_by,audit_remark,audit_sts,audit_tm,ent_id,uuid,guid,created_tm,user_work_card_audit_id,work_card_no,work_card_url from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}'
            res = self.db.selectsql(workaudit_sql)
            ent_id = res[0][4]
            # 获取EntFullName和entshortname
            entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            entname_res = self.db.selectsql(entname_sql)
            ent_fulll_name = entname_res[0][0]
            ent_short_name = entname_res[0][1]
            #获取audit_by
            if res[0][0]==0:
                auditby=''
            else:
                tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={res[0][0]} and t_id={pq_tenant_id} and is_deleted=0'
                auditbyres = self.db.selectsql(tenant_user_sql)
                auditby = auditbyres[0][0]
            # 获取idcardnum和real_name
            uuid = res[0][5]
            idcardnum_sql = f'select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0'
            idcardnumres = self.db.selectsql(idcardnum_sql)
            idcardnum = idcardnumres[0][0]
            real_name = idcardnumres[0][1]
            # 获取mobile
            guid = res[0][6]
            mobile_sql = f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
            mobileres = self.db.selectsql(mobile_sql)
            mobile = mobileres[0][0]
            #获取IneterviewDate、InterViewEntId、InterViewEntShortNme、InterviewEntFullName
            settle_sql = f'select intv_dt,ent_id from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            settleres=self.db.selectsql(settle_sql)
            intv_dt=settleres[0][0].__format__('%Y-%m-%d')
            settle_ent_id=settleres[0][1]
            settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
            settle_entname_res = self.db.selectsql(settle_entname_sql)
            settle_ent_fulll_name = settle_entname_res[0][0]
            settle_ent_short_name = settle_entname_res[0][1]
            # 构造对比数据
            dict = {'AuditBy': auditby,
                    'AuditRemark': '',
                    'AuditSts': 1,
                    'AuditTm': res[0][3],
                    'EntFullName': ent_fulll_name,
                    'EntId': ent_id,
                    'EntShortName': ent_short_name,
                    'IdCardNum': idcardnum,
                    'IneterviewDate': intv_dt,
                    'InterViewEntId': settle_ent_id,
                    'InterViewEntShortNme': settle_ent_short_name,
                    'InterviewEntFullName': settle_ent_fulll_name,
                    'Mobile': mobile,
                    'RealName': real_name,
                    'UploadTime': res[0][7].__format__('%Y-%m-%d %H:%M:%S.%f'),
                    'UserWorkCardAuditId': res[0][8],
                    'WorkCardNo': res[0][9],
                    'WorkCardUrl': res[0][10]
                    }
            pytest.assume(res_data['Data']['RecordList'][0] == dict)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('统计信息数据检查')
    @allure.severity('blocker')
    def test_workcardinfo_0007(self):
        """
                统计信息数据检查

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0007.__name__))
        with allure.step("step1:查询全部的工牌信息"):
            # 登录
            self.weblogin.login(pq_boss_user)
            # 获取全部的银行卡记录
            res=self.weblogin.create_api(WorkCardInfoList_Api,
                                     SequenceUploadTime=2,
                                     RecordIndex=0,
                                     RecordSize=10,
                                     EntId=-9999,
                                     AuditSts=-9999)

            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 1)
            #获取查询结果中审核通过数量
            passcnt_sql=f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres=self.db.selectsql(passcnt_sql)
            passcnt=passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] ==passcnt )
            #获取查询结果中总数量
            RecordCount_sql=f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            #获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            #获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('工牌信息列表查看未脱敏手机号、未脱敏身份证号码')
    @allure.severity('blocker')
    def test_workcardinfo_0008(self):
        """
                工牌信息列表查看未脱敏手机号、未脱敏身份证号码

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0008.__name__))
        with allure.step("step1:查询全部的工牌信息并随机获取其中一条工牌记录"):
            # 登录
            self.weblogin.login(pq_boss_user)
            # 获取全部的工牌记录
            res=self.weblogin.create_api(WorkCardInfoList_Api,
                                     SequenceUploadTime=2,
                                     RecordIndex=0,
                                     RecordSize=10,
                                     EntId=-9999,
                                     AuditSts=-9999)

            res_data=res.json()
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            #随机获取一条工牌记录
            workcardinfo=random.choice(res_data['Data']['RecordList'])
            # 获取脱敏的手机号码
            desenmobile = workcardinfo['Mobile']
            # 获取脱敏的身份证号码
            desenidcardnum = workcardinfo['IdCardNum']
            # 获取银行卡审核记录的audit_id
            audit_id = workcardinfo['UserWorkCardAuditId']

        with allure.step("step2:获取选择的工牌记录的未脱敏的身份证号码、手机号码"):
            # 获取guid,uuid
            guid_sql = f'select guid,uuid from member_user_work_card_audit where user_work_card_audit_id={audit_id} and ec_id={ec_id} and is_deleted=0'
            res = self.db.selectsql(guid_sql)
            guid = res[0][0]
            uuid=res[0][1]
            #获取未脱敏的身份证号码
            real_idcardnum_sql=f'select id_card_num from member_user_unique where uuid={uuid} and is_deleted=0'
            real_idcardnumres=self.db.selectsql(real_idcardnum_sql)
            real_idcardnum=real_idcardnumres[0][0]
            #获取未脱敏的手机号码
            real_mobile_sql = f'select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}'
            real_mobileres = self.db.selectsql(real_mobile_sql)
            real_mobile = real_mobileres[0][0]

        with allure.step("step3:查看未脱敏的手机号码并校验返回值"):
            # 查看未脱敏的手机号码
            res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=desenmobile)
            result = res.json()
        with allure.step("预期结果:接口返回的数据正确"):
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['DesenData'] == desenmobile)
            pytest.assume(result['Data']['OriData'] == real_mobile)
            pytest.assume(result['Data']['Typ'] == 1)

        with allure.step("step5:查看未脱敏的身份证号码并校验返回值"):
            # 查看未脱敏的身份证号码
            res = self.weblogin.create_api(DecryptAPI, Typ=2, DesenData=desenidcardnum)
            result = res.json()
        with allure.step("预期结果:接口返回的数据正确"):
            pytest.assume(result['Code'] == 0)
            pytest.assume(result['Desc'] == '成功')
            pytest.assume(result['Data']['DesenData'] == desenidcardnum)
            pytest.assume(result['Data']['OriData'] == real_idcardnum)
            pytest.assume(result['Data']['Typ'] == 2)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('默认查询项查询')
    @allure.severity('blocker')
    def test_workcardinfo_0009(self):
        """
                默认查询项查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0009.__name__))
        with allure.step("step1:默认查询项查询工牌信息记录"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 获取全部工牌记录
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 1)
            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]
                #获取未脱敏的身份证号码
                res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                               DesenData=workcardlist[one]['IdCardNum'])
                realidcardnum = res.json()['Data']['OriData']

                pytest.assume(realidcardnum == idcardnum)
                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                # 获取未脱敏的手机号码
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=workcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('身份证号码查询')
    @allure.severity('blocker')
    def test_workcardinfo_0010(self):
        """
                身份证号码查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0010.__name__))
        with allure.step("step1:前置条件：随便获取已存在工牌记录的身份证号码"):
            unique_sql=f"select a.id_card_num from member_user_unique as a left join member_user_work_card_audit as b on a.uuid=b.uuid where b.is_deleted=0 and b.ec_id={ec_id} and b.is_canceled=0 and b.uuid>0"
            uniqueres=self.db.selectsql(unique_sql)
            input_idcardnum=random.choice(uniqueres)[0]

        with allure.step("step2:填写身份证号码，查询工牌"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 获取全部工牌记录
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           IdCardNum=input_idcardnum)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            # 获取身份证号码对应的guid
            allguid_sql = f"select guid from member_user_unique as a left join member_user as b on a.uuid=b.uuid where a.id_card_num='{input_idcardnum}' and b.ec_id={ec_id}"
            res = self.db.selectsql(allguid_sql)
            allguid = ''
            for one in res:
                allguid = allguid + str(one[0]) + ','
            allguid = allguid[:-1]
            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]

                pytest.assume(workcardlist[one]['IdCardNum'] == idcardnum)
                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                pytest.assume(workcardlist[one]['Mobile'] == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])

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
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           IdCardNum=noneidcardnum)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('姓名查询')
    @allure.severity('blocker')
    def test_workcardinfo_0011(self):
        """
                姓名查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0011.__name__))
        with allure.step("step1:前置条件：随机获取已存在工牌记录的姓名"):
            unique_sql=f"select a.real_name from member_user_unique as a left join member_user_work_card_audit as b on a.uuid=b.uuid where b.is_deleted=0 and b.ec_id={ec_id} and b.is_canceled=0 and b.uuid>0"
            uniqueres=self.db.selectsql(unique_sql)
            input_real_name=random.choice(uniqueres)[0]

        with allure.step("step2:填写姓名，查询工牌"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 填写姓名，查询工牌
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           RealName=input_real_name)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            # 获取姓名对应的guid
            allguid_sql = f"select guid from member_user_unique as a left join member_user as b on a.uuid=b.uuid where a.real_name='{input_real_name}' and b.ec_id={ec_id}"
            res = self.db.selectsql(allguid_sql)
            allguid = ''
            for one in res:
                allguid = allguid + str(one[0]) + ','
            allguid = allguid[:-1]
            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]

                pytest.assume(workcardlist[one]['IdCardNum'] == idcardnum)
                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                pytest.assume(workcardlist[one]['Mobile'] == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])

        with allure.step("step3:输入不已存在工牌记录的姓名，查询工牌信息"):
            #随机生成不存在工牌审核记录的姓名
            while True:
                # 生成姓名
                nonerealname = create_name()
                # 校验姓名是否存在
                unique_sql = f"select id_card_num from member_user_unique where real_name='{nonerealname}'"
                res = self.db.selectsql(unique_sql)
                if res == ():
                    break

            # 不存在工牌记录的姓名查询
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           RealName=nonerealname)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('手机号码查询')
    @allure.severity('blocker')
    def test_workcardinfo_0012(self):
        """
                手机号码查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0012.__name__))
        with allure.step("step1:前置条件：随机获取已存在工牌记录的手机号码"):
            unique_sql=f"select a.mobile from member_user as a left join member_user_work_card_audit as b on a.guid=b.guid where b.is_deleted=0 and b.ec_id={ec_id} and b.is_canceled=0 and b.uuid>0"
            uniqueres=self.db.selectsql(unique_sql)
            input_mobile=random.choice(uniqueres)[0]

        with allure.step("step2:填写姓名，查询工牌"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 填写手机号码，查询工牌
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           Mobile=input_mobile)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)
            # 获取手机号码对应的guid
            allguid_sql = f"select guid from member_user where mobile='{input_mobile}' and ec_id={ec_id}"
            res = self.db.selectsql(allguid_sql)
            allguid = ''
            for one in res:
                allguid = allguid + str(one[0]) + ','
            allguid = allguid[:-1]
            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ({allguid}) and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]

                pytest.assume(workcardlist[one]['IdCardNum'] == idcardnum)
                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                pytest.assume(workcardlist[one]['Mobile'] == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])

        with allure.step("step3:输入不已存在工牌记录的姓名，查询工牌信息"):
            #随机生成不存在工牌审核记录的手机号码
            while True:
                # 生成姓名
                nonemobile = create_phone()
                # 校验姓名是否存在
                unique_sql = f"select mobile from member_user where mobile='{nonemobile}'"
                res = self.db.selectsql(unique_sql)
                if res == ():
                    break

            # 不存在工牌记录的手机号码查询
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           Mobile=nonemobile)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('标准企业查询')
    @allure.severity('blocker')
    def test_workcardinfo_0013(self):
        """
                标准企业查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0013.__name__))
        with allure.step("step1:前置条件：随机获取已存在工牌记录的标准企业"):
            workcardaudit_ent_sql=f"SELECT ent_id FROM member_user_work_card_audit  WHERE is_deleted = 0 AND is_canceled = 0  AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            workcardaudit_entres=self.db.selectsql(workcardaudit_ent_sql)
            input_ent=random.choice(workcardaudit_entres)[0]

        with allure.step("step2:选择标准企业，查询工牌"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 选择标准企业，查询工牌
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=input_ent,
                                           AuditSts=-9999)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 1)
            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND ent_id = {input_ent} and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND ent_id = {input_ent} and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND ent_id = {input_ent} and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND ent_id = {input_ent} and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND ent_id = {input_ent} and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]
                # 获取未脱敏的身份证号码
                res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                               DesenData=workcardlist[one]['IdCardNum'])
                realidcardnum = res.json()['Data']['OriData']

                pytest.assume(realidcardnum == idcardnum)

                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                # 获取未脱敏的手机号码
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=workcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])

        with allure.step("step3:输入不已存在工牌记录的标准企业，查询工牌信息"):
            #随机获取不存在工牌审核记录的标准企业
            noneent_sql=f"select ent_id from tenant_ent where is_deleted=0 and ec_id={ec_id} and ent_id not in(SELECT ent_id FROM member_user_work_card_audit  WHERE is_deleted = 0 AND is_canceled = 0  AND work_card_url > '' AND uuid > 0 AND ec_id ={ec_id})"
            noneentres=self.db.selectsql(noneent_sql)
            noneent=random.choice(noneentres)[0]

            # 不存在工牌记录的标准企业查询
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=noneent,
                                           AuditSts=-9999)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('工牌号查询')
    @allure.severity('blocker')
    def test_workcardinfo_0014(self):
        """
                工牌号查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0014.__name__))
        with allure.step("step1:前置条件：随机获取已存在工牌记录的工牌号"):
            workcardaudit_workcardno_sql=f"SELECT work_card_no FROM member_user_work_card_audit  WHERE is_deleted = 0 AND is_canceled = 0  AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            workcardaudit_workcardnores=self.db.selectsql(workcardaudit_workcardno_sql)
            input_workcardno=random.choice(workcardaudit_workcardnores)[0]

        with allure.step("step2:填写工牌号，查询工牌"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 填写工牌号码，查询工牌
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           WorkCardNo=input_workcardno)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 1)
            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND work_card_no ='{input_workcardno}' and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND work_card_no ='{input_workcardno}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND work_card_no ='{input_workcardno}' and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND work_card_no ='{input_workcardno}' and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND work_card_no ='{input_workcardno}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]
                # 获取未脱敏的身份证号码
                res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                               DesenData=workcardlist[one]['IdCardNum'])
                realidcardnum = res.json()['Data']['OriData']

                pytest.assume(realidcardnum == idcardnum)

                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                # 获取未脱敏的手机号码
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=workcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])

        with allure.step("step3:输入不已存在工牌记录的标准企业，查询工牌信息"):
            #随机生成不存在工牌审核记录的工牌号码
            while True:
                noneworkcardno='workcard'+str(random.randint(1,100000))
                noneworkcardno_sql=f"select * from member_user_work_card_audit where is_deleted=0 and ec_id={ec_id} and work_card_no='{noneworkcardno}'"
                noneworkcardnores=self.db.selectsql(noneworkcardno_sql)
                if noneworkcardnores==():
                    break

            # 不存在工牌记录的工牌号码查询
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           WorkCardNo=noneworkcardno)
            res_data = res.json()['Data']

        with allure.step("预期结果:校验接口返回的数据，接口返回数据正确"):
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            pytest.assume(res_data['RecordCount']==0)
            pytest.assume(res_data['RecordList'] == [])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('审核状态查询')
    @pytest.mark.parametrize('AuditSts', [2, 3, 1])
    @allure.severity('blocker')
    def test_workcardinfo_0015(self,AuditSts):
        """
                审核状态查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0015.__name__))

        with allure.step("step1:选择待审核、审核通过、审核不通过，查询工牌信息"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 选择待审核、审核通过、审核不通过，查询工牌信息
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=AuditSts)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            if res_data['Data']['RecordList'] == []:
                pytest.assume(res_data['Data']['NeedDesen'] == 0)
            else:
                pytest.assume(res_data['Data']['NeedDesen'] == 1)
            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = {AuditSts} and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = {AuditSts} and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = {AuditSts} and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = {AuditSts} and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = {AuditSts} and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]
                # 获取未脱敏的身份证号码
                res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                               DesenData=workcardlist[one]['IdCardNum'])
                realidcardnum = res.json()['Data']['OriData']

                pytest.assume(realidcardnum == idcardnum)

                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                # 获取未脱敏的手机号码
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=workcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('上传日期查询')
    @pytest.mark.parametrize('RegTimeBegin,RegTimeEnd', [(nowtime, None),
                                                         (None, nowtime),
                                                         (nowtime, nowtime)])
    @allure.severity('blocker')
    def test_workcardinfo_0016(self,RegTimeBegin,RegTimeEnd):
        """
                上传时期查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0016.__name__))

        with allure.step("step1:只选择开始时间、只选择结束时间、选择正确的时间区间，查询工牌记录"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 只选择开始时间、只选择结束时间、选择正确的时间区间，查询工牌记录
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=-9999,
                                           AuditSts=-9999,
                                           UploadTimeBegin=RegTimeBegin,
                                           UploadTimeEnd=RegTimeEnd)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            if res_data['Data']['RecordList']==[]:
                pytest.assume(res_data['Data']['NeedDesen'] == 0)
            else:
                pytest.assume(res_data['Data']['NeedDesen'] == 1)

            if RegTimeBegin==None:
                RegTimeEnd = RegTimeEnd + ' 23:59:59.000000'
            elif RegTimeEnd==None:
                RegTimeBegin = RegTimeBegin + ' 00:00:00.000000'
            else:
                RegTimeBegin=RegTimeBegin+' 00:00:00.000000'
                RegTimeEnd=RegTimeEnd+' 23:59:59.000000'

            # 获取查询结果中审核通过数量
            if RegTimeBegin==None:
                passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm <= '{RegTimeEnd}' and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            elif RegTimeEnd==None:
                passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            else:
                passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and created_tm <= '{RegTimeEnd}' and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)

            # 获取查询结果中总数量
            if RegTimeBegin==None:
                RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm <= '{RegTimeEnd}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            elif RegTimeEnd==None:
                RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            else:
                RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and created_tm <= '{RegTimeEnd}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"

            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            if RegTimeBegin==None:
                UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm <= '{RegTimeEnd}' and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            elif RegTimeEnd==None:
                UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            else:
                UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and created_tm <= '{RegTimeEnd}' and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)

            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)

            # 获取查询结果中审核不通过数量
            if RegTimeBegin==None:
                UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm <= '{RegTimeEnd}' and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            elif RegTimeEnd==None:
                UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            else:
                UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and created_tm <= '{RegTimeEnd}' and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            if RegTimeBegin==None:
                workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm <= '{RegTimeEnd}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            elif RegTimeEnd==None:
                workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            else:
                workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND created_tm >= '{RegTimeBegin}' and created_tm <= '{RegTimeEnd}' and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]
                # 获取未脱敏的身份证号码
                res = self.weblogin.create_api(DecryptAPI, Typ=2,
                                               DesenData=workcardlist[one]['IdCardNum'])
                realidcardnum = res.json()['Data']['OriData']

                pytest.assume(realidcardnum == idcardnum)

                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                # 获取未脱敏的手机号码
                res = self.weblogin.create_api(DecryptAPI, Typ=1, DesenData=workcardlist[one]['Mobile'])
                realmobile = res.json()['Data']['OriData']
                pytest.assume(realmobile == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])

    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('组合查询')
    @allure.severity('blocker')
    def test_workcardinfo_0017(self):
        """
                组合查询

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0017.__name__))
        with allure.step("step1:前置条件：随机获取已存在工牌记录的身份证号码、姓名、手机号码、工牌、标准企业、审核状态、上传日期"):
            workaudit_sql=f"select guid,uuid,work_card_no,ent_id,audit_sts,created_tm from member_user_work_card_audit where uuid>0 and is_canceled=0 and is_deleted=0 and audit_sts=2 and ec_id={ec_id}"
            workauditres=self.db.selectsql(workaudit_sql)
            workcardinfo=random.choice(workauditres)
            #获取身份证号码、姓名
            uuid=workcardinfo[1]
            sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
            res=self.db.selectsql(sql)
            input_idcardnum=res[0][0]
            input_realname=res[0][1]
            #获取手机号码
            guid=workcardinfo[0]
            sql=f"select mobile from member_user where guid={guid} and ec_id={ec_id} and is_deleted=0"
            res=self.db.selectsql(sql)
            input_mobile=res[0][0]
            #获取工牌、标准企业、审核状态
            input_workcardno=workcardinfo[2]
            input_entid=workcardinfo[3]
            input_auditsts=workcardinfo[4]
            # 获取上传时间
            uploadtime = workcardinfo[5].__format__('%Y-%m-%d')
            # 构造UploadTimeBegin和UploadTimend
            input_UploadTimeBegin = uploadtime + ' 00:00:00.000000'
            input_UploadTimend = uploadtime + ' 23:59:59.000000'

        with allure.step("step2:填写身份证号码、姓名、手机号码、工牌、标准企业、审核状态、上传日期,查询工牌"):
            #登录
            self.weblogin.login(pq_boss_user)
            # 填写工牌号码，查询工牌
            res = self.weblogin.create_api(WorkCardInfoList_Api,
                                           SequenceUploadTime=2,
                                           RecordIndex=0,
                                           RecordSize=10,
                                           EntId=input_entid,
                                           AuditSts=input_auditsts,
                                           IdCardNum=input_idcardnum,
                                           Mobile=input_mobile,
                                           RealName=input_realname,
                                           UploadTimeBegin=input_UploadTimeBegin,
                                           UploadTimeEnd=input_UploadTimend,
                                           WorkCardNo=input_workcardno)
            res_data=res.json()

        with allure.step("预期结果:接口调用成功，接口返回的数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['NeedDesen'] == 0)

            # 获取手机号码对应的guid
            allguid_sql = f"select guid from member_user where mobile='{input_mobile}' and ec_id={ec_id}"
            res = self.db.selectsql(allguid_sql)
            allguid = ''
            for one in res:
                allguid = allguid + str(one[0]) + ','
            allguid = allguid[:-1]

            # 获取查询结果中审核通过数量
            passcnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ('{allguid}') and ent_id ={input_entid} and work_card_no = '{input_workcardno}' and created_tm >= '{input_UploadTimeBegin}' and created_tm <= '{input_UploadTimend}' and audit_sts = {input_auditsts} and audit_sts = 2 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            passcntres = self.db.selectsql(passcnt_sql)
            passcnt = passcntres[0][0]
            pytest.assume(res_data['Data']['PassCnt'] == passcnt)
            # 获取查询结果中总数量
            RecordCount_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ('{allguid}') and ent_id ={input_entid} and work_card_no = '{input_workcardno}' and created_tm >= '{input_UploadTimeBegin}' and created_tm <= '{input_UploadTimend}' and audit_sts = {input_auditsts} and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id}"
            RecordCountres = self.db.selectsql(RecordCount_sql)
            RecordCount = RecordCountres[0][0]
            pytest.assume(res_data['Data']['RecordCount'] == RecordCount)
            # 获取查询结果中待审核数量
            UnAuditCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ('{allguid}') and ent_id ={input_entid} and work_card_no = '{input_workcardno}' and created_tm >= '{input_UploadTimeBegin}' and created_tm <= '{input_UploadTimend}' and audit_sts = {input_auditsts} and audit_sts = 1 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnAuditCntres = self.db.selectsql(UnAuditCnt_sql)
            UnAuditCnt = UnAuditCntres[0][0]
            pytest.assume(res_data['Data']['UnAuditCnt'] == UnAuditCnt)
            # 获取待审核总数量
            UnAuditRecordcount_sql = f'SELECT count(*) FROM `member_user`  WHERE is_deleted = 0 AND guid in (SELECT guid FROM member_user_work_card_audit  WHERE is_deleted = 0 AND audit_sts = 1 AND is_canceled = 0 AND ec_id = {ec_id}) AND uuid != 0 AND ec_id = {ec_id}'
            res = self.db.selectsql(UnAuditRecordcount_sql)
            UnAuditRecordcount = res[0][0]
            pytest.assume(res_data['Data']['UnAuditRecordcount'] == UnAuditRecordcount)
            # 获取查询结果中审核不通过数量
            UnPassCnt_sql = f"SELECT count(*) FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ('{allguid}') and ent_id ={input_entid} and work_card_no = '{input_workcardno}' and created_tm >= '{input_UploadTimeBegin}' and created_tm <= '{input_UploadTimend}' and audit_sts = {input_auditsts} and audit_sts = 3 AND is_canceled = 0 AND work_card_url > '' AND uuid >0 AND ec_id = {ec_id}"
            UnPassCntres = self.db.selectsql(UnPassCnt_sql)
            UnPassCnt = UnPassCntres[0][0]
            pytest.assume(res_data['Data']['UnPassCnt'] == UnPassCnt)

        with allure.step("预期结果:校验返回的recountlist数据，数据返回正确"):
            workaudit_sql=f"SELECT guid,uuid,audit_by,audit_remark,audit_sts,audit_tm,ent_id,created_tm,user_work_card_audit_id,work_card_no,work_card_url FROM member_user_work_card_audit  WHERE is_deleted = 0 AND guid in ('{allguid}') and ent_id ={input_entid} and work_card_no = '{input_workcardno}' and created_tm >= '{input_UploadTimeBegin}' and created_tm <= '{input_UploadTimend}' and audit_sts = {input_auditsts} and is_canceled = 0 AND work_card_url > '' AND uuid > 0 AND ec_id = {ec_id} ORDER BY audit_sts asc,created_tm desc,audit_tm desc LIMIT 10 OFFSET 0"
            db_res=self.db.selectsql(workaudit_sql)
            #获取接口返回的RecordList列表
            workcardlist=res_data['Data']['RecordList']
            for one in range(len(workcardlist)):
                # 获取audit_by
                if db_res[one][2] == 0:
                    auditby = ''
                else:
                    tenant_user_sql = f'SELECT user_name FROM tenant_user where guid={db_res[one][2]} and t_id={pq_tenant_id} and is_deleted=0'
                    auditbyres = self.db.selectsql(tenant_user_sql)
                    auditby = auditbyres[0][0]
                pytest.assume(workcardlist[one]['AuditBy']==auditby)
                pytest.assume(workcardlist[one]['AuditRemark'] == '')
                pytest.assume(workcardlist[one]['AuditSts'] == db_res[one][4])
                #获取audit_tm
                if db_res[one][5]=='0000-00-00 00:00:00':
                    audit_tm='0000-00-00 00:00:00'
                else:
                    audit_tm=db_res[one][5].__format__('%Y-%m-%d %H:%M:%S')
                pytest.assume(workcardlist[one]['AuditTm'] == audit_tm)
                # 获取EntFullName和entshortname
                ent_id = db_res[one][6]
                entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                entname_res = self.db.selectsql(entname_sql)
                ent_fulll_name = entname_res[0][0]
                ent_short_name = entname_res[0][1]

                pytest.assume(workcardlist[one]['EntFullName'] == ent_fulll_name)
                pytest.assume(workcardlist[one]['EntId'] == ent_id)
                pytest.assume(workcardlist[one]['EntShortName'] == ent_short_name)
                #获取身份证号码和realname
                uuid=db_res[one][1]
                idcardnum_sql=f"select id_card_num,real_name from member_user_unique where uuid={uuid} and is_deleted=0"
                idcardnumres=self.db.selectsql(idcardnum_sql)
                idcardnum=idcardnumres[0][0]
                real_name=idcardnumres[0][1]
                pytest.assume(workcardlist[one]['IdCardNum'] == idcardnum)

                pytest.assume(workcardlist[one]['RealName'] == real_name)

                settle_sql=f"SELECT intv_dt, ent_id, uuid FROM name_list_settle  WHERE uuid in ({uuid}) AND is_valid = 1 AND ec_id = {ec_id} AND is_deleted = 0 ORDER BY intv_dt desc,created_tm desc limit 1"
                settleres=self.db.selectsql(settle_sql)
                if settleres==():
                    pytest.assume(workcardlist[one]['IneterviewDate'] == '')
                    pytest.assume(workcardlist[one]['InterViewEntId'] == 0)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == '')
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == '')
                else:
                    intv_dt=settleres[0][0].__format__('%Y-%m-%d')
                    settle_ent_id=settleres[0][1]
                    # 获取EntFullName和entshortname
                    settle_entname_sql = f'select ent_full_name,ent_short_name from tenant_ent where ent_id={settle_ent_id} and is_enabled=1 and is_deleted=0 and ec_id={ec_id}'
                    settle_entname_res = self.db.selectsql(settle_entname_sql)
                    settle_ent_fulll_name = settle_entname_res[0][0]
                    settle_ent_short_name = settle_entname_res[0][1]
                    pytest.assume(workcardlist[one]['IneterviewDate'] == intv_dt)
                    pytest.assume(workcardlist[one]['InterViewEntId'] == settle_ent_id)
                    pytest.assume(workcardlist[one]['InterViewEntShortNme'] == settle_ent_short_name)
                    pytest.assume(workcardlist[one]['InterviewEntFullName'] == settle_ent_fulll_name)

                #获取mobile
                guid = db_res[one][0]
                mobile_sql=f"select mobile from member_user where guid={guid} and is_deleted=0 and ec_id={ec_id}"
                mobileres=self.db.selectsql(mobile_sql)
                mobile=mobileres[0][0]
                pytest.assume(workcardlist[one]['Mobile'] == mobile)

                pytest.assume(workcardlist[one]['UploadTime'] ==db_res[one][7].__format__('%Y-%m-%d %H:%M:%S.%f') )
                pytest.assume(workcardlist[one]['UserWorkCardAuditId'] == db_res[one][8])
                pytest.assume(workcardlist[one]['WorkCardNo'] == db_res[one][9])
                pytest.assume(workcardlist[one]['WorkCardUrl'] == db_res[one][10])


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('会员无结算名单审核工牌')
    @allure.severity('blocker')
    def test_workcardinfo_0018(self):
        """
                会员无结算名单审核工牌

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0018.__name__))
        with allure.step("step1:前置条件准备,会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:审核通过身份证"):
            upthreecard.idcard_auditpass(idcardaudit_id)

        with allure.step("step3:无结算名单审核工牌,InterViewEntId传值为None"):
            # 生成随机工牌
            workCardnum = 'workcard' + str(random.randint(1, 100000))
            # 审核通过工牌
            res = upthreecard.weblogin.create_api(AuditWorkCard_Api,
                                                  UserWorkCardAuditId=workcardaudit_id,
                                                  WorkCardNo=workCardnum,
                                                  InterViewEntId=None,
                                                  SubmitEntId=upthreecard.appletfunc.entid, )
            res_data = res.json()

        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_workcard_audit表数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id,audit_sts,audit_by,audit_remark,audit_name from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and is_canceled=0 and ec_id={ec_id}"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]==workCardnum)
            pytest.assume(workcardauditres[0][1] == upthreecard.appletfunc.entid)
            pytest.assume(workcardauditres[0][2] == 2)
            #获取audit_by和audit_name
            tenant_user_sql=f"select guid,user_name from tenant_user where t_id={pq_tenant_id} and mobile={pq_boss_user} and is_enabled=1 and is_deleted=0"
            tenant_user_res=self.db.selectsql(tenant_user_sql)
            audit_by=tenant_user_res[0][0]
            audit_name=tenant_user_res[0][1]

            pytest.assume(workcardauditres[0][3] == audit_by)
            pytest.assume(workcardauditres[0][4] == '通过')
            pytest.assume(workcardauditres[0][5] == audit_name)

        with allure.step("预期结果:member_user_workcard表新增一条数据，数据正确"):
            workcard_sql=f"select user_work_card_audit_id,guid,uuid,work_card_no,ent_id from member_user_work_card where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(len(workcardres)==1)
            pytest.assume(workcardres[0][0]==workcardaudit_id)
            pytest.assume(workcardres[0][1] == upthreecard.minilogin.Guid)
            #获取uuid
            uuid_sql=f"select uuid from member_user where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            uuidres=self.db.selectsql(uuid_sql)
            uuid=uuidres[0][0]
            pytest.assume(workcardres[0][2]==uuid)
            pytest.assume(workcardres[0][3]==workCardnum)
            pytest.assume(workcardres[0][4] ==upthreecard.appletfunc.entid)

        ret=[workcardaudit_id,workCardnum]
        return ret


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('会员有结算名单审核工牌')
    @allure.severity('blocker')
    def test_workcardinfo_0019(self):
        """
                会员有结算名单审核工牌

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0019.__name__))
        with allure.step("step1:前置条件准备:会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:前置条件准备:审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成真实姓名
            realname = create_name()
            # 审核通过身份证
            res = upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                  IdCardNum=idcardnum,
                                                  RealName=realname,
                                                  UserIdcardAuditId=idcardaudit_id)
        with allure.step("step2:前置条件准备:生成可预支名单"):
            # 创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            # 创建可预支名单
            namelist_id = namelistsettle.add_namelist_settle(idcardnum, realname, nowtime)
            while True:
                time.sleep(5)
                settle_sql=f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res=self.db.selectsql(settle_sql)
                if res!=():
                    break

        with allure.step("step3:审核通过工牌"):
            #生成随机工牌
            workCardnum='workcard'+str(random.randint(1,100000))
            #获取可预支名单的ent_id
            settle_ent_sql=f'select ent_id from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            settle_entres=self.db.selectsql(settle_ent_sql)
            namelist_ent_id=settle_entres[0][0]
            #审核通过工牌
            res=upthreecard.weblogin.create_api(AuditWorkCard_Api,
                                            UserWorkCardAuditId=workcardaudit_id,
                                            WorkCardNo=workCardnum,
                                            InterViewEntId=namelist_ent_id,
                                            SubmitEntId=namelist_ent_id,)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_workcard_audit表数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id,audit_sts,audit_by,audit_remark,audit_name from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and is_canceled=0 and ec_id={ec_id}"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]==workCardnum)
            pytest.assume(workcardauditres[0][1] == namelist_ent_id)
            pytest.assume(workcardauditres[0][2] == 2)
            #获取audit_by和audit_name
            tenant_user_sql=f"select guid,user_name from tenant_user where t_id={pq_tenant_id} and mobile={pq_boss_user} and is_enabled=1 and is_deleted=0"
            tenant_user_res=self.db.selectsql(tenant_user_sql)
            audit_by=tenant_user_res[0][0]
            audit_name=tenant_user_res[0][1]

            pytest.assume(workcardauditres[0][3] == audit_by)
            pytest.assume(workcardauditres[0][4] == '通过')
            pytest.assume(workcardauditres[0][5] == audit_name)

        with allure.step("预期结果:member_user_workcard表新增一条数据，数据正确"):
            workcard_sql=f"select user_work_card_audit_id,guid,uuid,work_card_no,ent_id from member_user_work_card where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(len(workcardres)==1)
            pytest.assume(workcardres[0][0]==workcardaudit_id)
            pytest.assume(workcardres[0][1] == upthreecard.minilogin.Guid)
            #获取uuid
            uuid_sql=f"select uuid from member_user where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            uuidres=self.db.selectsql(uuid_sql)
            uuid=uuidres[0][0]
            pytest.assume(workcardres[0][2]==uuid)
            pytest.assume(workcardres[0][3]==workCardnum)
            pytest.assume(workcardres[0][4] ==namelist_ent_id)

        with allure.step("预期结果:name_list_settle表名单的工牌数据更新正确"):
            settle_workcard_sql=f"select user_work_card_audit_id,work_card_no from name_list_settle where name_list_id={namelist_id} and is_valid=1 and is_deleted=0 and tenant_id={pq_tenant_id} and ec_id={ec_id}"
            settle_workcardres=self.db.selectsql(settle_workcard_sql)
            pytest.assume(settle_workcardres[0][0]==workcardaudit_id)
            pytest.assume(settle_workcardres[0][1]==workCardnum)

        ret=[namelist_id,namelist_ent_id,workCardnum,workcardaudit_id]
        return ret

    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('会员存在多条结算名单，审核工牌')
    @allure.severity('blocker')
    def test_workcardinfo_0020(self):
        """
                会员存在多条结算名单，审核工牌

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0019.__name__))
        with allure.step("step1:前置条件准备:会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:前置条件准备:审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成真实姓名
            realname = create_name()
            # 审核通过身份证
            res = upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                  IdCardNum=idcardnum,
                                                  RealName=realname,
                                                  UserIdcardAuditId=idcardaudit_id)
        with allure.step("step2:前置条件准备:生成可预支名单"):
            # 创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            # 创建第一条可预支名单
            namelist_id = namelistsettle.add_namelist_settle(idcardnum, realname, nowtime)
            while True:
                time.sleep(5)
                settle_sql = f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res = self.db.selectsql(settle_sql)
                if res != ():
                    break
            # 创建第二条可预支名单
            beforedate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            namelist_id1 = namelistsettle.add_namelist_settle(idcardnum, realname, beforedate)
            while True:
                time.sleep(5)
                settle_sql = f'select * from name_list_settle where name_list_id={namelist_id1} and ec_id={ec_id}'
                res = self.db.selectsql(settle_sql)
                if res != ():
                    break

        with allure.step("step3:审核通过工牌"):
            #生成随机工牌
            workCardnum='workcard'+str(random.randint(1,100000))
            #获取可预支名单的ent_id
            settle_ent_sql=f'select ent_id from name_list_settle where name_list_id={namelist_id1} and ec_id={ec_id}'
            settle_entres=self.db.selectsql(settle_ent_sql)
            namelist_ent_id=settle_entres[0][0]
            #审核通过工牌
            res=upthreecard.weblogin.create_api(AuditWorkCard_Api,
                                            UserWorkCardAuditId=workcardaudit_id,
                                            WorkCardNo=workCardnum,
                                            InterViewEntId=namelist_ent_id,
                                            SubmitEntId=namelist_ent_id,)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_workcard_audit表数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id,audit_sts,audit_by,audit_remark,audit_name from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and is_canceled=0 and ec_id={ec_id}"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]==workCardnum)
            pytest.assume(workcardauditres[0][1] == namelist_ent_id)
            pytest.assume(workcardauditres[0][2] == 2)
            #获取audit_by和audit_name
            tenant_user_sql=f"select guid,user_name from tenant_user where t_id={pq_tenant_id} and mobile={pq_boss_user} and is_enabled=1 and is_deleted=0"
            tenant_user_res=self.db.selectsql(tenant_user_sql)
            audit_by=tenant_user_res[0][0]
            audit_name=tenant_user_res[0][1]

            pytest.assume(workcardauditres[0][3] == audit_by)
            pytest.assume(workcardauditres[0][4] == '通过')
            pytest.assume(workcardauditres[0][5] == audit_name)

        with allure.step("预期结果:member_user_workcard表新增一条数据，数据正确"):
            workcard_sql=f"select user_work_card_audit_id,guid,uuid,work_card_no,ent_id from member_user_work_card where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(len(workcardres)==1)
            pytest.assume(workcardres[0][0]==workcardaudit_id)
            pytest.assume(workcardres[0][1] == upthreecard.minilogin.Guid)
            #获取uuid
            uuid_sql=f"select uuid from member_user where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            uuidres=self.db.selectsql(uuid_sql)
            uuid=uuidres[0][0]
            pytest.assume(workcardres[0][2]==uuid)
            pytest.assume(workcardres[0][3]==workCardnum)
            pytest.assume(workcardres[0][4] ==namelist_ent_id)

        with allure.step("预期结果:name_list_settle表只更新面试日期最新的可预支名单"):
            #验证面试日期最新的可预支名单的user_work_card_audit_id，work_card_no字段
            settle_workcard_sql=f"select user_work_card_audit_id,work_card_no from name_list_settle where name_list_id={namelist_id1} and is_valid=1 and is_deleted=0 and tenant_id={pq_tenant_id} and ec_id={ec_id}"
            settle_workcardres=self.db.selectsql(settle_workcard_sql)
            pytest.assume(settle_workcardres[0][0]==workcardaudit_id)
            pytest.assume(settle_workcardres[0][1]==workCardnum)
            # 验证面试日期非最新的可预支名单的user_work_card_audit_id，work_card_no字段
            settle_workcard_sql = f"select user_work_card_audit_id,work_card_no from name_list_settle where name_list_id={namelist_id} and is_valid=1 and is_deleted=0 and tenant_id={pq_tenant_id} and ec_id={ec_id}"
            settle_workcardres = self.db.selectsql(settle_workcard_sql)
            pytest.assume(settle_workcardres[0][0] == 0)
            pytest.assume(settle_workcardres[0][1] == '')


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('会员结算名单已作废，审核工牌页面的面试名单企业名、面试日期为空')
    @allure.severity('blocker')
    def test_workcardinfo_0021(self):
        """
                会员结算名单已作废，审核工牌页面的面试名单企业名、面试日期为空

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0021.__name__))
        with allure.step("step1:前置条件准备:会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:前置条件准备:审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成真实姓名
            realname = create_name()
            # 审核通过身份证
            res = upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                  IdCardNum=idcardnum,
                                                  RealName=realname,
                                                  UserIdcardAuditId=idcardaudit_id)
        with allure.step("step2:前置条件准备:生成可预支名单"):
            # 创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            # 创建可预支名单
            namelist_id = namelistsettle.add_namelist_settle(idcardnum, realname, nowtime)
            while True:
                time.sleep(5)
                settle_sql = f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res = self.db.selectsql(settle_sql)
                if res != ():
                    break

        with allure.step("step3:作废可预支名单"):
            #获取可预支名单的name_list_settle_id
            name_list_settle_id_sql=f"select name_list_settle_id from name_list_settle where name_list_id={namelist_id} and is_deleted=0"
            name_list_settle_idres=self.db.selectsql(name_list_settle_id_sql)
            name_list_settle_id=name_list_settle_idres[0][0]
            #作废可预支名单
            res = upthreecard.weblogin.create_api(ZXX_DeleteNameByIdList,
                                                  NameIdList=[name_list_settle_id],
                                                  IsValid=2)
            res_data=res.json()
            #接口调用成功
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == {})

        with allure.step("step4:工牌信息列表查询工牌"):
            res=upthreecard.weblogin.create_api(WorkCardInfoList_Api,
                                            SequenceUploadTime=2,
                                            RecordIndex=0,
                                            RecordSize=10,
                                            EntId=-9999,
                                            AuditSts=-9999,
                                            Mobile=upthreecard.mobile)
            res_data=res.json()
        with allure.step("预期结果:接口调用成功,接口返回工牌的IneterviewDate、InterViewEntId、InterViewEntShortNme、InterviewEntFullName字段为空"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data']['RecordList'][0]['IneterviewDate']=='')
            pytest.assume(res_data['Data']['RecordList'][0]['InterViewEntId'] == 0)
            pytest.assume(res_data['Data']['RecordList'][0]['InterViewEntShortNme'] == '')
            pytest.assume(res_data['Data']['RecordList'][0]['InterviewEntFullName'] == '')


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('审核不通过会员上传的工牌，检查member_user_workcard_audit表数据')
    @allure.severity('blocker')
    def test_workcardinfo_0022(self):
        """
                审核不通过会员上传的工牌，检查member_user_workcard_audit表数据

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0022.__name__))
        with allure.step("step1:前置条件准备,会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            #上传工牌
            workcardaudit_id=upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:审核通过身份证"):
            upthreecard.idcard_auditpass(idcardaudit_id)

        with allure.step("step3:审核不通过工牌"):
            # 审核不通过工牌
            res = upthreecard.weblogin.create_api(ZXX_GetNextWorkCardPic_Api,
                                                  UserWorkCardAuditId=workcardaudit_id)
            res_data = res.json()

        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code']==0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_workcard_audit表数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id,audit_sts,audit_by,audit_remark,audit_name from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and is_canceled=0 and ec_id={ec_id}"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]=='')
            pytest.assume(workcardauditres[0][1] == upthreecard.appletfunc.entid)
            pytest.assume(workcardauditres[0][2] == 3)
            #获取audit_by和audit_name
            tenant_user_sql=f"select guid,user_name from tenant_user where t_id={pq_tenant_id} and mobile={pq_boss_user} and is_enabled=1 and is_deleted=0"
            tenant_user_res=self.db.selectsql(tenant_user_sql)
            audit_by=tenant_user_res[0][0]
            audit_name=tenant_user_res[0][1]

            pytest.assume(workcardauditres[0][3] == audit_by)
            pytest.assume(workcardauditres[0][4] == '看不清')
            pytest.assume(workcardauditres[0][5] == audit_name)

        with allure.step("预期结果:member_user_workcard表无新增数据"):
            workcard_sql=f"select user_work_card_audit_id,guid,uuid,work_card_no,ent_id from member_user_work_card where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(workcardres==())


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('会员已有审核通过的工牌，再次上传新的工牌，检查member_user_workcard_audit、member_user_workcard表数据')
    @allure.severity('blocker')
    def test_workcardinfo_0023(self):
        """
                       会员已有审核通过的工牌，再次上传新的工牌，检查member_user_workcard_audit、member_user_workcard表数据

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0023.__name__))
        with allure.step("step1:前置条件准备:会员上传身份证、上传工牌"):
            # 创建upload_threecard对象
            upthreecard = upload_threecard()
            # 上传身份证
            idcardaudit_id = upthreecard.upload_idcard(fakeridcardpicture)
            # 上传工牌
            workcardaudit_id = upthreecard.upload_workcard(workCardpicture)

        with allure.step("step2:前置条件准备:审核通过身份证"):
            # 生成身份证号码
            idcardnum = create_IDCard()
            # 生成真实姓名
            realname = create_name()
            # 审核通过身份证
            res = upthreecard.weblogin.create_api(AuditIDCard_Api,
                                                  IdCardNum=idcardnum,
                                                  RealName=realname,
                                                  UserIdcardAuditId=idcardaudit_id)
        with allure.step("step3:前置条件准备:生成可预支名单"):
            # 创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            # 创建可预支名单
            namelist_id = namelistsettle.add_namelist_settle(idcardnum, realname, nowtime)
            while True:
                time.sleep(5)
                settle_sql = f'select * from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
                res = self.db.selectsql(settle_sql)
                if res != ():
                    break

        with allure.step("step4:前置条件准备，审核通过第一次上传的工牌"):
            # 生成随机工牌
            workCardnum = 'workcard' + str(random.randint(1, 100000))
            # 获取可预支名单的ent_id
            settle_ent_sql = f'select ent_id from name_list_settle where name_list_id={namelist_id} and ec_id={ec_id}'
            settle_entres = self.db.selectsql(settle_ent_sql)
            namelist_ent_id = settle_entres[0][0]
            # 审核通过工牌
            res = upthreecard.weblogin.create_api(AuditWorkCard_Api,
                                                  UserWorkCardAuditId=workcardaudit_id,
                                                  WorkCardNo=workCardnum,
                                                  InterViewEntId=namelist_ent_id,
                                                  SubmitEntId=namelist_ent_id, )
            res_data = res.json()
        with allure.step("预期结果:接口调用成功，接口返回数据正确"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("step5:获取第一次上传的工牌的member_user_work_card_audit表、member_user_work_card表数据"):
            #获取第一次上传的工牌的member_user_work_card_audit表信息
            first_workcardaudit_sql=f"select * from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and is_canceled=0 and ec_id={ec_id}"
            first_workcardauditres=self.db.selectsql(first_workcardaudit_sql)
            first_workcardauditinfo=first_workcardauditres[0][0]
            # 获取第一次上传的工牌的member_user_work_card表信息
            first_workcard_sql = f"select * from member_user_work_card where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}"
            first_workcardres = self.db.selectsql(first_workcardaudit_sql)
            first_workcardinfo = first_workcardres[0][0]

        with allure.step("step5:再次上传工牌并审核通过工牌"):
            #上传工牌
            workcardaudit_id1 = upthreecard.upload_workcard(workCardpicture)
            # 生成随机工牌
            workCardnum1 = 'workcard' + str(random.randint(1, 100000))
            # 审核通过工牌
            res = upthreecard.weblogin.create_api(AuditWorkCard_Api,
                                                  UserWorkCardAuditId=workcardaudit_id1,
                                                  WorkCardNo=workCardnum1,
                                                  InterViewEntId=namelist_ent_id,
                                                  SubmitEntId=namelist_ent_id, )
            res_data=res.json()
            with allure.step("预期结果:接口调用成功，接口返回数据正确"):
                pytest.assume(res_data['Code'] == 0)
                pytest.assume(res_data['Desc'] == '成功')
                pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:第二次上传的工牌member_user_workcard_audit表数据更新正确"):
            workcardaudit_sql = f"select work_card_no,ent_id,audit_sts,audit_by,audit_remark,audit_name from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id1} and is_deleted=0 and is_canceled=0 and ec_id={ec_id}"
            workcardauditres = self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0] == workCardnum1)
            pytest.assume(workcardauditres[0][1] == namelist_ent_id)
            pytest.assume(workcardauditres[0][2] == 2)
            # 获取audit_by和audit_name
            tenant_user_sql = f"select guid,user_name from tenant_user where t_id={pq_tenant_id} and mobile={pq_boss_user} and is_enabled=1 and is_deleted=0"
            tenant_user_res = self.db.selectsql(tenant_user_sql)
            audit_by = tenant_user_res[0][0]
            audit_name = tenant_user_res[0][1]

            pytest.assume(workcardauditres[0][3] == audit_by)
            pytest.assume(workcardauditres[0][4] == '通过')
            pytest.assume(workcardauditres[0][5] == audit_name)

        with allure.step("预期结果:第二次上传的工牌member_user_workcard表新增一条数据，数据正确"):
            workcard_sql = f"select user_work_card_audit_id,guid,uuid,work_card_no,ent_id from member_user_work_card where user_work_card_audit_id={workcardaudit_id1} and is_deleted=0 and ec_id={ec_id}"
            workcardres = self.db.selectsql(workcard_sql)
            pytest.assume(len(workcardres) == 1)
            pytest.assume(workcardres[0][0] == workcardaudit_id1)
            pytest.assume(workcardres[0][1] == upthreecard.minilogin.Guid)
            # 获取uuid
            uuid_sql = f"select uuid from member_user where guid={upthreecard.minilogin.Guid} and is_deleted=0 and ec_id={ec_id}"
            uuidres = self.db.selectsql(uuid_sql)
            uuid = uuidres[0][0]
            pytest.assume(workcardres[0][2] == uuid)
            pytest.assume(workcardres[0][3] == workCardnum1)
            pytest.assume(workcardres[0][4] == namelist_ent_id)

        with allure.step("预期结果:再次查询第一次上传的工牌的member_user_work_card_audit表、member_user_work_card表数据,并校验数据不变"):
            #获取第一次上传的工牌的member_user_work_card_audit表信息
            after_workcardaudit_sql=f"select * from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and is_canceled=0 and ec_id={ec_id}"
            after_workcardauditres=self.db.selectsql(after_workcardaudit_sql)
            after_workcardauditinfo=after_workcardauditres[0][0]
            # 获取第一次上传的工牌的member_user_work_card表信息
            after_workcard_sql = f"select * from member_user_work_card where user_work_card_audit_id={workcardaudit_id} and is_deleted=0 and ec_id={ec_id}"
            after_workcardres = self.db.selectsql(after_workcardaudit_sql)
            after_workcardinfo = after_workcardres[0][0]

            #校验第一次上传的工牌的member_user_work_card_audit表、member_user_work_card表数据没有更新
            pytest.assume(first_workcardauditinfo==after_workcardauditinfo)
            pytest.assume(first_workcardinfo == after_workcardinfo)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('修改工牌号码在name_list_settle表存在的工牌，选择的标准企业与可预支名单中的标准企业不一致')
    @allure.severity('blocker')
    def test_workcardinfo_0024(self):
        """
                修改工牌号码在name_list_settle表存在的工牌，选择的标准企业与可预支名单中的标准企业不一致

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0024.__name__))
        with allure.step("step1:前置条件准备,生成审核通过并且有可预支名单的工牌"):
            res=self.test_workcardinfo_0019()
            namelist_id=res[0]
            namelist_ent_id=res[1]
            workCardnum=res[2]
            workcardaudit_id=res[3]

        with allure.step("step2:选择标准企业与可预支名单中标准企业不一致，修改工牌号码"):
            #登录
            self.weblogin.login(pq_boss_user)
            #随机生成工牌号码
            newworkCardnum = 'workcard' + str(random.randint(1, 100000))
            # 随机获取一个ent_id
            tenant_ent_sql = f'SELECT ent_id FROM tenant_ent where is_deleted=0 and ec_id={ec_id} and is_enabled=1 and ent_id<>{namelist_ent_id}'
            res = self.db.selectsql(tenant_ent_sql)
            ent_id = random.choice(res)[0]
            res=self.weblogin.create_api(ZXX_ModifyWorkCardNo_Api,
                                     WorkCardNo=newworkCardnum,
                                     EntId=ent_id,
                                     UserWorkCardAuditId=workcardaudit_id)

            res_data=res.json()

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_work_card_audit表工牌数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]==newworkCardnum)
            pytest.assume(workcardauditres[0][1] == ent_id)

        with allure.step("预期结果:member_user_work_card表工牌数据更新正确"):
            workcard_sql=f"select work_card_no,ent_id from member_user_work_card where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(workcardres[0][0]==newworkCardnum)
            pytest.assume(workcardres[0][1] == ent_id)

        with allure.step("预期结果:name_list_settle表工牌数据不更新"):
            settle_sql=f"select work_card_no,user_work_card_audit_id from name_list_settle where name_list_id={namelist_id} and is_deleted=0"
            settleres=self.db.selectsql(settle_sql)
            pytest.assume(settleres[0][0] == workCardnum)
            pytest.assume(settleres[0][1] == workcardaudit_id)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('修改工牌号码在name_list_settle表存在的工牌，选择的标准企业与可预支名单中的标准企业一致')
    @allure.severity('blocker')
    def test_workcardinfo_0025(self):
        """
                修改工牌号码在name_list_settle表存在的工牌，选择的标准企业与可预支名单中的标准企业一致

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0025.__name__))
        with allure.step("step1:前置条件准备,生成审核通过并且有可预支名单的工牌"):
            res=self.test_workcardinfo_0019()
            namelist_id=res[0]
            namelist_ent_id=res[1]
            workCardnum=res[2]
            workcardaudit_id=res[3]

        with allure.step("step2:选择标准企业与可预支名单中标准企业一致，修改工牌号码"):
            #登录
            self.weblogin.login(pq_boss_user)
            #随机生成工牌号码
            newworkCardnum = 'workcard' + str(random.randint(1, 100000))
            #选择标准企业与可预支名单中标准企业一致，修改工牌号码
            res=self.weblogin.create_api(ZXX_ModifyWorkCardNo_Api,
                                     WorkCardNo=newworkCardnum,
                                     EntId=namelist_ent_id,
                                     UserWorkCardAuditId=workcardaudit_id)

            res_data=res.json()

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_work_card_audit表工牌数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]==newworkCardnum)
            pytest.assume(workcardauditres[0][1] == namelist_ent_id)

        with allure.step("预期结果:member_user_work_card表工牌数据更新正确"):
            workcard_sql=f"select work_card_no,ent_id from member_user_work_card where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(workcardres[0][0]==newworkCardnum)
            pytest.assume(workcardres[0][1] == namelist_ent_id)

        with allure.step("预期结果:name_list_settle表工牌数据更新正确"):
            settle_sql=f"select work_card_no,user_work_card_audit_id from name_list_settle where name_list_id={namelist_id} and is_deleted=0"
            settleres=self.db.selectsql(settle_sql)
            pytest.assume(settleres[0][0] == newworkCardnum)
            pytest.assume(settleres[0][1] == workcardaudit_id)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('工牌在name_list_settle表存在多条可预支名单，修改该工牌的工牌号码')
    @allure.severity('blocker')
    def test_workcardinfo_0026(self):
        """
                工牌在name_list_settle表存在多条可预支名单，修改该工牌的工牌号码'

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0026.__name__))
        with allure.step("step1:前置条件准备,生成审核通过并且有可预支名单的工牌"):
            res=self.test_workcardinfo_0019()
            namelist_id=res[0]
            namelist_ent_id=res[1]
            workCardnum=res[2]
            workcardaudit_id=res[3]

        with allure.step("step2:前置条件准备,创建第二条可预支名单,并检查工牌字段"):
            # 创建Name_list_settle对象
            namelistsettle = Name_list_settle()
            #获取idcardnum,realname
            settle_sql=f"select id_card_num,real_name from name_list_settle where name_list_id={namelist_id} and is_deleted=0"
            res = self.db.selectsql(settle_sql)
            idcardnum=res[0][0]
            realname = res[0][1]
            # 创建第二条可预支名单
            beforedate = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
            namelist_id1 = namelistsettle.add_namelist_settle(idcardnum, realname, beforedate,ent_id=namelist_ent_id)
            while True:
                time.sleep(5)
                settle_sql = f'select * from name_list_settle where name_list_id={namelist_id1} and ec_id={ec_id}'
                res = self.db.selectsql(settle_sql)
                if res != ():
                    break
            #检查name_list_settle表的work_card_no,user_work_card_audit_id
            settle_sql = f"select work_card_no,user_work_card_audit_id from name_list_settle where name_list_id={namelist_id1} and is_deleted=0"
            res = self.db.selectsql(settle_sql)
            pytest.assume(res[0][0]==workCardnum)
            pytest.assume(res[0][1] == workcardaudit_id)
        with allure.step("step2:选择标准企业与可预支名单中标准企业一致，修改工牌号码"):
            #登录
            self.weblogin.login(pq_boss_user)
            #随机生成工牌号码
            newworkCardnum = 'workcard' + str(random.randint(1, 100000))
            #选择标准企业与可预支名单中标准企业一致，修改工牌号码
            res=self.weblogin.create_api(ZXX_ModifyWorkCardNo_Api,
                                     WorkCardNo=newworkCardnum,
                                     EntId=namelist_ent_id,
                                     UserWorkCardAuditId=workcardaudit_id)

            res_data=res.json()

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_work_card_audit表工牌数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]==newworkCardnum)
            pytest.assume(workcardauditres[0][1] == namelist_ent_id)

        with allure.step("预期结果:member_user_work_card表工牌数据更新正确"):
            workcard_sql=f"select work_card_no,ent_id from member_user_work_card where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(workcardres[0][0]==newworkCardnum)
            pytest.assume(workcardres[0][1] == namelist_ent_id)

        with allure.step("预期结果:name_list_settle表工牌数据更新正确"):
            #校验第一条可预支名单的work_card_no、user_work_card_audit_id字段
            first_settle_sql=f"select work_card_no,user_work_card_audit_id from name_list_settle where name_list_id={namelist_id} and is_deleted=0"
            first_settleres=self.db.selectsql(first_settle_sql)
            pytest.assume(first_settleres[0][0] == newworkCardnum)
            pytest.assume(first_settleres[0][1] == workcardaudit_id)
            # 校验第二条可预支名单的work_card_no、user_work_card_audit_id字段
            second_settle_sql = f"select work_card_no,user_work_card_audit_id from name_list_settle where name_list_id={namelist_id1} and is_deleted=0"
            second_settleres = self.db.selectsql(second_settle_sql)
            pytest.assume(second_settleres[0][0] == newworkCardnum)
            pytest.assume(second_settleres[0][1] == workcardaudit_id)


    @allure.feature('会员信息管理')
    @allure.story('工牌信息查询')
    @allure.title('工牌在name_list_settle表不存在可预支名单，修改该工牌的工牌号码')
    @allure.severity('blocker')
    def test_workcardinfo_0027(self):
        """
                工牌在name_list_settle表不存在可预支名单，修改该工牌的工牌号码

        """
        print('\n{}测试开始\n'.format(self.test_workcardinfo_0027.__name__))
        with allure.step("step1:前置条件准备,生成审核通过的工牌"):
            res=self.test_workcardinfo_0018()
            workCardnum=res[1]
            workcardaudit_id=res[0]

        with allure.step("step2:修改工牌号码"):
            #登录
            self.weblogin.login(pq_boss_user)
            #随机生成工牌号码
            newworkCardnum = 'workcard' + str(random.randint(1, 100000))
            # 随机获取一个ent_id
            tenant_ent_sql = f'SELECT ent_id FROM tenant_ent where is_deleted=0 and ec_id={ec_id} and is_enabled=1'
            res = self.db.selectsql(tenant_ent_sql)
            ent_id = random.choice(res)[0]
            #选择标准企业与可预支名单中标准企业一致，修改工牌号码
            res=self.weblogin.create_api(ZXX_ModifyWorkCardNo_Api,
                                     WorkCardNo=newworkCardnum,
                                     EntId=ent_id,
                                     UserWorkCardAuditId=workcardaudit_id)

            res_data=res.json()

        with allure.step("预期结果:接口调用成功"):
            pytest.assume(res_data['Code'] == 0)
            pytest.assume(res_data['Desc'] == '成功')
            pytest.assume(res_data['Data'] == None)

        with allure.step("预期结果:member_user_work_card_audit表工牌数据更新正确"):
            workcardaudit_sql=f"select work_card_no,ent_id from member_user_work_card_audit where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardauditres=self.db.selectsql(workcardaudit_sql)
            pytest.assume(workcardauditres[0][0]==newworkCardnum)
            pytest.assume(workcardauditres[0][1] == ent_id)

        with allure.step("预期结果:member_user_work_card表工牌数据更新正确"):
            workcard_sql=f"select work_card_no,ent_id from member_user_work_card where user_work_card_audit_id={workcardaudit_id} and is_deleted=0"
            workcardres=self.db.selectsql(workcard_sql)
            pytest.assume(workcardres[0][0]==newworkCardnum)
            pytest.assume(workcardres[0][1] == ent_id)














