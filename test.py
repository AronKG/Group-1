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
        self.assertEqual(response.status, 400)
    
    # Testing that user can't login with empty passeword
    def tes_empty_password(self): 
        response = self.client.post('/login', data = {'username': 'testuser', 'passworde': ''})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()

