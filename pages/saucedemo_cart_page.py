from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SaucedemoCartPage(BasePage):
    """saucedemo.com/cart.html."""

    URL = "https://www.saucedemo.com/cart.html"

    CHECKOUT_BUTTON = (By.ID, "checkout")

    def go_to_checkout(self) -> None:
        self.wait().until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON)).click()
