import unittest
import socket
import threading
from client import Client

class TestClient(unittest.TestCase):
    def run_fake_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost",3000))
        server.listen(5)
        clientsocket, addr = server.accept()
        rmsg = clientsocket.recv(4096)
        clientsocket.send(rmsg)
        server.close()

    def test_client(self):
        server_thread = threading.Thread(target=self.run_fake_server)
        server_thread.start()
        
        client = Client("localhost",3000)
        smsg = "test"
        client.send_message(smsg)
        rmsg = client.get_response()
        self.assertEqual(smsg,rmsg)
        client.close()
        server_thread.join()
        

        
if __name__ == "__main__":
    unittest.main()