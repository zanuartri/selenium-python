from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class WindowsPage(BasePage):
    """the-internet.herokuapp.com/windows — link opens a new tab/window."""

    URL = "https://the-internet.herokuapp.com/windows"

    NEW_WINDOW_LINK = (By.CSS_SELECTOR, "a[href='/windows/new']")
    CONTENT_HEADING = (By.CSS_SELECTOR, "div.example h3")

    def open_new_window(self) -> None:
        self.driver.find_element(*self.NEW_WINDOW_LINK).click()

    def switch_to_new_window(self, original_handles: set[str]) -> None:
        self.wait(20).until(lambda driver: len(driver.window_handles) > len(original_handles))
        new_handle = (set(self.driver.window_handles) - original_handles).pop()
        self.driver.switch_to.window(new_handle)

    def switch_to_window(self, handle: str) -> None:
        self.driver.switch_to.window(handle)

    def heading_text(self) -> str:
        return self.wait().until(EC.visibility_of_element_located(self.CONTENT_HEADING)).text
