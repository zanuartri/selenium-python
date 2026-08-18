from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_TIMEOUT = 10


class BasePage:
    """Shared navigation/wait helpers for all page objects."""

    URL: str = ""

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def goto(self) -> None:
        assert self.URL, f"{type(self).__name__} must define URL"
        self.driver.get(self.URL)

    def wait(self, timeout: int = DEFAULT_TIMEOUT) -> WebDriverWait:
        """A fresh WebDriverWait — Selenium has no built-in auto-waiting, so every
        page object explicitly polls for the condition it needs via expected_conditions.
        """
        return WebDriverWait(self.driver, timeout)
