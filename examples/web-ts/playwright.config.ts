import { defineConfig, devices } from '@playwright/test';

// BASE_URL matches stacks.web.base_url_env in qa.config.yml. Nothing in this
// project hardcodes a URL.
const baseURL = process.env.BASE_URL ?? 'https://www.saucedemo.com';

const chrome = { ...devices['Desktop Chrome'] };

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,

  // One retry in CI only. Locally a flake should be visible, not smoothed over.
  retries: process.env.CI ? 1 : 0,

  reporter: process.env.CI ? [['html'], ['github']] : [['list'], ['html']],

  use: {
    baseURL,

    // Must match policies.test_id_attribute in qa.config.yml. saucedemo uses
    // data-test, not the data-testid Playwright looks for by default.
    testIdAttribute: 'data-test',

    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'off',
  },

  projects: [
    // Logs in once and writes .auth/user.json.
    { name: 'setup', testMatch: /auth\.setup\.ts/, use: chrome },

    // Tests of login itself, which need to start logged out.
    { name: 'anonymous', testDir: './tests/anonymous', use: chrome },

    // Everything else, handed a ready session. No UI login per test.
    {
      name: 'signed-in',
      testDir: './tests/signed-in',
      use: { ...chrome, storageState: '.auth/user.json' },
      dependencies: ['setup'],
    },
  ],
});
