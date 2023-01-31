import sys
import socket
from threading import Thread

print("client.py")

class Client:
    def __init__(self, host, port):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((host, port))

    def send_message(self, message):
        self.clientsocket.send(message.encode())
        self.get_response()

    def get_response(self):
        print("Server: ", self.clientsocket.recv(4096).decode())

    def close_connection(self):
        self.send_message("quit")
        self.clientsocket.close()

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    client = Client(host, port)
    while True:
        message = input("You: ")
        client.send_message(message)
        if message == 'quit':
            break
    client.close_connection()
