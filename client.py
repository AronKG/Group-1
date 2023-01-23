import sys
import socket
from threading import Thread
print("client.py")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"  #sys.argv[1]
port = 3000 #sys.argv[2]

s.connect((host,port))

while True: 
    send_msg = input("Write input value: ")
    s.send(send_msg.encode('ascii'))
    msg = s.recv(4096)
    print("server:",msg)
    if send_msg == "quit":
        break
    
s.close()
print(msg.decode())