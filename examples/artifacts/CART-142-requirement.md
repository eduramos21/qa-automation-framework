# CART-142 Show order totals at checkout

Source: `CART-142-source.md`   Refined: 2026-09-08   Status: draft

*Produced by `/qa:refine CART-142-source.md` against `examples/web-ts`. The
behaviour described here was checked against the running site, not assumed.*

## What changes

On the checkout overview page, a customer sees three lines before they confirm:
what the items cost, how much tax is added, and what they will actually be
charged. Today they reach that page and confirm without seeing the tax, so the
first time they see the real amount is on the card statement.

## Acceptance criteria

AC1. Given a cart with at least one item, when the customer reaches the checkout
overview page, then an item total is shown equal to the sum of the listed prices
of the items in the cart.

AC2. Given an item total, when the overview page is shown, then a tax line is
shown equal to 8% of the item total, rounded half up to two decimal places.

AC3. Given an item total and a tax line, when the overview page is shown, then a
total is shown equal to the item total plus the displayed tax line.

AC4. Given the overview page, when the customer confirms, then the order is
placed and the confirmation shows the same total that was displayed.

AC5. Given an empty cart, when the customer tries to reach the checkout overview
page, then they do not get there. See open question Q4 for what they see instead.

## Rules

Tax applies to the item total, not to each item. Rounding happens once, on the
tax line, before the total is added up. This matters: for two items at $29.99
and $9.99, per item rounding gives $2.40 plus $0.80 which is $3.20 by luck, but
for other combinations the two methods differ by a cent, and the cent shows up
on the invoice.

| | 1 | 2 | 3 |
|---|---|---|---|
| cart has items | Y | Y | N |
| tax rounds up at the third decimal | Y | N | any |
| **item total** | shown | shown | not reached |
| **tax** | rounded up | rounded down | not reached |
| **total** | item total + tax | item total + tax | not reached |

## Out of scope

- Shipping cost. The site shows "Free Pony Express Delivery" and no shipping
  line, so there is nothing to total.
- Discounts and promotions. There is no discount field anywhere in the flow.
- Currency other than USD. Every price on the site is in dollars and the
  requirement does not introduce another.
- Tax rates other than 8%. See Q1, this may not survive.

## Risks

| # | If this is wrong | Who notices, when | L | C | Score |
|---|---|---|---|---|---|
| R1 | Tax rounds the wrong way | Nobody, for months. It is one cent per order, so it will not be reported, it will be found during a reconciliation | 2 | 3 | 6 |
| R2 | The total does not equal item total plus tax | The customer, immediately, and they will not confirm | 1 | 3 | 3 |
| R3 | The item total misses an item when the cart has several | The customer, immediately, if it is under. Nobody, if it is over and the difference is small | 2 | 3 | 6 |
| R4 | The confirmed amount differs from the displayed one | The customer, on their statement, and it becomes a chargeback | 1 | 3 | 3 |
| R5 | An empty cart reaches checkout and totals $0.00 | Support, eventually, after a customer places an empty order | 2 | 2 | 4 |

## Open questions

| # | Question | Proposed answer | Blocks | Asked of |
|---|---|---|---|---|
| Q1 | Is 8% fixed, or does it depend on where the customer is? The ticket says 8% flat, but a tax rate that never varies is unusual enough to be worth confirming before it is hardcoded in both the app and the tests | Fixed at 8% for this release, with the rate held in one place so it can move later | build and test | product |
| Q2 | Round half up, half even, or truncate? The ticket says "calculated correctly", which is the ambiguity this whole story turns on. The site currently shows $3.20 for a tax of $3.1984, so it rounds rather than truncates, but half up and half even only differ on an exact half and that case has not been tried | Round half up to two decimals, the common retail convention | build and test | product, finance |
| Q3 | Is the total the item total plus the *displayed* tax, or plus the unrounded tax then rounded? These differ by a cent on some carts | Plus the displayed tax, so the three numbers on screen always add up. A customer who checks the arithmetic and finds it wrong will not trust the rest of the page | build and test | product |
| Q4 | What does a customer with an empty cart see if they navigate straight to the overview URL? | Send them back to the cart with a message. Currently the page loads and shows $0.00, which lets an empty order through | build and test | product |
| Q5 | Does the confirmation page repeat the totals, or only say thank you? AC4 assumes it repeats them | Repeat them. It is the only record the customer has before the email arrives | test | product |

Q2 and Q3 are the same class of question and neither is answered by the ticket.
Together they are the reason this story is not ready to build: three developers
would implement three different answers and all three would pass "tax is
calculated correctly".
