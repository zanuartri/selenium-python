from selenium.webdriver.remote.webdriver import WebDriver

from fixtures.test_data import Credentials
from pages.login_page import LoginPage
from pages.secure_page import SecurePage


def test_login_with_valid_credentials_reaches_secure_area(driver: WebDriver, valid_credentials: Credentials) -> None:
    login_page = LoginPage(driver)
    login_page.goto()

    login_page.login(valid_credentials.username, valid_credentials.password)

    secure_page = SecurePage(driver)
    assert "You logged into a secure area" in secure_page.flash_message_text(), (
        "expected the secure-area flash message after a valid login"
    )


def test_login_with_invalid_credentials_shows_error(driver: WebDriver, invalid_credentials: Credentials) -> None:
    login_page = LoginPage(driver)
    login_page.goto()

    login_page.login(invalid_credentials.username, invalid_credentials.password)

    assert "Your password is invalid" in login_page.flash_message_text(), (
        "expected an invalid-password flash message, login should not have succeeded"
    )
