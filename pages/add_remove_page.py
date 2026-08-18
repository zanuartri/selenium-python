from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class AddRemovePage(BasePage):
    """the-internet.herokuapp.com/add_remove_elements — state lives only in this page's DOM."""

    URL = "https://the-internet.herokuapp.com/add_remove_elements/"

    ADD_BUTTON = (By.CSS_SELECTOR, "button[onclick='addElement()']")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "button.added-manually")

    def add_elements(self, count: int) -> None:
        add_button = self.driver.find_element(*self.ADD_BUTTON)
        for _ in range(count):
            add_button.click()
        self.wait().until(
            lambda driver: len(driver.find_elements(*self.DELETE_BUTTONS)) == count
        )

    def delete_button_count(self) -> int:
        return len(self.driver.find_elements(*self.DELETE_BUTTONS))
