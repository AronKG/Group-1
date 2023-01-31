import socket
import sys
from threading import Thread

print("Server.py")

class Server:
    def __init__(self, host, port):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((host, port))
        print("Listening on " + host + ":" + str(port))

    def run(self):
        self.serversocket.listen(5)
        clientsocket, addr = self.serversocket.accept()
        print("Accepted connection from " + str(addr))
        while True:
            rmsg = clientsocket.recv(4096).decode()
            print("client: ", rmsg)
            if rmsg == 'quit':
                clientsocket.send(b"Server is closing your connection")
                break
            else:
                clientsocket.send(rmsg.encode('ascii'))

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    server = Server(host, port)
    server.run()
