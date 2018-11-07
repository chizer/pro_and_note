from socket import *
import re
import sys,os,time


def get_addr():
    if len(sys.argv)<3:
        print('argv Error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDRESS = (HOST,PORT)
    return ADDRESS

def main():

    s = socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    address = get_addr()
    try:
        s.connect(address)
    except Exception as e:
        print('Error',e)
        return
    while 1:
        word = input('查询单词：q退出')
        if word == 'q':
            s.send(b'q#')
            time.sleep(0.1)
            sys.exit('bye')
        s.send(word.encode())
        data = s.recv(512)
        print(data.decode())


if __name__ == '__main__':
    main()


