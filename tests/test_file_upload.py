from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from pages.upload_page import UploadPage


def test_file_upload_shows_uploaded_filename(driver: WebDriver, upload_file: Path) -> None:
    upload_page = UploadPage(driver)
    upload_page.goto()

    upload_page.upload(upload_file)

    assert upload_page.uploaded_file_name() == upload_file.name, (
        "expected the uploaded-files panel to show the name of the file we uploaded"
    )
