# Conventions for py-pytest-playwright

How tests get written in this stack. `profile.yaml` says where files go and how
to run them. This says what the code inside them looks like.

Working example of everything below: `examples/web-python/`.

## Test file shape

One file per feature area.

```python
# tests/test_login.py
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage


def test_valid_user_reaches_the_inventory_page(page: Page) -> None:
    login = LoginPage(page)

    login.goto()
    login.sign_in("standard_user", "secret_sauce")

    expect(page).to_have_url(re.compile(r"inventory\.html"))
```

Arrange, act, assert, separated by blank lines. A fourth block means it is two
tests.

Plain functions, not classes. `unittest.TestCase` style classes lose the fixture
injection that makes pytest worth using.

## Naming

- Files: `tests/test_<area>.py`.
- Test functions: `test_<behaviour_in_words>`. The function name is the report
  line, so `test_a_locked_out_user_sees_an_error` beats `test_login_2`.
- Page objects: `pages/login_page.py`, class `LoginPage`.
- Fixtures: named for what they give you, `logged_in_page`, not `setup`.

## Locators

Order in `profile.yaml`. In practice:

```python
page.get_by_role("button", name="Login")
page.get_by_label("Password")
page.get_by_test_id("inventory-item")
page.locator(".inventory_item")   # last resort, comment why
```

Banned: positional XPath, CSS chains longer than two parts, generated class
names.

The plugin looks for `data-testid` by default. If `policies.test_id_attribute`
in `qa.config.yml` says something else, override it in `conftest.py`:

```python
@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute("data-test")
```

## Waiting

No `time.sleep`. No `page.wait_for_timeout`.

```python
expect(cart.badge).to_have_text("1")   # retries until timeout
time.sleep(2)                           # no
```

`expect()` from `playwright.sync_api` retries. `assert` does not. If you need to
wait for something that is not an assertion, wait for that thing:
`page.wait_for_url`, `page.expect_response`, `locator.wait_for`.

## Page objects

Earns its existence at two or more tests on the same screen, or more than three
locators on one screen. Below that, put the locator in the test.

```python
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
```

Out: assertions, waits, hardcoded test data. The page object exposes locators
and actions, the test decides what is true.

Type hints on locators and method signatures. They are what makes a page object
navigable in an editor, and they are cheap.

## Fixtures and setup

Session scoped work goes in `conftest.py`. A logged in session is a fixture, not
a call at the top of every test:

```python
@pytest.fixture
def logged_in_page(page: Page) -> Page:
    login = LoginPage(page)
    login.goto()
    login.sign_in(os.environ["E2E_USER"], os.environ["E2E_PASSWORD"])
    return page
```

For a suite where login is slow, reuse storage state instead of repeating the
UI login. `browser.new_context(storage_state="...")` in a session fixture.

Anything a fixture creates, the same fixture removes after the yield. A test
that leaves rows behind is a test that breaks the next run.

## Assertions

Use `expect()` for page state, plain `assert` for values you computed yourself.

```python
expect(page.get_by_test_id("cart-badge")).to_have_text("1")     # retries
assert page.get_by_test_id("cart-badge").text_content() == "1"  # races
```

No assertion inside an `if`. A test that can skip its own check passes when the
feature is gone.

## Test data

Nothing depends on another test having run. `pytest -n auto` is the target, and
that only works if every test stands alone.

Unique values come from the worker id (`worker_id` fixture from xdist) so
parallel workers do not collide on the same email or SKU.

## What not to do

- `time.sleep`. The single most common finding in a suite audit.
- Bare `assert page.locator(...).is_visible()`. It checks once and returns
  False the moment the page is a frame behind. `expect(...).to_be_visible()`
  retries.
- `@pytest.mark.skip` with no reason and no ticket. A skipped test is a lie the
  suite tells about its coverage.
- One fixture called `setup` that does eight things. Name fixtures after what
  they hand back.
- `--reruns` from pytest-rerunfailures used to make a flaky suite green. It
  hides the flake. Use `flake-triage`.
- Page objects that inherit from a `BasePage` full of wrappers around
  `page.click`. The Playwright API is already the wrapper.
