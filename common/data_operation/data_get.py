# -*- coding: utf-8 -*-

import warnings

from common.base_utils.op_excel import operationExcel
from common.base_utils.op_json import operationJson
from common.data_operation import data_conf
from common.data_operation.mysql_db import OperateMDdb
from common.base_utils.comm_param import *
from config import Config

warnings.filterwarnings("ignore")
cf = Config.Config()


class getData(object):
    def __init__(self,test_file):
        self.op_excel = operationExcel(filename=test_file)
        self.selectdb = OperateMDdb()

    def get_case_lines(self):
        """获取表格行数"""
        return self.op_excel.get_rows()

    def get_case_id(self,x):
        """获取用例编号"""
        y = data_conf.get_case_id()
        case_id = self.op_excel.get_cell_value(x,y)
        return case_id

    def get_case_name(self,x):
        """获取用例名称"""
        y = data_conf.get_case_name()
        case_name = self.op_excel.get_cell_value(x,y)
        return case_name

    def get_request_url(self, x):
        """获取请求地址"""
        y = data_conf.get_url()
        url = self.op_excel.get_cell_value(x, y)
        request_url = cf.host + url
        return request_url

    def get_is_run(self, x):
        """获取case是否运行"""
        y = data_conf.get_run()
        run_value = self.op_excel.get_cell_value(x, y)
        if run_value == 'yes':
            flag = True
        else:
            flag = False
        return flag

    def get_platform(self,x):
        y = data_conf.get_platform()
        platform = self.op_excel.get_cell_value(x,y)
        if platform == '':
            return None
        else:
            return platform

    def get_case_dependent(self, x):
        """获取case依赖的值"""
        y = int(data_conf.get_case_depend())
        case_dependent = self.op_excel.get_cell_value(x, y)
        if case_dependent == '':
            return None
        else:
            return case_dependent

    def get_data_dependent(self,x):
        """获取数据依赖"""
        y= data_conf.get_response_data_depend()
        data_dependent = self.op_excel.get_cell_value(x,y)
        if data_dependent == '':
            return None
        else:
            return data_dependent

    def get_data_depend_key(self,x):
        """获取依赖关键字"""
        y = data_conf.get_data_depend_key()
        data_depend_key = self.op_excel.get_cell_value(x,y)
        if data_depend_key == '':
            return None
        else:
            return data_depend_key

    def get_request_data(self, x):
        """获取请求数据"""
        y = data_conf.get_request_data()
        request_data = self.op_excel.get_cell_value(x, y)
        if request_data == '':
            return None
        return request_data

    def get_data_for_json(self, x):
        """通过excel中的关键字去获取json数据"""
        op_json = operationJson()
        url = self.get_request_url(x)
        api_name = url.split("/")[-2]+'/'+url.split("/")[-1]
        data = op_json.get_key_words(api_name)
        return data

    def create_request_data(self,x):
        """根据实际传参构造data"""
        # 从json获取接口文档模板
        # json_data = self.get_data_for_json(x)
        # 从excel获取请求参数
        request_data = self.get_request_data(x)
        request_data = eval(request_data) # 将字符串转成字典

        # # 将excel的参数塞进接口文档模板中，去掉无值的参数，生成新的字典，用于发送请求
        # new_data = {}
        # for k,v in json_data.items():
        #     if k not in request_data:
        #         v = None
        #     else:
        #         v = request_data[k]
        #
        #         new_data[k]=v
        return request_data

    def get_expect_data(self, x):
        """获取预期结果数据"""
        y = data_conf.get_expect_result()
        expect_data = self.op_excel.get_cell_value(x, y)
        expect_condition = self.get_expect_condition(x)
        new_conditon = {}
        if expect_condition:
            for k, v in expect_condition.items():
                new_conditon[k] = self.selectdb.selectsql(v)[0][0]

        expect_data = eval(expect_data)
        for k,v in expect_data.items():
            keys = list(new_conditon.keys())
            for key in keys:
                if v == key:
                    expect_data[k]=new_conditon[key]
        if expect_data == '':
            return None
        return expect_data

    def get_expect_condition(self,x):
        """获取构造预期结果条件"""
        y = data_conf.get_expect_condition()
        expect_condition = self.op_excel.get_cell_value(x,y)
        if expect_condition:
            expect_condition = eval(expect_condition)
        return expect_condition

    def get_lis_login(self,x):
        y = data_conf.get_islogin()
        islogin = self.op_excel.get_cell_value(x, y)
        return islogin




