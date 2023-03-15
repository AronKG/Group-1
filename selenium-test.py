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
        cls.server_thread = threading.Thread(target=socketio.run, daemon=True, args=(app,), kwargs={'debug': True, 'use_reloader':False, 'host': '0.0.0.0', 'port': 5000})
        cls.server_thread.start()

        # Wait for the server to start up
        time.sleep(1)
        
    @classmethod
    def tearDownClass(cls):
        # Quit the web driver instance
        cls.driver.quit()
        return
    
    def perform_login(self, username):
        self.driver.delete_all_cookies()
        # Navigate to the login page
        self.driver.get('http://localhost:5000/')
        
        # Find the username input element and send keys
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys(username)

        # Find the login button element and click it
        login_button = self.driver.find_element(By.XPATH, "//input[@class='form-submit']")
        login_button.click()
        
        # Verify that the chat page is loaded
        try:
            self.driver.find_element(By.CLASS_NAME, "chat-container")
        except:
            print(f"Couldn't login successfully with username '{username}'")
        else:
            print(f"Logged in successfully with username '{username}'")
        
    def test_login(self):
        self.perform_login('testuser')
        
    def test_empty_username(self): 
        # Attempt to log in with an empty username
        self.perform_login('')
        
        # Verify that the chat page is NOT loaded
        try:
            self.driver.find_element(By.CLASS_NAME, "chat-container")
        except:
            print("Couldn't log in with empty username (as expected)")
        else:
            raise Exception("Logged in successfully with empty username")
        
    def test_send_message(self):
        # Perform login
        self.perform_login('testuser')
        
        # Enter a message
        message_input = self.driver.find_element(By.ID,'message-input')
        message_input.send_keys('Hello, world!')
        
        # Submit the message form
        message_input.send_keys(Keys.RETURN)
        time.sleep(1)
        
        # Verify that the message appears on the webpage
        chat_log = self.driver.find_element(By.CLASS_NAME,'message-sent')
        self.assertIn('Hello, world!', chat_log.text)
        
    def test_send_messages_with_rate_limit(self):
        # Perform login
        self.perform_login('testuser')
        
        # Enter first message
        message_input = self.driver.find_element(By.ID,'message-input')
        message_input.send_keys('First message')
        
        # Submit the first message
        message_input.send_keys(Keys.RETURN)
        
        # Verify that the first message appears on the webpage
        chat_log = self.driver.find_element(By.CLASS_NAME,'message-sent')
        self.assertIn('First message', chat_log.text)
        
        # Enter second message
        message_input = self.driver.find_element(By.ID,'message-input')
        message_input.send_keys('Second message')
        
        # Submit the second message
        message_input.send_keys(Keys.RETURN)
        
        # Wait for the second message to become visible or timeout after 5 seconds
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='message-sent'][contains(text(),'Second message')]")))
        
        # Verify that the second message is NOT displayed on the webpage
        chat_logs = self.driver.find_elements(By.CLASS_NAME,'message-sent')
        self.assertNotIn('Second message', [log.text for log in chat_logs])

if __name__ == '__main__':
    unittest.main()
