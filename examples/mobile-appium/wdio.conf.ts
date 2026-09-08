// APP_ID matches what the specs reset between tests. Nothing hardcodes a path.
const appId = process.env.APP_ID ?? 'io.appium.android.apis';
const app = process.env.APP_PATH ?? './app/ApiDemos-debug.apk';

export const config: WebdriverIO.Config = {
  runner: 'local',

  specs: ['./test/specs/**/*.e2e.ts'],

  // One device, so one session. Parallelism here is a hardware decision, not a
  // config one: two sessions against one emulator do not work.
  maxInstances: 1,

  capabilities: [
    {
      platformName: 'Android',
      'appium:automationName': 'UiAutomator2',
      'appium:deviceName': process.env.DEVICE_NAME ?? 'Android Emulator',
      'appium:app': app,
      'appium:appPackage': appId,
      'appium:autoGrantPermissions': true,
      'appium:newCommandTimeout': 240,
      // Keep the session across specs. Starting one costs 10 to 30 seconds and
      // the app reset in beforeEach is what makes tests independent.
      'appium:noReset': false,
      'appium:fullReset': false,
    },
  ],

  services: ['appium'],
  framework: 'mocha',
  reporters: ['spec'],
  mochaOpts: { ui: 'bdd', timeout: 120000 },

  logLevel: 'warn',
  waitforTimeout: 10000,
  connectionRetryTimeout: 120000,
  connectionRetryCount: 2,
};
