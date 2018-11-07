from socket import *
import re
import sys
import os


def handle(conn):
    while 1:
        data = conn.recv(1024)
        if not data:
            conn.close()
            # os._exit(0)
            sys.exit(0)

        if data == b'q#':
            conn.close()
            # os._exit(0)
            sys.exit(0)
        word = data.decode()
        try:
            f = open('dict.txt')
            for line in f:
                line_list = re.findall(r'(\w+)\s(.+)', line)
                if line_list[0][0] == word:
                    msg = line
                    conn.send(msg.encode())
                    f.close()
                    break
            else:
                conn.send(b'Not Found')
                f.close()

        except Exception as e:
             print(e)
        finally:
             f.close()


def main():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 7777))
    s.listen(3)
    print('Waiting for connection..')
    while 1:
        try:
            conn, _ = s.accept()
            print('come from', conn.getpeername())
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print('Error', e)
            continue
        pid = os.fork()
        if pid < 0:
            print('Error')
            return
        elif pid == 0:
            ppid = os.fork()
            if ppid == 0:
                s.close()
                handle(conn)
            else:
                conn.close()
                os._exit(0)
        else:
            conn.close()
            os.wait()
            continue


if __name__ == '__main__':
    main()


