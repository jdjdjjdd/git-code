# -*- coding: utf-8 -*-


import xlrd
from config.Config import Config
cf = Config()


class operationExcel():
    def __init__(self, file_path= cf.rootPath + "/test_data/",filename="*.xlsx", sheet_id=0):
        self.file = file_path + filename
        self.sheet_id = sheet_id
        self.data = self.get_data()

    def get_data(self):
        data = xlrd.open_workbook(self.file,on_demand=True)
        tables = data.sheets()[self.sheet_id]
        data.release_resources()
        return tables

    def get_rows(self):
        """获取单元格的排数"""
        return self.data.nrows

    def get_cell_value(self, x=0, y=0):
        """获取某个单元格的数据"""
        return self.data.cell_value(x, y)

    def get_x_values(self, case_id):
        """通过获取到的x坐标num值来获取到对应的内容"""
        x_num = self.get_x_nums(case_id)
        x_datas = self.get_x_data(x_num)
        return x_datas

    def get_x_nums(self, case_id):
        """根据传入的case_id的值来获取在表格x坐标的数值x=num"""
        num = 0
        x_datas = self.get_y_data()
        for x_data in x_datas:
            if case_id in x_data:
                return num
            num += 1

    def get_x_data(self, x=None):
        """获取表格某一行所有数据"""
        tables = self.data
        if x is not None:
            x_data = tables.row_values(x)
        else:
            x_data = tables.row_values(1)
        # print(x_data)
        return x_data

    def get_y_data(self, y=None):
        """获取表格某一列数据"""
        if y is not None:
            y_data = self.data.col_values(y)
        else:
            y_data = self.data.col_values(0)
        # print(y_data)
        return y_data


