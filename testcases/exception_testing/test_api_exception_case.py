# -*- coding: utf-8 -*-

# 获取根路径
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("autotest")+len("autotest")]
# 将根目录加入path
import sys,pytest
sys.path.append(rootPath)

from common.base_utils.compare_results import CompareResults
from common.base_utils.get_testfile import getTestFile,collect_data
from common.base_utils.Request import SendRequest
from common.base_utils.Assert import Assertions
from common.base_utils.Directsendreq import SendRequests
import warnings
warnings.filterwarnings('ignore')


class Test(object):

    def setup_class(self):
        self.compare_results = CompareResults()
        self.test_files = getTestFile()
        self.sd = SendRequest()
        self.test = Assertions()
        self.sendreq = SendRequests()

    @pytest.mark.parametrize('data',collect_data())
    def test_01(self,data):
        case_id = data[0] # 用例编号
        case_name = data[1] # 用例名称
        url = data[2]  # 接口地址
        platform = data[3]
        is_run = data[4]  # 用例是否运行
        req_data = data[5] # 请求参数
        expect_result = data[6]
        is_login = data[7]
        if is_run:
            if is_login:
                # 发起请求
                res = self.sendreq.excelsendReq(url, req_data)

                # 实际结果
                actual_result = res.json()
                # 比较测试结果，并打印测试因袭
                assert self.test.assert_body(actual_result, expect_result)
            else:
                # 发起请求
                res = self.sd.send_request(url=url, platform=platform, data=req_data)

                # 实际结果
                actual_result = res.json()
                # 比较测试结果，并打印测试因袭
                assert self.test.assert_body(actual_result, expect_result)

