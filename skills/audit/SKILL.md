---
description: Audit an automated test suite and score it against a rubric. Finds sleeps, duplication, missing assertions, tests at the wrong layer, coverage gaps against requirements, and what is slow. Use when asked to audit, review or assess a suite, when inheriting one, or when a suite is slow or flaky and nobody knows why.
---

# Audit a suite

Input: `$ARGUMENTS`. A path, a stack name, or nothing for every stack in the
config.

## Delegate this one

Hand it to the `suite-auditor` agent. An audit reads the whole suite, the
config, the profile, the CI history and the requirements, and almost none of
that needs to come back into this conversation. What comes back is the report.

Do it inline only when the user wants to look at one specific thing.

## What comes out

A report at `qa/audit/<date>.md`, with nine rubric scores, ranked findings with
evidence, coverage gaps against the requirements, and a suggested order for the
first three fixes.

The rubric is in `references/rubric.md`. It exists so two audits of the same
suite land in the same place, and so a suite re-audited in six months can be
compared against itself.

## The mechanical pass

Before any reading:

```bash
qa-context <platform>
qa-policy --stack <platform>
```

`qa-policy` finds sleeps, positional locators, tests with no assertion,
conditional assertions and shared state. Two of its five checks are heuristics
and it labels them, so verify those rather than repeating them into the report.

## Rules

**Evidence or it is not a finding.** A path and a line, or a command someone can
run. "Tests are flaky" is not a finding.

**Rank by cost over effort, not by severity.** A hundred two second sleeps beat
one missing assertion, even though the missing assertion sounds worse.

**Say what is good.** A report that only lists problems gets read as unfair and
then gets ignored.

**Change nothing.** Not even a one line fix. The report is the deliverable, and
mixing edits in means nobody can review either.

**No total score.** Publish the nine, not the average. An average invites an
argument about the number instead of a fix.

## Next

`/qa:fix` for the findings that are actual failures. For the structural ones,
the report's suggested order is the plan.

If the audit turns up that the suite's real conventions differ from the profile's
`CONVENTIONS.md`, that is not an audit finding about the suite, it is a wrong
profile. Run `/qa:profile`.
