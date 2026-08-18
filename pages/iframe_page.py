from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

BODY = (By.TAG_NAME, "body")
CONTENT = (By.ID, "content")


class NestedFramesPage(BasePage):
    """the-internet.herokuapp.com/nested_frames — a frame-top containing three
    child frames, plus a sibling frame-bottom. Demonstrates drilling through
    more than one level of frame nesting with switch_to.frame, and returning
    to the top document with switch_to.default_content() between reads.
    """

    URL = "https://the-internet.herokuapp.com/nested_frames"

    def _read_top_child_frame(self, frame_name: str, locator: tuple[str, str]) -> str:
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame-top")
        self.driver.switch_to.frame(frame_name)
        text = self.wait().until(EC.visibility_of_element_located(locator)).text
        self.driver.switch_to.default_content()
        return text

    def left_frame_text(self) -> str:
        return self._read_top_child_frame("frame-left", BODY)

    def middle_frame_text(self) -> str:
        return self._read_top_child_frame("frame-middle", CONTENT)

    def right_frame_text(self) -> str:
        return self._read_top_child_frame("frame-right", BODY)

    def bottom_frame_text(self) -> str:
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("frame-bottom")
        text = self.wait().until(EC.visibility_of_element_located(BODY)).text
        self.driver.switch_to.default_content()
        return text
