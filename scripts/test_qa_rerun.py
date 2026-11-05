#!/usr/bin/env python3
"""Checks that qa-rerun resolves the right command and reads the pattern right.

Run: python3 scripts/test_qa_rerun.py
"""

import importlib.machinery
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

_loader = importlib.machinery.SourceFileLoader("qa_rerun", str(ROOT / "bin" / "qa-rerun"))
_spec = importlib.util.spec_from_loader("qa_rerun", _loader)
qa_rerun = importlib.util.module_from_spec(_spec)
_loader.exec_module(qa_rerun)

failures = []


def check(label, got, want):
    ok = got == want
    print("  {}  {}".format("ok " if ok else "FAIL", label))
    if not ok:
        failures.append("{}: got {!r}, want {!r}".format(label, got, want))


print("command_for:")
profile = (
    "commands:\n"
    "  install: npm ci\n"
    '  test_one: npx playwright test {file} -g "{title}"\n'
    "  test: npx playwright test\n"
)
check("test_one", qa_rerun.command_for("test_one", profile),
      'npx playwright test {file} -g "{title}"')
check("missing key", qa_rerun.command_for("test_tagged", profile), None)

print("\nresolve_alone_command, using a shipped example:")
example = ROOT / "examples" / "web-ts"
template, error = qa_rerun.resolve_alone_command(example / "tests")
check("no error", error, None)
check("template", template, 'npx playwright test {file} -g "{title}"')

print("\nno config above the file:")
with tempfile.TemporaryDirectory() as tmp:
    template, error = qa_rerun.resolve_alone_command(Path(tmp))
    check("template is None", template, None)
    check("error says so", error is not None and "No qa.config.yml" in error, True)

print("\nverdict, the four named rows plus the partial cases:")
check("1 or 2", qa_rerun.verdict(False, False, False),
      "Fails alone, fails in the suite, fails parallel -> cause 1 or 2, a real "
      "difference.")
check("isolation", qa_rerun.verdict(True, False, False),
      "Passes alone, fails in the suite, fails parallel -> cause 4, isolation.")
check("timing", qa_rerun.verdict(True, True, False),
      "Passes alone, passes in the suite, fails parallel -> cause 3 or 4, timing "
      "under load.")
check("clean", qa_rerun.verdict(True, True, True),
      "Passes everywhere -> cause 5, or it is already fixed. Check what changed.")
check("alone only, failing", "cause 1 or 2" in qa_rerun.verdict(False, None, None), True)
check("alone only, passing", "flaky together" in qa_rerun.verdict(True, None, None), True)

print("\nrun_n and summarize, against real commands:")
results = qa_rerun.run_n("true", 3, Path.cwd())
check("all true", results, [True, True, True])
clean = qa_rerun.summarize("test", results)
check("summarize clean", clean, True)
results = qa_rerun.run_n("false", 3, Path.cwd())
clean = qa_rerun.summarize("test", results)
check("summarize dirty", clean, False)

if failures:
    print("\n{} failure(s)".format(len(failures)))
    for failure in failures:
        print("  - {}".format(failure))
    sys.exit(1)

print("\nall good")
