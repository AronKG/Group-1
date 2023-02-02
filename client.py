import sys
import socket
from threading import Thread
print("client.py")

class Client:
    def __init__(self, host="localhost", port=3000):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clientsocket.connect((host, port))
        except socket.error as msg:
            print(f"Error while connecting to the server: {msg}")
            sys.exit()

    def send_message(self, message):
        try:
            self.clientsocket.send(message.encode('ascii'))
            print(f'client sent: {message}')
        except socket.error as msg:
            print(f"Error while sending message to the server: {msg}")
            sys.exit()

    def get_response(self):
        try:
            rmsg = self.clientsocket.recv(4096).decode('ascii')
            return rmsg
        except socket.error as msg:
            print(f"Error while receiving message from the server: {msg}")
            sys.exit()

    def close(self):
        try:
            self.clientsocket.send("quit".encode('ascii'))
            self.clientsocket.close()
        except socket.error as msg:
            print(f"Error while closing the connection: {msg}")
            sys.exit()