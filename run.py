import sys
from server import Server
from client import Client
import time
from threading import Thread


if __name__ == '__main__':
    server = Server()
    t = Thread(target=server.run)
    t.start()

    client = Client()
    while True:
        smsg = input("enter your data here: ")
        client.send_message(smsg)
        if(smsg == "quit"):
            client.close()
            break
        rmsg = client.get_response()
        assert(smsg == rmsg)