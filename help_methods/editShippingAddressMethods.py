from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from help_methods.driverFile import *
from help_selectors.myAccountSelectors import *


class EditShippingAddress(Driver):

    def edit_shipping_address(self, street, country, region, phone_number, city, zip_code):
        # Find and select the shipping menu
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(EDIT_SHIPPING_ADDRESS_SELECTOR)).click()

        # Fill the required fields
        # Find elements
        street_input = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(SHIPPING_STREET_SELECTOR))
        country_menu = self.driver.find_element(*SHIPPING_COUNTRY_SELECTOR)
        region_menu = self.driver.find_element(*SHIPPING_REGION_SELECTOR)
        phone_input = self.driver.find_element(*SHIPPING_PHONE_NUMBER_SELECTOR)
        city_input = self.driver.find_element(*SHIPPING_CITY_SELECTOR)
        zip_input = self.driver.find_element(*SHIPPING_ZIP_CODE_SELECTOR)
        save_button = self.driver.find_element(*SHIPPING_SAVE_ADDRESS_SELECTOR)

        # Actions
        street_input.click()
        street_input.clear()
        street_input.send_keys(street)

        country_select = Select(country_menu)
        country_select.select_by_visible_text(country)

        region_select = Select(region_menu)
        region_select.select_by_visible_text(region)

        phone_input.click()
        phone_input.clear()
        phone_input.send_keys(phone_number)

        city_input.click()
        city_input.clear()
        city_input.send_keys(city)

        zip_input.click()
        zip_input.clear()
        zip_input.send_keys(zip_code)

        save_button.click()
