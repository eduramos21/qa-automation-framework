"""Login. These start logged out, so they use the plain page fixture."""

import re

from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_a_valid_user_reaches_the_inventory_page(page: Page) -> None:
    login = LoginPage(page)

    login.goto()
    login.sign_in("standard_user", "secret_sauce")

    expect(page).to_have_url(re.compile(r"inventory\.html"))


def test_a_locked_out_user_sees_an_error_and_stays_on_the_login_page(page: Page) -> None:
    login = LoginPage(page)

    login.goto()
    login.sign_in("locked_out_user", "secret_sauce")

    expect(login.error).to_contain_text("locked out")
    expect(page).not_to_have_url(re.compile(r"inventory\.html"))


def test_a_wrong_password_does_not_say_which_field_was_wrong(page: Page) -> None:
    login = LoginPage(page)

    login.goto()
    login.sign_in("standard_user", "not_the_password")

    # Leaking which half of the pair was wrong hands an attacker a user list.
    expect(login.error).to_contain_text("Username and password do not match")
