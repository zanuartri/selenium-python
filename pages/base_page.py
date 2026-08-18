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
        recovers from that race.

        Clicks are dispatched via JS (element.click()) rather than WebDriver's
        native coordinate-based click: on Linux headless Chrome the native click
        was observed to silently miss this button 100% of the time (confirmed via
        CI logs — no navigation, no error render, no console errors either), while
        it works fine on Windows. A JS-dispatched click still fires a real 'click'
        event the app's listener sees, without depending on viewport/coordinate
        rendering that differs across platforms.
        """
        last_exc: TimeoutException | None = None
        for _ in range(retries):
            element = self.wait().until(EC.element_to_be_clickable(click_locator))
            self.driver.execute_script("arguments[0].click();", element)
            try:
                return self.wait(retry_timeout).until(condition)
            except TimeoutException as exc:
                last_exc = exc
        raise last_exc
