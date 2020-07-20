# -*- coding: utf-8 -*-


class global_var:
    case_id = 0  # id
    case_name = 1 # 用例名称
    url = 2  # url
    run = 3  # 是否运行
    platform = 4 # 测试账号
    case_depend = 5  # case依赖
    response_data_depend = 6  # 依赖的返回数据
    data_depend_key = 7  # 数据依赖字段
    request_data = 8  # 请求数据
    expect_result = 9  # 预期结果
    expect_condition = 10 # 构造预期结果条件，生成动态预期结果的条件
    reality_result = 11  # 实际测试结果
    is_login=12 #无需登录


def get_case_id():
    return global_var.case_id

def get_case_name():
    return global_var.case_name

def get_url():
    return global_var.url

def get_run():
    return global_var.run

def get_platform():
    return global_var.platform

def get_case_depend():
    return global_var.case_depend

def get_response_data_depend():
    return global_var.response_data_depend

def get_data_depend_key():
    return global_var.data_depend_key

def get_request_data():
    return global_var.request_data

def get_expect_result():
    return global_var.expect_result

def get_expect_condition():
    return global_var.expect_condition

def get_reality_result():
    return global_var.reality_result

def get_islogin():
    return global_var.is_login