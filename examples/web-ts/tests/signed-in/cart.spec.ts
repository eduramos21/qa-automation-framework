import { expect, test } from '@playwright/test';

import { InventoryPage } from '../../pages/InventoryPage';

test.describe('cart', () => {
  test('adding an item shows a count of one on the cart', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.goto();

    await expect(inventory.cartBadge).toHaveCount(0);

    await inventory.addToCart('Sauce Labs Backpack');

    await expect(inventory.cartBadge).toHaveText('1');
  });

  test('adding a second item raises the count to two', async ({ page }) => {
    const inventory = new InventoryPage(page);
    await inventory.goto();

    await inventory.addToCart('Sauce Labs Backpack');
    await inventory.addToCart('Sauce Labs Bike Light');

    await expect(inventory.cartBadge).toHaveText('2');
  });
});
