#!/usr/bin/env python3
"""Checks for the one piece of qa-context that can be quietly wrong.

stacks_in reads the stacks block out of qa.config.yml with a regex instead of a
YAML parser, which keeps the script dependency free. That trade is only safe if
the regex handles the shapes real configs come in: commented out stacks, extra
keys under a stack, and a following top level key.

Run: python3 scripts/test_qa_context.py
"""

import importlib.machinery
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

spec = importlib.util.spec_from_loader(
    "qa_context",
    importlib.machinery.SourceFileLoader("qa_context", str(ROOT / "bin" / "qa-context")),
)
qa_context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa_context)
stacks_in = qa_context.stacks_in


def check(label, text, expected):
    actual = stacks_in(text)
    assert actual == expected, "{}: expected {}, got {}".format(label, expected, actual)
    print("  ok  {}".format(label))


print("stacks_in:")

check("plain", """
stacks:
  web:
    profile: ts-playwright
    root: e2e/
""", {"web": "ts-playwright"})

check("two stacks with extra keys", """
project:
  name: shop
stacks:
  web:
    profile: ts-playwright
    root: e2e/
    base_url_env: BASE_URL
  mobile:
    profile: mobile-appium-wdio
    platforms: [android, ios]
ci:
  provider: jenkins
""", {"web": "ts-playwright", "mobile": "mobile-appium-wdio"})

check("commented out stack is not picked up", """
stacks:
  web:
    profile: ts-playwright
  # mobile:
  #   profile: mobile-appium-wdio
""", {"web": "ts-playwright"})

check("stops at the next top level key", """
stacks:
  web:
    profile: ts-playwright
tracker:
  provider: jira
  profile: not-a-stack-profile
""", {"web": "ts-playwright"})

check("quoted value", """
stacks:
  web:
    profile: "ts-playwright"
""", {"web": "ts-playwright"})

check("no stacks block", "project:\n  name: shop\n", {})

# The configs that actually ship have to survive it too.
print("shipped configs:")
for config in sorted(ROOT.glob("examples/*/qa.config.yml")):
    found = stacks_in(config.read_text())
    assert found, "{} parsed to no stacks".format(config)
    print("  ok  {} -> {}".format(config.relative_to(ROOT), found))

print("\nall good")
