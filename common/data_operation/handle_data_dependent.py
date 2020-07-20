# -*- coding: utf-8 -*-
from common.base_utils.op_excel import operationExcel
from jsonpath_rw import parse
from common.data_operation.data_get import getData
import requests, json
from common.login import body


class HandleData(object):
    def __init__(self, dependent_case,login=None):
        if '.' in dependent_case:
            values = dependent_case.split('.')
            self.filename = values[0]
            self.case_id = values[1]
        else:
            self.case_id = dependent_case
        self.op_excel = operationExcel()
        self.data = getData()
        self.login = login

    def get_case_line_data(self):
        """获取case所在行数据"""
        x_datas = self.op_excel.get_x_values(self.case_id)
        return x_datas

    def run_dependent_case(self):
        """执行获取case所在的整行数据"""
        # run = RunMain()
        x = self.op_excel.get_x_nums(self.case_id)
        request_data = self.data.create_request_data(x)
        request_data = json.dumps(request_data,ensure_ascii=False)
        request_url = self.data.get_request_url(x)
        is_run = self.data.get_is_run(x)
        service = self.data.get_service_name(x)
        expect = self.data.get_expect_data(x)

        if '/fw/' not in request_url:
            req_body = body(request_data, guid=self.login.Guid, token=self.login.access_token, app_key='DJYWeb')
        else:
            req_body = body(request_data, app_id=self.login.zt_tid, guid=self.login.zt_guid, token=self.login.zt_token,
                            app_key='DJYWeb')

        if is_run:
            res = requests.post(url=request_url, json=req_body)
            return res.json()

    def get_data_for_key(self, x):
        """获取依赖返回数据中的key"""
        dependent_data = self.data.get_data_dependent(x)
        response_data = self.run_dependent_case()
        json_rule = parse(dependent_data)
        madle = json_rule.find(response_data)
        return [match.value for match in madle][0]



# login = Web_Login()
# login.login('13340000001')
# HandleData("case002",login).get_data_for_key(2)
