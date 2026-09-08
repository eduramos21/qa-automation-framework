# examples/mobile-appium

A WebdriverIO plus Appium suite built to the `mobile-appium-wdio` profile,
running against Appium's ApiDemos app on an Android emulator.

## What is and is not verified

Honest version, because the difference matters:

| | State |
|---|---|
| Types | Verified. `npx tsc --noEmit` is clean and runs in this repo's CI |
| Config resolution | Verified. `qa-context` resolves the mobile stack to this profile |
| House rules | Verified. `qa-policy --stack mobile` reports no violations |
| The tests actually passing on a device | Not verified in CI. There is no device on a GitHub runner. Run it locally with the steps below |

Nothing here claims a green run it has not had. The web examples are wired into
CI because a browser fits on a runner. A device does not, and pretending
otherwise is how a mobile suite ends up decorative.

## Run it locally

Needs Android Studio or the command line tools, an emulator, and Java.

```bash
npm ci
npm run app                              # downloads ApiDemos-debug.apk into app/
emulator -avd <your-avd> &               # or start one from Android Studio
adb wait-for-device
npm test
```

Appium starts and stops itself through `@wdio/appium-service`. The first run
downloads the UiAutomator2 driver.

```bash
npx wdio run wdio.conf.ts --spec test/specs/navigation.e2e.ts
npx tsc --noEmit
```

Point it at a different device or app with `DEVICE_NAME`, `APP_PATH` and
`APP_ID`.

The lockfile is generated with `--os=linux --cpu=x64 --os=darwin --cpu=arm64` so
it carries the platform specific binaries for both. Without that, a lockfile made
on a Mac makes `npm ci` fail on a Linux runner, and the error names a `sharp`
binary rather than saying what actually went wrong. If you regenerate it, use the
same flags.

## What is in here

```
qa.config.yml               points at the mobile-appium-wdio profile
wdio.conf.ts                one session, capabilities, Appium as a service
test/screens/               MainScreen, AccessibilityScreen
test/specs/navigation.e2e.ts  three tests
app/                        the apk lands here, not committed
```

## The parts worth looking at

**One session for the whole run.** Starting an Appium session costs 10 to 30
seconds. The specs reset app state in `beforeEach` with `mobile: clearApp`
rather than taking a new session per test. That single choice is usually the
difference between a ten minute mobile suite and an hour.

**Locators are getters, not fields.** On web, a Playwright locator is lazy and
building it in a constructor costs nothing. Here an element resolved at import
time binds to whatever was on screen then, and the failure it produces says
nothing useful. This is the main thing that does not carry over from the web
profile.

**Platform branching lives in one method.** `MainScreen.item()` knows about
Android and iOS. No spec does. A spec with `if (driver.isAndroid)` in it is two
specs pretending to be one, and nobody ever reads the second.

**No pauses.** `driver.pause()` is the mobile fixed sleep, and it is more
tempting here than on web because animations are genuinely real. Every wait in
here is `waitForDisplayed` or a retrying matcher.

## Why iOS is not wired up

The profile and the conventions cover both, and `MainScreen.item()` has the iOS
branch in it. What is missing is a second capability block and an iOS build of
the app under test, which needs a macOS machine with Xcode. Adding it is about
twenty lines in `wdio.conf.ts`, and it is left out rather than stubbed so nobody
mistakes a stub for a working iOS run.
