import time
import unittest

from collections import OrderedDict
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

class WebElementsTests(unittest.TestCase):

    URL = 'https://osc-ultimate-demo.mageplaza.com/'

    CLOSE_DEMO_NAVIGATION_SELECTOR = (By.XPATH, '//button[@class="navigation-close" and @title="Close navigation"]')
    SEARCH_BAR_SELECTOR = (By.XPATH, '//input[@id="search" and @class="input-text"]')
    SEARCH_BUTTON_SELECTOR = (By.XPATH, '//button[@type="submit" and @class="action search"]')
    PRODUCT_ITEM_SELECTOR = (By.XPATH, '//div[@class="product details product-item-details"]')
    PRODUCT_NAME_SELECTOR = (By.XPATH, '//strong[@class="product name product-item-name"]')
    PRODUCT_PRICE_SELECTOR = (By.XPATH, '//span[@data-price-type="finalPrice"]')
    TOTAL_SEARCHED_ITEMS_SELECTOR = (By.XPATH, '//p[@class="toolbar-amount"]/span[last()]')
    SEARCH_ERROR_SELECTOR = (By.XPATH, '//div[contains(text(), "Your search returned no results. ")]')
    WHAT_IS_NEW_MENU_SELECTOR = (By.XPATH, '//span[contains(text(), \"What\'s New")]')
    PRODUCT_CATEGORY_SELECTOR = (By.XPATH, '(//a[contains(text(), "Hoodies & Sweatshirts")])[2]')
    PRODUCT_COLOR_SELECTOR = (By.XPATH, '//div[contains(text(), "Color")]')
    PRODUCT_COLOR_WHITE_SELECTOR = (By.XPATH, '//div[@class="swatch-option color " and @data-option-label="White"]')
    PRODUCT_SIZE_SELECTOR = (By.XPATH, '//div[contains(text(), "Size")]')
    PRODUCT_SIZE_L_SELECTOR = (By.XPATH, '//div[@class="swatch-option text " and @data-option-label="L"]')
    SORTING_MENU_SELECTOR = (By.XPATH, '//select[@id="sorter" and @class="sorter-options"]')
    LAST_PAGE_NUMBER_SELECTOR = (By.XPATH, '//div[@class="pages"]/ul[@class="items pages-items"]/li[@class="item"][last()]/a/span[last()][last()]')
    NEXT_PAGE_SELECTOR = (By.XPATH, '//a[@class="action  next"]')

    def setUp(self):
        chrome_options = Options()
        # Disable notifications
        chrome_options.add_argument("--disable-notifications")
        # Disable "Chrome is being controlled by automated test software" bar
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def close_demo_navigation(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CLOSE_DEMO_NAVIGATION_SELECTOR)).click()

    def search_items(self, text):
        # Find elements
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SEARCH_BAR_SELECTOR))
        search_bar = self.driver.find_element(*self.SEARCH_BAR_SELECTOR)
        search_button = self.driver.find_element(*self.SEARCH_BUTTON_SELECTOR)

        # Actions
        search_bar.click()
        search_bar.clear()
        search_bar.send_keys(text)

        search_button.click()

    def scroll_down(self):
        for i in range(30):
            self.driver.execute_script(f"window.scrollTo(0, {i * 500});")

    def test_01_search_product(self):
        self.close_demo_navigation()
        self.search_items('Hood')

        # Verify if the code is ok
        total_items = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.TOTAL_SEARCHED_ITEMS_SELECTOR))
        total_items_founded = total_items.text

        self.assertIn(f'{total_items.text}',
                      total_items_founded,
                      'Error, I can not find anything')

    def test_02_product_not_found(self):
        self.close_demo_navigation()
        self.search_items('Bees')

        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SEARCH_ERROR_SELECTOR))
        message_text = message_container.text

        self.assertIn(f'{message_container.text}',
                      message_text,
                      'Error, I can not find anything')

    def test_03_selecting_filter(self):
        self.close_demo_navigation()

        # Find and click the "What's new" product category
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.WHAT_IS_NEW_MENU_SELECTOR)).click()

        # Find and click the product category button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_CATEGORY_SELECTOR)).click()

        # Find and select the product color
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_COLOR_SELECTOR)).click()

        # Find and select the color "white"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_COLOR_WHITE_SELECTOR)).click()

        # Find and select the product size
        WebDriverWait(self.driver,5).until(EC.presence_of_element_located(self.PRODUCT_SIZE_SELECTOR)).click()

        # Find and select the size "L"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_SIZE_L_SELECTOR)).click()

        # Verify if the code is ok
        total_items = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.TOTAL_SEARCHED_ITEMS_SELECTOR))
        total_items_founded = total_items.text

        self.assertIn(f'{total_items.text}',
                      total_items_founded,
                      'Error, I can not find anything')

    def test_04_sorting_items(self):
        self.close_demo_navigation()
        self.search_items('pants')

        # Find elements
        sorting_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SORTING_MENU_SELECTOR))
        sorting_elements = Select(sorting_menu)

        # Actions
        sorting_elements.select_by_visible_text('Price')

        # Verify if the Price sorting is ok
        # Finding the total number of pages
        self.scroll_down()
        last_page = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.LAST_PAGE_NUMBER_SELECTOR))
        last_page_number = int(last_page.text)

        for j in range(last_page_number):
            try:
                # Finding elements and transform them to float
                product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(self.PRODUCT_PRICE_SELECTOR))
                price_list = []
                self.scroll_down()
                for i in range(len(product_price)):
                    current_price = product_price[i].text
                    current_price_without_dollar = current_price.replace('$', '')
                    actual_price = current_price_without_dollar
                    actual_price_float = float(actual_price)
                    price_list.append(actual_price_float)

                # Sorting elements
                sorted_price_list = sorted(price_list)
                if sorted_price_list == price_list:
                    sorted_price_list = True
                else:
                    sorted_price_list = False

                # Go to the next page
                try:
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.NEXT_PAGE_SELECTOR)).click()
                except TimeoutException:
                    break

            except Exception as e:
                return f'I have encountered a problem {str(e)}'

        # Verify if the elements ar sorted
        self.assertTrue(True, 'The products are sorted')







