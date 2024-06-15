import time
import unittest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

class MyAccount(unittest.TestCase):

    URL = 'https://osc-ultimate-demo.mageplaza.com/'

    CLOSE_DEMO_NAVIGATION_SELECTOR = (By.XPATH, '//button[@class="navigation-close" and @title="Close navigation"]')
    EDIT_BUTTON_SELECTOR = (By.XPATH, '//span[contains(text(), "Edit")]')
    EDIT_SHIPPING_ADDRESS_SELECTOR = (By.XPATH, '//span[contains(text(), "Edit Address")]')
    MY_ACCOUNT_BUTTON_SELECTOR = (By.XPATH, '//li/a[contains(text(), "My Account")]')
    MY_ACCOUNT_MENU_SELECTOR = (By.XPATH, '//button[@class="action switch" and @data-action="customer-menu-toggle"]')
    SHIPPING_CITY_SELECTOR = (By.ID, 'city')
    SHIPPING_COUNTRY_SELECTOR = (By.ID, 'country')
    SHIPPING_PHONE_NUMBER_SELECTOR = (By.ID, 'telephone')
    SHIPPING_REGION_SELECTOR = (By.ID, 'region_id')
    SHIPPING_SAVE_ADDRESS_SELECTOR = (By.XPATH, '//span[contains(text(), "Save Address")]')
    SHIPPING_SAVE_ADDRESS_MESSAGE_SELECTOR = (By.XPATH, '//div[@data-bind="html: $parent.prepareMessageForHtml(message.text)"]')
    SHIPPING_STREET_SELECTOR = (By.ID, 'street_1')
    SHIPPING_ZIP_CODE_SELECTOR = (By.ID, 'zip')
    SIGNIN_BUTTON_SELECTOR = (By.ID, 'bnt-social-login-authentication')
    SIGNIN_EMAIL_SELECTOR = (By.ID, 'social_login_email')
    SIGNIN_PASSWORD_SELECTOR = (By.ID, 'social_login_pass')
    SIGNIN_SELECTOR = (By.XPATH, '//a[contains(text(), "Sign In")]')

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
            },
            'autofill.profile_enabled': False
        })
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def close_demo_navigation(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CLOSE_DEMO_NAVIGATION_SELECTOR)).click()

    def sign_in(self, email, password):
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SIGNIN_SELECTOR))
        sign_in = self.driver.find_element(*self.SIGNIN_SELECTOR)
        email_input = self.driver.find_element(*self.SIGNIN_EMAIL_SELECTOR)
        password_input = self.driver.find_element(*self.SIGNIN_PASSWORD_SELECTOR)
        signin_button = self.driver.find_element(*self.SIGNIN_BUTTON_SELECTOR)

        # Actions
        sign_in.click()

        email_input.click()
        email_input.clear()
        email_input.send_keys(email)

        password_input.click()
        password_input.clear()
        password_input.send_keys(password)

        signin_button.click()

    def edit_shipping_address(self, street, country, region, phone_number, city, zip_code):
        # Find and select the shipping menu
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.EDIT_SHIPPING_ADDRESS_SELECTOR)).click()

        # Fill the required fields
        # Find elements
        street_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SHIPPING_STREET_SELECTOR))
        country_menu = self.driver.find_element(*self.SHIPPING_COUNTRY_SELECTOR)
        region_menu = self.driver.find_element(*self.SHIPPING_REGION_SELECTOR)
        phone_input = self.driver.find_element(*self.SHIPPING_PHONE_NUMBER_SELECTOR)
        city_input = self.driver.find_element(*self.SHIPPING_CITY_SELECTOR)
        zip_input = self.driver.find_element(*self.SHIPPING_ZIP_CODE_SELECTOR)
        save_button = self.driver.find_element(*self.SHIPPING_SAVE_ADDRESS_SELECTOR)

        # Actions
        street_input.click()
        street_input.clear()
        street_input.send_keys(street)

        country_select = Select(country_menu)
        country_select.select_by_visible_text(country)

        region_select = Select(region_menu)
        region_select.select_by_visible_text(region)

        phone_input.click()
        phone_input.clear()
        phone_input.send_keys(phone_number)

        city_input.click()
        city_input.clear()
        city_input.send_keys(city)

        zip_input.click()
        zip_input.clear()
        zip_input.send_keys(zip_code)

        save_button.click()

    def test_01_edit_shipping_address_positive(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')

        # Find and select the account menu
        my_account_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MY_ACCOUNT_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(my_account_menu).click(my_account_menu).perform()

        # Find and click on MyAccount button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MY_ACCOUNT_BUTTON_SELECTOR)).click()

        # Edit the shipping address with correct values
        self.edit_shipping_address('Street', 'Romania', 'Alba', '0721234567', 'Cugir', '515600')

        # Verify if the changes were saved
        time.sleep(1)
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SHIPPING_SAVE_ADDRESS_MESSAGE_SELECTOR))
        message_text = message_container.text

        self.assertIn('You saved the address.',
                      message_text,
                      'The message is not the same')

    def test_02_edit_shipping_address_negative(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')

        # Find and select the account menu
        my_account_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MY_ACCOUNT_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(my_account_menu).click(my_account_menu).perform()

        # Find and click on MyAccount button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MY_ACCOUNT_BUTTON_SELECTOR)).click()

        # Edit the shipping address with correct values
        self.edit_shipping_address('@#$%', 'Romania', 'Alba', '1', '@#$%', '@#$%')

        # Verify if the changes were saved
        time.sleep(1)
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SHIPPING_SAVE_ADDRESS_MESSAGE_SELECTOR))
        message_text = message_container.text

        self.assertIn('You saved the address.',
                      message_text,
                      'The message is not the same')
