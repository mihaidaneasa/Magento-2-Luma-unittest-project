import time
import unittest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class SingInTests(unittest.TestCase):

    URL = 'https://osc-ultimate-demo.mageplaza.com/'

    CLOSE_DEMO_NAVIGATION_SELECTOR = (By.XPATH, '//button[@class="navigation-close" and @title="Close navigation"]')
    FACEBOOCK_ACCEPT_COOKIES_SELECTOR = (By.XPATH, '//button[@data-cookiebanner="accept_button" and @type="submit"] | //span[contains(text(), "Allow all cookies")]')
    FACEBOOCK_ERROR_MESSAGE_SELECTOR = (By.XPATH, '//div[@class="fsl fwb fcb" and contains(text(), "Error Accessing App")]')
    FACEBOOCK_LOGIN_SELECTOR = (By.XPATH, '//a[@class="btn btn-block btn-social btn-facebook"]')
    LINKEDIN_ERROR_MESSAGE_SELECTOR = (By.XPATH, '//p[@class="message"]')
    LINKEDIN_LOGIN_SELECTOR = (By.XPATH, '//a[@class="btn btn-block btn-social btn-linkedin"]')
    YAHOO_ACCEPT_COOKIES_SELECTOR = (By.XPATH, '//button[@class="pure-button puree-button-primary oauth2-authorize-button"]')
    YAHOO_CONFIRM_PASSWORD_SELECTOR = (By.XPATH, '//input[@id="request-password-confirmation"]')
    YAHOO_INPUT_PASSWORD_SELECTOR = (By.XPATH, '//input[@id="request-password-social"]')
    YAHOO_LOGIN_SELECTOR = (By.XPATH, '//a[@class="btn btn-block btn-social btn-yahoo"]')
    YAHOO_NEXT_BUTTON_SELECTOR_1 = (By.XPATH, '//input[@id="login-signin"]')
    YAHOO_NEXT_BUTTON_SELECTOR_2 = (By.XPATH, '//button[@id="login-signin"]')
    YAHOO_SUBMIT_SELECTOR = (By.XPATH, '//button[@class="action send primary"]')
    YAHOO_USER_EMAIL_SELECTOR = (By.XPATH, '//input[@class="phone-no "]')
    YAHOO_USER_PASSWORD_SELECTOR = (By.XPATH, '//input[@id="login-passwd" and @class="password"]')
    GITHUB_EMAIL_SELECTOR = (By.XPATH, '//input[@class="form-control input-block js-login-field"]')
    GITHUB_LOGIN_SELECTOR = (By.XPATH, '//a[@class="btn btn-block btn-social btn-github"]')
    GITHUB_PASSWORD_SELECTOR = (By.XPATH, '//input[@class="form-control form-control input-block js-password-field"]')
    GITHUB_SIGNIN_BUTTON_SELECTOR = (By.XPATH, '//input[@class="btn btn-primary btn-block js-sign-in-button"]')
    SIGNIN_BUTTON_SELECTOR = (By.XPATH, '//button[@id="bnt-social-login-authentication"]')
    SIGNIN_EMAIL_SELECTOR = (By.XPATH, '//input[@id="social_login_email"]')
    SIGNIN_ERROR_MESSAGE_1 = (By.XPATH, '//div[contains(text(), "Invalid login or password.")]')
    SIGNIN_ERROR_MESSAGE_2 = (By.XPATH, '//div[@id="social_login_email-error"]')
    SIGNIN_PASSWORD_SELECTOR = (By.XPATH, '//input[@id="social_login_pass"]')
    SIGNIN_SELECTOR = (By.XPATH, '//a[contains(text(), "Sign In")]')
    SIGN_OUT_BUTTON_SELECTOR = (By.XPATH, '//li[@class="link authorization-link"]')
    SIGN_OUT_MENU_SELECTOR = (By.XPATH, '//button[@class="action switch" and @data-action="customer-menu-toggle"]')
    SIGN_OUT_MESSAGE_SELECTOR = (By.XPATH, '//span[@data-ui-id="page-title-wrapper"]')
    WELCOME_MESSAGE_SELECTOR = (By.XPATH, '//span[@class="logged-in"]')


    def setUp(self, uc=None):
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

    def signin_button(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SIGNIN_SELECTOR)).click()

    def test_01_positive_signin(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        time.sleep(3)
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.WELCOME_MESSAGE_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Welcome, Mihai Daneasa!',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_02_wrong_email_signin(self):
        self.close_demo_navigation()
        self.sign_in('testare@test.com', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.SIGNIN_ERROR_MESSAGE_1))
        message_text = message_container.text

        # Actions
        self.assertIn('Invalid login or password.',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_03_wrong_password_signin(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'testalfa@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.SIGNIN_ERROR_MESSAGE_1))
        message_text = message_container.text

        # Actions
        self.assertIn('Invalid login or password.',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_04_invalid_email_signin(self):
        self.close_demo_navigation()
        self.sign_in('testabc#test.com', 'test@magento1')

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.SIGNIN_ERROR_MESSAGE_2))
        message_text = message_container.text

        # Actions
        self.assertIn('Please enter a valid email address (Ex: johndoe@domain.com).',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_05_faceboock_login(self):
        global login_page
        self.close_demo_navigation()

        # Storing the current window handle to get back to dashboard
        main_page = self.driver.current_window_handle
        self.signin_button()

        # Find and click the faceboock_login buuton
        self.driver.find_element(*self.FACEBOOCK_LOGIN_SELECTOR).click()

        # Storing the current window handle to get back to dashboard
        login_page = self.driver.current_window_handle

        # Changing the handles to access login page
        for currentWindow in self.driver.window_handles:
            self.driver.switch_to.window(currentWindow)
            url = self.driver.current_url
            if ("https://www.facebook.com/login.php?skip_api_login=1&api_key=744024889374221&kid_directed_site=0&app_id=744024889374221&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fdialog%2Foauth%3Fresponse_type%3Dcode%26client_id%3D744024889374221%26redirect_uri%3Dhttps%253A%252F%252Fosc-ultimate-demo.mageplaza.com%252Fsociallogin%252Fsocial%252Fcallback%252F%253Fhauth_done%253DFacebook%26scope%3Demail%252C%2Bpublic_profile%26state%3DHA-TWB70L86ASUXRNM4ZYDFGK3PCQ5J2HV9OEI1%26ret%3Dlogin%26fbapp_pres%3D0%26logger_id%3D7fd97cdf-3833-49a9-85eb-f22a7d66db6b%26tp%3Dunspecified&cancel_url=https%3A%2F%2Fosc-ultimate-demo.mageplaza.com%2Fsociallogin%2Fsocial%2Fcallback%2F%3Fhauth_done%3DFacebook%26error%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied%26state%3DHA-TWB70L86ASUXRNM4ZYDFGK3PCQ5J2HV9OEI1%23_%3D_&display=page&locale=en_US&pl_dbl=0" in url):
                login_page = self.driver.switch_to.window(currentWindow)
                break

        # Scroll down in page
        for i in range(30):
            self.driver.execute_script(f"window.scrollTo(0, {i * 500});")

        # Accept cookies
        accept_cookies = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.FACEBOOCK_ACCEPT_COOKIES_SELECTOR))
        ActionChains(self.driver).move_to_element(accept_cookies).click(accept_cookies).perform()

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.FACEBOOCK_ERROR_MESSAGE_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Error Accessing App',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_06_linkedin_login(self):
        global login_page
        self.close_demo_navigation()

        # Storing the current window handle to get back to dashboard
        main_page = self.driver.current_window_handle

        self.signin_button()

        # Find and click the linkedin_login button
        self.driver.find_element(*self.LINKEDIN_LOGIN_SELECTOR).click()

        # Storing the current window handle to get back to dashboard
        login_page = self.driver.current_window_handle

        # Changing the handles to access login page
        for currentWindow in self.driver.window_handles:
            self.driver.switch_to.window(currentWindow)
            url = self.driver.current_url
            if ('https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=86n928xh7uro9z&redirect_uri=https%3A%2F%2Fosc-ultimate-demo.mageplaza.com%2Fsociallogin%2Fsocial%2Fcallback%2F%3Fhauth.done%3DLinkedIn&scope=r_liteprofile+r_emailaddress&state=HA-5O0FMR9H2QZYS4UXA8LNW1ITG6V37PCKJBED' in url):
                login_page = self.driver.switch_to.window(currentWindow)
                break

        # Verify if the code is ok
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.LINKEDIN_ERROR_MESSAGE_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('The application is disabled',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_07_yahoo_login(self):
        global login_page
        self.close_demo_navigation()

        # Storing the current window handle to get back to dashboard
        main_page = self.driver.current_window_handle

        self.signin_button()

        # Find and click the yahoo_login button
        self.driver.find_element(*self.YAHOO_LOGIN_SELECTOR).click()

        # Storing the current window handle to get back to dashboard
        login_page = self.driver.current_window_handle

        # Changing the handles to access login page
        for currentWindow in self.driver.window_handles:
            self.driver.switch_to.window(currentWindow)
            url = self.driver.current_url
            if ('https://login.yahoo.com/?src=oauth&client_id=dj0yJmk9dXZGSk1oUzhLdHJKJmQ9WVdrOWFWbDNNMU5VTmpRbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTk4&crumb=&redirect_uri=https%3A%2F%2Fosc-ultimate-demo.mageplaza.com%2Fsociallogin%2Fsocial%2Fcallback%2F&done=https%3A%2F%2Fapi.login.yahoo.com%2Foauth2%2Fauthorize%3Fclient_id%3Ddj0yJmk9dXZGSk1oUzhLdHJKJmQ9WVdrOWFWbDNNMU5VTmpRbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTk4%26redirect_uri%3Dhttps%253A%252F%252Fosc-ultimate-demo.mageplaza.com%252Fsociallogin%252Fsocial%252Fcallback%252F%26response_type%3Dcode%26scope%3Dprofile%26state%3DHA-OGZC3P80SB6ALKFDW9M7Q5TJ2REY1NX4IHUV' in url):
                login_page = self.driver.switch_to.window(currentWindow)
                break

        # Input email
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.YAHOO_USER_EMAIL_SELECTOR))
        user_email = self.driver.find_element(*self.YAHOO_USER_EMAIL_SELECTOR)
        next_button = self.driver.find_element(*self.YAHOO_NEXT_BUTTON_SELECTOR_1)

        # Actions
        user_email.click()
        user_email.clear()
        user_email.send_keys('mihaiteste@yahoo.com')

        next_button.click()

        # Input password
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.YAHOO_USER_PASSWORD_SELECTOR))
        user_password = self.driver.find_element(*self.YAHOO_USER_PASSWORD_SELECTOR)
        next_button = self.driver.find_element(*self.YAHOO_NEXT_BUTTON_SELECTOR_2)

        # Actions
        user_password.click()
        user_password.clear()
        user_password.send_keys('030208@Serban')

        next_button.click()

        # Accept cookies
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.YAHOO_ACCEPT_COOKIES_SELECTOR))
        accept_cookies = self.driver.find_element(*self.YAHOO_ACCEPT_COOKIES_SELECTOR)

        # Actions
        accept_cookies.click()

        # Change control to main page
        self.driver.switch_to.window(main_page)

        # Find and click yahoo_login button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.YAHOO_LOGIN_SELECTOR)).click()

        # Input and confirm password
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.YAHOO_INPUT_PASSWORD_SELECTOR))
        insert_password = self.driver.find_element(*self.YAHOO_INPUT_PASSWORD_SELECTOR)
        confirm_password = self.driver.find_element(*self.YAHOO_CONFIRM_PASSWORD_SELECTOR)
        submit_button = self.driver.find_element(*self.YAHOO_SUBMIT_SELECTOR)

        # Actions
        insert_password.click()
        insert_password.clear()
        insert_password.send_keys('test@magento1')

        confirm_password.click()
        confirm_password.clear()
        confirm_password.send_keys('test@magento1')

        submit_button.click()

        # Verify if the code is ok
        # Find elements
        time.sleep(5)
        message_container = WebDriverWait(self.driver, 50).until(EC.presence_of_element_located(self.WELCOME_MESSAGE_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Welcome, Mihai Daneasa!',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_08_github_login(self):
        global login_page
        self.close_demo_navigation()

        # Storing the current window handle to get back to dashboard
        main_page = self.driver.current_window_handle

        self.signin_button()

        # Find and click the github_login button
        self.driver.find_element(*self.GITHUB_LOGIN_SELECTOR).click()

        # Storing the current window handle to get back to dashboard
        login_page = self.driver.current_window_handle

        # Changing the handles to access login page
        for currentWindow in self.driver.window_handles:
            self.driver.switch_to.window(currentWindow)
            url = self.driver.current_url
            if ('https://github.com/login?client_id=040e38eb71b7778fd9f8&return_to=%2Flogin%2Foauth%2Fauthorize%3Fclient_id%3D040e38eb71b7778fd9f8%26redirect_uri%3Dhttps%253A%252F%252Fosc-ultimate-demo.mageplaza.com%252Fsociallogin%252Fsocial%252Fcallback%252F%253Fhauth.done%253DGithub%26response_type%3Dcode%26scope%3Duser%253Aemail%26state%3DHA-3AI1QKYOC09BNSHLXFZJGM8P25DRWE674UVT' in url):
                login_page = self.driver.switch_to.window(currentWindow)
                break

        # Find Elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.GITHUB_EMAIL_SELECTOR))
        insert_email = self.driver.find_element(*self.GITHUB_EMAIL_SELECTOR)
        insert_password = self.driver.find_element(*self.GITHUB_PASSWORD_SELECTOR)
        signin_button = self.driver.find_element(*self.GITHUB_SIGNIN_BUTTON_SELECTOR)

        # Actions
        insert_email.click()
        insert_email.clear()
        insert_email.send_keys('mihaiteste')

        insert_password.click()
        insert_password.clear()
        insert_password.send_keys('030208@Serban')

        signin_button.click()

        # Change control to main page
        self.driver.switch_to.window(main_page)

        # Verify if we are logged in
        # Find elements
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.WELCOME_MESSAGE_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('Welcome, Mihai Daneasa!',
                      message_text,
                      'ERROR! The text is not present on page!')

    def test_09_log_out(self):
        self.close_demo_navigation()

        # Login
        self.sign_in('testabc@test.com', 'test@magento1')

        # Logout
        # Find and click the sign-out menu
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SIGN_OUT_MENU_SELECTOR)).click()

        # Find and click the sign-out button
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.SIGN_OUT_BUTTON_SELECTOR)).click()

        # Verify if the code is ok
        # Find elements
        time.sleep(3)
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SIGN_OUT_MESSAGE_SELECTOR))
        message_text = message_container.text

        # Actions
        self.assertIn('You are signed out',
                      message_text,
                      'ERROR! The text is not present on page!')