# -*- coding: utf-8 -*-


"""
封装Assert方法

"""
from common.base_utils import Consts, Log
import pytest


class Assertions:
    def __init__(self):
        self.log = Log.MyLog()

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert code == expected_code
            Consts.PASS_RESULT.append('pass')
            return True
        except:
            self.log.error("statusCode error, expected_code is %s, statusCode is %s " % (expected_code, code))
            Consts.FAIL_RESULT.append('fail')

            raise

    def assert_body(self, actual_result,expect_result):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            assert actual_result == expect_result
            Consts.PASS_RESULT.append('pass')
            return True

        except:
            self.log.error("actual_result != expect_result, expect_result is %s, actual_result is %s" % (expect_result, actual_result))
            Consts.FAIL_RESULT.append('fail')

            raise

    def assert_equal(self, actual_result,expect_result):
        """
        判断实际结果和预期结果是否相等，不相等打印日志
        :param actual_result:
        :param expect_result:
        :return:
        """
        try:
            pytest.assume(actual_result == expect_result)
            Consts.PASS_RESULT.append('pass')
            return True

        except BaseException :
            self.log.error("actual_result != expect_result, expect_result is %s, actual_result is %s" % (expect_result, actual_result))
            Consts.FAIL_RESULT.append('fail')

            raise
