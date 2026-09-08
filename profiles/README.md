# Profiles

A profile teaches the agents one stack. It holds no QA reasoning, just the
mechanics: how to run things, where files go, and what good code looks like
here. The agents hold the QA reasoning and know nothing about your runner.

That split is the whole point. Swapping Playwright for Selenium, or TypeScript
for Java, means writing a new profile. It does not mean touching a single agent.

## What is in one

```
profiles/<name>/
  profile.yaml      the machine readable part. Commands, layout, templates.
  CONVENTIONS.md    the prose part. How to write a test here, with examples.
  templates/        skeleton files the author agent copies and fills in.
  ci/               one pipeline file per CI provider this profile supports.
```

## Who reads what

| File | Read by | For |
|---|---|---|
| `profile.yaml` `commands` | maintainer, auditor | Running the suite, rerunning one test |
| `profile.yaml` `layout` | author, auditor | Deciding where a new file goes, finding tests to audit |
| `profile.yaml` `templates` | author | Starting a new test or page object |
| `profile.yaml` `selector_priority` | author, exploratory guide | Picking a locator |
| `CONVENTIONS.md` | author, maintainer | Everything the template cannot express |
| `ci/` | `/qa:init` | Dropping a pipeline into a new project |

## Adding one

1. `cp -r profiles/_template profiles/java-selenium-junit5`
2. Fill in `profile.yaml`. Set `name` to the folder name, it is checked.
3. Write `CONVENTIONS.md`. Show real code. This is the file that decides whether
   generated tests look like they belong in your repo or like they were bolted
   on, so it is worth the hour.
4. Put a real test file in `templates/`, with placeholders where the agent
   should fill in.
5. Add a CI file for each provider you care about.
6. `python3 scripts/validate_profiles.py` to check the wiring.
7. Point a project at it: `stacks.web.profile: java-selenium-junit5` in
   `qa.config.yml`.

## What ships here

| Profile | Language | Runner | Platform | State |
|---|---|---|---|---|
| `ts-playwright` | TypeScript | Playwright | web | working, demo in `examples/web-ts` |
| `py-pytest-playwright` | Python | pytest + Playwright | web | working, demo in `examples/web-python` |
| `mobile-appium-wdio` | TypeScript | WebdriverIO + Appium | mobile | working, demo in `examples/mobile-appium`, typechecked in CI but not run there |
| `_template` | any | any | any | blank starting point |

Java plus Selenium plus JUnit 5 is deliberately not here. It is the obvious next
profile and writing it from `_template` is the fastest way to check whether this
design actually holds up.

## The placeholders

`profile.yaml` commands take these, and the agent substitutes before running:

| Placeholder | Means |
|---|---|
| `{file}` | Path to one test file |
| `{title}` | The test name, for running or rerunning a single case |
| `{tag}` | A tag, marker or grep expression |

If your runner needs something else, add it to `notes` and say how it works.
