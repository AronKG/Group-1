import unittest
import socket
import threading
from server import Server

class TestServer(unittest.TestCase):

    def test_server(self):
        self.server = Server("localhost", 3000)
        server_thread = threading.Thread(target=self.server.run)
        server_thread.daemon = True
        server_thread.start()
        
        test_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      #  fake_client.settimeout(1)
        test_client.connect(("localhost", 3000))
        msg = "test1"
        test_client.send(msg.encode('ascii'))
        rmsg = test_client.recv(4096).decode('ascii')
        self.assertEqual(msg,rmsg)
        test_client.send(b"quit")
        test_client.close()
        

        

if __name__ == '__main__':
    unittest.main()