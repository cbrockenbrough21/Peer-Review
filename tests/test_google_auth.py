import os
import unittest
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class TestGoogleOAuth(unittest.TestCase):

    def setUp(self):
        # Set up Chrome WebDriver with options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get("http://127.0.0.1:8000")  # Replace with your app URL

    def test_google_auth_login(self):
        driver = self.driver

        # Click on the "Login" button which triggers Google OAuth login
        login_button = driver.find_element(By.LINK_TEXT, "Login")
        login_button.click()

        # Wait for the "Continue" button to be clickable and click it
        try:
            continue_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
            )
            continue_button.click()
        except TimeoutException as e:
            print("Timeout while waiting for the Continue button.")
            print(driver.page_source)
            raise e

        # Debug: Print the URL to make sure we switched correctly
        print("Switched to Google OAuth window. Current URL:", driver.current_url)

        # Increase the wait time for the email input
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
            )
            email_input.send_keys(os.getenv("GOOGLE_EMAIL"))
            email_input.send_keys(Keys.RETURN)
        except TimeoutException as e:
            print("Failed to find the email input field.")
            print(driver.page_source)
            raise e

        # Wait for the password field to load and fill it
        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
            )
            password_input.send_keys(os.getenv("GOOGLE_PASSWORD"))
            password_input.send_keys(Keys.RETURN)
        except TimeoutException as e:
            print("Failed to find the password input field.")
            print(driver.page_source)
            raise e

        # Wait and assert that login was successful by checking for some element in your dashboard
        try:
            dashboard_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[text()='Dashboard']"))
            )
            self.assertTrue(dashboard_element.is_displayed())
        except TimeoutException as e:
            print("Failed to locate the dashboard element after login.")
            print(driver.page_source)
            raise e

    def tearDown(self):
        # Close the browser window
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()