# The browser back button lets the same checkout be confirmed twice

*Produced by `bug-report` from finding F2 in
`session-2026-09-08-checkout-state.md`. `tracker.provider` is `none` in this
example project, so it was written to a file instead of filed.*

**Environment:** https://www.saucedemo.com, Chromium 148, `standard_user`, 2026-09-08
**Frequency:** every time, 5 out of 5

## Steps

1. Log in and add Sauce Labs Backpack to the cart
2. Go to the cart and press Checkout
3. Fill the form and press Continue, so the overview page shows
4. Press Finish. The confirmation page appears
5. Press the browser back button
6. Press Finish again

## Expected

Step 5 should not return to a page with a live Finish button. Once an order is
confirmed, that checkout is spent: either the back button lands somewhere that
cannot confirm anything, or Finish refuses because the order already exists.

Source: not written down anywhere. CART-142 says nothing about it, which is part
of the finding. The expectation comes from the convention that confirming a
purchase is not repeatable, and from the fact that the customer is given no sign
the second confirm happened.

## Actual

Step 5 returns to `/checkout-step-two.html` with the totals still shown and the
Finish button live. Step 6 confirms again and shows the same confirmation page,
"Thank you for your order!", with nothing to indicate this is a repeat.

## Impact

Every customer who presses back after ordering, which is a normal thing to do
when you are looking for a receipt or an order number. They get a second order
they did not intend and no sign it happened. There is no workaround from the
customer's side because nothing tells them anything went wrong.

If this exists in a real shop it is a duplicate charge and a support call, and
the customer finds out from their bank rather than from you.

## Notes

- Finding F3 in the same session is likely the same cause: with the overview open
  in one tab and the cart emptied in a second, Finish still succeeds. Both look
  like the cart being trusted from the rendered page instead of re-read when the
  order is confirmed. Worth checking before writing two fixes.
- Finding F1, an empty cart reaching the overview by URL and confirming for
  $0.00, is a third case of the same thing. Validating the cart at confirm time
  covers all three.
- Refreshing the overview page does not reproduce it, only the back button does.
- Not tried: two tabs pressing Finish at the same moment.

## Once it is fixed

This deserves a scripted test, and it is cheap: confirm an order, go back, and
assert the Finish button is not there. It is `/qa:generate` work, and it belongs
next to the CART-142 checkout tests.
