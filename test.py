import unittest
import tempfile
from server import app, contains_spam

class FlaskTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_chat(self):
        with self.app as client:
            with client.session_transaction() as session:
                session['username'] = 'testuser'
            response = self.app.get('/chat')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'testuser' in response.data)

    def test_contains_spam(self):
        self.assertTrue(contains_spam('Fuck you'))
        self.assertFalse(contains_spam('Hello world!'))
    
    def test_empty_message(self): 
        with self.app as client:
            with client.session_transaction() as session:
                session['username'] = 'testuser'
            response = self.app.post('/send_message', data={'message': ''})
            self.assertEqual(response.status_code, 400)
            self.assertTrue(b'Message canot be empty' in response.data)
            

if __name__ == '__main__':
    unittest.main()
