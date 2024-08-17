from selenium.webdriver.common.by import By

EDIT_BUTTON_SELECTOR = (By.XPATH, '//span[contains(text(), "Edit")]')
EDIT_SHIPPING_ADDRESS_SELECTOR = (By.XPATH, '//span[contains(text(), "Edit Address")]')
MY_ACCOUNT_BUTTON_SELECTOR = (By.XPATH, '//li/a[contains(text(), "My Account")]')
MY_ACCOUNT_MENU_SELECTOR = (By.XPATH, '//button[@class="action switch" and @data-action="customer-menu-toggle"]')
SHIPPING_CITY_SELECTOR = (By.ID, 'city')
SHIPPING_COUNTRY_SELECTOR = (By.ID, 'country')
SHIPPING_PHONE_NUMBER_SELECTOR = (By.ID, 'telephone')
SHIPPING_REGION_SELECTOR = (By.ID, 'region_id')
SHIPPING_SAVE_ADDRESS_SELECTOR = (By.XPATH, '//span[contains(text(), "Save Address")]')
SHIPPING_SAVE_ADDRESS_MESSAGE_SELECTOR = (By.XPATH, '//div[@data-bind="html: $parent.prepareMessageForHtml(message.text)"]')
SHIPPING_STREET_SELECTOR = (By.ID, 'street_1')
SHIPPING_ZIP_CODE_SELECTOR = (By.ID, 'zip')
