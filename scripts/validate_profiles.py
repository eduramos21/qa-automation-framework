#!/usr/bin/env python3
"""Check that every profile is wired up correctly.

A profile is the contract between the stack agnostic agents and one real stack.
If a key is missing or a path is dangling, the agents fail at the worst possible
moment, halfway through writing a test. This catches it up front instead.

Run it from the repo root:

    python3 scripts/validate_profiles.py

Exits 0 when everything checks out, 1 with a list of problems otherwise.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROFILES = ROOT / "profiles"

PLATFORMS = {"web", "mobile", "api", "desktop"}
REQUIRED_TOP = ["name", "language", "runner", "platform"]
REQUIRED_COMMANDS = ["install", "test", "test_one"]
REQUIRED_LAYOUT = ["tests", "test_glob"]


def load(path):
    with path.open() as fh:
        return yaml.safe_load(fh)


def check_profile(directory, problems):
    def fail(msg):
        problems.append("{}: {}".format(directory.name, msg))

    manifest = directory / "profile.yaml"
    if not manifest.exists():
        fail("no profile.yaml")
        return

    try:
        profile = load(manifest)
    except yaml.YAMLError as exc:
        fail("profile.yaml does not parse: {}".format(exc))
        return

    if not isinstance(profile, dict):
        fail("profile.yaml is not a mapping")
        return

    for key in REQUIRED_TOP:
        if not profile.get(key):
            fail("missing required key '{}'".format(key))

    if profile.get("name") and profile["name"] != directory.name:
        fail("name is '{}' but the folder is '{}', they must match".format(
            profile["name"], directory.name))

    platform = profile.get("platform")
    if platform and platform not in PLATFORMS:
        fail("platform '{}' is not one of {}".format(
            platform, ", ".join(sorted(PLATFORMS))))

    commands = profile.get("commands") or {}
    for key in REQUIRED_COMMANDS:
        if not commands.get(key):
            fail("missing commands.{}".format(key))

    test_one = commands.get("test_one") or ""
    if test_one and "{file}" not in test_one and "{title}" not in test_one:
        fail("commands.test_one has no {file} or {title} placeholder, so the "
             "agent cannot rerun a single test")

    layout = profile.get("layout") or {}
    for key in REQUIRED_LAYOUT:
        if not layout.get(key):
            fail("missing layout.{}".format(key))

    templates = profile.get("templates") or {}
    if not templates.get("test"):
        fail("missing templates.test")
    for name, rel in templates.items():
        if rel and not (directory / rel).exists():
            fail("templates.{} points at '{}' which does not exist".format(name, rel))

    for provider, rel in (profile.get("ci") or {}).items():
        if rel and not (directory / rel).exists():
            fail("ci.{} points at '{}' which does not exist".format(provider, rel))

    if not (directory / "CONVENTIONS.md").exists():
        fail("no CONVENTIONS.md, the author agent has nothing to imitate")


def check_example_config(problems, known):
    example = ROOT / "qa.config.example.yml"
    if not example.exists():
        problems.append("qa.config.example.yml is missing")
        return
    try:
        config = load(example)
    except yaml.YAMLError as exc:
        problems.append("qa.config.example.yml does not parse: {}".format(exc))
        return
    for stack, settings in (config.get("stacks") or {}).items():
        name = (settings or {}).get("profile")
        if name not in known:
            problems.append(
                "qa.config.example.yml stacks.{} points at profile '{}' which "
                "does not exist".format(stack, name))


def main():
    if not PROFILES.is_dir():
        print("no profiles/ directory found at {}".format(PROFILES))
        return 1

    # Folders starting with _ are starting points, not real profiles. They are
    # full of TODO placeholders on purpose.
    directories = sorted(
        d for d in PROFILES.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    )

    problems = []
    for directory in directories:
        check_profile(directory, problems)

    check_example_config(problems, {d.name for d in directories})

    if problems:
        print("Found {} problem(s):\n".format(len(problems)))
        for problem in problems:
            print("  - {}".format(problem))
        return 1

    print("{} profile(s) OK: {}".format(
        len(directories), ", ".join(d.name for d in directories) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
