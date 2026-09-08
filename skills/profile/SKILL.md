---
description: Build a profile from a test suite that already exists, by reading it. Drafts profile.yaml and CONVENTIONS.md describing what the repo actually does, so generated tests match the repo instead of a generic example. Use when a project has tests but no profile fits, when generated code does not match the house style, or when the user says my repo already has tests.
---

# Build a profile from an existing suite

Input: `$ARGUMENTS`. A stack name, a path to a suite, or nothing, in which case
find the suites and ask which one.

Most repos that need this already have hundreds of tests and a house style
nobody wrote down. The job is to write it down, from the code, without
correcting it on the way past.

## The one rule

**Describe what the repo does. Do not prescribe what it should do.**

If their page objects contain assertions, the conventions say page objects
contain assertions. If half the suite uses `data-qa` and the shipped profile
prefers `getByRole`, the conventions say `data-qa`.

You will see things worth changing. Put them in a separate report at the end,
never inside `CONVENTIONS.md`. The moment the conventions file mixes "what we do"
with "what we should do", every agent that reads it writes code in a style the
repo does not use, the reviewer rejects it, and the whole thing gets uninstalled.

Improving the suite is `/qa:audit` and `/qa:fix`. This is not that.

## Steps

**1. Find the starting point.** List the shipped profiles. If one matches the
language and runner, copy it and edit. If none does, start from
`profiles/_template`. Either way the copy goes in `<project>/profiles/<name>/`,
because project profiles win over the plugin's and this description belongs to
this repo.

```bash
cp -r <plugin>/profiles/ts-playwright <project>/profiles/acme-web
```

Name it after the repo or the stack, not after the runner. `acme-web` ages
better than `ts-playwright-2`.

**2. Get the commands right.** These have to be exact, everything downstream
runs them.

| Look at | For |
|---|---|
| `package.json` scripts, `Makefile`, `justfile`, `tox.ini`, `pom.xml` | The command a human actually types |
| CI workflow files | The command CI actually runs, which is often the honest one |
| README | What they think they run, sometimes out of date |

Prefer the wrapper if there is one. If the repo has `npm run e2e`, that is
`commands.test`, not `npx playwright test`. The wrapper usually sets env or
flags that matter.

Work out `test_one` and verify it. A `test_one` that does not actually run a
single test breaks `/qa:fix` in a way that is annoying to diagnose later.

**3. Read the layout.** Where tests live, where page objects live, what a test
file is named. Take it from the tree, not from what the shipped profile assumed.

**4. Sample the right tests.** Not a random handful, and not the oldest.

```bash
git log --format= --name-only -n 200 -- <tests dir> | sort | uniq -c | sort -rn | head -20
```

Read the most recently touched ones. Recent code is the current style, and the
style someone will be reviewed against. Old tests are archaeology. Read a couple
anyway, and note where the two diverge, that gap is worth reporting.

Aim for 10 to 20 files, spread across areas.

**5. Extract what is actually there.** For each, write down what the code does,
not what you would do:

- How test files and test titles are named. Take real examples.
- Which locator strategies appear, and how often. Count them. The order in
  `selector_priority` is the order the repo actually uses, not the order the
  framework recommends.
- How they wait. If there are sleeps, that is what the repo does, and it goes in
  the report, not silently into the conventions as if it were fine.
- Whether page objects exist, what they hold, whether they assert.
- How setup and auth work. A fixture, a base class, a `beforeEach`, a global.
- How test data is made and cleaned up.
- Which assertion library and which matchers.

**6. Where the repo disagrees with itself, ask.** A suite of any age has two or
three eras in it. Do not pick silently. Put it to the user with
AskUserQuestion, showing both patterns with a file and line, and asking which is
the one to write new tests in. This is the highest value question in the whole
process and it takes them ten seconds to answer.

**7. Write `CONVENTIONS.md`.** Same section order as the shipped profiles, so
they are comparable. Every rule gets a real example lifted from their repo, with
the path it came from. Nothing invented.

The "What not to do" section is the exception to lifting examples: fill it from
what you saw go wrong in this repo, if anything, and otherwise leave it thin
rather than padding it with generic advice.

**8. Fill in `policies` in `qa.config.yml`.** From what the repo does. If the
suite is full of sleeps, do not put `hard_sleeps` in `forbid` on day one. The
hook only fires on lines an edit touches, so it will not block their existing
code, but a `forbid` list nobody agreed to still reads as the tool making
decisions for them. Propose it, say what it would flag today, let them choose.

**9. Check it.**

```bash
python3 scripts/validate_profiles.py
qa-context <platform>
```

Then the real test: `/qa:generate` one small test and see whether it looks like
it belongs. If it does not, the conventions are still wrong, and it is much
cheaper to fix them now than after fifty generated tests.

## The report, separate from the conventions

At the end, and in the conversation rather than in the profile:

- What you could not work out, and what you assumed instead.
- Where the suite contradicts itself, and which way you were told to go.
- What is worth revisiting: sleeps, duplication, missing assertions, order
  dependence. Name them, do not fix them, and point at `/qa:audit` for the
  ranked version with evidence.
- Anything in the repo that is genuinely good and worth keeping when someone
  next proposes a rewrite.

## Rules

**No invented examples.** Every code sample in `CONVENTIONS.md` comes from their
repo, with a path. A generic example is how the file drifts from the truth.

**Never write a `beforeEach` login into the conventions because the repo has
one.** Write that the repo has one. The difference matters: the first is you
endorsing it, the second is you describing it, and only the second survives them
changing it later.

**Do not touch their tests.** This reads and writes a profile. Nothing else.

**Say what you are unsure about.** A conventions file that is confidently wrong
about one section costs more than one that says "the suite does both of these
and nobody has decided".

## Next

- `/qa:generate` a small test to check the profile fits.
- `/qa:audit` for what the suite should change, which is a different question
  and a different conversation.
