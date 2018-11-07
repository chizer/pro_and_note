import pymysql
import re

f= open('dict.txt')
db = pymysql.connect(host='localhost',user='root',password='123456',database='dict',port=3306)

cur =db.cursor()


for line in f:
    try:
        obj = re.match(r'([-a-zA-Z]+)\s+(.*)',line)
        word = obj.group(1)
        interpret = obj.group(2)
    except:
        continue
    sql = "insert into words(word,interpret) values('%s','%s')"%(word,interpret)
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
cur.close()
db.close()
f.close()
