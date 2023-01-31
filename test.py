import unittest
import threading
from server import Server
from client import Client



class Test(unittest.TestCase):
    def test_main(self):
        server = Server('localhost',3000)
       
        server_thread = threading.Thread(target=server.run)
        server_thread.daemon = True
        server_thread.start()

        client = Client('localhost',3000)

        smsg = "Test"
        client.send_message(smsg)
        rmsg = client.get_response()
        self.assertEqual(smsg,rmsg)
        client.close()
        

if __name__ == "__main__":
    unittest.main()
