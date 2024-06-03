import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class CreateAccountTests(unittest.TestCase):

    URL = 'https://osc-ultimate-demo.mageplaza.com/'

    CLOSE_DEMO_NAVIGATION_SELECTOR = (By.XPATH, '//button[@class="navigation-close" and @title="Close navigation"]')
    CONFIRM_PASSWORD_SELECTOR = (By.XPATH, '//input[@id="password-confirmation-social" and @title="Confirm Password"]')
    CREATE_ACCOUNT_SELECTOR = (By.XPATH, '//a[contains(text(), "Create an Account")]')
    CREATE_ACCOUNT_BUTTON_SELECTOR = (By.XPATH, '//button[@id="button-create-social" and @title="Create an Account"]')
    CREATE_FIRST_NAME_INVALID_SELECTOR = (By.XPATH, '//div[contains(text(), "First Name is not valid!")]')
    CREATE_INVALID_PASSWORD_SELECTOR = (By.XPATH, '//div[contains(text(), "Minimum of different classes of characters in password is 3. Classes of characters: Lower Case, Upper Case, Digits, Special Characters.")]')
    CREATE_LAST_NAME_INVALID_SELECTOR = (By.XPATH, '//div[contains(text(), "Last Name is not valid!")]')
    CREATE_SIX_CHARACTER_PASSWORD_SELECTOR = (By.XPATH, '//div[contains(text(), "The password needs at least 8 characters. Create a new password and try again.")]')
    CREATE_SHORT_PASSWORD_SELECTOR = (By.XPATH, '//div[@id="password-social-error"]')
    EMAIL_ADDRESS_SELECTOR = (By.XPATH, '//input[@id="email_address_create" and @title="Email"]')
    ERROR_CREATE_MESSAGE_SELECTOR = (By.XPATH, '//div[contains(text(), "There is already an account with this email address. If you are sure that it is your email address, ")]')
    ERROR_INVALID_FIELD_SELECTOR = (By.XPATH, '//div[@id="email_address_create-error"]')
    FIRST_NAME_SELECTOR = (By.XPATH, '//input[@id="firstname" and @title="First Name"]')
    LAST_NAME_SELECTOR = (By.XPATH, '//input[@id="lastname" and @title="Last Name"]')
    PASSWORD_INPUT_SELECTOR = (By.XPATH, '//input[@id="password-social" and @title="Password"]')
    WELCOME_MESSAGE_SELECTOR = (By.XPATH, '//span[@class="logged-in"]')

    def setUp(self):
        chrome_options = Options()
        # Disable notifications
        chrome_options.add_argument("--disable-notifications")
        # Disable "Chrome is being controlled by automated test software" bar
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # Disable "Save password for this site" popup
        chrome_options.add_experimental_option('prefs', {
            'credentials_enable_service': False,
            'profile': {
                'password_manager_enabled': False
            }
        })
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def close_demo_navigation(self):
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CLOSE_DEMO_NAVIGATION_SELECTOR)).click()

    def create_account(self, firstname, lastname, email, password, confirmPassword):
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CREATE_ACCOUNT_SELECTOR))
        create_account = self.driver.find_element(*self.CREATE_ACCOUNT_SELECTOR)
        first_name = self.driver.find_element(*self.FIRST_NAME_SELECTOR)
        last_name = self.driver.find_element(*self.LAST_NAME_SELECTOR)
        email_address = self.driver.find_element(*self.EMAIL_ADDRESS_SELECTOR)
        password_input = self.driver.find_element(*self.PASSWORD_INPUT_SELECTOR)
        confirm_password = self.driver.find_element(*self.CONFIRM_PASSWORD_SELECTOR)
        create_account_button = self.driver.find_element(*self.CREATE_ACCOUNT_BUTTON_SELECTOR)

        # Actions
        create_account.click()

        first_name.click()
        first_name.clear()
        first_name.send_keys(firstname)

        last_name.click()
        last_name.clear()
        last_name.send_keys(lastname)

        email_address.click()
        email_address.clear()
        email_address.send_keys(email)

        password_input.click()
        password_input.clear()
        password_input.send_keys(password)

        confirm_password.click()
        confirm_password.clear()
        confirm_password.send_keys(confirmPassword)

        create_account_button.click()

    def test_01_positive_create(self):
        self.close_demo_navigation()
        self.create_account('Mihai', 'Daneasa', 'testabc@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        try:
            message_container = self.driver.find_element(*self.WELCOME_MESSAGE_SELECTOR)
            create_account = True
        except:
            # message_container = self.driver.find_element(*self.ERROR_CREATE_MESSAGE_SELECTOR)
            create_account = False

        if create_account:
            time.sleep(5)
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.WELCOME_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn('Welcome, Mihai Daneasa!',
                          message_text,
                          'ERROR! The text is not present on page!')

        if not create_account:
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ERROR_CREATE_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn('There is already an account with this email address. If you are sure that it is your email address, ',
                          message_text,
                          'ERROR! The text is not present on page!')

    def test_02_negative_create(self):
        self.close_demo_navigation()
        self.create_account('Mihai', 'Daneasa', 'test#test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ERROR_INVALID_FIELD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Please enter a valid email address (Ex: johndoe@domain.com',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_03_special_character_first_name_create(self):
        self.close_demo_navigation()
        self.create_account('Mih@i', 'Daneasa', 'testare@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CREATE_FIRST_NAME_INVALID_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('First Name is not valid!',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_04_special_character_last_name_create(self):
        self.close_demo_navigation()
        self.create_account('Mihai', 'Daneas@', 'tastare@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CREATE_LAST_NAME_INVALID_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Last Name is not valid!',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_05_digit_character_in_name_create(self):
        self.close_demo_navigation()
        self.create_account('Mihai1', 'Daneasa1', 'testbeta@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        try:
            message_container = self.driver.find_element(*self.WELCOME_MESSAGE_SELECTOR)
            create_account = True
        except:
            # message_container = self.driver.find_element(*self.ERROR_CREATE_MESSAGE_SELECTOR)
            create_account = False

        if create_account:
            time.sleep(5)
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.WELCOME_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn('Welcome, Mihai1 Daneasa1!',
                          message_text,
                          'ERROR! The text is not present on page!')

        if not create_account:
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ERROR_CREATE_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn(
                'There is already an account with this email address. If you are sure that it is your email address, ',
                message_text,
                'ERROR! The text is not present on page!')

    def test_06_short_password_create(self):
        self.close_demo_navigation()
        self.create_account('Mihai', 'Daneasa', 'test123@test.com', '123', '123')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CREATE_SHORT_PASSWORD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Please enter 6 or more characters. Leading and trailing spaces will be ignored',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_07_six_character_password_create(self):
        self.close_demo_navigation()
        self.create_account('Mihai', 'Daneasa', 'test123@test.com', '123456', '123456')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CREATE_SIX_CHARACTER_PASSWORD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('The password needs at least 8 characters. Create a new password and try again.',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_08_invalid_password_create(self):
        self.close_demo_navigation()
        self.create_account('Mihai', 'Daneasa', 'test123@test.com', '12345678', '12345678')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CREATE_INVALID_PASSWORD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Minimum of different classes of characters in password is 3. Classes of characters: Lower Case, Upper Case, Digits, Special Characters.',
                      message_text,
                      'ERROR! The text is not present on page!')