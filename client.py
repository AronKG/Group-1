import sys
import socket
from threading import Thread
print("client.py")

class Client:
    def __init__(self, host="localhost", port=3000):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((host,port))
    
    def send_message(self, message):
        self.clientsocket.send(message.encode())
        self.get_response()

    def get_response(self):
        print("Server: ", self.clientsocket.recv(4096).decode())

    def close_connection(self):
        self.send_message("quit")
