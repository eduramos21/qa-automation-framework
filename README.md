# qa-automation-framework

A skeleton for wiring AI agents into a real test automation stack, on web and
native mobile. It ships the agents, the skills they use, and the connective
tissue that lets them work against whatever language, runner, CI and tracker a
project already picked.

Five QA workflows, working against one project:

- Requirement refinement and test design
- Assisted exploratory and manual testing
- Automated test generation
- Test maintenance and refactoring
- Quality auditing of automation suites

Full docs: **https://eduramos21.github.io/qa-automation-framework/**

## The idea

Two layers with one contract between them.

**The AI layer**, `agents/` and `skills/`, knows QA. It knows nothing about
Playwright or pytest.

**The profile layer**, `profiles/<name>/`, knows one stack. How to run it, where
files go, what good code looks like there. No QA reasoning in it.

**The contract** is `qa.config.yml` at the project root, plus a `profile.yaml`
in each profile.

```yaml
# qa.config.yml
stacks:
  web:
    profile: ts-playwright       # this line picks your language and runner
    root: e2e/
    base_url_env: BASE_URL
ci:
  provider: github-actions       # github-actions | gitlab-ci | jenkins
tracker:
  provider: jira                 # jira | github-issues | none
  project_key: SHOP
policies:
  test_id_attribute: data-testid
  forbid: [hard_sleeps, absolute_xpath, conditional_assertions]
```

```yaml
# profiles/ts-playwright/profile.yaml
commands:
  test_one: npx playwright test {file} -g "{title}"
layout:
  tests: tests/
  test_glob: "**/*.spec.ts"
selector_priority: [getByRole, getByLabel, getByTestId, getByText]
```

When an agent needs to rerun one test it reads `commands.test_one`. When it
needs to write a page object it reads the template and `CONVENTIONS.md`. That is
why the framework is open on language, runner and CI: adding Java plus Selenium
means writing four files and changing zero agents.

One command hands an agent all of it:

```
$ qa-context web
config:       /repo/qa.config.yml
web:          ts-playwright -> /plugin/profiles/ts-playwright
===== ...the config, the profile, and a pointer at the conventions... =====
```

## Install

```
/plugin marketplace add eduramos21/qa-automation-framework
/plugin install qa@eduramos21-qa
```

Then in a project:

```
/qa:init
```

That works out the language, runner and CI from the repo, asks about what it
cannot see, writes `qa.config.yml`, and drops in a pipeline file.

To try it without installing, `claude --plugin-dir .` from a clone.

## The workflows

| Command | Does | Produces |
|---|---|---|
| `/qa:refine` | Ticket to testable acceptance criteria, ambiguities, risk. Asks the questions that need a human | `qa/requirements/<id>.md` |
| `/qa:design` | Risk scored coverage matrix. What to check, at which layer, what not to cover | `qa/design/<id>.md` |
| `/qa:explore` | Session based exploratory testing in a real browser or on a device | `qa/sessions/<date>-<charter>.md` |
| `/qa:generate` | Writes tests in the profile's style, runs them, then breaks them to prove they can fail | test files, plus what it did not write |
| `/qa:fix` | Triages through five causes before changing anything, fixes the cause once | edits, plus what it found and did not fix |
| `/qa:audit` | Nine area rubric with evidence, findings ranked by cost over effort | `qa/audit/<date>.md` |

## Try the demos

Both run against saucedemo.com, so they need no setup and no credentials.

```bash
cd examples/web-ts
npm ci && npx playwright install chromium && npx playwright test
# 9 passed (2.6s)

cd examples/web-python
pip install -r requirements.txt && playwright install chromium && pytest
# 5 passed in 4.31s
```

`examples/mobile-appium` runs WebdriverIO plus Appium against an Android
emulator. It is typechecked in CI but not run there, because there is no device
on a GitHub runner, and its README says so rather than implying a green run it
has not had.

## A worked example, end to end

`examples/artifacts/` holds one ticket taken all the way through, against the
same site the demo suites test. Every number in it was checked against the
running site.

**The ticket** says the checkout page should show item total, tax and total, and
that tax is 8%. Three acceptance criteria, one of which is "tax is calculated
correctly". A developer commented that it should be quick.

**`/qa:refine`** turns that into five acceptance criteria, a decision table, a
risk table, and five open questions. Two of them are why the story was not ready
to build: nobody said whether to round half up, half even or truncate, and
nobody said whether the total adds the displayed tax or the raw one. Three
developers would pick three answers and all three would satisfy "correctly".
That is one cent per order, nobody reports it, and finance finds it at month
end.

**`/qa:design`** produces thirteen conditions, risk scored and assigned to a
layer. Eight are unit, three are e2e, one waits on an open question, one is
deliberately not automated. It picks its test cart on purpose: $29.99 plus $9.99
gives a raw tax of $3.1984, so truncation gives $3.19 and rounding gives $3.20.
A cart where both agree would pass either way and tell you nothing.

**`/qa:generate`** writes the three e2e rows, runs them, then breaks each one to
confirm it fails for the right reason. It leaves the eight unit rows unwritten,
because this project has no unit layer and promoting them to e2e would make them
slow and make them fail without saying which of forty things broke. It also
finds that half an acceptance criterion is untestable: the requirement says the
confirmation repeats the total, and the confirmation page shows no amount at
all.

**`/qa:explore`** runs a 55 minute session against a charter the design produced
and finds three real defects on the live site. The back button after confirming
an order returns to a live Finish button and confirms again. Emptying the cart
in a second tab does not stop the first tab confirming. Navigating straight to
the overview URL with an empty cart shows `Item total: $0` next to `Tax: $0.00`
and lets a $0.00 order through. All three look like one cause, which turns three
fixes into one.

**`/qa:audit`** scores the resulting suite 5 on speed, isolation, waiting and
assertions, and 2 on layers and coverage. Both twos are the same thing: the
highest risk item in the requirement is a unit row, there is no unit layer, so
nothing in the repo would catch a rounding error.

None of those gaps is an accident. Each was a recorded decision. The audit's job
is noticing that the decisions have not been acted on since.

## Repo layout

```
.claude-plugin/     plugin manifest and marketplace entry
agents/             test-author, test-maintainer, suite-auditor
skills/             the workflows and the reference skills
bin/                qa-context, qa-policy
hooks/              one PostToolUse hook, blocks forbidden patterns on write
profiles/           ts-playwright, py-pytest-playwright, mobile-appium-wdio, _template
examples/           three runnable projects, plus the artifacts above
scripts/            the checks that run in CI
docs/               the site, plain HTML and CSS, no build step
```

## Adding a stack

```bash
cp -r profiles/_template profiles/java-selenium-junit5
# fill in profile.yaml, write CONVENTIONS.md with real code
python3 scripts/validate_profiles.py
```

Then point a project at it with `stacks.web.profile: java-selenium-junit5`. No
agent changes.

Java plus Selenium plus JUnit 5 is deliberately not shipped. It is the obvious
next profile, and writing it from the template is the fastest way to find out
whether this design holds up.

## Phases

| Phase | What | State |
|---|---|---|
| 0 | Skeleton, config contract, profile template, validator | done |
| 1 | TypeScript and Python web profiles, runnable demos | done |
| 2 | Requirement refinement and test design | done |
| 3 | Automated test generation | done |
| 4 | Assisted exploratory and manual testing | done |
| 5 | Test maintenance and suite auditing | done |
| 6 | Mobile profile and Appium demo | done |
| 7 | Docs site | done |

## License

MIT
