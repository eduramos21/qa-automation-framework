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

## Still to come

| From | Lands in |
|---|---|
| An exploratory session sheet, `/qa:explore` | phase 4 |
| A suite audit report, `/qa:audit` | phase 5 |
