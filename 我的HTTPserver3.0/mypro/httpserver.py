#coding=utf-8
'''
httpserver3.0
'''

from socket import *
from threading import Thread
from settings import *
import sys,re

#和WebFrame通信
def connect_frame(env):
    s = socket(AF_INET,SOCK_STREAM)
    s.connect(frame_address)
    s.send(env)
    s.accept()      #连接框架服务器地址


class Http_Server(object):
    def __init__(self,address):
        self.address = address
        self.creat_socket()
        self.bind(address)

    def creat_socket(self):
        self.sockfd = socket(AF_INET,SOCK_STREAM)
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

    def bind(self,address):
        self.ip,self.port = address
        self.sockfd.bind(address)

    def serve_forever(self):
        self.sockfd.listen(5)
        print('listen the port %d..'%self.port)
        while True:
            try:
                conn,addr = self.sockfd.accept()
                print('Connect from',addr)
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务器退出')
            except Exception as e:
                print('Error',e)
                continue
            handle_client = Thread(target=self.handle,args=(conn,))
            handle_client.setDaemon(True)
            handle_client.start()
    def handle(self,conn):
        request =conn.recv(4096)
        if not request:
            conn.close()
            return
        #按行切割请求头　b格式
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode('utf-8')
        # print(request_line)
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            env = re.match(pattern=pattern,string=request_line).groupdict()
            print(env)
            # connect_frame(env=env)

        except :
            response_headers='HTTP/1.1 500 SERVER ERROR\r\n'
            response_headers += '\r\n'
            response_body = 'Server error'
            response = response_headers+response_body
            conn.send(response.encode())

        conn.close()




if __name__ == "__main__":
    httpfd= Http_Server(ADDR)
    httpfd.serve_forever()