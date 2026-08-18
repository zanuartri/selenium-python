from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from fixtures.test_data import Credentials
from pages.saucedemo_cart_page import SaucedemoCartPage
from pages.saucedemo_checkout_page import SaucedemoCheckoutPage
from pages.saucedemo_inventory_page import SaucedemoInventoryPage
from pages.saucedemo_login_page import SaucedemoLoginPage


def _reach_checkout(driver: WebDriver, credentials: Credentials) -> SaucedemoCheckoutPage:
    login_page = SaucedemoLoginPage(driver)
    login_page.goto()
    login_page.login(credentials.username, credentials.password)

    inventory_page = SaucedemoInventoryPage(driver)
    inventory_page.add_item_and_go_to_cart()

    SaucedemoCartPage(driver).go_to_checkout()
    return SaucedemoCheckoutPage(driver)


def test_checkout_requires_first_name(driver: WebDriver, saucedemo_credentials: Credentials) -> None:
    checkout_page = _reach_checkout(driver, saucedemo_credentials)

    checkout_page.fill_form(last_name="Doe", postal_code="12345")

    assert checkout_page.error_message_text() == "Error: First Name is required", (
        "expected a required-field error when First Name is left blank"
    )


def test_checkout_requires_last_name(driver: WebDriver, saucedemo_credentials: Credentials) -> None:
    checkout_page = _reach_checkout(driver, saucedemo_credentials)

    checkout_page.fill_form(first_name="Jane", postal_code="12345")

    assert checkout_page.error_message_text() == "Error: Last Name is required", (
        "expected a required-field error when Last Name is left blank"
    )


def test_checkout_requires_postal_code(driver: WebDriver, saucedemo_credentials: Credentials) -> None:
    checkout_page = _reach_checkout(driver, saucedemo_credentials)

    checkout_page.fill_form(first_name="Jane", last_name="Doe")

    assert checkout_page.error_message_text() == "Error: Postal Code is required", (
        "expected a required-field error when Postal Code is left blank"
    )


def test_checkout_with_all_fields_proceeds(driver: WebDriver, saucedemo_credentials: Credentials) -> None:
    checkout_page = _reach_checkout(driver, saucedemo_credentials)

    checkout_page.fill_form(first_name="Jane", last_name="Doe", postal_code="12345")

    WebDriverWait(driver, 5).until(
        lambda d: d.current_url == "https://www.saucedemo.com/checkout-step-two.html",
        "expected checkout to proceed to step two when all required fields are filled",
    )
