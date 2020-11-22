import pymysql


conn = pymysql.connect(host='localhost', user='root', password='000000', database='recommend', charset='utf8')
cursor = conn.cursor()
sql = "insert into users values ('xiaoming', '123456')"

cursor.execute(sql)
conn.commit()
# a = cursor.fetchone()
# result = cursor.fetchall()
#
# print(a)
# print(result)  # ((1, 'xiaoming'), (2, 'zhangshan'))
cursor.close()
conn.close()
