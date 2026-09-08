# Conventions for mobile-appium-wdio

How tests get written in this stack. `profile.yaml` says where files go and how
to run them. This says what the code inside them looks like.

Working example: `examples/mobile-appium/`.

Mobile is not web with a smaller screen. Three things drive everything below:
sessions are expensive, the same app is two apps, and the device is a real thing
that can be busy, rotated, interrupted by a call, or out of storage.

## Test file shape

```ts
// test/specs/navigation.e2e.ts
import { mainScreen } from '../screens/main.screen';
import { accessibilityScreen } from '../screens/accessibility.screen';

describe('navigation', () => {
  it('opening Accessibility shows the accessibility list', async () => {
    await mainScreen.open('Accessibility');

    await expect(accessibilityScreen.header).toHaveText('Accessibility');
  });
});
```

Arrange, act, assert. Screen objects are exported as instances, not classes, so
a spec never news anything up.

## Naming

- Specs: `test/specs/<area>.e2e.ts`.
- Screens: `test/screens/<name>.screen.ts`, exporting `<name>Screen`.
- Titles: a sentence about behaviour. Same rule as anywhere, the title is what
  someone reads in a failing nightly run.

## Selectors

Order in `profile.yaml`. In practice:

```ts
$('~submit')                                    // accessibility id, both platforms
$('android=new UiSelector().text("Submit")')    // Android only
$('-ios predicate string:label == "Submit"')    // iOS only
$('//android.widget.Button[3]')                 // no
```

Accessibility id first, always. It is the one selector that means the same thing
on both platforms, and an element without one is usually an element a screen
reader cannot reach either. When you cannot find one, that is a finding about the
app worth reporting, not just an inconvenience.

XPath is last and slow. On a real device an XPath query walks the whole view
hierarchy over the wire, and a positional one breaks the first time a view is
inserted above it.

## Waiting

`driver.pause()` is the mobile fixed sleep. It is more tempting here than on web
because animations are genuinely real, and it is still wrong.

```ts
await button.waitForDisplayed({ timeout: 5000 });                 // yes
await driver.waitUntil(async () => (await list.length) > 0);      // yes
await driver.pause(2000);                                          // no
```

WebdriverIO's `expect` matchers retry. Use them against elements rather than
pulling a value out and asserting on it.

The one place a pause is defensible is waiting out an animation the framework
cannot observe, and it needs a comment saying which animation and why nothing
else works.

## Screen objects

Same rule as elsewhere: a screen object earns its existence at two or more tests,
or more than three locators. Mobile hits both faster than web does.

```ts
import { $, type ChainablePromiseElement } from '@wdio/globals';

class MainScreen {
  // Getters, not fields. An element resolved at import time points at a screen
  // that does not exist yet, and the failure it produces says nothing useful.
  get list(): ChainablePromiseElement {
    return $('~main-list');
  }

  item(label: string): ChainablePromiseElement {
    return driver.isAndroid
      ? $(`android=new UiSelector().text("${label}")`)
      : $(`-ios predicate string:label == "${label}"`);
  }

  async open(label: string): Promise<void> {
    const target = await this.item(label);
    await target.waitForDisplayed({ timeout: 10000 });
    await target.click();
  }
}

export const mainScreen = new MainScreen();
```

Getters rather than fields is the mobile specific part. On web a Playwright
locator is lazy and costs nothing to build early. Here, resolving an element
early binds it to whatever is on screen at import time.

**Platform differences live in the screen object, behind one method.** A spec
with `if (driver.isAndroid)` in it is two specs pretending to be one, and the
second one is never read.

**No assertions in screen objects.** Same as everywhere.

## Sessions and app state

Starting a session costs 10 to 30 seconds. Doing it per test is the single
biggest reason a mobile suite takes an hour.

One session for the run. Reset app state between tests:

```ts
beforeEach(async () => {
  await driver.execute('mobile: clearApp', { appId: process.env.APP_ID });
});
```

WebdriverIO keeps the session by default. Do not turn that off to "make tests
independent", the app reset is what makes them independent.

If a test genuinely needs a fresh session, say why in a comment, because the next
person will otherwise copy it.

## Test data and device state

The device is shared state. Anything a test writes, another test can read:
files, permissions, notifications, the clipboard, the keyboard language.

Reset what you touch. Grant permissions in capabilities rather than by tapping
through a system dialog, because system dialogs differ by OS version and are not
part of what you are testing.

Parallel runs need one device each. Two sessions against one device do not work,
so parallelism here is a hardware decision, not a config one.

## Assertions

```ts
await expect(header).toHaveText('Accessibility');    // retries
expect(await header.getText()).toBe('Accessibility'); // races
```

Assert on the element. `getText` on a view still animating in returns whatever
was there a frame ago.

## What not to do

- `driver.pause()`. Top of the list, for the same reason as everywhere, plus
  it is slower here because everything is.
- A fresh session per test. It is the difference between a ten minute suite and
  an hour.
- `if (driver.isAndroid)` in a spec. Push it into the screen object.
- XPath, especially positional. Slow over the wire and brittle.
- Testing the OS. Whether the keyboard opens, whether the share sheet works,
  whether notifications appear in the shade. That is Apple and Google's suite,
  not yours.
- Tapping through permission dialogs. Grant them in capabilities.
- One test that walks eight screens. On mobile it takes two minutes and tells
  you nothing when it fails.
- Screenshots on every step. They are large and the run has to upload them.
