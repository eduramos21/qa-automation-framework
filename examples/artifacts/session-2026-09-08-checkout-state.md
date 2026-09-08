# Session: does checkout hold its state when you leave and come back

Tester: Eduardo Ramos, with the exploratory guide
Date: 2026-09-08   Timebox: 60 minutes   Actual: 55
Build or URL: https://www.saucedemo.com, live
Environment: Chromium 148 headless, `standard_user`

*Produced by `/qa:explore`, against the second charter in
`CART-142-design.md`.*

## Charter

Explore the checkout flow with the browser back button, a refresh, and a second
tab, to discover whether totals can go stale or an order can be placed twice.

## What was covered

The cart, the checkout form, the overview page and the confirmation page, as
`standard_user`. Six threads: navigating straight to a later step, going back
after confirming, refreshing mid flow, changing the cart from a second tab,
logging out and back in with a cart, and reaching a protected URL logged out.

Not covered: the other demo accounts, mobile viewports, anything to do with
payment, and the sort order on the inventory page.

## Findings

| # | What happened | Why it matters | Type |
|---|---|---|---|
| F1 | With an empty cart, going straight to `/checkout-step-two.html` loads the overview and shows Item total: $0, Tax: $0.00, Total: $0.00. Finish then completes and shows the normal confirmation | An order can be placed with nothing in it. Whatever is downstream of confirm now has an order with no lines in it | bug |
| F2 | After confirming an order, the browser back button returns to the overview with the Finish button still live. Clicking it confirms again and shows the confirmation again | Two orders from one checkout, and the customer sees nothing to say the second one happened. This is the charter's question, answered yes | bug |
| F3 | With the overview open in one tab, removing the only item from the cart in a second tab, then pressing Finish in the first tab, confirms successfully. The overview still showed the old total | The cart is not re-read at confirm time. Same class as F2: the page state is trusted after the state underneath it changed | bug |
| F4 | On the empty cart overview, the item total reads `$0` while tax and total read `$0.00` | One line formats money differently from the two next to it. Small on its own, but it means the item total is not going through the same formatter, which is where a rounding difference would hide | bug |
| F5 | Refreshing the overview page keeps the totals and stays on the page | Working as it should. Noted so the next session does not retry it | note |
| F6 | Adding an item, logging out, logging back in: the cart still holds the item | Probably deliberate for a demo. On a shared machine it means the next person sees your cart. Needs a decision rather than a fix | question |
| F7 | Requesting `/inventory.html` while logged out redirects and shows "Epic sadface: You can only access '/inventory.html' when you are logged in" | Working as it should, and the message names the URL rather than being generic. Noted | note |

## Questions

**Q1, from F6.** Should a cart survive logout? Keeping it is friendlier for one
user on one machine, and wrong for a shared one. There is no requirement either
way, so this is product's call, not a defect.

**Q2, from F1.** Is an empty order supposed to be reachable at all, or is the
overview page simply not meant to be reachable directly? The two have different
fixes: validate the cart at confirm, or guard the route. Validating at confirm
also fixes F3, which is the reason to prefer it.

## Notes for next time

- F2 and F3 are probably the same missing check, a cart that is not re-read when
  the order is confirmed. Worth confirming before two separate fixes get written.
- Not tried: two tabs both pressing Finish at the same moment. F2 shows the
  sequential case, the concurrent one may behave differently.
- Not tried: the other demo accounts. `problem_user` and `error_user` exist and
  are meant to misbehave, so a session against those needs a different charter.
- Not tried: what the back button does from the confirmation page after F2's
  second confirm. There may be a third.
- The inventory sort order was never touched and has no coverage anywhere.

## Time split

About 30 minutes exploring, 20 investigating F2 and F3, 5 writing up.
Investigation ran long because F2 turned up in the first ten minutes and F3 came
out of asking what else trusts stale state, which is the useful kind of overrun.
