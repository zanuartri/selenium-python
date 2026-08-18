import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.add_remove_page import AddRemovePage

# /add_remove_elements has no server-side persistence — its state lives only
# in the DOM of the page that loaded it. If these tests shared a single driver
# (e.g. a module- or session-scoped fixture), the element count from one test
# would leak into the next, and running with `pytest -n auto` (pytest-xdist)
# would make the leakage non-deterministic depending on worker scheduling.
#
# The fix: the function-scoped `driver` fixture in conftest.py launches a
# fresh Chrome instance per test. Each test below gets an independent browser
# and DOM whether run serially or with `-n auto`.


@pytest.mark.parametrize("count", [1, 3, 5])
def test_adding_elements_yields_matching_delete_button_count(driver: WebDriver, count: int) -> None:
    add_remove_page = AddRemovePage(driver)
    add_remove_page.goto()

    add_remove_page.add_elements(count)

    assert add_remove_page.delete_button_count() == count, (
        f"expected {count} delete buttons after adding {count} elements"
    )
