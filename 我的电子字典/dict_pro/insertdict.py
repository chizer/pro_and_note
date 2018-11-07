import re
import pymysql

CONFIG = {
    'host':'localhost'
    ,'user':'root'
    ,'password':'123456'
    ,'database':'dict_pro'
    ,'charset':'utf8'
    ,'port':3306
}
db = pymysql.connect(**CONFIG)
cur = db.cursor()

patten=r'(\w+)\s+(.+)'  #按行匹配　每行匹配到首个单词　之后的都是解释
f= open('dict.txt')
for line in f:

    s = re.findall(patten,line) #s=[(words,interpret)]
    # words,interpret = s[0]  #注意此处的是变量，下面的数据库中的两个字段
    sql = 'insert into words(word,interpret) values(%s,%s)'
    try:
        cur.execute(sql,s[0])
        db.commit()
    except:
        db.rollback()
cur.close()
db.close()
f.close()

