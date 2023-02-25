import unittest
import tempfile
from server import app

class TestChatApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home(self):
        # Test that the home page returns a 200 status code
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_chatpage(self):
        with self.client.session_transaction() as session:
            session['id'] = 'abc123'
            session['username'] = 'testuser'
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 200)
    
    #this will test that users can't login with an empty username
    def test_empty_username(self):
        response = self.client.post('/login',data={'username': '', 'password': 'password'})
        self.assertEqual(response.status_code, 404)
    
    # Testing that user can't login with empty passeword
    def tes_empty_password(self): 
        response = self.client.post('/login', data = {'username': 'testuser', 'passworde': ''})
        self.assertEqual(response.status_code, 404)
    
    #Testing that user can not log in with an invalid username
    def tet_invalid_username(self): 
        response = self.client.post('/login', data={'username': 'invalid', 'password': 'password'})
        self.assertEqual(response.status_code, 401)

    #Testing that the server works correctly 
    def test_server_start(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Chat App', response.data)
        self.assertIn(b'Username', response.data)
        self.assertEqual(app.config['SERVER_NAME'], 'localhost:500')

    #Testing that that a user can log in successfully by providing a username,
    def test_login_success(self):
        response = self.client.post('/login', data={'username': 'Nasim'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', session)
        self.assertEqual(session['username'], 'Nasim')


        
    #Testing that a user can't use invalied password
    #def test_invalid_password(self):
        #response = self.client.post('/login', data={'username': 'testuser', 'password': 'invalid'})
        #self.assertEqual(response.status_code, 401)
    
    #testing the maximam size of text a user can send. 
    #def test_maxsize_message(self): 
       # with self.client.session_transaction() as session: 
            #session['username'] = 'testuser'
        
        #max_message_length = 1000 
        #message = 'a' * max_message_length
        #response = self.client.post('/send_message', data={'message':message})
        #self.assertEqual(response.status_code,200)
    #chck that the message was added to the chat history
        #response = self.client.get('/message')
        #self.assertIn(message.encode(), response.data)

if __name__ == '__main__':
    unittest.main()








