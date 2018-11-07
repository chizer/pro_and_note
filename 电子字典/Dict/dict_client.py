#coding=utf-8

from socket import *
import sys,getpass

def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket(AF_INET,SOCK_STREAM)
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    while 1:
        print('''
        ==============welcome==============
        -- 1.注册     2.登录        3.退出--
        ===================================
        ''')
        cmd = input('输入')
        if cmd not in ('1','2','3'):
            print('输入有误')
            continue
        elif cmd == '1':
            do_register(s)
        elif cmd == '2':
            name = do_login(s)  #登录之后返回姓名则成功，否则失败回到登录注册界面
            if name:
                login(s,name)   #用户注销之后回到当前界面
            else:               #登录失败回到当前界面
                continue
        elif cmd == '3':
            s.send(b'E')
            sys.exit('Bye')

def do_register(s):
    while True:
        name = input('user:')
        if not name:
            continue
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('Again:')
        if (' ' in name) or (' ' in passwd):
            print('用户名或密码不能有空')
            continue
        if passwd != passwd1:
            print('两次密码不一致')
            continue
        msg = 'R %s %s'%(name,passwd)
        s.send(msg.encode())
        #等待接收
        data = s.recv(128)
        if data == b'OK':
            print('注册成功')
        elif data == b'EXISTS':
            print('该用户已存在')
        else:
            print('注册失败')
        return

def do_login(s):
    name = input('Name:')
    passwd = getpass.getpass('Passwd:')
    msg = 'L {0} {1}'.format(name,passwd)
    s.send(msg.encode())
    data = s.recv(128)
    if data == b'OK':
        print('Welcome %s'%name)
        return name
    else:
        print('登录失败')
        return 0

def login(s,name):
    while 1:
        print('''
           ==============welcome==============
           -- 1.查单词     2.历史记录   3.注销--
           ===================================
           ''')
        cmd = input('输入')
        if cmd not in ('1', '2', '3'):
            print('输入有误')
            continue
        elif cmd == '1':
            do_query(s,name)
        elif cmd == '2':
            do_history(s,name)
        elif cmd == '3':#退出当前界面，回到一级界面
            return

def do_query(s,name):
    while 1:
        word = input('单词：')
        if word == '##':
            return
        msg = 'Q {} {}'.format(name,word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'FALSE':
            print('没有该单词')
        else:
            print(data)

def  do_history(s,name):
    msg = 'H %s'%name
    s.send(msg.encode())
    data = s.recv(2048).decode()
    if data == "FALSE":
        print('没有历史记录')
        return
    else:
        print(data)
        return

if __name__ == '__main__':
    main()
