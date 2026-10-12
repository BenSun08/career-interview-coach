# Phase 1 Setup Evidence

**Date**: 2026-10-12
**Scope**: Phase 1, T001–T005 only
**Environment**: Python 3.12.1, Django 5.2.18, Node 24.14.0, npm 11.21.0. The Python runtime requirement is `>=3.12,<3.13`; dependency locks pin package versions and include hashes. The browser packages are exact-version pinned in `package-lock.json`.

No personal data, provider credentials, external services, or paid resources were used. Django tests use a disposable owner-only temporary data root and a process-only synthetic secret. Browser smoke tests use a disposable loopback server and synthetic HTML.

## T004 boundary tests

The first executable RED run used importable placeholder helpers, so failures came from assertions and expected behavior rather than missing imports. `python -m unittest tests.unit.test_test_boundaries` ran seven tests and failed: the clock did not advance, IDs/effects returned placeholders, the temporary directory was not private, two in-memory SQLite connections did not share a table, and the unguarded socket call did not raise the required network-denial exception. This demonstrated the intended gaps before implementing the helpers.

After implementation, the same command passed; a DNS-denial case was then added, bringing the suite to eight tests. Fresh final results:

| Command | Result |
| --- | --- |
| `.venv/bin/python -m unittest tests.unit.test_test_boundaries` | Exit 0; 8 tests passed. |
| `.venv/bin/python manage.py test --settings=config.test_settings tests.unit tests.contract tests.integration tests.migrations` | Exit 0; 8 tests passed; Django system check reported no issues. |

The tests verify controllable aware clocks, explicit ID sequence exhaustion, recorded synthetic effects, owner-only temporary directories, two independent connections to one file-backed SQLite database, and rejection of external DNS, `connect`, `connect_ex`, `sendto`, and `sendmsg` targets without issuing network traffic. A destinationless `sendmsg` must be on a connected loopback socket. `config.test_settings` also clears proxy environment variables, disables external services, and installs the denial boundary before loading Django settings.

## Dependency setup

| Command | Result |
| --- | --- |
| `python3.12 -m venv /private/tmp/career-helper-setup-venv-check` | Exit 0; created a clean Python 3.12.1 environment in a disposable path, then removed it. |
| `.venv/bin/python -m pip install --require-hashes -r requirements-dev.lock` | Exit 0; all locked runtime and development packages were satisfied with hash checking enabled. |
| `npm ci` | Exit 0; clean lockfile install completed (`added 7 packages`). |
| `npm run install:browsers` | Exit 0; Chromium is available in the ignored local `.local/playwright-browsers/` cache. |

## Fresh scaffold checks

| Command | Result |
| --- | --- |
| `.venv/bin/python manage.py check --settings=config.test_settings` | Exit 0; no issues. |
| `.venv/bin/python -m ruff check .` | Exit 0; all checks passed. |
| `.venv/bin/python -m mypy career_helper` | Exit 0; no issues in the application scaffold. |
| `.venv/bin/python manage.py test --settings=config.test_settings tests.unit tests.contract tests.integration tests.migrations` | Exit 0; 8 tests passed and Django system check reported no issues. |
| `npm test` | Exit 0; TypeScript `checkJs` passed, 2 Node browser-rule tests passed, and 1 Playwright fixture smoke test passed. The smoke test confirmed an external request was blocked. |

Playwright requires permission to bind its synthetic server to `127.0.0.1` in this environment. That local-only test ran successfully with loopback binding enabled; it did not access an external service. `npm run install:browsers` is a one-time local setup command and may need internet access on a machine that has not cached Chromium.

## Limits

This evidence covers only the Phase 1 scaffold and its offline boundaries. There are no career-product models, migrations, user workflows, owner provisioning command, job or retention workers, live provider integrations, or human acceptance results. Application setup and acceptance commands in [quickstart.md](../quickstart.md) remain marked as planned. T006 and later tasks were not started.
