from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SaucedemoCartPage(BasePage):
    """saucedemo.com/cart.html."""

    URL = "https://www.saucedemo.com/cart.html"

    CHECKOUT_BUTTON = (By.ID, "checkout")

    def go_to_checkout(self) -> None:
        self.click_until(self.CHECKOUT_BUTTON, EC.url_contains("/checkout-step-one.html"))
