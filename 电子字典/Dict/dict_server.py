#coding=utf-8
from socket import *
import sys,os,pymysql,time
from threading import Thread


DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)
DBCONFIG = {
    'host':'localhost'
    ,'user':'root'
    ,'password':'123456'
    ,'port':3306
    ,'database':'dict'
}

#每个线程函数等待各自开辟的线程
def zombie():
    os.wait()




def main():
    db =pymysql.connect(**DBCONFIG)
    s=socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    print('waiting for connect..')
    while 1:
        try:
            conn,addr = s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            sys.exit('Bye')
        except Exception as e:
            print(e)
            continue
        #创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(conn,db)
        else:
            conn.close()
            t = Thread(target=zombie)
            t.setDaemon(True)
            t.start()
            continue

def do_child(conn,db):
    while 1:
        data = conn.recv(128).decode()
        print(conn.getpeername(),data)
        if (not data) or data[0] == 'E' :
            conn.close()
            sys.exit('bye')
        elif data[0] == "R":
            do_register(conn,db,data)
        elif data[0] == 'L':
            do_login(conn,db,data)
        elif data[0] == 'Q':
            do_query(conn,db,data)
        elif data[0] == 'H':
            do_history(conn,db,data)

def do_register(conn,db,data):
    _,name,passwd = data.split(' ')
    cur =db.cursor()
    sql = "select * from user where name='%s';"%name
    cur.execute(sql)
    r = cur.fetchone()

    if r is not None:
        conn.send(b'EXISTS')
        return
    else:
        sql = "insert into user(name,passwd) values('%s','%s');"%(name,passwd)
        try:
            cur.execute(sql)
            db.commit()
            conn.send(b'OK')
        except:
            db.rollback()
            db.close()
            conn.send(b'FALSE')

def do_login(conn,db,data):
    _,name,passwd = data.split(' ')
    cur = db.cursor()
    sql = "select name,passwd from user where name='%s' and passwd='%s'; " %(name,passwd)
    cur.execute(sql)
    r= cur.fetchone()
    if r :
        conn.send(b'OK')
        print('Comefrom %s:%s'%(conn.getpeername(),name))
    else:
        conn.send(b'FALSE')

def do_query(conn,db,data):
    _,name,word = data.split(' ')
    cur = db.cursor()
    def insert_history():
        tm = time.ctime()
        sql = "insert into hist(name,word,time) values('%s','%s','%s');"%(name,word,tm)
        try:
            cur.execute(sql)
            db.commit()
        except:
            db.rollback()
    try:
        f = open(DICT_TEXT)
    except:
        conn.send(b'FALSE')
        return
    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            conn.send(b'FALSE')
            f.close()
            return
        elif tmp == word:
            conn.send(line.encode())
            f.close()
            insert_history()
            return
    conn.send(b'FALSE')
    f.close()

def do_history(conn,db,data):
    _,name = data.split(' ')
    cur = db.cursor()
    sql = "select word,time from hist where name='%s'limit10;"%name
    cur.execute(sql)
    r = cur.fetchall()
    if r is None:
        conn.send(b'FALSE')
    else:
        msg=''
        for i in r:
            msg += '{} {}\n'.format(i[0],i[1])
        conn.send(msg.encode())
        #考虑 上面再for循环外合成消息，一次发送
        #如果在循环里面一条一条发送，考虑tcp粘包问题
        #思路：查到结果，先通知客户端准备接收
        #发送一条，等待0.1s，再继续发

if __name__ == '__main__':
    main()
