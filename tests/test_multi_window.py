from selenium.webdriver.remote.webdriver import WebDriver

from pages.windows_page import WindowsPage


def test_new_window_opens_and_shows_expected_heading(driver: WebDriver) -> None:
    windows_page = WindowsPage(driver)
    windows_page.goto()

    original_handle = driver.current_window_handle
    original_handles = set(driver.window_handles)
    windows_page.open_new_window()
    windows_page.switch_to_new_window(original_handles)

    assert len(driver.window_handles) == len(original_handles) + 1, (
        "expected exactly one new browser tab/window to have opened"
    )
    assert windows_page.heading_text() == "New Window", "expected the new tab to show the 'New Window' heading"

    driver.close()
    windows_page.switch_to_window(original_handle)
    assert windows_page.heading_text() == "Opening a new window", (
        "expected switching back to the original window to restore its content"
    )
