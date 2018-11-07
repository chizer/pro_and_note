import sys
from socket import *
import getpass

#从命令行获取远程服务器地址
def get_addr():
    if len(sys.argv)<3:
        print('argv Error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDRESS = (HOST,PORT)
    return ADDRESS

#注册功能，无论注册失败成功，都会到一级主循环界面，此处循环只用于判断输入格式
def do_register(s):
    while 1:
        name = input('name:')
        if not name:
            continue
        passwd = getpass.getpass('passwd:')
        if not passwd:
            continue
        if ' ' in name or ' ' in passwd:
            print('用户名密码不能出现空格')
            continue
        passwd1 = getpass.getpass('again:')
        if passwd != passwd1:
            print('确认错误，请重新填写')
            continue
        msg = 'R {} {}'.format(name,passwd)
        s.send(msg.encode())
        data = s.recv(1024)
        if data == b'EXISTS':
            return 0
        elif data == b'OK':
            return 1
        elif data == b'FALL':
            return 2

#登录功能．登录一次，失败或者成功回到一级界面，一级主循环根据返回值
#及登录成功与否 决定是否进入二级界面
def do_login(s):
    name = input('name:')
    passwd = getpass.getpass('passwd:')
    msg = 'L {} {}'.format(name,passwd)
    s.send(msg.encode())
    data = s.recv(128)
    if data == b'OK':
        return name
    else:
        return 0

#循环查询，如果不再继续查询回到二级选择界面
def do_query(name,s):
    while True:
        words = input('要查询单词##退出：')
        if words == '##':
            return
        msg = 'Q {} {}'.format(name,words)
        s.send(msg.encode())
        data = s.recv(1024)
        if data == b'FALSE':
            print('NOT FOUND')
        else:
            print(data.decode())

#查询历史记录一次，完毕之后回到二级选择界面
def do_hist(name,s):
    msg = 'H %s'%name
    s.send(msg.encode())
    data = s.recv(1024)
    if data == b'FALSE':
        print('没有历史记录')
    else:
        print(data.decode())

#二级界面，循环处理登录成功之后事件
def login_in(name,s):
    print('welcom %s'%name)
    while True:
        print('''
                     ===========Welcome================
                     -- 1.查单词   2.历史记录    3.注销--
                     ==================================
                    ''')
        cmd = input('输入选项>>')
        if cmd in ('1', '2', '3'):
            if cmd == '1':
                do_query(name,s)
                continue
            elif cmd == '2':
                do_hist(name,s)
                continue
            elif cmd == '3':
                return
        else:
            print('输入有误')
            continue

#主循环，登录服务器，进入主循环界面，考虑没有网络无法登录的情况，是否应该进入在选择登录？
def connect_server(address):
    s = socket(AF_INET,SOCK_STREAM)
    try:
        s.connect(address)
    except Exception as e:
        print(e)
        return
    while True:
        print('''
                   ===========Welcome==========
                   -- 1.注册   2.登录    3.退出--
                   ============================
                   ''')
        cmd = input('输入选项>>')
        if cmd in ('1','2','3'):
            if cmd == '1':
                r = do_register(s)
                if r == 0:
                    print('用户名已经存在，请重新输入')
                elif r == 1:
                    print('注册成功')
                elif r == 2:
                    print('注册失败')
            elif cmd == '2':
                name = do_login(s)
                if name:
                    print('登录成功')
                    login_in(name,s)    #返回姓名，说明登录成功，则进入登录二级界面
                    continue
                else:
                    print('登录失败')
                    continue
            elif cmd =='3':
                s.send(b'E')
                sys.exit('Bye')
        else:
            print('请输入正确选项')
            continue

#主函数负责调用接受服务器地址，之后调用主循环函数
def main():
    address = get_addr()
    print(address)
    connect_server(address)

if __name__ == '__main__':
    main()