from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SecurePage(BasePage):
    """the-internet.herokuapp.com/secure — landed on after a successful login."""

    URL = "https://the-internet.herokuapp.com/secure"

    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a.button")

    def flash_message_text(self) -> str:
        return self.wait().until(EC.visibility_of_element_located(self.FLASH_MESSAGE)).text
