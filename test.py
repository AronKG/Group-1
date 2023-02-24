import unittest
import tempfile
from server import app

import unittest
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

    def test_send_message(self):
        # Test that a logged in user can send a message
        data = {'message': 'test message'}
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'
            response = c.post('/chat', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Check that the message was received by the server
            response = c.get('/messages')
            messages = response.get_json()
            self.assertTrue(any(m['message'] == 'test message' for m in messages))

    def test_get_users(self):
        # Test that a logged in user can get the list of all currently chatting users
        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'
            response = c.get('/users')
            self.assertEqual(response.status_code, 200)
            users = response.get_json()
            self.assertIn('testuser', users)

if __name__ == '__main__':
    unittest.main()

