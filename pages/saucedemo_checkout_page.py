from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SaucedemoCheckoutPage(BasePage):
    """saucedemo.com/checkout-step-one.html."""

    URL = "https://www.saucedemo.com/checkout-step-one.html"

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def fill_form(self, first_name: str = "", last_name: str = "", postal_code: str = "") -> None:
        if first_name:
            self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        if last_name:
            self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        if postal_code:
            self.driver.find_element(*self.POSTAL_CODE_INPUT).send_keys(postal_code)
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def error_message_text(self) -> str:
        return self.wait().until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text
