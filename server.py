import socket
from threading import Thread
from socket import error as SocketError
import errno
import sys

class Server:
    def __init__(self, host="localhost", port=3000):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.serversocket.bind((host,port))
        except SocketError as e:
            if e.errno == errno.EADDRINUSE:
                print(f"Address {host}:{port} already in use")
                self.serversocket.close()
                sys.exit(1)
        print("Listening on port " + str(port))

    def run(self):
        self.serversocket.listen(5)
        try:
            clientsocket, addr = self.serversocket.accept()
        except SocketError as e:
            if e.errno == errno.EINTR:
                print("The server socket was closed")
                self.serversocket.close()
                sys.exit(1)
        while True:
            try:
                rmsg = clientsocket.recv(4096).decode('ascii')
            except SocketError as e:
                if e.errno == errno.ECONNRESET:
                    print("The client socket was closed")
                    clientsocket.close()
                    sys.exit(1)
            print(f'server recived: {rmsg}')
            if rmsg == 'quit':
                self.serversocket.close()
                return
            else:
                try:
                    clientsocket.send(rmsg.encode('ascii'))
                except SocketError as e:
                    if e.errno == errno.EPIPE:
                        print("The client socket was closed")
                        clientsocket.close()
                        sys.exit(1)
