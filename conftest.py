import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from fixtures.test_data import SAUCEDEMO_VALID, THE_INTERNET_INVALID, THE_INTERNET_VALID
from utils.files import make_temp_upload_file

RESULTS_PATH = Path(__file__).parent / "results" / "results.json"


@pytest.fixture
def driver() -> Iterator[WebDriver]:
    """Function-scoped WebDriver — a fresh browser instance per test, which is what
    makes this suite safe under pytest-xdist (`-n auto`): each worker/test gets its
    own isolated Chrome process, driver via Selenium Manager (Selenium 4.6+), no
    manually downloaded/pinned driver binaries.
    """
    options = Options()
    if os.environ.get("HEADLESS", "true").lower() != "false":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    chrome_driver = webdriver.Chrome(options=options)
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture
def valid_credentials():
    return THE_INTERNET_VALID


@pytest.fixture
def invalid_credentials():
    return THE_INTERNET_INVALID


@pytest.fixture
def saucedemo_credentials():
    return SAUCEDEMO_VALID


@pytest.fixture
def upload_file(tmp_path) -> Path:
    """A fresh temp file per test — no shared fixture state across parallel workers."""
    return make_temp_upload_file(tmp_path)


# ---------------------------------------------------------------------------
# results/results.json reporting
#
# Uses pytest_terminal_summary rather than pytest_runtest_makereport because
# it only fires once, in the controller process, after pytest-xdist has
# already forwarded and aggregated every worker's reports into
# terminalreporter.stats — collecting reports the naive way would silently
# drop everything but the last worker's results when run with -n auto.
# ---------------------------------------------------------------------------

_session_start = 0.0


def pytest_sessionstart(session: pytest.Session) -> None:
    global _session_start
    _session_start = time.time()


def pytest_terminal_summary(terminalreporter, exitstatus: int, config: pytest.Config) -> None:
    status_map = {"passed": "passed", "failed": "failed", "error": "failed", "skipped": "skipped"}
    tests: list[dict[str, Any]] = []
    for status, reports in terminalreporter.stats.items():
        if status not in status_map:
            continue
        for report in reports:
            if getattr(report, "when", "call") not in ("call", "setup"):
                continue
            if report.when == "setup" and report.outcome == "passed":
                continue
            tests.append(
                {
                    "name": report.nodeid,
                    "status": status_map[status],
                    "duration": round(report.duration, 4),
                }
            )

    passed = sum(1 for t in tests if t["status"] == "passed")
    failed = sum(1 for t in tests if t["status"] == "failed")
    skipped = sum(1 for t in tests if t["status"] == "skipped")

    payload = {
        "stack": "selenium-python",
        "platform": "web",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "total": len(tests),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "duration_seconds": round(time.time() - _session_start, 4),
        "tests": tests,
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
