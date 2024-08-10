from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from help_selectors.createAccountSelectors import *
from help_methods.driverFile import *

class CreateAccount(Driver):

    def create_account(self, firstname, lastname, email, password, confirmPassword):
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CREATE_ACCOUNT_SELECTOR))
        create_account = self.driver.find_element(*CREATE_ACCOUNT_SELECTOR)
        first_name = self.driver.find_element(*FIRST_NAME_SELECTOR)
        last_name = self.driver.find_element(*LAST_NAME_SELECTOR)
        email_address = self.driver.find_element(*EMAIL_ADDRESS_SELECTOR)
        password_input = self.driver.find_element(*PASSWORD_INPUT_SELECTOR)
        confirm_password = self.driver.find_element(*CONFIRM_PASSWORD_SELECTOR)
        create_account_button = self.driver.find_element(*CREATE_ACCOUNT_BUTTON_SELECTOR)

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