# Risk scoring

## The score

```
risk = likelihood  x  cost
```

Both on 1 to 3, so the score runs 1 to 9.

| Score | What it means |
|---|---|
| 6 to 9 | Automate it. If it cannot be automated, it gets a named manual check that runs every release |
| 3 to 4 | Cover it once, at the cheapest layer that can see it |
| 1 to 2 | Do not test it. Write down that you decided not to |

The third row is the one that gets skipped, and it is the one that keeps a suite
from growing into something nobody can run.

## Likelihood, 1 to 3

Goes up with:

- Code written or changed this sprint.
- A boundary between two systems, especially two teams.
- Anything with a date, a timezone, a currency, or a rounding rule.
- Anything concurrent, queued, retried, or cached.
- Code with a history. Check the git log, a file that has been fixed four times
  will be fixed a fifth.
- Anything a developer called simple or obvious.

Goes down with: code untouched for a year that runs a thousand times a day.

## Cost, 1 to 3

Goes up with:

- Money moves the wrong way.
- Data is lost or corrupted.
- A user cannot get in, or gets into someone else's account.
- A legal, privacy or accessibility obligation is breached.
- The failure is silent. A wrong number displayed for a month is worse than a
  crash, because a crash gets reported.
- The blast radius is everyone rather than one customer.

Goes down with: a cosmetic issue on a page with a workaround.

## Writing a risk line people read

Bad: "Risk: payment issues."

Good: "If the rounding rule is wrong on multi currency orders, every invoice in
that currency is off by up to a cent, we would not notice until finance
reconciles at month end, and correcting issued invoices is manual. Likelihood 3,
new code touching currency. Cost 3, money and a month of silence. Score 9."

The pattern: what breaks, who notices, when they notice, what it costs to
correct. A product manager can make a call on that. They cannot make a call on
"payment issues".

## Where risk comes from

Do not invent it alone. Pull from:

- The git log for the files the change touches.
- Production incidents and support tickets from the last quarter.
- The bug tracker, filtered to this area.
- The developers. Ask what part of the change they are least sure about. They
  usually know, and are rarely asked.
- The flakiest tests in the suite. Flake often marks a genuinely unstable area.
