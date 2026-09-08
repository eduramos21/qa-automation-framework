"""Shared fixtures.

Two things happen here that are easy to get wrong elsewhere:

1. The test id attribute is set to match policies.test_id_attribute in
   qa.config.yml. saucedemo tags with data-test, and pytest-playwright looks for
   data-testid unless told otherwise, so without this every get_by_test_id call
   would quietly find nothing.

2. Login happens once per session and is handed to tests as saved storage state,
   not repeated through the UI in every test.
"""

import os
from collections.abc import Iterator
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, Playwright, expect

from pages.login_page import LoginPage

BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com")
AUTH_DIR = Path(".auth")


@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright: Playwright) -> None:
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def auth_state(browser: Browser, worker_id: str) -> str:
    """Sign in once per worker and hand back the saved session.

    The file is named after the xdist worker. Under pytest -n auto every worker
    would otherwise write the same path at the same time, which is a race that
    shows up as a rare, unexplainable auth failure.
    """
    AUTH_DIR.mkdir(exist_ok=True)
    auth_file = AUTH_DIR / f"{worker_id}.json"

    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()

    login = LoginPage(page)
    login.goto()
    login.sign_in(
        os.environ.get("E2E_USER", "standard_user"),
        os.environ.get("E2E_PASSWORD", "secret_sauce"),
    )
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")

    context.storage_state(path=str(auth_file))
    context.close()

    return str(auth_file)


@pytest.fixture
def signed_in_page(browser: Browser, auth_state: str) -> Iterator[Page]:
    """A page that is already logged in. Fresh context, so tests stay isolated."""
    context = browser.new_context(base_url=BASE_URL, storage_state=auth_state)
    page = context.new_page()
    yield page
    context.close()
