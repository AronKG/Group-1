import sys
from server import Server
from client import Client
import time
from threading import Thread

server = Server()
t = Thread(target=server.run)
t.start()

client = Client()
client.send_message("Hello")
client.send_message("World")
client.close_connection()
time.sleep(2)
