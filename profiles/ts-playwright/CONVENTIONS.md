# Conventions for ts-playwright

How tests get written in this stack. `profile.yaml` says where files go and how
to run them. This says what the code inside them looks like.

Working example of everything below: `examples/web-ts/`.

## Test file shape

One file per feature area. Named after the area, not after the page.

```ts
// tests/login.spec.ts
import { expect, test } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('login', () => {
  test('a valid user reaches the inventory page', async ({ page }) => {
    const login = new LoginPage(page);

    await login.goto();
    await login.signIn('standard_user', 'secret_sauce');

    await expect(page).toHaveURL(/inventory\.html/);
  });
});
```

Three blocks separated by blank lines: arrange, act, assert. If a test needs a
fourth block it is testing two things and should be two tests.

## Naming

- Files: `tests/<area>.spec.ts`, lowercase, no `test_` prefix.
- `describe`: the area, lowercase, one word where possible.
- Test titles: a sentence describing the behaviour, present tense, no "should".
  `'a locked out user sees an error'`, not `'should show error'`.
- Page objects: `pages/LoginPage.ts`, class `LoginPage`, one per meaningful
  screen.

The title is what shows up in a failing CI run at 2am. Write it so someone can
tell what broke without opening the file.

## Locators

Order in `profile.yaml`. In practice:

```ts
page.getByRole('button', { name: 'Login' })   // first choice
page.getByLabel('Password')                    // form fields with a label
page.getByTestId('inventory-item')             // when the DOM has no semantics
page.locator('.inventory_item')                // last resort, add a comment saying why
```

Banned:

- Absolute or positional XPath. `//div[3]/span` breaks on any layout change.
- CSS chains longer than two parts. `.a > .b > .c > span` is the same problem.
- Anything matching on generated class names, the `css-1x2y3z` kind.

`testIdAttribute` in `playwright.config.ts` must match
`policies.test_id_attribute` in `qa.config.yml`. They drift and then every
`getByTestId` silently misses.

## Waiting

There are no fixed sleeps in this stack. Not one.

```ts
await expect(cart.badge).toHaveText('1');        // yes, retries until timeout
await page.waitForTimeout(2000);                 // no
```

`expect(locator)` assertions retry on their own. That is the wait. If you need
to wait for something that is not an assertion, wait for the thing itself:
`page.waitForURL`, `page.waitForResponse`, `locator.waitFor`.

If a test only passes with a sleep in it, the sleep is hiding a real race and
the app probably has a bug worth reporting.

## Page objects

A page object earns its existence when two or more tests touch the same screen,
or when one screen needs more than three locators. Below that, put the locator
in the test and move on. A page object per page whether or not it holds anything
is just more files to open.

What goes in:

```ts
import { type Locator, type Page } from '@playwright/test';

export class LoginPage {
  readonly username: Locator;
  readonly password: Locator;
  readonly submit: Locator;
  readonly error: Locator;

  constructor(private readonly page: Page) {
    this.username = page.getByPlaceholder('Username');
    this.password = page.getByPlaceholder('Password');
    this.submit = page.getByRole('button', { name: 'Login' });
    this.error = page.getByTestId('error');
  }

  async goto() {
    await this.page.goto('/');
  }

  async signIn(user: string, pass: string) {
    await this.username.fill(user);
    await this.password.fill(pass);
    await this.submit.click();
  }
}
```

What stays out:

- Assertions. The page object exposes locators, the test decides what is true.
  A `assertLoginFailed()` method hides the expectation from the test that owns
  it.
- Waits and retries. See above, the assertion is the wait.
- Test data. Pass it in.

Locators are fields assigned in the constructor. Playwright locators are lazy,
so building them early costs nothing and gives you one place to fix a selector.

## Fixtures and setup

Logging in through the UI in `beforeEach` is the most common reason a suite
takes ten minutes. Do it once with a setup project and reuse the storage state:

```ts
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /.*\.setup\.ts/ },
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'], storageState: '.auth/user.json' },
    dependencies: ['setup'],
  },
],
```

Anything a test needs beyond that goes in a custom fixture under `fixtures/`,
not in a helper function the test has to remember to call.

Keep `.auth/` out of git.

## Assertions

Assert on the locator, not on a value you pulled out of it:

```ts
await expect(page.getByTestId('cart-badge')).toHaveText('1');   // retries
expect(await page.getByTestId('cart-badge').textContent()).toBe('1');  // races
```

Web first assertions retry until the timeout. The `await expect(...)` form is
the only one that should appear against page state.

Never put an assertion inside an `if`. A test that can skip its own check is a
test that passes when the feature is gone.

## Test data

No test depends on data another test created, and no test depends on running
after another. Files run in parallel by default and that is left on.

Data that has to exist goes in through the API in a fixture, not through the UI,
and gets cleaned up in the same fixture's teardown. Unique values come from a
per worker seed so parallel workers do not collide.

## What not to do

- `waitForTimeout`. Covered above, but it is the number one thing that shows up
  in a suite audit.
- `test.only` left in a file. It silently drops the rest of the suite. CI should
  run with `--forbid-only`.
- Soft assertions everywhere. `expect.soft` is for collecting several checks in
  one pass, not for making a red test yellow.
- A single test that walks through six screens. When it fails you learn that
  something in the app is broken, which you already knew. Split it.
- Retries set above 1 in the config to make a flaky suite look green. Retries
  hide the flake, they do not fix it. Use `flake-triage` instead.
- Screenshots or videos on every run. Turn them on for failures only, the
  artifacts get big fast.
