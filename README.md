# Selenium + Python — Web UI Test Automation

![tests](https://github.com/zanuartri/selenium-python/actions/workflows/tests.yml/badge.svg)

A portfolio-scale UI test suite built with **Selenium 4 + pytest**, targeting two public demo apps: [the-internet.herokuapp.com](https://the-internet.herokuapp.com) and [saucedemo.com](https://www.saucedemo.com). Driver management is handled entirely by **Selenium Manager** (built into Selenium 4.6+) — no manually downloaded or pinned `chromedriver` binary. No credentials or setup on the target sites are required — anyone can clone and run this.

## Structure (Page Object Model)

```
pages/      one class per page, locators + actions, no assertions
tests/      one scenario per file, assertions live here only
fixtures/   test data (credentials) as plain dataclasses
utils/      small stateless helpers (e.g. temp file creation)
conftest.py pytest fixtures (WebDriver setup/teardown, credentials, results.json hook)
```

Locators and page structure change often; assertions and business flow change less often. Splitting them means a selector change touches one `pages/*.py` file instead of every test that uses that page. Page objects never assert — that keeps failure messages in the test file where the *intent* of the check is obvious, and keeps page objects reusable across positive and negative scenarios (e.g. `LoginPage` is used by both the happy-path and invalid-credentials tests).

## Explicit waits vs. Playwright's auto-waiting

Selenium has no built-in auto-waiting: `driver.find_element()` returns (or raises `NoSuchElementException`) the instant it's called, whether or not the element is present, visible, or interactable yet — there's no retry loop hidden inside the API the way there is with Playwright's locators. Every page object in this repo that touches dynamic content (`DynamicLoadingPage`, `AddRemovePage`, `WindowsPage`, the login flash message) goes through `WebDriverWait(driver, timeout).until(expected_conditions.*)`, polling the DOM until the condition holds or the timeout elapses. This is the main skill Selenium demands that Playwright abstracts away — get the wait condition wrong (or skip it and reach for `time.sleep()`) and the suite becomes flaky on a slower CI runner or a fast one alike. There is no `time.sleep()` anywhere in this codebase.

## iframe handling

`pages/iframe_page.py` targets `/nested_frames`, which has a `frame-top` containing three child `<frame>`s (`frame-left`, `frame-middle`, `frame-right`) plus a sibling `frame-bottom`. Selenium can only see elements inside the frame the driver is currently focused on, so reading each frame's text means `driver.switch_to.frame("frame-top")` then `driver.switch_to.frame("frame-middle")` to drill into the nested frame, followed by `driver.switch_to.default_content()` to climb back out to the top document before switching into the next one. Forgetting that reset is the most common iframe bug in Selenium suites — every read in this page object explicitly returns to `default_content()` when it's done.

## Multi-window/tab handling

`pages/windows_page.py` targets `/windows`, where a link opens a second tab. `driver.window_handles` is a list of every open tab/window's opaque handle; a new tab doesn't automatically become the "active" one Selenium commands are sent to. The pattern here: snapshot the handle set before triggering the new tab, `WebDriverWait` until a new handle appears (openings aren't synchronous), diff the before/after sets to find the new handle, then `driver.switch_to.window(new_handle)`. `test_multi_window.py` also demonstrates closing the second tab and switching back to the original one — leaving a stale handle referenced after its tab closes is the other common bug this test guards against.

## Setup

```bash
pip install -r requirements.txt
```

Selenium Manager downloads/locates a matching `chromedriver` automatically the first time Chrome is launched — nothing else to install.

## Run

```bash
pytest                 # serial, headless by default
pytest -n auto         # parallel, via pytest-xdist — each test gets its own WebDriver instance
HEADLESS=false pytest  # watch the browser locally
```

Each run writes `results/results.json`:

```json
{
  "stack": "selenium-python",
  "platform": "web",
  "run_at": "2026-08-18T12:00:00+00:00",
  "total": 13, "passed": 13, "failed": 0, "skipped": 0,
  "duration_seconds": 55.2,
  "tests": [{"name": "tests/test_login.py::test_login_with_valid_credentials_reaches_secure_area", "status": "passed", "duration": 2.9}]
}
```

## CI

`.github/workflows/tests.yml` installs dependencies, runs the suite headless against Chrome (preinstalled on the `ubuntu-latest` runner, picked up automatically by Selenium Manager), and uploads `results/results.json` as a build artifact on every push/PR to `main`. The build fails whenever pytest reports a failure (default pytest exit code). CI runs with `-n 2` rather than `-n auto` — the runner's CPU headroom doesn't comfortably sustain more concurrent real Chrome instances than that without starving each browser's JS execution.

## Parity with the Playwright repos

This repo mirrors the scenarios (and, where the target app allows, the exact tests) in the sibling `playwright-python`/`playwright-js` repos — same demo sites, same test intent — so the three stacks are directly comparable on structure and approach rather than on what's being tested.
