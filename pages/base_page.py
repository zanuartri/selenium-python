from typing import Callable

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
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

    def click_until(self, click_locator: tuple[str, str], condition: Callable, retries: int = 3, retry_timeout: int = 5):
        """Click, then wait for the click's effect (e.g. a navigation). Some SPAs
        (saucedemo.com among them) render a button as visible/enabled before its
        click handler is actually bound, so Selenium's element_to_be_clickable
        check can pass on an element that silently no-ops when clicked. Re-clicking
        after a short wait — rather than one click plus a long wait — is what
        actually recovers from that race.
        """
        last_exc: TimeoutException | None = None
        for attempt in range(retries):
            self.wait().until(EC.element_to_be_clickable(click_locator)).click()
            try:
                return self.wait(retry_timeout).until(condition)
            except TimeoutException as exc:
                last_exc = exc
                print(
                    f"[click_until DEBUG] attempt {attempt + 1}/{retries} on {click_locator}: "
                    f"url={self.driver.current_url!r} title={self.driver.title!r}"
                )
                try:
                    for entry in self.driver.get_log("browser"):
                        print(f"[click_until DEBUG] console: {entry}")
                except Exception as log_exc:  # get_log support varies by driver/browser version
                    print(f"[click_until DEBUG] get_log unavailable: {log_exc}")
        raise last_exc
