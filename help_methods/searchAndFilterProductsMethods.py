from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from help_methods.driverFile import *
from help_selectors.searchAndFilterProductsSelectors import *

class SearchAndFilterProducts(Driver):

    def scroll_down(self):
        for i in range(30):
            self.driver.execute_script(f"window.scrollTo(0, {i * 500});")

    def search_items(self, text):
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SEARCH_BAR_SELECTOR))
        search_bar = self.driver.find_element(*SEARCH_BAR_SELECTOR)
        search_button = self.driver.find_element(*SEARCH_BUTTON_SELECTOR)

        # Actions
        search_bar.click()
        search_bar.clear()
        search_bar.send_keys(text)

        search_button.click()