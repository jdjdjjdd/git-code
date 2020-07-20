# -*- coding: utf-8 -*-
from common.base_utils.comm_utils import get_api_result

class CompareResults(object):

    def __init__(self):
        self.total_case_num = 0
        self.pass_case_num = 0
        self.pass_case_ids = []
        self.fail_case_num = 0
        self.fail_case_ids = []
        self.skip_case_num = 0
        self.skip_case_ids = []




    def test_info(self,case_id,case_name,url,is_run,req_data,actual_result,expect):
        """统计用例执行情况"""
        # 打印用例信息
        print(f'测试用例编号：{case_id}')
        print(f'测试用例名称：{case_name}')
        print(f'接口地址：{url}')
        print(f'是否运行：{is_run}')

        # 计算用例总数
        self.total_case_num += 1
        if is_run:
            print(f'请求参数：{req_data}')
            print(f'预期结果：{expect}')
            print(f'实际结果：{actual_result}')
            flag = self.compareResult(actual_result,expect)
            print(f'测试结果：{flag}')
            if flag:
                # 计算pass的用例数
                self.pass_case_num += 1
            else:
                # 计算失败的用例数
                self.fail_case_num += 1
                # 将失败的用例id放入列表
                self.fail_case_ids.append(case_id)
        else:
            # 计算跳过的用例
            self.skip_case_num += 1
        print("*" * 60 + "分割线" + "*" * 60)

    def compareResult(self,reality, expect):
        """比较测试结果"""
        # 初始化flag为None
        flag = None
        # 获取预期结果的key列表
        ex_keys = list(expect.keys())
        # 从ex_kyes遍历取值去res中查找实际结果
        result = []
        print("-" * 30 + "结果比较" + "-" * 30)

        for ex_key in ex_keys:
            # 获取实际结果
            real_value = get_api_result(reality,ex_key)
            # 判断预期结果值是否为列表，如果是，且实际结果返回值是列表，将实际结果值从列表中取出
            if not isinstance(expect[ex_key],list) and isinstance(real_value,list):
                real_value = real_value[0]
            # 如果查询的实际结果和预期结果值相等，将flag置为true
            flag = real_value == expect[ex_key]

            print(f'    实际结果{ex_key}：{real_value}和预期结果{ex_key}:{expect[ex_key]}进行判断,结果为{flag}')

            result.append(flag)
        print("-" * 30 + "结果比较" + "-" * 30)
        if False not in result:
            return True
        else:
            return False
