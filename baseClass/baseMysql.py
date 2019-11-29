import pymysql


class MysqlConn(object):
    def __init__(self, host, user, password, database, charset):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)
        self.cursor = self.conn.cursor()

    def select(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add(self, sql):
        self.cursor.execute(sql)
        self.cursor.commit()
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
