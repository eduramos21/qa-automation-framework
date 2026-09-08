import { type Locator, type Page } from '@playwright/test';

/**
 * Covers the checkout form and the overview that follows it. They are two URLs
 * but one flow with no branch in it, and splitting them would give two classes
 * that are only ever used together.
 */
export class CheckoutPage {
  readonly firstName: Locator;
  readonly lastName: Locator;
  readonly postalCode: Locator;
  readonly continue: Locator;

  readonly itemTotal: Locator;
  readonly tax: Locator;
  readonly total: Locator;
  readonly finish: Locator;

  readonly confirmation: Locator;

  // No page field: this object is always reached by navigating the flow, so it
  // never needs to go anywhere itself.
  constructor(page: Page) {
    this.firstName = page.getByTestId('firstName');
    this.lastName = page.getByTestId('lastName');
    this.postalCode = page.getByTestId('postalCode');
    this.continue = page.getByTestId('continue');

    this.itemTotal = page.getByTestId('subtotal-label');
    this.tax = page.getByTestId('tax-label');
    this.total = page.getByTestId('total-label');
    this.finish = page.getByTestId('finish');

    this.confirmation = page.getByTestId('complete-header');
  }

  async enterDetails(first: string, last: string, postcode: string): Promise<void> {
    await this.firstName.fill(first);
    await this.lastName.fill(last);
    await this.postalCode.fill(postcode);
    await this.continue.click();
  }

  /** The three summary lines, as numbers, so a test can check they add up. */
  async amounts(): Promise<{ itemTotal: number; tax: number; total: number }> {
    const [itemTotal, tax, total] = await Promise.all([
      money(this.itemTotal),
      money(this.tax),
      money(this.total),
    ]);
    return { itemTotal, tax, total };
  }
}

/** Pulls the number out of a line like "Item total: $39.98". */
async function money(line: Locator): Promise<number> {
  const text = (await line.textContent()) ?? '';
  const match = text.match(/\$([\d,]+\.\d{2})/);
  if (match === null) {
    throw new Error(`No amount in "${text}"`);
  }
  return Number(match[1].replace(/,/g, ''));
}
