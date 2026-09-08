#!/usr/bin/env python3
"""Checks that qa-policy finds what it claims to find.

A policy checker that never fires is worse than none, because it reads as
coverage. These samples are the shapes it is supposed to catch, and the clean
ones are the shapes it must not fire on.

Run: python3 scripts/test_qa_policy.py
"""

import importlib.machinery
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_loader = importlib.machinery.SourceFileLoader("qa_policy", str(ROOT / "bin" / "qa-policy"))
_spec = importlib.util.spec_from_loader("qa_policy", _loader)
qa_policy = importlib.util.module_from_spec(_spec)
_loader.exec_module(qa_policy)

failures = []


def fires(rule, code, should_fire=True, label=""):
    description, finder, _ = qa_policy.RULES[rule]
    hits = list(finder(code))
    ok = bool(hits) == should_fire
    verb = "fires" if should_fire else "stays quiet"
    print("  {}  {} {} on {}".format("ok " if ok else "FAIL", rule, verb, label))
    if not ok:
        failures.append("{} on {}: got {}".format(rule, label, hits))


print("hard_sleeps:")
fires("hard_sleeps", "await page.waitForTimeout(2000);", label="playwright ts")
fires("hard_sleeps", "page.wait_for_timeout(2000)", label="playwright python")
fires("hard_sleeps", "time.sleep(3)", label="python")
fires("hard_sleeps", "Thread.sleep(1000);", label="java")
fires("hard_sleeps", "driver.implicitly_wait(10)", label="selenium implicit wait")
fires("hard_sleeps", "cy.wait(500)", label="cypress fixed wait")
fires("hard_sleeps", "cy.wait('@getUser')", should_fire=False, label="cypress alias wait")
fires("hard_sleeps", "// await page.waitForTimeout(2000);", should_fire=False, label="commented out")
fires("hard_sleeps", "await expect(badge).toHaveText('1');", should_fire=False, label="a real wait")

print("absolute_xpath:")
fires("absolute_xpath", 'page.locator("//div[3]/span")', label="positional")
fires("absolute_xpath", 'By.xpath("/html/body/div")', label="rooted at html")
fires("absolute_xpath", 'page.locator("//button[@data-test=\'go\']")', should_fire=False,
      label="attribute xpath, not positional")

print("conditional_assertions:")
fires("conditional_assertions", """
  if (await banner.isVisible()) {
    await expect(banner).toHaveText('Welcome');
  }
""", label="assertion inside an if")
fires("conditional_assertions", """
  if (await banner.isVisible()) {
    await banner.click();
  }
  await expect(page).toHaveURL(/home/);
""", should_fire=False, label="assertion after the if, not inside")

print("no_assertion:")
fires("no_assertion", """
test('adds an item', async ({ page }) => {
  await page.goto('/');
  await page.click('#add');
});
""", label="test that never checks")
fires("no_assertion", """
test('adds an item', async ({ page }) => {
  await page.click('#add');
  await expect(badge).toHaveText('1');
});
""", should_fire=False, label="test that checks")
fires("no_assertion", """
def test_adds_an_item(page):
    page.click("#add")
""", label="python test that never checks")

print("shared_mutable_state:")
fires("shared_mutable_state", "test.describe.serial('checkout', () => {", label="serial describe")
fires("shared_mutable_state", "let orderId;", label="module level mutable")
fires("shared_mutable_state", "const ITEM_TOTAL = 39.98;", should_fire=False, label="module level constant")

print("forbidden_in:")
block = """
policies:
  forbid:
    - hard_sleeps
    - absolute_xpath
"""
got = qa_policy.forbidden_in(block)
assert got == ["hard_sleeps", "absolute_xpath"], got
print("  ok   block list")
got = qa_policy.forbidden_in("  forbid: [hard_sleeps, 'no_assertion']\n")
assert got == ["hard_sleeps", "no_assertion"], got
print("  ok   inline list")
assert qa_policy.forbidden_in("policies:\n  test_id_attribute: data-test\n") == []
print("  ok   no forbid block")

print("\nthe shipped suites stay clean:")
for config in sorted(ROOT.glob("examples/*/qa.config.yml")):
    forbid = qa_policy.forbidden_in(config.read_text())
    tests = qa_policy.test_files_for("web", config, config.parent)
    assert tests, "found no test files for {}".format(config)
    violations = qa_policy.check(tests, forbid)
    assert not violations, "{}: {}".format(config, violations)
    print("  ok   {} files under {}".format(len(tests), config.parent.name))

if failures:
    print("\n{} failure(s)".format(len(failures)))
    for failure in failures:
        print("  - {}".format(failure))
    sys.exit(1)

print("\nall good")
