from playwright.sync_api import Locator, Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username: Locator = page.get_by_placeholder("Username")
        self.password: Locator = page.get_by_placeholder("Password")
        self.submit: Locator = page.get_by_role("button", name="Login")
        self.error: Locator = page.get_by_test_id("error")

    def goto(self) -> None:
        self.page.goto("/")

    def sign_in(self, user: str, password: str) -> None:
        self.username.fill(user)
        self.password.fill(password)
        self.submit.click()
