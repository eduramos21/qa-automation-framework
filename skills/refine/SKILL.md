---
description: Turn a requirement, user story or ticket into something testable. Produces acceptance criteria, an ambiguity list, and a risk table, and asks the questions that need a human. Use when given a ticket to test, when a story is vague, before writing any test for new work, or when the user says refine, groom, or what should this do.
---

# Refine a requirement

Input: `$ARGUMENTS`. A ticket key, a path to a file, a URL, or pasted text.

The output of this is not test cases. It is a requirement someone can build
from and someone else can test against, plus a short list of things nobody
decided yet. That second list is the whole point. A requirement that survives
this without producing a single question was either already excellent or was
not read carefully.

## Steps

**1. Read the setup.** Run `qa-context`. You need `tracker` and `requirements`
to know where the source is, and `project.glossary` if there is one, so the
output uses the words the business uses.

**2. Get the source.** Depending on `requirements.source`:

- `jira` or `confluence`: use the Atlassian tools. Fetch the item, and also its
  linked items and comments, the decisions usually live in the comments.
- `github-issues`: `gh issue view <n> --comments`.
- `markdown`: read the file under `requirements.path`.
- Pasted text: use it as is.

Also read whatever the requirement points at: a design file, a linked spec, the
API contract. And look at the code if it exists, because the gap between what
the ticket says and what the code does is a finding on its own.

**3. Restate it.** In two or three sentences, what changes for a user when this
is done. If you cannot write that without hedging, the requirement is not ready
and the rest of this is guesswork. Say so.

**4. Find the holes.** Go through the requirement looking for:

- Words that hide a decision: quickly, appropriate, relevant, valid, secure,
  user friendly, handle gracefully, if needed, etc.
- Missing error behaviour. What happens when it fails, times out, or gets called
  twice.
- Missing boundaries. Every limit, length, amount and date range that is not
  written down.
- Missing permissions. Who can do this, who cannot, what the second group sees.
- Missing state. What if it is already done, already cancelled, already expired.
- Missing non functional expectations. How fast, how many, on what devices.
- Anything that contradicts existing behaviour.

Use `test-design-techniques` for the checklists. Build the decision table early
if there are rules, the empty cells are the questions.

**5. Score the risk.** Where would this hurt if it were wrong. See
`references/risk.md` in `test-design-techniques`.

**6. Ask.** Take the ambiguities that block writing a test and put them to the
user with AskUserQuestion, with your recommended answer first. Not all of them,
only the ones that change what gets built or tested. The rest go in the document
as open questions with a proposed answer attached, so someone can approve them
in one pass rather than answering an interview.

**7. Write it.** To `<requirements.path>/<id>.md` if that is set, otherwise
`qa/requirements/<id>.md`. Tell the user the path.

## Output shape

```markdown
# <ID> <title>

Source: <link or path>   Refined: <date>   Status: draft | agreed

## What changes

Two or three sentences. What a user can do after this that they could not before.

## Acceptance criteria

AC1. Given <context>, when <action>, then <observable result>.
AC2. ...

One observable result per criterion. If a criterion has an "and" in the "then",
split it. Every criterion must be checkable by someone who cannot see the code.

## Rules

Only if there are combining rules. The decision table, collapsed.

## Out of scope

What this deliberately does not cover, so nobody tests it and files a bug.

## Risks

| # | If this is wrong | Who notices, when | Likelihood | Cost | Score |
|---|---|---|---|---|---|

## Open questions

| # | Question | Proposed answer | Blocks | Asked of |
|---|---|---|---|---|

Blocks: build, test, or neither. A question that blocks neither is a note, and
should probably not be a row.
```

## Rules

**Every criterion is observable.** "The order is processed correctly" is not
testable. "The order status becomes Paid and a confirmation email is sent within
one minute" is.

**Do not invent the answer.** If the requirement does not say what happens when
the card is declined, that is an open question, not an assumption you quietly
resolve. Proposing an answer is fine and useful. Presenting it as the
requirement is not.

**Do not write test cases here.** That is `/qa:design`. Mixing them makes a
document that neither a developer nor a tester will read to the end.

**Use the project's words.** If the glossary says "booking", do not write
"reservation". Terminology drift between a requirement and a test suite is how
two teams end up sure they are talking about the same thing.

**Keep it short.** If the refined requirement is longer than the original plus
the tables, it is padded.

## Next

`/qa:design <the file you just wrote>`.
