# The techniques, with the traps

## Equivalence partitioning

Split the input into classes where every member is expected to be treated the
same, then test one member of each. The saving is real: if a field takes any
integer from 1 to 99, you do not need 99 tests, you need one valid, one below,
one above.

Worked example, a discount code field that accepts a 6 to 10 character
alphanumeric string:

| Class | Example | Expected |
|---|---|---|
| valid, alphanumeric, in range | `SAVE20` | accepted |
| too short | `SAVE` | rejected, length message |
| too long | `SAVE20FOREVER` | rejected, length message |
| contains a symbol | `SAVE-20` | rejected, format message |
| empty | `` | rejected, required message |

Traps:

- Assuming a class is uniform when it is not. "Any European country" is one
  class until VAT rules split it into five.
- Forgetting the empty and the null class. They are different, and code often
  treats them differently by accident.
- Only partitioning the input. Partition the output too: what inputs produce
  each distinct outcome.

## Boundary value analysis

Bugs cluster at the edges because that is where the off by one lives. For each
boundary test the value just below, the value itself, and the value just above.

For 1 to 99: test 0, 1, 2, and 98, 99, 100.

Traps:

- Only testing the edge and not both sides of it. `>` versus `>=` is invisible
  unless you test both.
- Missing the boundary that is not in the requirement. Field length limits,
  integer overflow, the maximum a database column holds.
- Dates. Month ends, leap days, daylight saving transitions, the last day of a
  billing period. Any requirement with a date in it has boundaries the author
  did not write down.

## Decision tables

For rules that combine. Put conditions in rows, one column per combination,
outcomes at the bottom. Then collapse the columns that produce the same outcome
for the same reason.

Free shipping over 50 euro, unless the item is oversized, and members always get
it:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| order over 50 | Y | Y | N | N |
| oversized | N | Y | any | any |
| member | any | any | Y | N |
| **free shipping** | yes | no | yes | no |

Four tests instead of eight. The value is not only the tests, it is that
building the table finds the combination nobody specified. If a cell makes you
say "I do not know what should happen there", that is the finding, and it is
worth more than the test.

Traps:

- Building the full 2^n table and testing all of it. Collapse first.
- Treating an unspecified combination as an edge case. It is an open question
  for whoever wrote the requirement.

## State transition

For anything with a lifecycle: an order, a subscription, a document, a user
account. Draw the states and the allowed transitions, then test three things:

1. Every allowed transition works.
2. Every disallowed transition is refused. This is where the bugs are.
3. Every state can be reached and, if it should be, left.

Traps:

- Testing only the happy path around the loop. The interesting question is what
  happens when you try to cancel something already cancelled, or pay for
  something already refunded.
- Ignoring the transitions triggered by time rather than by a user. Expiry is a
  transition.
- Ignoring concurrent transitions. Two tabs, both hitting cancel.

## Pairwise

When several independent settings combine, most bugs come from a pair
interacting, not from all six at once. Pairwise picks a small set of
combinations where every pair of values appears at least once.

Three browsers, two currencies, two account types is 12 full combinations,
pairwise covers it in about 6.

Use a tool to generate the set. Generating it by hand is slow and gets it wrong.

Traps:

- Using it where the factors are not independent. If currency determines which
  payment methods appear, that is a decision table.
- Trusting it for the combination you already know is risky. Add that one
  explicitly on top.

## Error guessing and the checklists

Not a technique so much as using what you already know. Keep a list per domain
and run it against every requirement:

- What if it is empty, null, zero, negative, enormous?
- What if the same request arrives twice?
- What if it arrives out of order, or very late?
- What if the user hits back, refreshes, or opens a second tab?
- What if the network drops halfway?
- What if the value is in another timezone, another locale, another script?
- What about a name with an apostrophe, an emoji, a right to left script?
- What happens on the second attempt after a failure?

This list finds more real bugs than any of the formal techniques. Keep it, add
to it every time production surprises you.
