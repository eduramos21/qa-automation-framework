---
description: Set up the QA framework in a project. Works out the stack, writes qa.config.yml, and drops in a CI file. Use when starting on a repo that has no qa.config.yml, when qa-context says no config was found, or when the user says set this up, init, or wire this in.
---

# Set up a project

Input: `$ARGUMENTS`, optionally a path. Otherwise the current repo.

The goal is one `qa.config.yml` that is true. A config that guesses wrong is
worse than no config, because every agent afterwards trusts it.

## Steps

**1. Look before asking.** Work out what you can from the repo:

| Look at | Tells you |
|---|---|
| `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `*.csproj` | language |
| dependencies and dev dependencies | runner. `@playwright/test`, `selenium`, `cypress`, `pytest`, `junit`, `appium` |
| `playwright.config.*`, `pytest.ini`, `wdio.conf.*`, `cypress.config.*`, `testng.xml` | runner, and often where tests live |
| existing test folders | `stacks.<platform>.root` and `layout` |
| `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/` | `ci.provider` |
| `.git/config` remote, existing issue links in commits | `tracker.provider` |
| a `docs/`, `specs/` or `requirements/` folder | `requirements.source` and path |
| how existing tests pick elements | `policies.test_id_attribute` |

**2. Match a profile.** List what is in `profiles/` in the plugin, plus any
`profiles/` next to the project. Three outcomes:

- **Nothing matches the language and runner.** Say so and run `/qa:profile`,
  which reads their suite and drafts one. Do not force a near match, a Selenium
  project pointed at the Playwright profile generates code that does not compile.
- **One matches and the repo has no tests yet.** Use it as is.
- **One matches and the repo already has a suite.** Use it, and say that the
  shipped `CONVENTIONS.md` describes a house style that is probably not theirs.
  Offer `/qa:profile` to rewrite it from their code. They can skip it and come
  back when the first generated test looks wrong, which is the usual moment.

**3. Ask about the rest.** Only what the repo cannot tell you. Usually the
tracker and project key, where requirements live, and the base URL env var name.
Use AskUserQuestion with your best guess first.

**4. Write `qa.config.yml`.** At the project root. Base it on
`qa.config.example.yml` from the plugin, keep the comments that explain a
non-obvious choice, drop the rest. Fill in `policies` from what the existing
tests already do rather than from the example, since the point is to describe
this project.

**5. Drop in CI.** If `ci.provider` matches a file in the profile's `ci/` folder,
copy it to the right place and adjust the working directory to match
`stacks.<platform>.root`. If a pipeline already exists, do not overwrite it. Show
the diff you would make and let the user decide.

**6. Check it.** Run `qa-context`. It should resolve every stack. Then run the
profile's `commands.test` to confirm the suite actually runs from a clean state.

**7. Say what is next.** On a repo that already has a suite, `/qa:audit` first:
it needs nothing but this config, reads code they already have, and hands back
something useful in one go. On a new project, `/qa:refine` with the first
requirement.

## Rules

**Describe, do not prescribe.** `policies` should say what this project already
does. If the existing tests use `data-qa`, write `data-qa`, do not write
`data-testid` because the example does. You can point out a policy worth
tightening, separately, after the config is true.

**Do not invent a profile match.** No profile is a normal outcome, and
`/qa:profile` builds one by reading the suite. Guessing wrong costs more than
either.

**A matching profile is not a matching style.** The runner being right does not
mean the conventions are. On a repo that already has tests, say so.

**Do not overwrite.** An existing `qa.config.yml` or pipeline gets a proposed
diff, not a replacement.
