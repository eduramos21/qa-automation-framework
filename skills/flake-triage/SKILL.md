---
description: Work out why a test is failing or flaky before changing anything. A decision tree over the five real causes, and the rerun protocol that tells a flake from a real defect. Use when a test fails, when a test passes locally and fails in CI, when a build is red intermittently, or when someone suggests adding a retry.
---

# Why is this test red

Five causes. Work through them in order, because the first is the most common and
the one people skip.

Nothing gets changed until you know which one it is. A fix applied to the wrong
cause makes the test green and loses the information.

## 1. The app is broken

The test is right. This is the good case, and it happens more often than the
reflex "the test is flaky again" suggests.

Check first: did the app change? Look at what shipped since the last green run.
`git log` the files the test touches. If a developer changed that area yesterday
and the test started failing yesterday, that is your answer.

Then look at the failure itself. A wrong value, a missing element that should be
there, a status that did not change. Those are defects until proven otherwise.

If it is this: `bug-report`. Do not touch the test.

## 2. The app changed on purpose

The behaviour is now different and intended. Renamed button, reworked flow,
different copy.

Check: is there a ticket or a commit that says so? If nobody can point at an
intended change, go back to cause 1, because "it was intended" is also what an
unintended change looks like from the outside.

If it is this: update the test to the new intended behaviour. Update the
requirement too if it still describes the old one.

## 3. The test waits badly

The test looks for something before it is there, or after it is gone.

Signs:
- Fails on a slower machine, in CI, or under parallel load.
- Passes when you run it alone, fails in the suite.
- Passes when you watch it headed, fails headless.
- The failure is a timeout on a locator rather than a wrong value.
- There is already a sleep in it, and the fix being proposed is a longer sleep.

The fix is a condition, never a duration. Wait for the state you actually need:
the element attached, the request finished, the URL changed, the assertion true.
Every runner has a retrying assertion, use it.

If the only thing that works is a sleep, stop. That is a race in the app, and the
race exists for real users too. It is cause 1 wearing a disguise.

## 4. The test is not isolated

It depends on data, on another test, or on the order.

Signs:
- Passes alone, fails in the suite, and it is not a timing problem.
- Fails only when run in parallel.
- Fails the second time you run it but not the first, or the other way round.
- Fails on a fresh environment but not on yours.
- Two tests use the same account, record, or fixed identifier.

The fix is in the fixture, not in the test. Give it its own data, make the
identifier unique per worker, clean up after the yield. Making the suite run
serially to avoid this is not a fix, it is paying for the bug forever in wall
clock time.

## 5. The environment

The test and the app are both fine and something around them is not. A service
down, a certificate expired, a rate limit, a full disk, a browser version bump.

Signs: several unrelated tests fail at once, the failure is a network or driver
error, or it started at the same moment across the suite.

Say so plainly. Do not encode a workaround in the test, because the workaround
outlives the outage and nobody remembers what it was for.

## The rerun protocol

For an intermittent failure, one run tells you nothing. Before deciding anything:

```
run it 10 times alone
run it 10 times inside the full suite
run it 10 times with parallelism turned up
```

Then read the pattern:

| Alone | In the suite | Parallel | Cause |
|---|---|---|---|
| fails | fails | fails | 1 or 2, a real difference |
| passes | fails | fails | 4, isolation |
| passes | passes | fails | 3 or 4, timing under load |
| passes | passes | passes | 5, or it is already fixed. Check what changed |

Record the numbers. "Flaky" with no rate behind it cannot be prioritised, and it
is how a test ends up quarantined for two years.

## What not to do

**Do not add a retry.** A retry makes the suite green and ships the race to
users. Retry counts above one in a runner config are a suite level admission that
nobody triaged.

**Do not raise the timeout.** Occasionally right, usually a way of not asking why
it got slower.

**Do not quarantine and forget.** If a test is skipped, it needs an owner and a
date, and it should be deleted if neither exists. A skipped test is a lie the
suite tells about its coverage.

**Do not fix it in the test if the cause is in the app.** The most expensive
outcome of this whole process is a real defect turned into a passing test.
