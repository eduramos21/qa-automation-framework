---
description: Write a bug report someone can act on, and file it to whatever tracker the project uses. Use when a test fails for a real reason, when exploring turns something up, or when the user says file a bug, raise a ticket, or report this.
---

# Report a bug

A bug report has one job: get the defect fixed with the fewest round trips. Every
round trip costs a day. Most of what makes a report bad is the reporter knowing
something and not writing it down.

## Steps

**1. Reproduce it.** From a clean state, following your own steps. If you cannot,
say so in the report and say how many times you tried. An intermittent bug is
still worth filing, but it has to be labelled as one or someone will close it as
not reproducible.

**2. Narrow it.** Cut every step that is not needed. Ten steps become four.
Then ask which is the real variable: does it happen with a different account, a
different browser, a different amount? The answer usually points at the cause and
saves the developer the search.

**3. Check it is new.** Search the tracker before filing. A duplicate splits the
discussion across two tickets.

**4. Work out what it costs.** Not how annoying it is. How many users, how often,
what happens if it ships, and whether there is a workaround. That is what someone
prioritises on.

**5. Write it.** Shape below.

**6. File it.** Per `tracker` in `qa.config.yml`:

- `jira`: create the issue with the Atlassian tools, in `tracker.project_key`.
- `github-issues`: `gh issue create`.
- `none`: write it to a file and tell the user where.

Attach what you have: screenshot, trace, video, the failing test output, the
network log if the failure is a request.

## Shape

```markdown
# <One line. What is wrong, where. Not "checkout broken">

**Environment:** <url or build, browser or device, account, date>
**Frequency:** every time | <n> times out of <m> | seen once

## Steps

1. From <clean starting state>
2. ...
3. ...

## Expected

<What should happen, and where that comes from. A requirement, an acceptance
criterion, an existing behaviour, or a convention. If the answer is "I think it
should", say that, and it may be a question rather than a bug.>

## Actual

<What happens. Exact text, exact numbers, exact error.>

## Impact

Who hits this, how often, what it costs them, and whether there is a way around
it.

## Notes

What you ruled out. Other browsers, other accounts, whether it survives a
refresh, when it started. This is the section that saves the round trip.
```

## Rules

**Title says what is wrong and where.** Someone scanning fifty tickets should be
able to tell them apart from the titles alone.

**Exact values.** "The total was wrong" is not a report. "The total showed $43.18
for an item total of $39.98 and tax of $3.20" is.

**Expected needs a source.** If you cannot point at where the expectation comes
from, you may have found a question for product rather than a defect. File it as
one. Filing a question as a bug starts an argument about whether it is a bug,
which is not the conversation that needs to happen.

**Do not diagnose in the title.** You will sometimes be wrong, and a wrong
diagnosis in the title sends everyone the wrong way. Put your theory in Notes
where it helps and costs nothing if it is off.

**One bug per report.** Two defects in one ticket means one gets fixed and the
ticket gets closed.

**Severity is about cost, not about how loud it looks.** A wrong number nobody
notices for a month is often worse than a crash, because a crash gets reported.
