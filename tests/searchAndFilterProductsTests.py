import time
import unittest

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from help_methods.baseMethods import *
from help_methods.searchAndFilterProductsMethods import *


class SearchAndFilterProducts(unittest.TestCase, BaseMethods, SearchAndFilterProducts):
    URL = 'https://osc-ultimate-demo.mageplaza.com/'

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

    def test_01_search_product(self):
        BaseMethods.close_demo_navigation(self)
        SearchAndFilterProducts.search_items(self, 'Hood')

        # Verify if the code is ok
        while True:
            total_items = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(TOTAL_SEARCHED_ITEMS_SELECTOR))
            total_items_founded = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(TOTAL_ITEMS_ON_PAGE_SELECTOR))
            total_items_on_page = self.driver.find_element(*TOTAL_ITEMS_ON_PAGE_SELECTOR)

            try:
                if total_items.text != total_items_on_page.text:
                    SearchAndFilterProducts.scroll_down(self)
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(NEXT_PAGE_SELECTOR)).click()
                    SearchAndFilterProducts.scroll_down(self)
                else:
                    break

            except TimeoutException:
                break

        self.assertIn(f'{total_items.text}',
                      f'{total_items_founded.text}',
                      'Error, I can not find anything')

    def test_02_product_not_found(self):
        BaseMethods.close_demo_navigation(self)
        SearchAndFilterProducts.search_items(self, 'Bees')

        # Verify if the code is ok
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SEARCH_ERROR_SELECTOR)).text

        self.assertEqual(f'{message_container}',
                         'Your search returned no results.\nDid you mean\nbeat\nbest',
                         'Error, The message is not the same')

    def test_03_selecting_products_filter(self):
        BaseMethods.close_demo_navigation(self)

        # Find and click the "What's new" product category
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(WHAT_IS_NEW_MENU_SELECTOR)).click()

        # Find and click the product category button
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_CATEGORY_SELECTOR)).click()

        # Find and select the product color
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_COLOR_SELECTOR)).click()

        # Find and select the color "white"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_COLOR_WHITE_SELECTOR)).click()

        # Find and select the product size
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_SIZE_SELECTOR)).click()

        # Find and select the size "L"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_SIZE_L_SELECTOR)).click()

        # Verify if the code is ok
        total_items = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(TOTAL_SEARCHED_ITEMS_SELECTOR))
        total_items_founded = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(PRODUCT_ITEM_SELECTOR))

        self.assertEqual(f'{int(total_items.text)}',
                         f'{len(total_items_founded)}',
                         'Error, the results don\'t match')

    def test_04_sorting_items(self):
        BaseMethods.close_demo_navigation(self)
        SearchAndFilterProducts.search_items(self, 'pants')

        # Find elements
        sorting_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SORTING_MENU_SELECTOR))
        sorting_elements = Select(sorting_menu)

        # Actions
        sorting_elements.select_by_visible_text('Price')

        # Verify if the Price sorting is ok
        i = 1
        while True:
            try:
                # Finding elements and transform them to float
                product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(PRODUCT_PRICE_SELECTOR))
                price_list = []
                SearchAndFilterProducts.scroll_down(self)

                for i in range(len(product_price)):
                    current_price = product_price[i].text
                    current_price_without_dollar = current_price.replace('$', '')
                    actual_price = float(current_price_without_dollar)
                    price_list.append(actual_price)

                # Sorting elements
                sorted_price_list = sorted(price_list)

                # Go to the next page
                try:
                    if sorted_price_list == price_list:
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(NEXT_PAGE_SELECTOR)).click()
                        message = 'The list is sorted'
                    elif sorted_price_list != price_list:
                        message = 'The list is unsorted'
                    else:
                        break

                except TimeoutException:
                    break

            except Exception as e:
                return f'I have encountered a problem {str(e)}'
            i += 1

            # Verify if the elements ar sorted
            self.assertIs('The list is sorted',
                          message,
                          'The list is unsorted')

    def test_05_apply_filters_to_a_product(self):
        BaseMethods.close_demo_navigation(self)

        # Select pants products from the list
        man_manu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MAN_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(man_manu).perform()
        bottoms_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MAN_BOTTOMS_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(bottoms_menu).perform()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(MAN_PANTS_MENU_SELECTOR)).click()

        # Find and select the product style
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_STYLE_SELECTOR)).click()

        # Find and select "Sweatpants" style
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_STYLE_SWEATPANTS_SELECTOR)).click()

        # Find and select the desired product
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_NAME_SELECTOR)).click()

        # Verify if the product has presentation images
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_PRESENTATION_IMAGES_SELECTOR))
        presentation_images = self.driver.find_elements(*PRODUCT_PRESENTATION_IMAGES_SELECTOR)
        listed_images_1 = list(presentation_images)

        # Find and select the size "34"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_SIZE_34_SELECTOR)).click()

        # Find and select the color "Blue"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_COLOR_BLUE_SELECTOR)).click()
        time.sleep(1)

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_PRESENTATION_IMAGES_SELECTOR))
        presentation_images = self.driver.find_elements(*PRODUCT_PRESENTATION_IMAGES_SELECTOR)
        listed_images_2 = list(presentation_images)

        print(len(listed_images_1))
        print(len(listed_images_2))
        # Verify if the filter modifies the page
        self.assertEqual(f'{len(listed_images_1)}', f'{len(listed_images_2)}', 'The page was modified')
