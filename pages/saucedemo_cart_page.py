from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SaucedemoCartPage(BasePage):
    """saucedemo.com/cart.html."""

    URL = "https://www.saucedemo.com/cart.html"

    CHECKOUT_BUTTON = (By.ID, "checkout")

    def go_to_checkout(self) -> None:
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
