from selenium.webdriver.remote.webdriver import WebDriver

from pages.iframe_page import NestedFramesPage


def test_can_read_content_from_nested_frames(driver: WebDriver) -> None:
    frames_page = NestedFramesPage(driver)
    frames_page.goto()

    assert frames_page.left_frame_text() == "LEFT", "expected frame-left body text to read LEFT"
    assert frames_page.middle_frame_text() == "MIDDLE", "expected frame-middle #content text to read MIDDLE"
    assert frames_page.right_frame_text() == "RIGHT", "expected frame-right body text to read RIGHT"
    assert frames_page.bottom_frame_text() == "BOTTOM", "expected frame-bottom body text to read BOTTOM"
