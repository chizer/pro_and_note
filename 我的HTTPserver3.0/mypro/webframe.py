from socket import *
from threading import Thread
from settings import frame_address

class Webframe(object):
    def __init__(self, address):
        self.address = address
        self.creat_socket()
        self.bind(address)

    def creat_socket(self):
        self.sockfd = socket(AF_INET, SOCK_STREAM)
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self, address):
        self.ip, self.port = address
        self.sockfd.bind(address)

    def serve_forever(self):
        self.sockfd.listen(5)
        print('listen the port %d..' % self.port)
        while True:
            try:
                conn, addr = self.sockfd.accept()
                print('Connect from', addr)
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit('服务器退出')
            except Exception as e:
                print('Error', e)
                continue
            handle_client = Thread(target=self.handle, args=(conn,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle(self, conn):
        request = conn.recv(4096)
        if not request:
            conn.close()
            return



 def get_html(self,connfd,getRequest):
        if getRequest == '/':
            filename = self.static_dir + '/index.html'
        else:
            filename = self.static_dir + getRequest
        print(filename)
        try:
            f = open(filename)
        except Exception:
            #没找到网页
            responseHeaders = 'HTTP/1.1 404 Not found\r\n'
            responseHeaders += '\r\n'
            responseBody = 'Sorry,not found the page'

        else:
            #如果找到网页则返回
            responseHeaders = 'HTTP/1.1 200 OK\r\n'
            responseHeaders += '\r\n'
            responseBody = f.read()

        finally:
            response = responseHeaders + responseBody
            connfd.send(response.encode())

    #通过客户端发送的请求数据，给客户端返回响应
    def get_data(self,connfd,getResquest):
        urls = ['/time','/tedu','/python']

        if getResquest in urls:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += '\r\n'
            if getResquest == '/time':
                import time
                responseBody = time.ctime()
            elif getResquest == '/tedu':
                responseBody = '欢迎来到德莱联盟'
            elif    getResquest == '/python':
                responseBody = '这里是python学习交流中心'
        else:
            responseHeaders = 'HTTP/1.1 404 Not found\r\n'
            responseHeaders += '\r\n'
            responseBody = 'Not data,Bye!'
        response = responseHeaders + responseBody
        connfd.send(response.encode())