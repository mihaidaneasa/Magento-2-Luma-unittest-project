import time
import unittest

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class CartTests(unittest.TestCase):

    URL = 'https://osc-ultimate-demo.mageplaza.com/'

    ACCEPT_AGREEMENT = (By.ID, "agreement__1")
    ADD_TO_CART_SELECTOR = (By.XPATH, '//button[@type="submit" and @title="Add to Cart"]')
    CART_PRODUCT_NAME_SELECTOR = (By.XPATH, '//strong[@class="product-item-name"]')
    CART_PRODUCT_PRICE_SELECTOR = (By.XPATH, '//span[@class="cart-price"]')
    CART_SELECTOR = (By.XPATH, '//a[@class="action showcart"]')
    CLOSE_DEMO_NAVIGATION_SELECTOR = (By.XPATH, '//button[@class="navigation-close" and @title="Close navigation"]')
    CHECKBOX_BILLING_ADDRESS_SELECTOR = (By.XPATH, '//input[@type="checkbox" and @name="billing-address-same-as-shipping"]')
    DELETED_ITEMS_MESSAGE_SELECTOR = (By.XPATH, '//span[contains(text(), "You have no items in your shopping cart.")]')
    DISCOUNT_AMOUNT_SELECTOR = (By.XPATH, '//span[@data-th="checkout.sidebar.summary.totals.discount"]')
    EDIT_ITEM_IN_CART_SELECTOR = (By.XPATH, '//div[@class="primary"]/a[@class="action edit" and @title="Edit item"]')
    MAN_BOTTOMS_MENU_SELECTOR = (By.XPATH, '//a[@id="ui-id-18"]')
    MAN_MENU_SELECTOR = (By.XPATH, '//li[@class="level0 nav-3 category-item level-top parent ui-menu-item"]')
    MAN_PANTS_MENU_SELECTOR = (By.XPATH, '//a[@id="ui-id-19"]')
    PLACE_ORDER_SELECTOR = (By.XPATH, '//div[@class="place-order-primary"]/button[@class="action primary checkout" and @type="button"]')
    PRODUCT_FIRST_COLOR_SELECTOR = (By.XPATH, '(//div[@class="swatch-option color"])[1]')
    PRODUCT_SECOND_COLOR_SELECTOR = (By.XPATH, '(//div[@class="swatch-option color"])[2]')
    PRODUCT_NAME_SELECTOR = (By.XPATH, '(//strong[@class="product name product-item-name"])[2]')
    PRODUCT_FINAL_PRICE_SELECTOR = (By.XPATH, '//span[@data-price-type="finalPrice"]')
    PRODUCT_FIRST_SIZE_SELECTOR = (By.XPATH, '(//div[@class="swatch-option text"])[3]')
    PRODUCT_SECOND_SIZE_SELECTOR = (By.XPATH, '(//div[@class="swatch-option text"])[2]')
    PRODUCT_STYLE_SELECTOR = (By.XPATH, '//div[contains(text(), "Style")]')
    PRODUCT_STYLE_SWEATPANTS_SELECTOR = (By.XPATH, '//a[contains(text(), "Sweatpants")]')
    QUANTITY_SELECTOR = (By.XPATH, '//input[@type="number"]')
    REMOVE_ITEM_BUTTON_SELECTOR = (By.XPATH, '//button[@class="action-primary action-accept"]')
    REMOVE_ITEM_FROM_CART_SELECTOR = (By.XPATH, '//div[@class="secondary"]/a[@class="action delete" and @title="Remove item"]')
    SEARCH_BUTTON_SELECTOR = (By.XPATH, '//button[@type="submit" and @class="action search"]')
    SEE_DETAILS_SELECTOR = (By.XPATH, '//span[@data-role="title" and @class="toggle"]/span[contains(text(), "See Details")]')
    SELECTED_PRODUCT_NAME_SELECTOR = (By.XPATH, '//span[@itemprop="name"]')
    SIGNIN_BUTTON_SELECTOR = (By.XPATH, '//button[@id="bnt-social-login-authentication"]')
    SIGNIN_EMAIL_SELECTOR = (By.XPATH, '//input[@id="social_login_email"]')
    SIGNIN_PASSWORD_SELECTOR = (By.XPATH, '//input[@id="social_login_pass"]')
    SIGNIN_SELECTOR = (By.XPATH, '//a[contains(text(), "Sign In")]')
    SHIPPING_FEE_SELECTOR = (By.XPATH, '//span[@data-th="Shipping"]')
    THANKS_MESSAGE_SELECTOR = (By.XPATH, '//h1[@class="page-title"]')
    TOTAL_PRODUCT_PRICE_SELECTOR = (By.XPATH, '//strong/span[@data-bind="text: getValue()"]')
    UPDATE_CART_SELECTOR = (By.XPATH, '//button[@type="submit" and @title="Update Cart"]')
    UPDATE_MESSAGE_SELECTOR = (By.XPATH, '//div[contains(text(), "Geo Insulated Jogging Pant was updated in your shopping cart.")]')


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
            }
        })
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def close_demo_navigation(self):
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CLOSE_DEMO_NAVIGATION_SELECTOR)).click()

    def select_a_product(self):
        time.sleep(1)
        # Select pants products from the list
        man_manu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MAN_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(man_manu).perform()
        bottoms_menu = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MAN_BOTTOMS_MENU_SELECTOR))
        ActionChains(self.driver).move_to_element(bottoms_menu).perform()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.MAN_PANTS_MENU_SELECTOR)).click()

        # Find and select the product style
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_STYLE_SELECTOR)).click()

        # Find and select "Sweatpants" style
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.PRODUCT_STYLE_SWEATPANTS_SELECTOR)).click()

        # Find and select the desired product
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_NAME_SELECTOR)).click()

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

    def remove_items(self):
        # Find the remove item button
        cart_selector = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CART_SELECTOR))
        ActionChains(self.driver).move_to_element(cart_selector).click(cart_selector).perform()
        time.sleep(1)
        see_details = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SEE_DETAILS_SELECTOR))
        ActionChains(self.driver).move_to_element(see_details).click(see_details).perform()
        remove_item = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.REMOVE_ITEM_FROM_CART_SELECTOR))
        ActionChains(self.driver).move_to_element(remove_item).click(remove_item).perform()
        time.sleep(1)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.REMOVE_ITEM_BUTTON_SELECTOR)).click()
        time.sleep(1)

    def select_size_and_color(self, quantity):
        # Find and select the size "34"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_FIRST_SIZE_SELECTOR)).click()

        # Find and select the color "Blue"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_FIRST_COLOR_SELECTOR)).click()

        # Find and select the quantity
        ordered_quantity = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.QUANTITY_SELECTOR))
        ordered_quantity.click()
        ordered_quantity.clear()
        ordered_quantity.send_keys(quantity)

    def test_01_adding_products_to_cart(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')
        time.sleep(3)
        self.select_a_product()

        # storing the product name
        selected_product_name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SELECTED_PRODUCT_NAME_SELECTOR))
        product_name_1 = selected_product_name.text

        # Select the desired options
        self.select_size_and_color(1)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ADD_TO_CART_SELECTOR)).click()

        time.sleep(10)
        # Verify if we are redirected to the cart page
        current_url = self.driver.current_url
        message_text = current_url
        self.assertEqual(message_text, 'https://osc-ultimate-demo.mageplaza.com/onestepcheckout/', 'The page is not the same')

        # Verify if the product in cart is the same with the selected one
        time.sleep(2)
        cart_product_name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CART_PRODUCT_NAME_SELECTOR))
        product_name_2 = cart_product_name.text
        self.assertEqual(f'{product_name_1}', f'{product_name_2}', 'The product is not the same')

        # Emptying the cart
        self.remove_items()

    def test_02_remove_product_from_cart(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')
        time.sleep(3)
        self.select_a_product()

        # Select the desired options
        self.select_size_and_color(1)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ADD_TO_CART_SELECTOR)).click()

        time.sleep(10)

        # Emptying the cart
        self.remove_items()

        # Verify if the cart is empty
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.DELETED_ITEMS_MESSAGE_SELECTOR))
        message_text = message_container.text
        self.assertIn('You have no items in your shopping cart.',
                      message_text,
                      'The message is not present')

    def test_03_verify_subtotal_price(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')
        time.sleep(3)
        self.select_a_product()

        # Storing the product base price
        i = 2
        product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_FINAL_PRICE_SELECTOR))
        current_price = product_price.text
        current_price_without_dollar = current_price.replace('$', '')
        actual_price = float(current_price_without_dollar)
        final_price = actual_price * i

        # Select the desired options
        self.select_size_and_color(i)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ADD_TO_CART_SELECTOR)).click()

        # Verify if the product price in cart is the same with the selected product price
        time.sleep(1)
        cart_product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CART_PRODUCT_PRICE_SELECTOR))
        cart_current_price = cart_product_price.text
        cart_current_price_without_dollar = cart_current_price.replace('$', '')
        subtotal_price = float(cart_current_price_without_dollar)
        self.assertEqual(f'{final_price}', f'{subtotal_price}', 'The product is not the same')

        # Emptying the cart
        self.remove_items()

    def test_04_verify_total_price(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')
        time.sleep(3)
        self.select_a_product()

        # Storing the product base price
        i = 5
        product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_FINAL_PRICE_SELECTOR))
        current_price = product_price.text
        current_price_without_dollar = current_price.replace('$', '')
        actual_price = float(current_price_without_dollar)

        # Select the desired options
        self.select_size_and_color(i)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ADD_TO_CART_SELECTOR)).click()

        # Verify if the cart total price is correctly calculated
        time.sleep(1)
        shipping_product_fee = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SHIPPING_FEE_SELECTOR))
        shipping_current_fee = shipping_product_fee.text
        shipping_current_fee_without_dollar = shipping_current_fee.replace('$', '')
        shipping_value = float(shipping_current_fee_without_dollar)

        total_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.TOTAL_PRODUCT_PRICE_SELECTOR))
        total_current_price = total_price.text
        total_current_price_without_dollar = total_current_price.replace('$', '')
        order_total = float(total_current_price_without_dollar)

        try:
            if i >= 3:
                discount_amount = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.DISCOUNT_AMOUNT_SELECTOR))
                discount_value = discount_amount.text
                discount_value_without_dollar = discount_value.replace('$', '')
                total_discount_value = float(discount_value_without_dollar)
                order_value = (actual_price * i) + total_discount_value
            else:
                order_value = actual_price * i
        except:
            order_value = actual_price * i

        order_price = order_value + shipping_value

        self.assertEqual(f'{order_price}', f'{order_total}', 'The product is not the same')

        # Emptying the cart
        self.remove_items()

    def test_05_edit_item_in_cart(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')
        time.sleep(3)
        self.select_a_product()

        # Select the desired options
        i = 2
        self.select_size_and_color(i)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ADD_TO_CART_SELECTOR)).click()

        time.sleep(10)

        # Find and click on edit button
        cart_selector = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CART_SELECTOR))
        ActionChains(self.driver).move_to_element(cart_selector).click(cart_selector).perform()
        time.sleep(1)
        see_details = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SEE_DETAILS_SELECTOR))
        ActionChains(self.driver).move_to_element(see_details).click(see_details).perform()
        time.sleep(1)
        edit_item = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.EDIT_ITEM_IN_CART_SELECTOR))
        ActionChains(self.driver).move_to_element(edit_item).click(edit_item).perform()

        # Change order options
        # Find and select the size "33"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_SECOND_SIZE_SELECTOR)).click()

        # Find and select the color "Green"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.PRODUCT_SECOND_COLOR_SELECTOR)).click()

        # Find and select the quantity
        ordered_quantity = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.QUANTITY_SELECTOR))
        ordered_quantity.click()
        ordered_quantity.clear()
        ordered_quantity.send_keys('4')

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.UPDATE_CART_SELECTOR)).click()

        # Verify if the cart was successfully updated
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.UPDATE_MESSAGE_SELECTOR))
        message_text = message_container.text

        self.assertIn('Geo Insulated Jogging Pant was updated in your shopping cart.',
                      message_text,
                      'The message is not present')

        # Emptying the cart
        self.remove_items()

    def test_06_place_order(self):
        self.close_demo_navigation()
        self.sign_in('testabc@test.com', 'test@magento1')
        time.sleep(3)
        self.select_a_product()

        # storing the product name
        selected_product_name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.SELECTED_PRODUCT_NAME_SELECTOR))
        product_name_1 = selected_product_name.text

        # Select the desired options
        self.select_size_and_color(1)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ADD_TO_CART_SELECTOR)).click()

        time.sleep(10)
        # Find elements
        billing_address = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.CHECKBOX_BILLING_ADDRESS_SELECTOR))
        accept_agreement = self.driver.find_element(*self.ACCEPT_AGREEMENT)

        # Actions
        billing_address.click()

        accept_agreement.click()

        place_order = self.driver.find_element(*self.PLACE_ORDER_SELECTOR)
        ActionChains(self.driver).move_to_element(place_order).click(place_order).perform()
        # place_order.click()
        time.sleep(5)
        # Verify if the order was successfully placed
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.THANKS_MESSAGE_SELECTOR))
        message_text = message_container.text

        self.assertIn('Thank you for your purchase!',
                      message_text,
                      'The message is not present')