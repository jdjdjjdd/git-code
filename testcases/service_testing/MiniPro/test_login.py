# 获取根路径
import os, sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest") + len("autotest")]
# 将根目录加入path
sys.path.append(rootPath)

from common.base_utils.Directsendreq import *
from common.login.login_basic import *
from common.base_utils.comm_utils import *
from common.data_operation.mysql_db import OperateMDdb
from common.venv.var import *
import pytest, allure
from common.venv.api_path_mb import *


class TestLoin():

    def setup_class(self):
        self.directsq = SendRequests()
        self.db = OperateMDdb()

    def setup_method(self):
        # 定义每个用例变量
        self.name = create_name()
        self.idnum = create_IDCard()
        self.mobile = create_phone()

    @allure.feature('小程序登录')
    @allure.story('登录')
    @allure.title('输入正确的手机号码，获取验证码')
    @allure.severity('blocker')
    def test_minilogin_0001(self):
        """
                输入正确的手机号码，获取验证码

        """
        print('\n{}测试开始\n'.format(self.test_minilogin_0001.__name__))
        with allure.step('step1:输入正确的手机号码，发送请求'):
            reqdata = databuild(SPhone=self.mobile)
            res = self.directsq.sendRequests(get_vcode_api, reqdata)

        with allure.step('step2:校验接口返回的结果'):
            # 断言
            pytest.assume(res.status_code == 200)
            response = res.json()
            pytest.assume(response['Code'] == 0)
            pytest.assume(response['Desc'] == '成功')
            pytest.assume(response['Data'] != '')

    @allure.feature('小程序登录')
    @allure.story('登录')
    @allure.title('输入正确的验证码和手机号码,tenant_type为2登录')
    @allure.severity('blocker')
    def test_minilogin_0002(self):
        """
                        输入正确的验证码和手机号码,tenant_type为2登录

        """
        print('\n{}测试开始\n'.format(self.test_minilogin_0002.__name__))
        with allure.step('step1:获取验证码'):
            # 创建系统不存在的手机号码
            while True:
                # 生成手机号码
                mobile = create_phone()
                # 校验手机号码是否存在
                mobilesql = f"select guid from center_user where login_name={mobile}"
                res = self.db.selectsql(mobilesql)
                if res == ():
                    break

            reqdata = databuild(SPhone=mobile)
            res = self.directsq.sendRequests(get_vcode_api, reqdata)
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            code = res.json()['Data']
        with allure.step('step2:输入正确的手机号码和验证码登录'):
            reqdata = databuild(mobile=mobile, vcode=code, tenant_type=2)
            res = self.directsq.sendRequests(applet_Login_api, reqdata)

        with allure.step('step3:校验接口返回的数据'):
            pytest.assume(res.status_code == 200)
            response = res.json()
            pytest.assume(response['Code'] == 0)
            pytest.assume(response['Desc'] == '成功')
            # 获取guid
            mobilesql = f"select guid from center_user where login_name={mobile}"
            res = self.db.selectsql(mobilesql)
            guid = res[0][0]
            # 拼接client_id和zt_client_id
            client_id = pq_tenant_id + '-' + str(guid)
            zt_client_id = pq_tenant_id + '-' + str(guid)
            # 校验client_id和zt_client_id
            pytest.assume(response['Data']['client_id'] == client_id)
            pytest.assume(response['Data']['zt_client_id'] == zt_client_id)
            # 校验user_id
            user_id = response['Data']['user_id']
            pytest.assume(response['Data']['user_id'] == guid)
            # 校验uuid
            pytest.assume(response['Data']['uuid'] == 0)
            # 校验手机号码
            pytest.assume(response['Data']['mobile'] == mobile)
            # 校验member_user表是否新增数据
            member_user_sql = f'select mobile from member_user where guid={user_id}'
            res = self.db.selectsql(member_user_sql)
            db_mobile = res[0][0]
            pytest.assume(db_mobile == mobile)

    @allure.feature('小程序登录')
    @allure.story('登录')
    @allure.title('输入正确的验证码和手机号码,tenant_type为1登录')
    @allure.severity('blocker')
    def test_minilogin_0003(self):
        """
                        输入正确的验证码和手机号码,tenant_type为1登录

        """
        print('\n{}测试开始\n'.format(self.test_minilogin_0003.__name__))
        with allure.step('step1:获取验证码'):
            # 获取身份证已审核通过的手机号码
            mobilesql = f"select mobile,uuid,guid from member_user where uuid <> 0 order by user_id desc limit 1"
            res = self.db.selectsql(mobilesql)
            mobile=res[0][0]
            uuid=res[0][1]
            guid=res[0][2]
            #获取验证码
            reqdata = databuild(SPhone=mobile)
            res = self.directsq.sendRequests(get_vcode_api, reqdata)
            pytest.assume(res.json()['Code'] == 0)
            pytest.assume(res.json()['Desc'] == '成功')
            code = res.json()['Data']
        with allure.step('step2:输入正确的手机号码和验证码登录'):
            #登录
            reqdata = databuild(mobile=mobile, vcode=code, tenant_type=1)
            res = self.directsq.sendRequests(applet_Login_api, reqdata)
            pytest.assume(res.status_code == 200)
            response = res.json()
            pytest.assume(response['Code'] == 0)
            pytest.assume(response['Desc'] == '成功')
        with allure.step('step2:校验接口返回的数据'):
            # 拼接client_id和zt_client_id
            client_id = zp_tenant_id + '-' + str(guid)
            zt_client_id = zp_tenant_id + '-' + str(guid)
            # 校验client_id和zt_client_id
            pytest.assume(response['Data']['client_id'] == client_id)
            pytest.assume(response['Data']['zt_client_id'] == zt_client_id)
            # 校验user_id
            user_id = response['Data']['user_id']
            pytest.assume(response['Data']['user_id'] == guid)
            # 校验uuid
            pytest.assume(response['Data']['uuid'] == uuid)