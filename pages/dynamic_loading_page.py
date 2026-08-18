from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class DynamicLoadingPage(BasePage):
    """the-internet.herokuapp.com/dynamic_loading/{example} — content that appears async."""

    BASE = "https://the-internet.herokuapp.com/dynamic_loading"

    START_BUTTON = (By.CSS_SELECTOR, "#start button")
    LOADING_INDICATOR = (By.ID, "loading")
    FINISH_TEXT = (By.CSS_SELECTOR, "#finish h4")

    def __init__(self, driver: WebDriver, example: int) -> None:
        super().__init__(driver)
        self.URL = f"{self.BASE}/{example}"

    def start_and_wait_for_result(self) -> str:
        self.driver.find_element(*self.START_BUTTON).click()
        # No sleeps: wait for the loader to disappear, then for the real
        # content to become visible, polling via expected_conditions.
        self.wait().until(EC.invisibility_of_element_located(self.LOADING_INDICATOR))
        finish_element = self.wait().until(EC.visibility_of_element_located(self.FINISH_TEXT))
        return finish_element.text
