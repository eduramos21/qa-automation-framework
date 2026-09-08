# examples/web-python

A real, running pytest suite built to the `py-pytest-playwright` profile. It
points at [saucedemo.com](https://www.saucedemo.com), a public demo shop, so you
can clone this and get a green run with no setup and no credentials.

Same five behaviours as `examples/web-ts`, in a different stack, driven by the
same agents. That is the point of the profile system.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest
```

Five tests, about four seconds. `pytest -n auto` runs them in parallel.

```bash
pytest -k locked_out                       # one test
pytest --headed                            # watch it
pytest --tracing=retain-on-failure         # then: playwright show-trace <path>
```

## What is in here

```
qa.config.yml              points at the py-pytest-playwright profile
pytest.ini                 test paths, markers, default browser
conftest.py                test id attribute, per worker auth state
pages/                     LoginPage, InventoryPage
tests/test_login.py        starts logged out, uses the plain page fixture
tests/test_cart.py         needs a session, uses signed_in_page
```

## The parts worth looking at

**The test id attribute is set from the config.** saucedemo uses `data-test`,
and pytest-playwright looks for `data-testid`. Without the override in
`conftest.py`, every `get_by_test_id` would find nothing and fail with a
timeout that tells you nothing about the real cause.

**Auth is per worker, not per test.** `auth_state` signs in once and saves
storage state to `.auth/<worker_id>.json`. The worker id matters: under
`pytest -n auto` all workers would otherwise write the same file at the same
moment, and that race surfaces later as a rare auth failure nobody can
reproduce.

**No sleeps.** Every wait is an `expect()` from `playwright.sync_api`, which
retries on its own. `assert locator.is_visible()` checks once and races.

**Page objects hold no assertions.** They expose locators and actions. The test
decides what should be true.
