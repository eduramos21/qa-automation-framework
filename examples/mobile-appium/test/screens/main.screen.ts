import { $, driver } from '@wdio/globals';
import type { ChainablePromiseElement } from 'webdriverio';

/**
 * The ApiDemos launcher list. Everything else in the app is reached from here.
 *
 * Locators are getters rather than fields on purpose. An element resolved at
 * import time is bound to whatever was on screen then, and the failure that
 * produces points nowhere useful.
 */
class MainScreen {
  get list(): ChainablePromiseElement {
    return $('android=new UiSelector().resourceId("android:id/list")');
  }

  /**
   * A row in the list, by its visible label. This is the one place the two
   * platforms differ, so it is the one method that knows about them.
   */
  item(label: string): ChainablePromiseElement {
    return driver.isAndroid
      ? $(`android=new UiSelector().text("${label}")`)
      : $(`-ios predicate string:label == "${label}"`);
  }

  async open(label: string): Promise<void> {
    const row = this.item(label);
    await row.waitForDisplayed({ timeout: 10000 });
    await row.click();
  }
}

export const mainScreen = new MainScreen();
