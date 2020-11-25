import pymysql


class Database(object):
    def __init__(self, host='localhost', user='root', password='000000', database=None, charset='utf8'):
        self.conn = pymysql.connect(host=host, user=user, password=password, database=database, charset=charset)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()