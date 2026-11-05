---
description: Check staged changes against policies.forbid before you commit, the same check the edit hook runs, run on demand. Use when asked to pre-validate, pre-commit check, or lint a change before committing, or when the user wants this standalone without the rest of the plugin.
---

# Pre-validate before committing

Input: `$ARGUMENTS`. Nothing (checks what is staged), or specific file paths.

This is `qa-policy`, the same checker the `PostToolUse` edit hook already runs,
pointed at what you are about to commit instead of what was just written. It is
a leaf skill: it does not design, write, or fix anything, it only reports.

## Steps

**1. Read the setup.** `qa-context <platform>` if you need to know which stack
you are in. `qa-policy` resolves this itself from `qa.config.yml`, so this step
is only needed if you want to explain the result.

**2. Find what to check.** No arguments: `git diff --cached --name-only`, the
files about to be committed. Arguments given: check those paths instead.

**3. Run it.**

```bash
qa-policy --changed-only <file> [<file> ...]
```

`--changed-only` means only lines this working tree added or changed get
reported, same as the edit hook. A file that already had three sleeps in it
before this change reports nothing for those three; a new one in the same file
reports.

**4. Report.** Exit 0: say so, nothing to fix. Nonzero: show the violations
`qa-policy` printed, by file and line, and stop there — do not edit the file
yourself unless asked. Fixing a policy violation can change what the test
actually verifies, and that is a decision for whoever wrote it.

## Using this without the plugin installed

`qa-policy` is a standalone, stdlib-only Python 3 script. A developer who wants
only this check, not the rest of the plugin, has two options:

- **The `pre-commit` framework.** Add this repo as a hook source:

  ```yaml
  # .pre-commit-config.yaml, in the target project
  repos:
    - repo: https://github.com/eduramos21/qa-automation-framework
      rev: <tag or commit>
      hooks:
        - id: qa-policy
  ```

  See `.pre-commit-hooks.yaml` at this repo's root for the hook definition.

- **A raw git hook, husky, lint-staged, or anything else that runs a shell
  command on staged files.** Clone or vendor `bin/qa-policy` and `bin/qa-context`
  (they must stay siblings) and call:

  ```bash
  bin/qa-policy --changed-only <staged files>
  ```

Either way, the target repo still needs a `qa.config.yml` with at least a
`policies.forbid` list — `qa-policy` has nothing to check against otherwise. A
bare `policies:` block with no `stacks:` is enough; the full plugin setup is
not required.

## Rules

**Report, do not silently fix.** This skill's job is the same as the edit hook's:
catch it before it lands and name it. Changing the test to satisfy the checker
is a different decision than the one this skill is scoped to make.

**Do not loosen `--changed-only`.** Checking a whole legacy file on every commit
reports violations nobody introduced today and gets the hook disabled. That
problem belongs to `/qa:audit`, not here.

## Next

Violations found: fix them, or run `/qa:fix` if one is a real flake rather than
a policy miss. Clean: commit as planned.
