
import socket
from threading import Thread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 3000

print("Server.py")
serversocket.bind((host,port))

print("Listening on port " + str(port))

def run():    
    serversocket.listen(5)
    clientsocket, addr = serversocket.accept()
    while True:
        rmsg = clientsocket.recv(4096).decode()
        print("client: ",rmsg)
        clientsocket.send(rmsg.encode('ascii'))
        if rmsg == 'quit':
            clientsocket.send(b"Server is closing your connection")
            break
        
     

t = Thread (target=run)
t.start()
