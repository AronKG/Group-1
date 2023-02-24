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

    def test_chat_not_logged_in(self):
        # Test that the chat page redirects to the login page if not logged in
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/'))

    def test_login(self):
        # Test that a user can log in and is redirected to the chat page
        data = {'username': 'testuser'}
        response = self.client.post('/', data=data, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/chat'))

   

if __name__ == '__main__':
    unittest.main()

