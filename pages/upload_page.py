from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class UploadPage(BasePage):
    """the-internet.herokuapp.com/upload."""

    URL = "https://the-internet.herokuapp.com/upload"

    FILE_INPUT = (By.ID, "file-upload")
    UPLOAD_BUTTON = (By.ID, "file-submit")
    UPLOADED_FILES = (By.ID, "uploaded-files")

    def upload(self, file_path: Path) -> None:
        self.driver.find_element(*self.FILE_INPUT).send_keys(str(file_path))
        self.driver.find_element(*self.UPLOAD_BUTTON).click()

    def uploaded_file_name(self) -> str:
        return self.wait().until(EC.visibility_of_element_located(self.UPLOADED_FILES)).text
