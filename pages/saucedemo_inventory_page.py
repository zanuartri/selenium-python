from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SaucedemoInventoryPage(BasePage):
    """saucedemo.com/inventory.html."""

    URL = "https://www.saucedemo.com/inventory.html"

    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def add_item_and_go_to_cart(self) -> None:
        self.wait().until(EC.element_to_be_clickable(self.ADD_TO_CART_BUTTON)).click()
        self.driver.find_element(*self.CART_LINK).click()
