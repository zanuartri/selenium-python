from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SaucedemoLoginPage(BasePage):
    """saucedemo.com login."""

    URL = "https://www.saucedemo.com/"

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def login(self, username: str, password: str) -> None:
        self.wait().until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.click_until(self.LOGIN_BUTTON, EC.url_contains("/inventory.html"))
