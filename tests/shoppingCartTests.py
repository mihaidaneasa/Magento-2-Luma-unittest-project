import unittest

from help_methods.baseMethods import *
from help_methods.shoppingCartMethods import *


class CartTests(unittest.TestCase, BaseMethods, ShoppingCart):

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
            }
        })
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.driver.get(self.URL)

    def tearDown(self):
        self.driver.quit()

    def test_01_adding_products_to_cart(self):
        BaseMethods.close_demo_navigation(self)
        BaseMethods.sign_in(self, 'testabc@test.com', 'test@magento1')
        time.sleep(3)
        ShoppingCart.select_a_product(self)

        # storing the product name
        selected_product_name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SELECTED_PRODUCT_NAME_SELECTOR))
        product_name_1 = selected_product_name.text

        # Select the desired options
        ShoppingCart.select_size_and_color(self, 1)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ADD_TO_CART_SELECTOR)).click()
        time.sleep(10)

        # Verify if we are redirected to the cart page
        current_url = self.driver.current_url
        self.assertEqual(current_url, 'https://osc-ultimate-demo.mageplaza.com/default/admindemo/', 'The page is not the same')

        # Verify if the product in cart is the same with the selected one
        time.sleep(2)
        cart_product_name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CART_PRODUCT_NAME_SELECTOR))
        product_name_2 = cart_product_name.text
        self.assertEqual(f'{product_name_1}', f'{product_name_2}', 'The product is not the same')

        # Emptying the cart
        ShoppingCart.remove_items(self)

    def test_02_remove_product_from_cart(self):
        BaseMethods.close_demo_navigation(self)
        BaseMethods.sign_in(self, 'testabc@test.com', 'test@magento1')
        time.sleep(3)
        ShoppingCart.select_a_product(self)

        # Select the desired options
        ShoppingCart.select_size_and_color(self, 1)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ADD_TO_CART_SELECTOR)).click()

        time.sleep(10)

        # Emptying the cart
        ShoppingCart.remove_items(self)

        # Verify if the cart is empty
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(DELETED_ITEMS_MESSAGE_SELECTOR))
        message_text = message_container.text
        self.assertIn('You have no items in your shopping cart.',
                      message_text,
                      'The message is not present')

    def test_03_verify_subtotal_price(self):
        BaseMethods.close_demo_navigation(self)
        BaseMethods.sign_in(self, 'testabc@test.com', 'test@magento1')
        time.sleep(3)
        ShoppingCart.select_a_product(self)

        # Storing the product base price
        i = 2
        product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_FINAL_PRICE_SELECTOR))
        current_price = product_price.text
        current_price_without_dollar = current_price.replace('$', '')
        actual_price = float(current_price_without_dollar)
        final_price = actual_price * i

        # Select the desired options
        ShoppingCart.select_size_and_color(self, i)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ADD_TO_CART_SELECTOR)).click()

        # Verify if the product price in cart is the same with the selected product price
        time.sleep(1)
        cart_product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CART_PRODUCT_PRICE_SELECTOR))
        cart_current_price = cart_product_price.text
        cart_current_price_without_dollar = cart_current_price.replace('$', '')
        subtotal_price = float(cart_current_price_without_dollar)
        self.assertEqual(f'{final_price}', f'{subtotal_price}', 'The product is not the same')

        # Emptying the cart
        ShoppingCart.remove_items(self)

    def test_04_verify_total_price(self):
        BaseMethods.close_demo_navigation(self)
        BaseMethods.sign_in(self, 'testabc@test.com', 'test@magento1')
        time.sleep(3)
        ShoppingCart.select_a_product(self)

        # Storing the product base price
        i = 5
        product_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_FINAL_PRICE_SELECTOR))
        current_price = product_price.text
        current_price_without_dollar = current_price.replace('$', '')
        actual_price = float(current_price_without_dollar)

        # Select the desired options
        ShoppingCart.select_size_and_color(self, i)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ADD_TO_CART_SELECTOR)).click()

        # Verify if the cart total price is correctly calculated
        time.sleep(1)
        shipping_product_fee = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SHIPPING_FEE_SELECTOR))
        shipping_current_fee = shipping_product_fee.text
        shipping_current_fee_without_dollar = shipping_current_fee.replace('$', '')
        shipping_value = float(shipping_current_fee_without_dollar)

        total_price = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(TOTAL_PRODUCT_PRICE_SELECTOR))
        total_current_price = total_price.text
        total_current_price_without_dollar = total_current_price.replace('$', '')
        order_total = float(total_current_price_without_dollar)

        try:
            if i >= 3:
                discount_amount = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(DISCOUNT_AMOUNT_SELECTOR))
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
        ShoppingCart.remove_items(self)

    def test_05_edit_item_in_cart(self):
        BaseMethods.close_demo_navigation(self)
        BaseMethods.sign_in(self, 'testabc@test.com', 'test@magento1')
        time.sleep(3)
        ShoppingCart.select_a_product(self)

        # Select the desired options
        i = 2
        ShoppingCart.select_size_and_color(self, i)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ADD_TO_CART_SELECTOR)).click()

        time.sleep(10)

        # Find and click on edit button
        cart_selector = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CART_SELECTOR))
        ActionChains(self.driver).move_to_element(cart_selector).click(cart_selector).perform()
        time.sleep(1)
        see_details = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SEE_DETAILS_SELECTOR))
        ActionChains(self.driver).move_to_element(see_details).click(see_details).perform()
        time.sleep(1)
        edit_item = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(EDIT_ITEM_IN_CART_SELECTOR))
        ActionChains(self.driver).move_to_element(edit_item).click(edit_item).perform()

        # Change order options
        # Find and select the size "33"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_SECOND_SIZE_SELECTOR)).click()

        # Find and select the color "Green"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_SECOND_COLOR_SELECTOR)).click()

        # Find and select the quantity
        ordered_quantity = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(QUANTITY_SELECTOR))
        ordered_quantity.click()
        ordered_quantity.clear()
        ordered_quantity.send_keys('4')

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(UPDATE_CART_SELECTOR)).click()

        # Verify if the cart was successfully updated
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(UPDATE_MESSAGE_SELECTOR))
        message_text = message_container.text

        self.assertIn('Geo Insulated Jogging Pant was updated in your shopping cart.',
                      message_text,
                      'The message is not present')

        # Emptying the cart
        ShoppingCart.remove_items(self)

    def test_06_place_order(self):
        BaseMethods.close_demo_navigation(self)
        BaseMethods.sign_in(self, 'testabc@test.com', 'test@magento1')
        time.sleep(3)
        ShoppingCart.select_a_product(self)

        # Select the desired options
        ShoppingCart.select_size_and_color(self, 1)

        # Add the product to cart
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(ADD_TO_CART_SELECTOR)).click()

        time.sleep(10)
        # Find elements
        billing_address = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CHECKBOX_BILLING_ADDRESS_SELECTOR))
        accept_agreement = self.driver.find_element(*ACCEPT_AGREEMENT)

        # Actions
        billing_address.click()

        accept_agreement.click()

        place_order = self.driver.find_element(*PLACE_ORDER_SELECTOR)
        ActionChains(self.driver).move_to_element(place_order).click(place_order).perform()
        # place_order.click()
        time.sleep(5)
        # Verify if the order was successfully placed
        message_container = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(THANKS_MESSAGE_SELECTOR))
        message_text = message_container.text

        self.assertIn('Thank you for your purchase!',
                      message_text,
                      'The message is not present')
