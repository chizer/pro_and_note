from socket import *
import sys
import os
import pymysql

IP = '0.0.0.0'
PORT = 9999
ADDR=(IP,PORT)
CONFIG = {
    'host':'localhost'
    ,'user':'root'
    ,'password':'123456'
    ,'database':'dict_pro'
    ,'charset':'utf8'
    ,'port':3306
}

#注册，根据用户名密码判断数据库是否存在，返回客户端
def do_register(conn,data,db):
    print('注册用户')
    _,name,passwd = data.decode().split(' ')
    cur = db.cursor()
    sql = "select * from user where name='%s'"%name
    cur.execute(sql)
    r = cur.fetchone()
    if r is not None:
        conn.send(b'EXISTS')
        return
    sql = "insert into user(name,passwd) values('%s','%s')"%(name,passwd)
    try:
        cur.execute(sql)
        db.commit()
        conn.send(b'OK')
    except:
        db.rollback()
        conn.send(b'FALL')
    print('%s注册成功'%name)

#登录，从数据库判读用户名密码是否正确
def do_login(conn,data,db):
    print('用户登录')
    _,name,passwd = data.decode().split(' ')
    cur = db.cursor()
    sql = "select * from user where name='%s' and passwd='%s'" % (name,passwd)
    cur.execute(sql)
    r = cur.fetchone()
    if r is None:
        conn.send(b'FALL')
        return
    else:
        conn.send(b'OK')
        print('%s登录成功'%name)

#根据用户名及单词　查询　有则记录查询并返回记录
def do_query(conn,data,db):
    print('查单词')
    _,name,word = data.decode().split(' ')
    cur = db.cursor()
    def insert_hist():  #闭包，用来准备进行插入记录到数据库
        import time
        ct = time.ctime()
        sql = "insert into hist(name,word,time) values('%s','%s','%s');"%(name,word,ct)
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()

    sql = "select word,interpret from words where word='%s';"%word
    cur.execute(sql)
    r = cur.fetchone()
    if r is None:
        conn.send(b'FALSE')
        return
    else:
        msg = '%s,%s'%r
        conn.send(msg.encode())
        insert_hist()   #如果查询成功　则执行插入历史记录的操作

#查询历史记录，根据用户名，
def do_hostory(conn,data,db):
    print('查历史记录')
    _,name = data.decode().split(' ')
    cur = db.cursor()
    sql = "select word,time from hist where name='%s' limit 10;"%name
    cur.execute(sql)
    l = cur.fetchall()
    if not l:
        conn.send(b'FALSE')
        return
    else:
        msg = ''
        for i in l:
            msg +='%s %s\n'%i
        conn.send(msg.encode())

#子进程主循环处理事件
def handler(conn):
    db = pymysql.connect(**CONFIG)#在各个客户端的连接进程中创建数据库连接对象
    while 1:
        data = conn.recv(1024)
        if (not data) or data.decode()[0] == 'E':
            conn.close()
            sys.exit()  # 退出子进程
        elif data.decode()[0] == 'R':
            do_register(conn,data,db)
        elif data.decode()[0] == 'L':
            do_login(conn,data,db)
        elif data.decode()[0] == 'Q':
            do_query(conn,data,db)
        elif data.decode()[0] == 'H':
            do_hostory(conn,data,db)

#主进程只负责循环接受客户端请求，有则交给子进程处理事务
def main():

    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    print('Waitting for connect..')
    while True:
        try:
            conn, addr = s.accept()
            print('come from ', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('Error', e)
            continue

        pid = os.fork()
        if pid<0:
            print('创建进程失败')
        elif pid == 0:
            ppid = os.fork()
            if ppid < 0:
                print('创建二级子进程失败')
            elif ppid == 0:
                s.close()
                handler(conn)
            else:
                os._exit(0)
        else:
            conn.close()
            os.wait()
            continue

if __name__ == '__main__':
    main()