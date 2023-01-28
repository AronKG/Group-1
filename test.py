import unittest
import socket
from client import Client
from server import Server
from threading import Thread

class TestClientServer(unittest.TestCase):

    #In this example, the setUp method creates a new instance of the Server and starts its thread, and a new instance of the Client.
    def setUp(self):
        self.server = Server()
        self.server_thread = Thread(target=self.server.run)
        self.server_thread.start()
        self.client = Client()

    #The tearDown method closes the client's connection and joins the server thread.
    def tearDown(self):
        self.client.close_connection()
        self.server_thread.join()

    #The test_client_server_communication method sends two messages to the server and asserts that the server received both messages.
    def test_client_server_communication(self):
        self.client.send_message("Hello")
        self.client.send_message("World")
        self.assertEqual(self.server.received_message, "HelloWorld")

    #The test_client_close_connection method sends the "quit" message to the server and asserts that the server received it.
    def test_client_close_connection(self):
        self.client.close_connection()
        self.assertEqual(self.server.received_message, "quit")


print("inmplementing new featurs")

#tying to make a conflict between main and new-feature-implementation branch
print("a conflict that will be resolved")
print("This conflict is resolved")

if __name__ == '__main__':
    unittest.main()
