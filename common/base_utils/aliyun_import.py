import oss2

from common.venv.api_path_zt import *


class AlImport():
    def __init__(self,login=None):
        # 初始化静态属性，属性值为登录的类
        self.login = login

    def ali_import(self,myObjectName,myLocalFile,region = 'http://oss-cn-shanghai.aliyuncs.com',bucketname= 'woda-app-private-test'):
        # 调用接口
        res = self.login.create_api(url=ALI_GetAliSTS).json()
        # 定义变量
        AccessKeyId = res['Data']['AccessKeyId']
        AccessKeySecret = res['Data']['AccessKeySecret']
        SecurityToken = res['Data']['SecurityToken']
        # 上传excel到阿里云
        auth = oss2.StsAuth(AccessKeyId, AccessKeySecret, SecurityToken)
        bucket = oss2.Bucket(auth, region, bucketname)
        bucket.put_object_from_file(myObjectName, myLocalFile)
