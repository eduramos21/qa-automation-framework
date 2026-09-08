# CART-142 generation report

Design: `CART-142-design.md`   Generated: 2026-09-08
Stack: `ts-playwright`, into `examples/web-ts`

*What `/qa:generate CART-142-design.md` reported back.*

## Files

| Path | What |
|---|---|
| `examples/web-ts/tests/signed-in/checkout.spec.ts` | three tests |
| `examples/web-ts/pages/CheckoutPage.ts` | new, covers the form and the overview |
| `examples/web-ts/pages/CartPage.ts` | new, two locators, earns its place because three tests go through the cart |

## Covered

| Row | Test |
|---|---|
| T8 | the item total, tax and total are right and add up |
| T9 | the overview page shows an item total, a tax line and a total |
| T10, first half | confirming the order reaches the confirmation page |

## Not written

| Row | Why |
|---|---|
| T1 to T7, T13 | Unit rows. This project is an e2e suite with no unit layer, so they are not written rather than promoted to e2e. Eight checks of a rounding rule through a browser would be slow, and each one would fail without saying which of forty things broke. They need a home in whatever repo holds the calculation |
| T10, second half | Cannot be tested. See findings |
| T11 | The design marks it `later`, pending CART-142 Q4 |
| T12 | The design marks it `no` |

## Findings

**AC4 is half untestable.** It says the confirmation shows the same total that
was displayed. The confirmation page shows no amount at all, only "Thank you for
your order!" and a dispatch message. So either the app is missing something the
requirement asked for, or the requirement asked for something nobody intended.
This is exactly Q5 in the refined requirement, which is still open. The test
asserts only what is on the page, and the gap is written in a comment above it so
whoever reads it knows the coverage is partial on purpose.

**T8 asserts a provisional expectation.** The expected tax of $3.20 depends on
rounding half up, which is the proposed answer to Q2 and not a confirmed one. The
test carries a comment pointing at Q2, so a failure sends the reader to the
requirement before they start debugging the app.

**The cart chosen by the design does its job.** $29.99 plus $9.99 gives a raw tax
of $3.1984. Truncating gives $3.19, rounding gives $3.20. A test written against
a cart where both methods agree would have passed either way and told you
nothing.

**The arithmetic check is separate from the value checks.** Asserting item total,
tax and total individually does not prove they agree with each other. A total
built from the unrounded tax passes all three and fails
`total == itemTotal + tax`. That is a fourth assertion in the same test rather
than a fourth test, because it is the same behaviour looked at from a different
angle.

## Verification

Each test was run, then broken on purpose and run again to confirm it goes red
for the right reason. Setting the expected tax to $3.19:

```
✘ checkout totals › the item total, tax and total are right and add up
  Expected: 3.19
  Received: 3.2
```

Then restored. A locator that matches nothing produces a test that asserts
nothing and passes forever, and running it once green does not catch that.

## Run it

```bash
cd examples/web-ts
npx playwright test tests/signed-in/checkout.spec.ts
```
