import socket
from threading import Thread

print("Server.py")

class Server:
    def __init__(self, host="localhost", port=3000):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((host,port))
        print("Listening on port " + str(port))


    def run(self):
        self.serversocket.listen(5)
        clientsocket, addr = self.serversocket.accept()
        while True:
            rmsg = clientsocket.recv(4096).decode('ascii')
            print(f'server recived: {rmsg}')
            if rmsg == 'quit':
                self.serversocket.close()
                return
            else:
                clientsocket.send(rmsg.encode('ascii')) 
