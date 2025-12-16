import { test, expect } from '@playwright/test';

test('register -> login -> calculator -> profile', async ({ page }) => {
  const user = 'u' + Date.now();
  const email = `${user}@example.com`;

  await page.goto('/register');
  await page.getByPlaceholder('username').fill(user);
  await page.getByPlaceholder('you@example.com').fill(email);
  await page.getByPlaceholder('min 8 chars').fill('Password123!');
  await page.getByRole('button', { name: 'Create account' }).click();

  await page.waitForURL('**/');

  await page.getByRole('button', { name: 'Compute' }).click();
  await expect(page.locator('#calcMsg')).toContainText('Result');

  await page.goto('/profile');
  await page.locator('#p_username').fill(user + 'x');
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.locator('#profileMsg')).toContainText('Saved');
});
