import { type Locator, type Page } from '@playwright/test';

export class InventoryPage {
  readonly title: Locator;
  readonly items: Locator;
  readonly cartBadge: Locator;

  constructor(private readonly page: Page) {
    this.title = page.getByText('Products', { exact: true });
    this.items = page.locator('.inventory_item');
    this.cartBadge = page.locator('.shopping_cart_badge');
  }

  async goto(): Promise<void> {
    await this.page.goto('/inventory.html');
  }

  /** The card for one product, so actions stay scoped to it. */
  item(name: string): Locator {
    return this.items.filter({ hasText: name });
  }

  async addToCart(name: string): Promise<void> {
    await this.item(name).getByRole('button', { name: 'Add to cart' }).click();
  }
}
