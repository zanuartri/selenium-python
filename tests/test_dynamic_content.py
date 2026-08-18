import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.dynamic_loading_page import DynamicLoadingPage


@pytest.mark.parametrize("example", [1, 2])
def test_content_appears_after_async_load(driver: WebDriver, example: int) -> None:
    """example 1: the element exists but is hidden until loaded.
    example 2: the element doesn't exist in the DOM until loaded.
    Both are handled the same way — WebDriverWait + expected_conditions poll
    instead of sleeping; Selenium has no built-in auto-waiting like Playwright.
    """
    dynamic_page = DynamicLoadingPage(driver, example)
    dynamic_page.goto()

    finish_text = dynamic_page.start_and_wait_for_result()

    assert finish_text == "Hello World!", (
        f"expected 'Hello World!' to appear after the async load on example {example}"
    )
