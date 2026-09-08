---
description: Resolve the project's QA setup, which profile is active, how to run tests, and what the code conventions are. Use at the start of any QA task, before writing a test, reading a suite, refining a requirement, or auditing anything. Also use when a QA task fails because the profile or config could not be found.
---

# Reading the QA setup

Nothing in this plugin knows what stack a project uses until it asks. Run this
first, always, before touching a test file or reasoning about the suite:

```bash
qa-context              # every stack in the config
qa-context web          # just one stack
qa-context --paths      # paths only, when you already know the contents
```

If `qa-context` is not on PATH, run it from the plugin: `bin/qa-context`.

## What comes back

```
config:       /repo/qa.config.yml
project root: /repo
web:          ts-playwright -> /plugin/profiles/ts-playwright

===== /repo/qa.config.yml =====
...the whole config...

===== /plugin/profiles/ts-playwright/profile.yaml =====
...commands, layout, templates, selector priority...

conventions for web: /plugin/profiles/ts-playwright/CONVENTIONS.md
```

Read `CONVENTIONS.md` before you write or change any test. It is the difference
between code that looks like it belongs in the repo and code that looks bolted
on. It is not optional and it is not a summary of the profile, it holds the
things the machine readable part cannot express.

## Which file answers what

| Question | Where |
|---|---|
| What is this project, what are the house rules | `qa.config.yml` |
| Which stack am I in | `stacks.<platform>.profile` |
| Where does test code live | `stacks.<platform>.root` plus `layout` in the profile |
| How do I run the suite, or one test | `commands` in the profile |
| What locator should I reach for | `selector_priority`, then `CONVENTIONS.md` |
| What does a test file look like here | `templates`, then `CONVENTIONS.md` |
| What will an audit fail me for | `policies.forbid` |
| Where do requirements come from, where do bugs go | `requirements`, `tracker` |

## Rules

**Never hardcode a command.** If you need to rerun one test, take
`commands.test_one` and substitute `{file}` and `{title}`. Do not type
`npx playwright test` from memory, the project may have a wrapper.

**Never hardcode a URL.** `stacks.<platform>.base_url_env` names the env var.

**Obey `policies`.** `forbid` is not advice. A generated test that contains
anything on that list is wrong even if it passes.

**Project profiles win.** `qa-context` looks in `<project>/profiles/` before the
plugin's own. A project that needs a tweak forks one profile, not the plugin.

## When it fails

| Output | What it means | Do this |
|---|---|---|
| `No qa.config.yml found` | Not a set up project, or you are in the wrong directory | Run `/qa:init`, or `qa-context --from <path>` |
| `profile 'x' NOT FOUND` | Config names a profile that does not exist | Check the spelling, or add it from `profiles/_template` |
| `declares no stacks` | Config is a stub | Fill in the `stacks` block |

Do not guess past any of these. Working from a wrong assumption about the stack
produces tests that look right and do not run, which costs more to clean up than
stopping to ask.
