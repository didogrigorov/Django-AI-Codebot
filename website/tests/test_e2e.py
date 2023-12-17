from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class CustomTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testaccount', password='testadmin')
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(10)
        self.selenium.get(f"{self.live_server_url}")


class UserLoginTests(CustomTestCase):
    def test_user_authentication_valid(self):
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("testaccount")
        password_input = self.selenium.find_element(By.XPATH, "//input[@type='password']")
        password_input.send_keys("testadmin")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        self.selenium.implicitly_wait(5)

        text = 'You have been loggedin successfully!'
        self.assertTrue(text in self.selenium.page_source)

    def test_user_authentication_invalid(self):
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("testaccount")
        password_input = self.selenium.find_element(By.XPATH, "//input[@type='password']")
        password_input.send_keys("testadmin123")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        self.selenium.implicitly_wait(5)

        text = 'Invalid username or password. Please try again.'
        self.assertTrue(text in self.selenium.page_source)


class TestOpenAI(CustomTestCase):
    def test_openai_model_response(self):
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("testaccount")
        password_input = self.selenium.find_element(By.XPATH, "//input[@type='password']")
        password_input.send_keys("testadmin")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()
        self.selenium.implicitly_wait(5)
        language_selection = self.selenium.find_element(By.NAME, "language_selection")
        language_selection.send_keys("Python")
        user_prompt = self.selenium.find_element(By.NAME, "user_request")
        user_prompt.send_keys("Print hello world for me.")
        self.selenium.find_element(By.XPATH, '//button[@type="submit"]').click()

        text = 'print("Hello world")'
        self.assertTrue(text in self.selenium.page_source)
