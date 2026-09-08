import { expect, test as setup } from '@playwright/test';

import { LoginPage } from '../pages/LoginPage';

const AUTH_FILE = '.auth/user.json';

// Runs once, before the signed-in project. Every test that needs a session gets
// it from the saved storage state instead of logging in through the UI again.
setup('sign in once and save the session', async ({ page }) => {
  const login = new LoginPage(page);

  await login.goto();
  await login.signIn(
    process.env.E2E_USER ?? 'standard_user',
    process.env.E2E_PASSWORD ?? 'secret_sauce',
  );

  await expect(page).toHaveURL(/inventory\.html/);

  await page.context().storageState({ path: AUTH_FILE });
});
