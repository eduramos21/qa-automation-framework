---
description: Run a session based exploratory test against a running app, in a real browser or on a device, and keep the session sheet. Produces findings, questions and bug drafts. Use when asked to explore, poke at, or manually test something, when a design says a condition needs a human rather than a script, or when there is no requirement to test against yet.
---

# Explore

Input: `$ARGUMENTS`. A charter, an area, a ticket, or nothing, in which case
propose three charters and let the user pick.

Exploratory testing is not clicking around. It is a timeboxed search for
information about a specific question, with a record of what was tried. The
record is half the value: without it you cannot tell the difference between "we
looked and it was fine" and "nobody looked".

## The charter

One sentence, in this shape:

```
Explore <target>
with <resources>
to discover <information>
```

Example: *Explore the checkout flow with the browser back button and a second
tab to discover whether an order can be placed twice or totals can go stale.*

A charter is good when it can be wrong. "Explore checkout" cannot be wrong.
"Discover whether the total can disagree with what gets charged" can.

Timebox it. Sixty minutes is a normal session, ninety is the ceiling. Say the
box up front and stop when it runs out, even mid thread. What you did not get to
goes in the sheet.

## Steps

**1. Read the setup.** `qa-context`. You need the base URL env var and the
tracker so bugs go to the right place.

**2. Get a browser.** Use the Playwright MCP tools for web. For mobile, use the
Appium or WebdriverIO MCP if the project has one configured, otherwise drive the
device the way the mobile profile's notes describe.

Never guess at what the screen shows. Take the accessibility snapshot and read
it. A finding based on what you assumed is on the page is not a finding.

**3. Explore.** Work in threads. Start one, follow it until it is exhausted or
boring, note where you got to, start the next. Keep a running note as you go
rather than reconstructing at the end, because the interesting detail is the one
you will not remember.

Useful moves, roughly in order of how often they find something:

- Go where the flow does not expect you. Type the URL of a later step directly.
  Use the back button after a point of no return. Refresh mid form.
- Do it twice. Submit twice, open two tabs, run the same action concurrently.
- Use the wrong shape of data. Empty, zero, negative, enormous, an apostrophe in
  a name, an emoji, a right to left script, a very long string.
- Change the state underneath. Empty the cart in one tab, check out in the other.
- Leave and come back. Log out, log in, is the state still there and should it
  be.
- Follow the money and the dates. Anything that rounds, converts, or crosses
  midnight.
- Read what the page actually says. Error messages that name the wrong field,
  amounts that do not add up, labels that contradict the button.

**4. Write the sheet.** As you go, not after.

**5. File what deserves filing.** Use `bug-report` for anything worth a ticket.
Not everything is a bug: some findings are questions for product, and some are
notes for the next tester.

## Session sheet

```markdown
# Session: <charter, one line>

Tester: <who>   Date: <date>   Timebox: <n> minutes   Actual: <n>
Build or URL: <what was tested>
Environment: <browser, device, account used>

## Charter

Explore <target> with <resources> to discover <information>.

## What was covered

Areas, flows and data actually touched. Be specific enough that someone can tell
what was not touched.

## Findings

| # | What happened | Why it matters | Type |
|---|---|---|---|

Type: bug, question, or note.
Filed bugs get their ticket reference here.

## Questions

Things the product has to decide, not things the app got wrong.

## Notes for next time

Threads left unpulled when the box ran out. This is what makes the next session
start faster instead of starting over.

## Time split

Roughly: exploring, investigating a finding, writing it up. If investigation ate
the session, say so, it usually means the first finding was a big one.
```

## Rules

**One charter per session.** If you find something big enough to pull you off
the charter, note it and decide out loud: follow it now and say the charter
changed, or write it down and come back. Drifting silently is how a session ends
with no record of what was actually covered.

**Report what happened, not what you think happened.** "The total showed $43.18
while the cart listed $39.98 and $3.20" is a finding. "Totals are broken" is not.

**Separate a bug from a question.** If the app does something nobody specified,
that is a question for product. Filing it as a bug starts an argument instead of
a decision.

**A quiet session is a result.** Sixty minutes that found nothing, written down
clearly, is worth having. Do not pad the sheet.

**Do not fix anything.** This is a search, not a repair.

## Next

- `bug-report` for the findings worth a ticket.
- `/qa:generate` for any finding that should become a permanent scripted test.
  A bug found by exploring, once fixed, usually deserves one.
