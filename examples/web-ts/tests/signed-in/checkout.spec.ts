import { expect, test, type Page } from '@playwright/test';

import { CartPage } from '../../pages/CartPage';
import { CheckoutPage } from '../../pages/CheckoutPage';
import { InventoryPage } from '../../pages/InventoryPage';

// Generated from examples/artifacts/CART-142-design.md, rows T8, T9 and T10.
//
// Rows T1 to T7 and T13 are unit rows. This project has no unit layer, so they
// are not written here rather than promoted to e2e.

const BACKPACK = 'Sauce Labs Backpack';
const BIKE_LIGHT = 'Sauce Labs Bike Light';

// 29.99 + 9.99 gives a raw tax of 3.1984, which rounds to 3.20 and truncates to
// 3.19. The design picks this cart on purpose: it separates the two.
const ITEM_TOTAL = 39.98;
const TAX = 3.2;
const TOTAL = 43.18;

async function reachTheOverview(page: Page): Promise<CheckoutPage> {
  const inventory = new InventoryPage(page);
  const cart = new CartPage(page);
  const checkout = new CheckoutPage(page);

  await inventory.goto();
  await inventory.addToCart(BACKPACK);
  await inventory.addToCart(BIKE_LIGHT);

  await cart.goto();
  await cart.checkout.click();

  await checkout.enterDetails('Ada', 'Lovelace', '12345');
  return checkout;
}

test.describe('checkout totals', () => {
  // T9
  test('the overview page shows an item total, a tax line and a total', async ({ page }) => {
    const checkout = await reachTheOverview(page);

    await expect(checkout.itemTotal).toContainText('Item total');
    await expect(checkout.tax).toContainText('Tax');
    await expect(checkout.total).toContainText('Total');
  });

  // T8. The expected tax here depends on the answer to CART-142 Q2, which
  // product has not confirmed. If this fails, check the requirement before
  // assuming the app broke.
  test('the item total, tax and total are right and add up', async ({ page }) => {
    const checkout = await reachTheOverview(page);

    const amounts = await checkout.amounts();

    expect(amounts.itemTotal).toBe(ITEM_TOTAL);
    expect(amounts.tax).toBe(TAX);
    expect(amounts.total).toBe(TOTAL);

    // The three numbers a customer can see have to agree with each other. A
    // total built from the unrounded tax passes the three checks above and
    // fails this one.
    expect(amounts.total).toBeCloseTo(amounts.itemTotal + amounts.tax, 2);
  });

  // T10, first half. The second half of AC4, that the confirmation repeats the
  // total, cannot be tested: the confirmation page shows no amount at all. That
  // is CART-142 Q5 and it is unanswered, so this asserts only what is there.
  test('confirming the order reaches the confirmation page', async ({ page }) => {
    const checkout = await reachTheOverview(page);

    await checkout.finish.click();

    await expect(page).toHaveURL(/checkout-complete\.html/);
    await expect(checkout.confirmation).toHaveText('Thank you for your order!');
  });
});
