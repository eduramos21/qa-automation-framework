---
description: Pick and apply test design techniques. Equivalence partitioning, boundary values, decision tables, state transitions, pairwise, risk scoring, and choosing which layer a check belongs in. Use when turning a requirement into test cases, deciding what to cover, judging whether a suite covers enough, or when someone asks what to test.
---

# Test design techniques

The job is to get the most information about the product from the fewest tests.
Everything below is a way of not writing the other four hundred cases.

Start from the requirement, not from the UI. If you start from the UI you end up
testing what was built rather than what was asked for, and the two differ in
exactly the places that matter.

## Which technique for which requirement

Read the requirement and look for the shape. Most requirements are one of these,
and a few are several at once.

| The requirement says | Shape | Technique |
|---|---|---|
| A field accepts a range, or a length, or an amount | continuous input | boundary values, then equivalence partitioning |
| A field accepts one of a set | discrete input | equivalence partitioning, one per class |
| If A and B then X, if A and not B then Y | rules | decision table |
| Something moves between statuses | lifecycle | state transition |
| Several independent settings interact | combinations | pairwise |
| Users do this to achieve that | flow | scenario, then error paths off it |
| It must be fast, or handle N | quality attribute | not a functional test, say so and route it |

Never apply a technique because it is thorough. Apply it because the requirement
has that shape. A decision table over a requirement with one rule is ceremony.

## Risk first

Coverage is not the goal. Finding the expensive bug is the goal. Score every
condition before deciding what to automate:

```
risk = likelihood of it being wrong  x  cost when it is wrong
```

Both on 1 to 3. Anything scoring 6 or more gets an automated test. Anything
scoring 1 or 2 probably gets nothing, and saying so out loud is part of the job.

Likelihood goes up with: new code, code changed this sprint, an integration
boundary, anything with a date, a currency, a timezone, or concurrency, and
anything a developer described as "simple".

Cost goes up with: money moving, data lost, a user locked out, a legal or
privacy obligation, silence (the failure nobody notices for a month).

## Which layer

The right test at the wrong layer is a slow test that fails for the wrong
reason. Push each check to the lowest layer that can actually see the thing.

| Check | Layer |
|---|---|
| A calculation, a validation rule, a format | unit |
| A contract between two services | api or contract test |
| Data actually persists and comes back | integration |
| A user can complete the journey | e2e, and only a handful of these |
| It looks right | visual, or a human |
| It feels right, is it confusing, is it usable | exploratory, a human |

If a condition can be checked at the unit layer, an e2e test for it is waste:
slower, flakier, and it fails without telling you which of forty things broke.

## What not to automate

Say this out loud in every design, it is as much of a decision as the rest:

- Anything that runs once, ever.
- Anything where the expected result is a judgement call.
- A screen still being redesigned. Automating it now buys maintenance, not
  information.
- Something already covered at a lower layer.
- A path so rare that the test costs more than the bug.

## The techniques themselves

Details, worked examples, and the traps for each one:

- `references/techniques.md` for equivalence partitioning, boundary values,
  decision tables, state transition and pairwise.
- `references/risk.md` for the scoring table and how to write a risk line that
  a product manager will actually read.

## Output

A test design is a table, not prose. One row per condition:

| ID | Condition | Technique | Risk | Layer | Automate | Notes |
|---|---|---|---|---|---|---|

Plus two lists that people skip and should not: what is deliberately not
covered, and what could not be designed because the requirement is still
ambiguous. The second list is the one that saves a release.
