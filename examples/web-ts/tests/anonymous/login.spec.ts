import { expect, test } from '@playwright/test';

import { LoginPage } from '../../pages/LoginPage';

test.describe('login', () => {
  test('a valid user reaches the inventory page', async ({ page }) => {
    const login = new LoginPage(page);

    await login.goto();
    await login.signIn('standard_user', 'secret_sauce');

    await expect(page).toHaveURL(/inventory\.html/);
  });

  test('a locked out user sees an error and stays on the login page', async ({ page }) => {
    const login = new LoginPage(page);

    await login.goto();
    await login.signIn('locked_out_user', 'secret_sauce');

    await expect(login.error).toContainText('locked out');
    await expect(page).not.toHaveURL(/inventory\.html/);
  });

  test('a wrong password does not say which field was wrong', async ({ page }) => {
    const login = new LoginPage(page);

    await login.goto();
    await login.signIn('standard_user', 'not_the_password');

    // Leaking which half of the pair was wrong hands an attacker a user list.
    await expect(login.error).toContainText('Username and password do not match');
  });
});
