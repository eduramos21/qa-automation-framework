# qa-automation-framework

A skeleton for wiring AI agents into a real test automation stack, on web and
native mobile. It ships the agents, the skills they use, and the connective
tissue that lets them work against whatever language, runner and CI a project
already picked.

Being built in phases. See the phase table below for what is live.

Full docs: https://eduramos21.github.io/qa-automation-framework/

## Status

| Phase | What | State |
|---|---|---|
| 0 | Skeleton, config contract, profile template, validator | done |
| 1 | TypeScript and Python web profiles, runnable demos | done |
| 2 | Requirement refinement and test design | done |
| 3 | Automated test generation | done |
| 4 | Assisted exploratory and manual testing | done |
| 5 | Test maintenance and suite auditing | done |
| 6 | Mobile profile and Appium demo | done |
| 7 | Docs site | in progress |

## Try the demos

Both run against saucedemo.com, so they need no setup and no credentials.

```bash
cd examples/web-ts && npm ci && npx playwright install chromium && npx playwright test
cd examples/web-python && pip install -r requirements.txt && playwright install chromium && pytest
```

Same five behaviours, two stacks, one set of agents. That is what the profile
system buys.

## License

MIT
