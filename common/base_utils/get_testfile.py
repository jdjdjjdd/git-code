# -*- coding: utf-8 -*-

import os,re
from common.data_operation.data_get import getData
from config.Config import Config
cf = Config()

def getTestFile():
    path = cf.rootPath + '/test_data/'
    filenames = os.listdir(path=path)
    test_excel_list = []
    for filename in filenames:
        if re.findall(r'.xlsx$', filename) and (not re.findall(r'^~', filename)):
            test_excel_list.append(filename)
    return test_excel_list

def collect_data():
    lst = []
    excel_list = getTestFile()
    for i in range(len(excel_list)):
        data = getData(excel_list[i])
        row_counts = data.get_case_lines()  # 获取excel表格行数
        for row_count in range(1, row_counts):
            case_id = data.get_case_id(row_count)  # 用例编号
            case_name = data.get_case_name(row_count)  # 用例名称
            url = data.get_request_url(row_count)  # 接口地址
            platform = data.get_platform(row_count) # 登陆账号
            is_run = data.get_is_run(row_count)  # 用例是否运行
            req_data = data.create_request_data(row_count)  # 请求参数
            expect = data.get_expect_data(row_count) # 预期结果
            is_login=data.get_lis_login(row_count)#是否无需登录
            lst.append([case_id,case_name,url,platform,is_run,req_data,expect,is_login])
    return lst

if __name__=='__main__':
    res = collect_data()
    print('res',res)