# examples/artifacts

Real output from the agents, committed so you can see what each workflow
produces without having to run it first.

## CART-142, order totals at checkout

A worked example that runs end to end through the phases, against the same
saucedemo site `examples/web-ts` tests.

| File | Produced by | What it shows |
|---|---|---|
| `CART-142-source.md` | nobody, this is the input | A normal ticket. Three acceptance criteria, one of which is "tax is calculated correctly" |
| `CART-142-requirement.md` | `/qa:refine` | The same story with five acceptance criteria, a decision table, a risk table, and five open questions. Two of those questions are the reason the story was not ready to build |
| `CART-142-design.md` | `/qa:design` | Thirteen conditions, risk scored, assigned to a layer. Eight of them are unit tests, three are e2e, one waits on an open question, one is deliberately not automated. Plus what is not being covered and why |
| `CART-142-generated.md` | `/qa:generate` | What got written, what did not, and why. The eight unit rows were left unwritten rather than promoted to e2e, and one acceptance criterion turned out to be half untestable |

The thing worth looking at is what the refinement found. The original ticket says
tax is 8% and that it should be calculated correctly. It does not say whether to
round half up, half even, or truncate, and it does not say whether the total adds
the rounded tax or the raw one. Three developers would pick three answers and all
three would satisfy "calculated correctly". That is a one cent difference per
order that nobody reports and finance finds at month end.

Numbers in these documents were checked against the running site rather than
assumed. Two items at $29.99 and $9.99 give an item total of $39.98, a raw tax of
$3.1984, a displayed tax of $3.20 and a total of $43.18. That cart is the one the
design uses for the rounding test, because it passes under rounding and fails
under truncation.

The generated code is in `examples/web-ts/tests/signed-in/checkout.spec.ts`, next
to the design rows it came from. Two things there are worth more than the tests:
the eight unit rows that were left unwritten because this project has no unit
layer, and the half of AC4 that could not be tested because the confirmation page
shows no total. Both are reported rather than papered over.

## Exploring the same feature

| File | Produced by | What it shows |
|---|---|---|
| `session-2026-09-08-checkout-state.md` | `/qa:explore` | A 55 minute session against the second charter the design produced. Seven findings: three bugs, one formatting bug, two notes, one question |
| `BUG-checkout-confirm-twice.md` | `bug-report` | The most serious of them, written up so it can be fixed without a round trip |

The session was run against the live site, and the findings are real. Pressing
the browser back button after confirming an order returns to a page with a live
Finish button, and pressing it confirms again with nothing to say it was a
repeat. Emptying the cart in a second tab does not stop the first tab from
confirming. Navigating straight to the overview URL with an empty cart shows
`Item total: $0` next to `Tax: $0.00` and lets a $0.00 order through.

Three of those look like one cause: the cart is trusted from the rendered page
rather than re-read when the order is confirmed. Saying that in the report is
worth more than the three tickets, because it turns three fixes into one.

## Auditing the suite that came out of it

| File | Produced by | What it shows |
|---|---|---|
| `audit-2026-09-08-web-ts.md` | `/qa:audit` | Nine rubric scores with evidence, six ranked findings, the coverage gaps, and the first three things to do |

The suite scores 5 on speed, isolation, waiting and assertions, and 2 on layers
and on coverage against requirements. Both low scores come from the same place:
eight of the thirteen design rows are unit rows, this project has no unit layer,
so the highest risk item in the whole requirement has no test anywhere. The three
defects the exploratory session found have no regression tests either.

None of that is a hole in what was written. Every one of those rows was a
recorded decision. The finding is that the decisions have not been acted on
since, which is a different problem and needs a different conversation.

A report normally goes to `qa/audit/<date>.md` inside the project. This one lives
here instead so it sits next to the requirement, design, generation report and
session sheet it refers to.
