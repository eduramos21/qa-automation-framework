# Suite audit: saucedemo-web-ts

Date: 2026-09-08   Stack: `ts-playwright`   Suite: `examples/web-ts`
9 tests across 3 spec files plus one setup, 4 page objects, 0 skipped.
Full run: 2.6 seconds on 5 workers. CI: 4 runs, 4 green.

*Produced by `/qa:audit examples/web-ts`.*

## The short version

The mechanics are in good shape. Nothing sleeps, nothing shares state, every test
asserts something specific, and a fresh clone gets to green in one command. What
this suite cannot do is tell you whether the thing CART-142 is actually about
works, because the rounding rule scored the highest risk in the whole design and
has no test anywhere: it belongs at the unit layer, and this project has no unit
layer to put it in. Three defects found by exploring the same feature also have
no regression test. As a release signal, this suite currently answers "can a user
get through checkout", which is worth having and is not the question the
requirement asked.

## Score

| Area | Score | Why |
|---|---|---|
| It runs | 5 | `npm ci`, `playwright install chromium`, `npx playwright test`. Green from a fresh clone, documented in the README, no credentials needed |
| Speed | 5 | 2.6 seconds. Login happens once in `tests/auth.setup.ts` and is reused through storage state, so no test pays for it twice |
| Reliability | 4 | 4 CI runs, 4 green, no reruns. Not a 5 because the target is a third party site nobody here controls. The weekly scheduled run in `demo-web.yml` is the mitigation and it has not been exercised yet |
| It actually checks something | 5 | `qa-policy --stack web` reports no violations. Every test has a specific assertion. `checkout.spec.ts:60` checks that the three displayed numbers agree with each other, not only that each matches a constant, which is the assertion most suites miss |
| Layers | 2 | Everything is e2e. 8 of the 13 rows in `CART-142-design.md` are unit rows with nowhere to go. See finding 1 |
| Isolation | 5 | `fullyParallel: true`, no `beforeEach` login, no shared fixtures, no order dependence. `qa-policy` finds no shared state. Tests of login live in a separate project from tests that need a session, so neither has to work around the other |
| Waiting | 5 | No sleeps. Every wait is a retrying assertion. `retries` is 1 in CI and 0 locally, so a flake is visible to whoever caused it |
| Maintainability | 4 | Page objects hold locators and actions and no assertions. `CheckoutPage` covers three URLs and says in a comment why. Not a 5 because `reachTheOverview` in `checkout.spec.ts:22` is a local helper that will be copied into the next spec file that needs it, and it should be a fixture before that happens |
| Coverage against requirements | 2 | 3 of 13 design rows covered. The three highest risk rows, T4, T6 and T8 in `CART-142-design.md`, are the rounding cases, and only T8 has a test. Three bugs from `session-2026-09-08-checkout-state.md` have none |

## Findings

| # | Finding | Evidence | Cost of leaving it | Effort |
|---|---|---|---|---|
| 1 | No unit layer, so the tax rounding rule has no test at all | `CART-142-design.md` rows T1 to T7 and T13, marked unit, none written. `CART-142-generated.md` says why | This is the highest risk item in the requirement, scored 9. A rounding error is one cent per order, nobody reports it, and finance finds it at month end. Right now nothing in this repo would catch it | Medium. The tests are trivial, the work is deciding which repo holds the calculation |
| 2 | Three known defects have no regression test | F1, F2, F3 in `session-2026-09-08-checkout-state.md`. Confirming twice via the back button, confirming with a cart emptied elsewhere, and confirming an empty cart | Whatever fixes these can regress silently. All three are cheap e2e tests, and they are e2e for the right reason: they are about page state and navigation | Low. Half a day |
| 3 | One browser, one account | `playwright.config.ts:38`, only a `chromium` project. Every test uses `standard_user` | The site ships `problem_user`, `error_user`, `performance_glitch_user` and `visual_user` specifically to behave badly, and none is exercised. A suite that only ever sees the happy account will not notice the day the unhappy ones break | Low for the accounts, medium for browsers |
| 4 | `reachTheOverview` is a helper, not a fixture | `checkout.spec.ts:22` | It works today with one caller. The second spec file that needs a cart at checkout will copy it, and then there are two. This is how a suite grows the duplication that later needs an audit to find | Low, and it is much lower now than later |
| 5 | Login has three tests and no field validation | `tests/anonymous/login.spec.ts` | Empty username, empty password, and whitespace only are not covered. These are the cheapest tests in any suite and are usually the first thing a new joiner adds, so their absence reads as a gap in the pattern rather than a decision | Low |
| 6 | The inventory sort control has no coverage anywhere | No test references it. Noted in the exploratory session as never touched | Unknown risk rather than known low risk, which is worse. Nobody can say whether it works | Low to find out, unknown to fix |

Ranked by cost over effort. Finding 2 is cheaper than finding 1 and worth doing
first for that reason, even though finding 1 is the more serious gap.

## What is good

**Login is not repeated per test.** `tests/auth.setup.ts` signs in once and saves
storage state, and the `signed-in` project picks it up. This is the single most
common reason an e2e suite takes twenty minutes, and it was handled up front
rather than after it hurt.

**The tests of login start logged out, in their own project.** The usual bodge is
one project plus a conditional logout, which puts a branch in the setup path.
Splitting them costs ten lines of config and removes the branch.

**`testIdAttribute` is wired to the config.** `policies.test_id_attribute` in
`qa.config.yml` and `use.testIdAttribute` in `playwright.config.ts` agree, and
there is a comment saying why they have to. Where these drift, `getByTestId`
finds nothing and fails with a timeout that points nowhere.

**Provisional expectations are labelled.** `checkout.spec.ts:50` carries a
comment saying the expected tax depends on CART-142 Q2, which is unanswered. When
it fails, the reader goes to the requirement rather than debugging the app.

**Nothing is skipped.** No `.skip`, no `.only`, no quarantine list. Rare.

## Coverage gaps

| Source | Condition | Status |
|---|---|---|
| `CART-142-design.md` T1, T2 | Item total sums the listed prices | no test |
| `CART-142-design.md` T3, T4, T5, T6 | Tax is 8% rounded half up, at the boundaries | no test. T4 and T6 score 9, the highest in the design |
| `CART-142-design.md` T7 | Total uses the displayed tax, not the raw one | no test |
| `CART-142-design.md` T13 | Tax rate comes from configuration | no test |
| `CART-142-design.md` T11 | Empty cart cannot reach the overview | deliberately deferred, waiting on Q4 |
| `CART-142-requirement.md` AC4, second half | Confirmation repeats the total | untestable, the page shows no amount. Q5, open |
| `session-2026-09-08-checkout-state.md` F1, F2, F3 | The three confirm time defects | no test |
| everywhere | Inventory sort order | no test, never explored |

Nothing here is a hole in what was written. Every row was a decision, recorded in
the design or the generation report. The gap is that the decisions have not been
acted on since.

## Suggested order

**1. Write regression tests for F2 and F3.** Two e2e tests, they belong at this
layer, and they cover live defects. Do this before the fixes land so the fixes
have something to prove themselves against.

**2. Decide where the rounding tests live.** They do not belong here and they do
not belong nowhere. This needs a conversation with whoever owns the calculation,
not more test code. Until it happens, finding 1 stays open and the suite cannot
answer the question CART-142 asked.

**3. Turn `reachTheOverview` into a fixture.** Ten minutes now, and it stops the
next spec file from copying it.

Findings 3, 5 and 6 are worth doing and are not urgent. Finding 6 in particular
should start as an exploratory session rather than as tests, because nobody knows
what the sort control is supposed to do.
