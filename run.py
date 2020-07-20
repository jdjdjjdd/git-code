# -*- coding: utf-8 -*-

"""
运行用例集：
    python3 run.py

# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'

"""

from config import Config
import pytest,time
from report.compresse import zipDir
from common.base_utils.send_email import SendEmail
from common.base_utils.Log import MyLog
from common.base_utils import Consts, Shell

cf = Config.Config()


# conf = Config('sit').read_section()
log = MyLog()
log.info('初始化配置文件, path=' + cf.conf_path)

shell = Shell.Shell()
xml_report_path = cf.xml_report_path
html_report_path = cf.html_report_path

# 定义测试集
args = ['-s', '-q', '--alluredir', xml_report_path]
pytest.main(args)

cmd = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)

try:
    shell.invoke(cmd)
except Exception:
    log.error('执行用例失败，请检查环境配置')
    raise

time.sleep(10)
# 压缩测试报告
outfullname = cf.rootPath+'/report/zip_file/'+cf.zipname
zipDir(dirpath=cf.rootPath+'/report/html',outFullName=outfullname)

# 发送测试报告
pass_count = len(Consts.PASS_RESULT)
fail_count = len(Consts.FAIL_RESULT)

time.sleep(15)
sd = SendEmail()
sd.send_main(pass_count,fail_count,file_path=outfullname)



