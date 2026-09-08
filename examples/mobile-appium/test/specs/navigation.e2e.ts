import { driver, expect } from '@wdio/globals';

import { accessibilityScreen } from '../screens/accessibility.screen';
import { mainScreen } from '../screens/main.screen';

const APP_ID = process.env.APP_ID ?? 'io.appium.android.apis';

describe('navigation', () => {
  beforeEach(async () => {
    // App state resets, the session does not. Starting a session costs 10 to 30
    // seconds and doing it per test is what makes a mobile suite take an hour.
    await driver.execute('mobile: clearApp', { appId: APP_ID });
    await driver.activateApp(APP_ID);
  });

  it('the launcher list is shown when the app opens', async () => {
    await expect(mainScreen.list).toBeDisplayed();
    await expect(mainScreen.item('Accessibility')).toBeDisplayed();
  });

  it('opening Accessibility shows the accessibility section', async () => {
    await mainScreen.open('Accessibility');

    await expect(accessibilityScreen.header).toHaveText('Accessibility');
    await expect(accessibilityScreen.items).toBeDisplayed();
  });

  it('going back from a section returns to the launcher list', async () => {
    await mainScreen.open('Accessibility');
    await expect(accessibilityScreen.header).toHaveText('Accessibility');

    await driver.back();

    await expect(mainScreen.item('Accessibility')).toBeDisplayed();
  });
});
