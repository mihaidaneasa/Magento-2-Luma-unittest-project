import time

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from help_methods.driverFile import *
from help_selectors.shoppingCartSelectors import *

class ShoppingCart(Driver):

    def select_a_product(self):
        time.sleep(1)
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

    def remove_items(self):
        # Find the remove item button
        cart_selector = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(CART_SELECTOR))
        ActionChains(self.driver).move_to_element(cart_selector).click(cart_selector).perform()
        time.sleep(1)
        see_details = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SEE_DETAILS_SELECTOR))
        ActionChains(self.driver).move_to_element(see_details).click(see_details).perform()
        remove_item = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(REMOVE_ITEM_FROM_CART_SELECTOR))
        ActionChains(self.driver).move_to_element(remove_item).click(remove_item).perform()
        time.sleep(1)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(REMOVE_ITEM_BUTTON_SELECTOR)).click()
        time.sleep(1)

    def select_size_and_color(self, quantity):
        # Find and select the size "34"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_FIRST_SIZE_SELECTOR)).click()

        # Find and select the color "Blue"
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(PRODUCT_FIRST_COLOR_SELECTOR)).click()

        # Find and select the quantity
        ordered_quantity = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(QUANTITY_SELECTOR))
        ordered_quantity.click()
        ordered_quantity.clear()
        ordered_quantity.send_keys(quantity)