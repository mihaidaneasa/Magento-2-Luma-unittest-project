import unittest

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

    ADD_TO_CART_SELECTOR = (By.XPATH, '//button[@type="submit" and @title="Add to Cart"]')
    CART_MESSAGE_SELECTOR = (By.XPATH, '//')
    CLOSE_DEMO_NAVIGATION_SELECTOR = (By.XPATH, '//button[@class="navigation-close" and @title="Close navigation"]')
    LAST_PAGE_NUMBER_SELECTOR = (By.XPATH, '//div[@class="pages"]/ul[@class="items pages-items"]/li[@class="item"][last()]/a/span[last()][last()]')
    MAN_BOTTOMS_MENU_SELECTOR = (By.XPATH, '//a[@id="ui-id-18"]')
    MAN_MENU_SELECTOR = (By.XPATH, '//li[@class="level0 nav-3 category-item level-top parent ui-menu-item"]')
    MAN_PANTS_MENU_SELECTOR = (By.XPATH, '//a[@id="ui-id-19"]')
    NEXT_PAGE_SELECTOR = (By.XPATH, '//a[@class="action  next"]')
    PRODUCT_CATEGORY_SELECTOR = (By.XPATH, '(//a[contains(text(), "Hoodies & Sweatshirts")])[2]')
    PRODUCT_COLOR_SELECTOR = (By.XPATH, '//div[contains(text(), "Color")]')
    PRODUCT_COLOR_WHITE_SELECTOR = (By.XPATH, '//div[@class="swatch-option color " and @data-option-label="White"]')
    PRODUCT_COLOR_BLUE_SELECTOR = (By.XPATH, '//div[@class="swatch-option color" and @data-option-label="Blue"]')
    PRODUCT_ITEM_SELECTOR = (By.XPATH, '//div[@class="product details product-item-details"]')
    PRODUCT_NAME_SELECTOR = (By.XPATH, '(//strong[@class="product name product-item-name"])[2]')
    PRODUCT_PRESENTATION_IMAGES_SELECTOR = (By.XPATH, '//div[@class="fotorama__thumb fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img"]')
    PRODUCT_FINAL_PRICE_SELECTOR = (By.XPATH, '//span[@data-price-type="finalPrice"]')
    PRODUCT_PRICE_SELECTOR = (By.XPATH, '//span[@data-price-type="finalPrice"]')
    PRODUCT_SIZE_SELECTOR = (By.XPATH, '//div[contains(text(), "Size")]')
    PRODUCT_SIZE_34_SELECTOR = (By.XPATH, '//div[@class="swatch-option text" and @data-option-label="34"]')
    PRODUCT_SIZE_L_SELECTOR = (By.XPATH, '//div[@class="swatch-option text " and @data-option-label="L"]')
    PRODUCT_STYLE_SELECTOR = (By.XPATH, '//div[contains(text(), "Style")]')
    PRODUCT_STYLE_SWEATPANTS_SELECTOR = (By.XPATH, '//a[contains(text(), "Sweatpants")]')
    SEARCH_BAR_SELECTOR = (By.XPATH, '//input[@id="search" and @class="input-text"]')
    SEARCH_BUTTON_SELECTOR = (By.XPATH, '//button[@type="submit" and @class="action search"]')
    SEARCH_ERROR_SELECTOR = (By.XPATH, '//div[@class="message notice"]/div[contains(text(), "Your search returned no results. ")]')
    SORTING_MENU_SELECTOR = (By.XPATH, '//select[@id="sorter" and @class="sorter-options"]')
    TOTAL_SEARCHED_ITEMS_SELECTOR = (By.XPATH, '//p[@class="toolbar-amount"]/span[last()]')
    WHAT_IS_NEW_MENU_SELECTOR = (By.XPATH, '//span[contains(text(), \"What\'s New")]')

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

    def scroll_down(self):
        for i in range(30):
            self.driver.execute_script(f"window.scrollTo(0, {i * 500});")

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

        self.assertIn(f'{message_text}',
                      message_text,
                      'Error, I can not find anything')

    def test_03_selecting_products_filter(self):
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
        i = 1
        while True:
            try:
                # Finding elements and transform them to float
                product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located(self.PRODUCT_PRICE_SELECTOR))
                price_list = []
                self.scroll_down()

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
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.NEXT_PAGE_SELECTOR)).click()
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
        self.close_demo_navigation()

        # Select pants products from the list
        man_manu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MAN_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(man_manu).perform()
        bottoms_menu = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.MAN_BOTTOMS_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(bottoms_menu).perform()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MAN_PANTS_MENU_SELECTOR)).click()

        # Find and select the product style
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_STYLE_SELECTOR)).click()

        # Find and select "Sweatpants" style
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_STYLE_SWEATPANTS_SELECTOR)).click()

        # Find and select the desired product
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_NAME_SELECTOR)).click()

        # Verify if the product has presentation images
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_PRESENTATION_IMAGES_SELECTOR))
        presentation_images = self.driver.find_elements(*self.PRODUCT_PRESENTATION_IMAGES_SELECTOR)
        listed_images_1 = list(presentation_images)

        # Find and select the size "34"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_SIZE_34_SELECTOR)).click()

        # Find and select the color "Blue"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_COLOR_BLUE_SELECTOR)).click()

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_PRESENTATION_IMAGES_SELECTOR))
        presentation_images = self.driver.find_elements(*self.PRODUCT_PRESENTATION_IMAGES_SELECTOR)
        listed_images_2 = list(presentation_images)

        # Verify if the filter modifies the page
        self.assertEqual(f'{len(listed_images_1)}', f'{len(listed_images_2)}', 'The page was modified')