from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from help_methods.driverFile import *
from help_selectors.signInSelectors import *

class BaseMethods(Driver):

    def close_demo_navigation(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CLOSE_DEMO_NAVIGATION_SELECTOR)).click()

    def sign_in(self, email, password):
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SIGNIN_SELECTOR))
        sign_in = self.driver.find_element(*SIGNIN_SELECTOR)
        email_input = self.driver.find_element(*SIGNIN_EMAIL_SELECTOR)
        password_input = self.driver.find_element(*SIGNIN_PASSWORD_SELECTOR)
        signin_button = self.driver.find_element(*SIGNIN_BUTTON_SELECTOR)

        # Actions
        sign_in.click()

        email_input.click()
        email_input.clear()
        email_input.send_keys(email)

        password_input.click()
        password_input.clear()
        password_input.send_keys(password)

        signin_button.click()

    def signin_button(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SIGNIN_SELECTOR)).click()