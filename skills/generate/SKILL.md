---
description: Write automated tests from a test design or a described behaviour, in whatever stack the project uses. Use when asked to generate, write or add tests, to automate a design, or to cover a new feature with tests.
---

# Generate tests

Input: `$ARGUMENTS`. A path to a test design, a path to a refined requirement
(a `/qa:refine` doc, with an `## Acceptance criteria` section), pasted
acceptance criteria, a ticket key, or a described behaviour.

## When to delegate

If the input is a design with more than about three rows, or acceptance
criteria with more than about three criteria, hand it to the `test-author`
agent. It reads a lot of files (the profile, the conventions, the existing
suite) and none of that needs to come back into this conversation.

For one to three tests, or when the user is iterating and wants to see each
step, do it here and follow the same rules.

## Steps

**1. Read the setup.** `qa-context <platform>`. Then read the whole
`CONVENTIONS.md` for the resolved profile.

**2. Read the design, or the acceptance criteria.** Three shapes of input:

- A test design from `/qa:design`. Each row already says the condition, the
  layer, and whether to automate it. Use it as is.
- Acceptance criteria, with no design: either a refined requirement's
  `## Acceptance criteria` list, or pasted `AC1. Given... when... then...`
  text. Write one test per criterion directly, at the layer the profile
  defaults to. Do not run risk scoring or pick a layer per row, that is what
  `/qa:design` is for and this path skips it on purpose, so say so in the
  report. The criterion's "then" clause is already required to be an
  observable result (`/qa:refine` enforces that) — use it as the expected
  value. If a "then" is not concrete enough to assert on, that is an open
  question to ask about, never a guess.
- Anything else, a ticket key or a described behaviour with no design and no
  acceptance criteria: run `/qa:design` first, or at minimum agree the
  expected result with the user before writing an assertion against it.

**3. Read the neighbours.** Two or three existing tests from `layout.tests`.
Where they disagree with the conventions file, the existing tests win, and the
gap is worth mentioning.

**4. Write only the automatable rows.** Rows marked `no` or `later` stay
unwritten. Rows at a layer this project does not have stay unwritten, and you say
which and why.

**5. Run it.** `commands.test_one` from the profile, with `{file}` and `{title}`
substituted.

**6. Prove it can fail.** Break the expected value, run again, confirm it goes
red for the right reason, put it back. A locator that matches nothing produces a
test that never asserts anything and passes forever.

**7. Lint.** `commands.lint` if the profile has one.

## Report

- Files written, by path.
- Design rows, or acceptance criteria, covered, by ID.
- Rows not written, and why.
- If this ran straight from acceptance criteria: say so explicitly, "written
  directly from acceptance criteria, no `/qa:design` matrix, no risk or layer
  scoring" — so nobody mistakes it for a design-backed test.
- Anything found on the way: markup with no stable hook, behaviour that differs
  from the design, existing tests that contradict the conventions.
- The command to run them.

## Rules

The full set is in the `test-author` agent. The ones that get broken most:

- Do not promote a unit row to e2e because e2e is the layer you can reach.
- Do not write a test for a row the design said not to automate.
- Do not invent an expected result. A test asserting current behaviour looks
  like coverage and is not.
- No fixed sleeps, ever. If the test only passes with one, the app has a race
  and that is the finding.
- One behaviour per test. An "and" in the title means two tests.
