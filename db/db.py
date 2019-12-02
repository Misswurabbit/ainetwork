# encoding: utf-8

import sys
sys.path.append('../')
import config as config
import pymysql
import MySQLdb as db
import MySQLdb.cursors as cursors

DBNAME = config.db_name
DBHOST = config.db_host
DBUSER = config.db_user
DBPWD = config.db_pwd


class database:

    def __init__(self,dict=False):
        self.conn = db.connect(DBHOST, DBUSER, DBPWD, DBNAME, charset='utf8mb4')
        self.cur = self.conn.cursor(cursors.DictCursor if dict is True else None)
        self.errormsg = ''

    def cur(self):
        return self.cur()

    def fetch_all(self, sql):
        res = ''
        if self.conn:
            try:
                self.cur.execute(sql)
                res = self.cur.fetchall()
            except Exception:
                res = False
        return res

    def commit(self):
        self.conn.commit()

    def save(self, sql):
        flag = False
        if self.conn:
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                # print("error sql:" + sql)
                self.errormsg = str(e)
                flag = False
            else:
                flag = True
        return flag

    def get_last_id(self):
        if self.cur.lastrowid:
            self.conn.commit()
            return int(self.cur.lastrowid)  # 最后插入行的主键ID
        else:
            return None

    def __del__(self):  # 析构函数
        self.cur.close()
        self.conn.close();  # 关闭数据库连接
