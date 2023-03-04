import unittest
import tempfile

from server import app, profanity, socketio, users, messages


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
    
    #Testing that user can not log in with an invalid username
    def tet_invalid_username(self): 
        response = self.client.post('/login', data={'username': 'invalid', 'password': 'password'})
        self.assertEqual(response.status_code, 401)

      

    #Testing that a user can log in successfully by providing a username,
    def test_login_success(self):
        with self.client as c:
            with c.session_transaction() as session:
                session['id'] = '1234'
            resp = c.post('/chat', data={'username': 'testuser'})
            self.assertIn(b'testuser', resp.data)
     
    def test_rate_limit(self):
        self.client.post('/login', data=dict(username='valid_user'))
        for i in range(11):
            response = self.client.post('/send_message', data=dict(message='Message {}'.format(i)))
        self.assertEqual(response.status_code, 404)
    
    # error handling
    def test_error_handling(self): 
        response = self.client.post('/invalid_endpoint')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'404', response.data) 



if __name__ == '__main__':
    unittest.main()








