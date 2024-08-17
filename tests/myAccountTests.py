import time
import unittest

from selenium.webdriver import ActionChains
from help_methods.baseMethods import *
from help_methods.editShippingAddressMethods import *
from help_selectors.myAccountSelectors import *


class MyAccount(unittest.TestCase, BaseMethods, EditShippingAddress):

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
            },
            'autofill.profile_enabled': False
        })
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def test_01_edit_shipping_address_positive(self):
        BaseMethods.close_demo_navigation(self)
        BaseMethods.sign_in(self, 'testabc@test.com', 'test@magento1')

        # Find and select the account menu
        my_account_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MY_ACCOUNT_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(my_account_menu).click(my_account_menu).perform()

        # Find and click on MyAccount button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MY_ACCOUNT_BUTTON_SELECTOR)).click()

        # Edit the shipping address with correct values
        EditShippingAddress.edit_shipping_address(self, 'Street', 'Romania', 'Alba', '0721234567', 'Cugir', '515600')

        # Verify if the changes were saved
        time.sleep(1)
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(SHIPPING_SAVE_ADDRESS_MESSAGE_SELECTOR))
        message_text = message_container.text

        self.assertIn('You saved the address.',
                      message_text,
                      'The message is not the same')

    def test_02_edit_shipping_address_negative(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')

        # Find and select the account menu
        my_account_menu = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(MY_ACCOUNT_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(my_account_menu).click(my_account_menu).perform()

        # Find and click on MyAccount button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MY_ACCOUNT_BUTTON_SELECTOR)).click()

        # Edit the shipping address with correct values
        EditShippingAddress.edit_shipping_address(self, '@#$%', 'Romania', 'Alba', '1', '@#$%', '@#$%')

        # Verify if the changes were saved
        time.sleep(1)
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(SHIPPING_SAVE_ADDRESS_MESSAGE_SELECTOR))
        message_text = message_container.text
        print(message_text)

        self.assertIn('You entered incorrect values.',
                      message_text,
                      'The message is not the same')
