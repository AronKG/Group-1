import sys
import socket
from threading import Thread
print("client.py")

class Client:
    def __init__(self, host="localhost", port=3000):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((host,port))
    
    def send_message(self, message):
        self.clientsocket.send(message.encode('ascii'))
        print(f'client sent: {message}')

    def get_response(self):
        rmsg = self.clientsocket.recv(4096).decode('ascii')
        return rmsg


    def close(self):
        self.clientsocket.send("quit".encode('ascii'))
        self.clientsocket.close()
