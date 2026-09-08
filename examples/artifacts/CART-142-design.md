# CART-142 test design

Requirement: `CART-142-requirement.md`   Designed: 2026-09-08
Stack: `ts-playwright`, from `examples/web-ts/qa.config.yml`

*Produced by `/qa:design CART-142-requirement.md`.*

## Coverage

| ID | Condition | From | Technique | L | C | Risk | Layer | Automate | Exists |
|---|---|---|---|---|---|---|---|---|---|
| T1 | Item total equals the sum of the listed prices, one item | AC1 | partition, one item class | 1 | 3 | 3 | unit | yes | no |
| T2 | Item total equals the sum of the listed prices, several items | AC1 | partition, many item class | 2 | 3 | 6 | unit | yes | no |
| T3 | Tax equals 8% of the item total, rounded half up | AC2 | rule | 2 | 3 | 6 | unit | yes | no |
| T4 | Tax rounds up when the third decimal is 5 or more | AC2, Q2 | boundary | 3 | 3 | 9 | unit | yes | no |
| T5 | Tax rounds down when the third decimal is under 5 | AC2, Q2 | boundary | 2 | 3 | 6 | unit | yes | no |
| T6 | Tax on an exact half cent, the case that separates half up from half even | AC2, Q2 | boundary | 3 | 3 | 9 | unit | yes | no |
| T7 | Total equals item total plus the displayed tax | AC3, Q3 | rule | 2 | 3 | 6 | unit | yes | no |
| T8 | The three numbers on screen add up, for a cart where rounding is not exact | AC1, AC2, AC3 | scenario | 2 | 3 | 6 | e2e | yes | no |
| T9 | A customer can reach the overview page and see all three lines | AC1 to AC3 | flow | 2 | 2 | 4 | e2e | yes | partly, cart.spec.ts covers the cart badge only |
| T10 | Confirming places the order and shows the same total | AC4 | flow | 1 | 3 | 3 | e2e | yes | no |
| T11 | An empty cart cannot reach the overview page | AC5, Q4 | state | 2 | 2 | 4 | e2e | later | no |
| T12 | Totals survive a page refresh on the overview page | error guessing | scenario | 2 | 2 | 4 | e2e | no | no |
| T13 | Tax rate is read from configuration, not hardcoded twice | Q1 | inspection | 2 | 2 | 4 | unit | yes | no |

## Not covering

| Condition | Why not |
|---|---|
| Every currency format | Single currency, USD only, out of scope in the requirement |
| Tax rates other than 8% | Out of scope until Q1 is answered. If it comes back as "varies by state", this design gets redone rather than patched |
| Item total with 100 items in the cart | Score 2. The sum is the same code path as two items, and the interesting failure is a display one, which T9 would catch |
| Shipping line | The site charges no shipping and shows no line |
| Discount codes | No such field exists in the flow |
| Card is declined | Payment is out of this story. It belongs to whatever ticket introduces real payment |

## Explore instead

| Charter | Why this is not a scripted test |
|---|---|
| Explore the checkout overview page with carts of unusual shapes, one very cheap item, the most expensive item alone, the same item many times, looking for totals that read wrong even when they add up | The expected result is "a person would not be confused", which no assertion captures |
| Explore navigating away and back mid checkout, using browser back, refreshing, and opening the overview in a second tab, looking for totals that go stale or an order that can be placed twice | Looking for the unknown, not confirming a known expectation. The double order case, if it exists, becomes its own scripted test after it is found |

## Test data

T1 to T7 and T13 need no fixtures, they are pure calculation and take their
inputs directly.

T8 needs a cart whose 8% tax does not land on an exact cent. Sauce Labs Backpack
at $29.99 plus Sauce Labs Bike Light at $9.99 gives an item total of $39.98 and
a raw tax of $3.1984, which the site displays as $3.20 and totals to $43.18.
That cart is the one to use, because it fails under truncation and passes under
rounding, which is exactly the distinction Q2 is about.

T6 needs a cart whose raw tax ends in an exact half cent. There may not be one
reachable from the catalogue, in which case T6 stays at the unit layer only and
that is noted rather than quietly dropped.

T9 and T10 reuse the existing signed in session from `tests/auth.setup.ts`. They
do not log in through the UI.

T10 places a real order in the demo environment. It creates no state that
another test reads, so it is safe in parallel.

## Blocked

T4, T5, T6 and T7 are designed against the proposed answers to Q2 and Q3. They
can be written now, but they are asserting a convention that product has not
confirmed. If Q2 comes back as half even, T6 inverts. Flag them in the code with
a reference to Q2 so whoever reads a failure knows the expectation is provisional
rather than assuming the app broke.

T11 waits on Q4. Automating the current behaviour would lock in the bug.
