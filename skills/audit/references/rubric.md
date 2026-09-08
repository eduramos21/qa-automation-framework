# Suite audit rubric

Nine areas, scored 1 to 5. The point of a rubric is that two people auditing the
same suite land in roughly the same place, and that a suite re-audited in six
months can be compared to itself.

Score against what you can evidence. If you cannot find out, score it "not
assessed" and say why, do not guess a 3.

## 1. It runs

| 5 | Fresh clone, install, run, green. One command, documented |
| 4 | Green after one documented extra step |
| 3 | Green after some undocumented fiddling |
| 2 | Only runs on a machine that was already set up |
| 1 | Nobody present can get it green |

Everything else is worth less if this is under 3, because a suite a new joiner
cannot run is a suite they will stop trusting within a month.

## 2. Speed

Against `policies.max_test_runtime_s` and against how often people need to run it.

| 5 | Full suite in under 5 minutes, or well parallelised and under 10 |
| 4 | Under 15 minutes |
| 3 | Under 30 minutes, and someone is watching it |
| 2 | Over 30 minutes, run nightly because it cannot run per commit |
| 1 | Nobody runs the whole thing |

## 3. Reliability

| 5 | No known flakes. Reruns are rare and investigated |
| 4 | Under 1% of runs fail for a reason other than a real defect |
| 3 | A handful of known flaky tests, tracked, with owners |
| 2 | Rerunning red builds is normal and nobody flags it |
| 1 | Red is the default state and the build is ignored |

Score 2 or below has a cost beyond the suite: the team stops reading failures at
all, so the one real failure gets rerun with the rest.

## 4. It actually checks something

| 5 | Every test asserts something specific. Assertions are tight |
| 4 | A few loose assertions, no missing ones |
| 3 | Some tests drive the app with weak or partial checks |
| 2 | Tests exist that assert nothing, or assert things that cannot fail |
| 1 | The suite is green because it is not looking |

Evidence: `qa-policy` `no_assertion` output, plus a read of the loosest
assertions you can find. `toBeVisible` on a container that is always there is the
usual shape.

## 5. Layers

| 5 | Most checks at the lowest layer that can see them. E2e is a thin top |
| 4 | Mostly right, a few things tested higher than needed |
| 3 | Heavy at e2e but the cheap layers exist |
| 2 | Almost everything is e2e |
| 1 | Everything is e2e and the suite is slow and flaky because of it |

This is usually the root cause behind a low speed and reliability score, which
makes it the finding worth fixing rather than its symptoms.

## 6. Isolation

| 5 | Every test standalone. Runs in parallel. Cleans up after itself |
| 4 | Parallel safe, some leftover data |
| 3 | Parallel with a few known exceptions |
| 2 | Must run in order, or shares a fixed account or record |
| 1 | Order dependent and nobody knows the required order |

Evidence: `qa-policy` `shared_mutable_state`, plus whether the runner is actually
configured for parallelism.

## 7. Waiting

| 5 | No fixed sleeps. Waits are conditions |
| 4 | One or two sleeps, each with a comment saying why |
| 3 | A handful of sleeps |
| 2 | Sleeps are the normal way to wait here |
| 1 | Sleeps plus retries plus timeouts raised to make it pass |

Evidence: `qa-policy` `hard_sleeps`, plus the retry setting in the runner config.

## 8. Maintainability

| 5 | A new joiner adds a test by copying a neighbour and it fits |
| 4 | Clear patterns, a little duplication |
| 3 | Patterns exist but are applied inconsistently |
| 2 | Every test is its own shape. Locators repeated everywhere |
| 1 | Only the original author can change it safely |

Evidence: pick the three most recently added tests. If they look like three
different codebases, that is the score.

## 9. Coverage against requirements

Not line coverage. Whether the conditions in the requirements have tests.

| 5 | Traceable. Every high risk condition has a test, and gaps are deliberate |
| 4 | High risk covered, some gaps unrecorded |
| 3 | The main flows are covered, nobody has checked against requirements |
| 2 | Coverage follows whatever was easy to automate |
| 1 | Nobody can say what this suite covers |

Score 3 is where most suites are, and moving to 4 is usually one afternoon of
reading requirements next to the test list.

## Reading the total

Do not publish the total. It invites arguing about the number instead of fixing
the thing. Publish the nine scores and the ranked findings.

If you must summarise: any area at 1 or 2 is what to talk about. A suite with
eight fours and one two has one problem, not an average of 3.8.
