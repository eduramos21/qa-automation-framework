---
description: Fix failing or flaky tests, and refactor a suite that has grown duplication. Finds the root cause rather than making the test green. Use when a test fails, when a suite has gone flaky, after a UI change broke locators, or when asked to clean up tests.
---

# Fix tests

Input: `$ARGUMENTS`. A failing test, a failure output, a CI run, or nothing, in
which case run the suite and start from what is red.

## When to delegate

More than two or three failures, or a refactor across the suite: hand it to the
`test-maintainer` agent. It will read a lot of files.

One failure the user is watching: do it here.

## The order

**1. Reproduce.** `commands.test_one` from the profile. If it passes locally and
fails in CI, that gap is the finding. CI has no cached session, real parallelism,
a different viewport, a slower machine, possibly a different timezone.

**2. Triage.** Use `flake-triage` to work out which of five things it is. Doing
this before touching anything is the whole discipline, because four of the five
have different fixes and the fifth means not touching the test at all.

**3. Fix the cause, once.** If four tests fail the same way there is one fix,
usually in a page object or a fixture. Grep before editing, the sibling tests are
broken too and nobody has noticed.

**4. Prove it.** Run it. If flake was the complaint, run it several times, one
green run says nothing about an intermittent failure. Then break it on purpose
and confirm it still fails for the right reason.

## Never

**A sleep.** Not a small one, not temporarily. If it only passes with one, there
is a race and it is usually in the app.

**A wider assertion.** Changing `toHaveText` to `toContainText` because it failed
removes the check that found something.

**Retries.** They hide the flake and ship the race.

**Deleting a test to clear a red build.** Deleting a test that duplicates another
or covers a feature that is gone is fine, and is a decision said out loud.

**Changing what a test asserts while refactoring how it is written.** If the
assertion looks wrong, that is a separate change with its own reasoning.

## Report

- The cause, one line per failure. The cause, not the symptom.
- What changed, by path.
- What you found and did not fix, especially siblings broken the same way.
- Bugs filed, if the answer was that the app is broken.
- How you verified.
