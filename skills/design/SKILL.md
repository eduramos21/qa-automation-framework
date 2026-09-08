---
description: Turn a refined requirement into a test design. Produces a risk scored coverage matrix saying what to check, at which layer, and what to automate, plus what is deliberately not covered and which charters to explore by hand. Use after refining a requirement, when planning test coverage, or when the user says test design, test plan, what should we test, or coverage.
---

# Design the tests

Input: `$ARGUMENTS`. A path to a refined requirement, a ticket key, or nothing,
in which case ask which requirement.

The output is a table of conditions with a decision attached to each one. Every
row says what to check, why it matters, where it belongs, and whether it gets
automated. Rows that say "do not test this" count.

## Steps

**1. Read the setup.** Run `qa-context`. The `layout` and `policies` in the
profile decide what an automatable row actually looks like, and which layers
this project has at all.

**2. Read the requirement.** If it has not been through `/qa:refine`, do that
first. Designing against an ambiguous requirement produces a design that has to
be redone.

**3. Find the shape.** Use `test-design-techniques`. For each acceptance
criterion, work out which shape it is (range, set, rules, lifecycle,
combinations, flow) and apply the matching technique. One requirement usually
has several shapes in it.

**4. Look at what already exists.** Before adding a row, check whether the suite
already covers it. Use `layout.tests` and `layout.test_glob` from the profile to
find the tests, and grep for the behaviour, not the file name. Duplicate
coverage is the second most common finding in a suite audit, after sleeps.

**5. Score each condition.** Likelihood times cost, both 1 to 3. See
`references/risk.md` in `test-design-techniques`.

**6. Pick the layer.** Push every check to the lowest layer that can see it. A
validation rule tested through the browser is a slow test that fails for the
wrong reason.

**7. Decide what not to do.** Explicitly. This is the part that keeps the suite
runnable in a year.

**8. Write charters for the rest.** Whatever cannot be pinned to an expected
result is exploratory work, not a gap. Write it as a charter, see `/qa:explore`.

**9. Write it.** To `qa/design/<id>.md`. Tell the user the path.

## Output shape

```markdown
# <ID> test design

Requirement: <path>   Designed: <date>

## Coverage

| ID | Condition | From | Technique | L | C | Risk | Layer | Automate | Exists |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Discount code of 5 characters is rejected | AC2 | boundary | 2 | 2 | 4 | unit | yes | no |
| T2 | ... |

From: which acceptance criterion, so coverage can be traced back.
L and C: likelihood and cost, 1 to 3. Risk is the product.
Layer: unit, api, integration, e2e, visual, manual.
Automate: yes, no, or later, with the reason in Notes if it is not obvious.
Exists: the test that already covers this, or no.

## Not covering

| Condition | Why not |
|---|---|

Reasons that hold: covered at a lower layer, risk score under 3, the screen is
being redesigned, the expected result is a judgement call, it runs once ever.
"No time" is not a design decision, it is a scheduling one, and it belongs in
the ticket rather than here.

## Explore instead

| Charter | Why this is not a scripted test |
|---|---|

## Test data

What each row needs to exist before it runs, and how that gets created and
cleaned up. If two rows need conflicting data, say so here rather than finding
out when they run in parallel.

## Blocked

Conditions that could not be designed because a question is still open. Link the
question in the requirement.
```

## Rules

**Trace every row back.** The From column ties a test to a criterion. A row with
no source is either scope creep or a criterion nobody wrote down, and both are
worth knowing.

**Not everything is e2e.** If a design has fifteen e2e rows, it is wrong. E2e
answers "can a user get through this journey", and you need a handful of those.
Everything else has a cheaper home.

**Say the negative out loud.** A design with an empty "Not covering" table is a
design where nobody made a decision.

**Do not write code.** Conditions and expected results, not test files. That is
`/qa:generate`, which reads this document.

**Keep the risk honest.** If everything scores 9, nothing does. Most rows are 2
to 4 and that is fine.

## Next

- `/qa:generate <this file>` writes the automated rows.
- `/qa:explore <charter>` for the exploratory rows.
