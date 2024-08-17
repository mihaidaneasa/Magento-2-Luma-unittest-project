import time
import unittest

from help_methods.baseMethods import *
from help_methods.createAccountMethods import *


class CreateAccountTests(unittest.TestCase, BaseMethods, CreateAccount):

    URL = 'https://osc-ultimate-demo.mageplaza.com/'

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

    def test_01_positive_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mihai', 'Daneasa', 'testabc@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        try:
            message_container = self.driver.find_element(*WELCOME_MESSAGE_SELECTOR)
            create_account = True
        except:
            # message_container = self.driver.find_element(*self.ERROR_CREATE_MESSAGE_SELECTOR)
            create_account = False

        if create_account:
            time.sleep(5)
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(WELCOME_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn('Welcome, Mihai Daneasa!',
                          message_text,
                          'ERROR! The text is not present on page!')

        if not create_account:
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ERROR_CREATE_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn('There is already an account with this email address. If you are sure that it is your email address, ',
                          message_text,
                          'ERROR! The text is not present on page!')

    def test_02_negative_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mihai', 'Daneasa', 'test#test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ERROR_INVALID_FIELD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Please enter a valid email address (Ex: johndoe@domain.com).',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_03_special_character_first_name_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mih@i', 'Daneasa', 'testare@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CREATE_FIRST_NAME_INVALID_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('First Name is not valid!',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_04_special_character_last_name_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mihai', 'Daneas@', 'tastare@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CREATE_LAST_NAME_INVALID_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Last Name is not valid!',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_05_digit_character_in_name_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mihai1', 'Daneasa1', 'testbeta@test.com', 'test@magento1', 'test@magento1')

        # Verify if the code is ok
        try:
            message_container = self.driver.find_element(*WELCOME_MESSAGE_SELECTOR)
            create_account = True
        except:
            # message_container = self.driver.find_element(*self.ERROR_CREATE_MESSAGE_SELECTOR)
            create_account = False

        if create_account:
            time.sleep(5)
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(WELCOME_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn('Welcome, Mihai1 Daneasa1!',
                          message_text,
                          'ERROR! The text is not present on page!')

        if not create_account:
            message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ERROR_CREATE_MESSAGE_SELECTOR))
            message_text = message_container.text
            self.assertIn(
                'There is already an account with this email address. If you are sure that it is your email address, ',
                message_text,
                'ERROR! The text is not present on page!')

    def test_06_short_password_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mihai', 'Daneasa', 'test123@test.com', '123', '123')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CREATE_SHORT_PASSWORD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Please enter 6 or more characters. Leading and trailing spaces will be ignored',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_07_six_character_password_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mihai', 'Daneasa', 'test123@test.com', '123456', '123456')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CREATE_SIX_CHARACTER_PASSWORD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('The password needs at least 8 characters. Create a new password and try again.',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_08_invalid_password_create(self):
        BaseMethods.close_demo_navigation(self)
        CreateAccount.create_account(self, 'Mihai', 'Daneasa', 'test123@test.com', '12345678', '12345678')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CREATE_INVALID_PASSWORD_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Minimum of different classes of characters in password is 3. Classes of characters: Lower Case, Upper Case, Digits, Special Characters.',
                      message_text,
                      'ERROR! The text is not present on page!')
