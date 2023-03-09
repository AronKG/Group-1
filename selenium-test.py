import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
import time
from server import app, socketio


class TestServer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Start a web driver instance
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument("--enable-javascript")
        cls.driver = webdriver.Chrome(options=options)

        # Start the server on a separate thread
        cls.server_thread = threading.Thread(target=socketio.run, args=(app,), kwargs={'debug': True, 'allow_unsafe_werkzeug'=True, 'use_reloader':False, 'host': '0.0.0.0', 'port': 5000})
        cls.server_thread.start()

        # Wait for the server to start up
        time.sleep(1)
        
    @classmethod
    def tearDownClass(cls):
        # Quit the web driver instance
        cls.driver.quit()

        # Stop the server
        socketio.stop()

        # Wait for the server thread to finish
        cls.server_thread.join()

    def test_login(self):
        # Navigate to the login page
        self.driver.get('http://localhost:5000/')
        
        # Find the username input element and send keys
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('testuser')

        # Find the login button element and click it
        login_button = self.driver.find_element(By.XPATH, "//input[@class='form-submit']")
        login_button.click()
        
        # Verify that the chat page is loaded
        #chat_input_placeholder = self.driver.find_element(By.XPATH,"//*[@id='message-input']1[contains(text(),'Enter your message')]")
        #self.assertEqual(chat_page_header.text, 'Chat')
        get_url = self.driver.current_url
        print("The current url is:"+str(get_url))
        self.assertIn("http://localhost:5000/chat", str(get_url))
        
    def test_send_message(self):
        # Navigate to the chat page
        
        

        # Enter a message
        message_input = self.driver.find_element(By.ID,'message-input')
        message_input.send_keys('Hello, world!')
        
        # Submit the message form
        message_input.send_keys(Keys.RETURN)
        time.sleep(1)
        
        # Verify that the message appears in the chat log
        chat_log = self.driver.find_element(By.CLASS_NAME,'message-sent')
        self.assertIn('Hello, world!', chat_log.text)


if __name__ == '__main__':
    unittest.main()
