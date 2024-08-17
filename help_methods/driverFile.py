from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Driver():

    URL = 'https://osc-ultimate-demo.mageplaza.com/'

    def driver(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.driver.get(self.URL)
