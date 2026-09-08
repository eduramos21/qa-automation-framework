import { $ } from '@wdio/globals';
import type { ChainablePromiseElement } from 'webdriverio';

/** The Accessibility section, one level down from the launcher list. */
class AccessibilityScreen {
  get header(): ChainablePromiseElement {
    return $('android=new UiSelector().resourceId("android:id/action_bar_title")');
  }

  get items(): ChainablePromiseElement {
    return $('android=new UiSelector().resourceId("android:id/list")');
  }
}

export const accessibilityScreen = new AccessibilityScreen();
