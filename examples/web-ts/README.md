# examples/web-ts

A real, running Playwright suite built to the `ts-playwright` profile. It points
at [saucedemo.com](https://www.saucedemo.com), which is a public demo shop, so
you can clone this and get a green run without any setup or credentials.

It exists to prove the profile is not just documentation. Everything
`profiles/ts-playwright/CONVENTIONS.md` claims is in here, including the parts
that are easy to skip.

## Run it

```bash
npm ci
npx playwright install chromium
npx playwright test
```

Nine tests, about three seconds.

```bash
npx playwright test --headed    # watch it
npx playwright show-report      # last report
npx tsc --noEmit                # typecheck
```

## What is in here

```
qa.config.yml            points at the ts-playwright profile
playwright.config.ts     three projects: setup, anonymous, signed-in
pages/                   LoginPage, InventoryPage
tests/auth.setup.ts      logs in once, saves storage state
tests/anonymous/         tests of login itself, start logged out
tests/signed-in/         everything else, handed a ready session
```

`tests/signed-in/checkout.spec.ts` was generated from
`../artifacts/CART-142-design.md`. The report on what it did and did not write is
in `../artifacts/CART-142-generated.md`.

## The parts worth looking at

**No UI login per test.** `auth.setup.ts` signs in once and writes
`.auth/user.json`. The `signed-in` project picks that up through `storageState`.
Tests of login itself live in `tests/anonymous/` because they have to start
logged out. This split is why the suite runs in three seconds instead of ten.

**`testIdAttribute` is wired to the config.** saucedemo uses `data-test`, not the
`data-testid` Playwright defaults to. `policies.test_id_attribute` in
`qa.config.yml` and `use.testIdAttribute` in `playwright.config.ts` have to
agree, and when they do not, `getByTestId` misses silently instead of failing
loudly. That is the kind of thing the suite auditor checks.

**No sleeps.** Every wait is an `await expect(locator)` assertion, which retries
until the timeout on its own.

**Page objects hold no assertions.** `LoginPage` exposes an `error` locator. The
test decides what that error should say.
