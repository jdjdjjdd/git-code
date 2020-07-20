import pymysql

from config.Config import Config

cf = Config()

class OperateMDdb:
    def __init__(self):
        self.conn = pymysql.connect(
            host=cf.db_host,
            user=cf.db_user,
            password=cf.db_password,
            port=int(cf.db_port),
            db=cf.db_zt,
            charset=cf.db_charset,
        )
        self.cur = self.conn.cursor()

    def selectsql(self,sql):
        try:
            count = self.cur.execute(sql)
            res = self.cur.fetchall()
            print('查询sql：{0}\n'
                  '查询结果{1}\n'.format(sql, res))
            return res
        except Exception as e:
            print(e)

    def updatesql(self,sql):
        try:
            count =self.cur.execute(sql)
            print('更新sql：{0}\n'.format(sql))
            self.conn.commit()
        except  Exception as e:
            # 如果发生错误则回滚
            self.conn.rollback()
            print("更新失败")
            print(e)


    def close(self):
        self.cur.close()
        self.conn.close()





class OperateTMdb:
    def __init__(self):
        self.conn = pymysql.connect(
            host=cf.db_host,
            user=cf.db_user,
            password=cf.db_password,
            port=int(cf.db_port),
            db=cf.db_mb,
            charset=cf.db_charset,
        )

    def selectsql(self, sql):
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        res = self.cur.fetchall()
        print('查询sql：{0}\n'
              '查询结果{1}\n'.format(sql, res))
        return res

    def close(self):
        self.cur.close()
        self.conn.close()
