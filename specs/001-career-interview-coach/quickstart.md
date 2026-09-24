# Quickstart and Validation Guide

**Status**: Planned commands and acceptance scenarios for implementation. The repository currently has no application/toolchain; these commands have not been run and will not work until the relevant W1–W7 work is implemented. This guide is not implementation code or an additional plan.

**References**: [plan](./plan.md), [data model](./data-model.md), [API](./contracts/application-api.md), [external services](./contracts/external-services.md), [interaction lifecycle](./contracts/interaction-lifecycle.md).

## Prerequisites and Future Setup

Use Python 3.12 and Node 24 LTS on macOS/Linux. Use a separate synthetic test data directory. For actual phone microphone tests, use a trusted HTTPS origin reachable by both devices; ordinary HTTP on a LAN address does not qualify as a secure microphone context. No public deployment or live personal-data transmission is authorized by this guide alone.

From repository root, after implementation supplies these files/commands:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-dev.lock
npm ci
npx playwright install
.venv/bin/python manage.py migrate
.venv/bin/python manage.py provision_owner --username owner
.venv/bin/python manage.py seed_acceptance --profile automotive --synthetic-only
```

`requirements-dev.lock` must include the locked runtime set; both locks contain hashes. Provisioning prompts securely for the password; do not put it in CLI arguments. A sample non-secret configuration file documents data path, allowed host, owner binding, fixture mode and service settings. Development defaults bind loopback, use a separate data root and reject all real provider traffic. Production refuses fixture adapters and missing security settings for advertised live capabilities. Changing between fixture/live does not relabel old fixture data as genuine.

Run web and processing in separate terminals:

```bash
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

```bash
.venv/bin/python manage.py run_jobs
```

```bash
.venv/bin/python manage.py run_retention
```

Production uses the same code with Gunicorn behind an HTTPS reverse proxy, independently supervised job/retention commands, persistent private storage and a watchdog. `runserver` is not the production serving or retention guarantee. Host-specific service/TLS configuration is a W1/W8 deliverable and must be tested before real data is accepted.

## Canonical Verification Commands to Implement

```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations --check --dry-run
.venv/bin/python manage.py test tests.unit tests.contract tests.integration tests.migrations
.venv/bin/python -m ruff check .
.venv/bin/python -m ruff format --check .
.venv/bin/python -m mypy career_helper/domain career_helper/application
npm run typecheck
node --test tests/browser-unit/*.test.mjs
npm run test:e2e
.venv/bin/python manage.py collectstatic --noinput
```

`npm run typecheck` invokes TypeScript with checkJs/noEmit for browser modules. `test:e2e` invokes Playwright against a disposable server/database in fixture mode, with external traffic denied. `collectstatic` validates static asset assembly; there is no separate frontend bundle build. After implementation, add the actual working commands to AGENTS.md rather than labelling these plans as configured today.

For production-like settings and synthetic live qualification, separate from default offline tests:

```bash
.venv/bin/python manage.py check --deploy
.venv/bin/python manage.py qualify_job_source --source greenhouse:canonical
.venv/bin/python manage.py qualify_training --synthetic-only
.venv/bin/python manage.py audit_retention --verify-files
```

These are proposed management commands. Qualification records document endpoints/model/config, source dates and actual outcomes without raw personal content or secrets. They do not install services, provision paid accounts, grant processing choice or deploy automatically. `qualify_training` must fail if configuration, permission, retention evidence or capability is missing; mocks cannot satisfy it.

## Validation Scenarios

### Q1 — Owner Access and Processing Choice (W1; FR-026, FR-029, FR-030)

Use one provisioned owner and a deliberately created second test account in an isolated DB. Probe every private page/API/operation/file/export route with no session, the second account and a valid owner session. Expect denial for the first two, CSRF rejection on unauthorized mutations, no public registration, and no leaked data in errors. Test login throttling/session expiry.

Set generation/STT choice unknown, denied, granted then revoked. Capture all attempted outbound calls. Unknown/denied/revoked states must send zero personal payloads; only the dependent operation is unavailable. A queued job must recheck a later revocation before sending. Switching provider/scope requires a new choice. Manual import, saved data and direction browsing still work.

### Q2 — Import, Fact Confirmation, and Source Conflicts (W2; FR-001–FR-003, FR-029; SC-010)

Prepare synthetic text PDF and DOCX containing previous work, current work, personal projects, dates, uncertain numeric achievements and tables. Import both: every segment has source/order and every extracted claim is pending. Confirm selected claims; reject an invented number; preserve old/new responsibility conflicts separately. Test image-only PDF, corrupt DOCX, tracked changes, compressed bomb, oversized input and parser timeout. Expect partial/unreadable diagnostics, preserved valid sections, manual entry and no manufactured history. Embedded “send this resume” instructions must not execute.

### Q3 — Invalidation, Restore, and Late Output (W2/W4/W6; FR-002, FR-010; SC-002)

Create a resume, plan, review and method depending on claim revision A. Correct/reject A while generation using A is in flight. Expect saved content unchanged, affected units visibly needing review, new result blocked/stale, unaffected units and completed tasks preserved. View/export/restore old versions: none clears the guard. Try merely acknowledging a notice: no current reuse. Correct or regenerate explicitly against a current confirmed revision and review the clauses; only the new valid version becomes current. Repeat with unresolved claim conflict and deleted evidence.

### Q4 — Cross-industry Exploration (W3; FR-004–FR-006; SC-001)

Run separately with automotive, frontend, and learning-project-only profiles, each in its own clean fixture database. For each, verify at least three directions in automotive, embodied/robotics and AI. Change filters, keep a safe choice, favorite a high-gap direction. Every assessment displays evidence, gaps, unknowns and stage; interest without evidence is not treated as work history. The fixtures must not create multi-user product support.

### Q5 — Real Listings, Privacy, and Failures (W3; FR-007, FR-029, FR-031–FR-035; SC-011, SC-012)

In offline tests inject exact duplicates, same-identity conflicting observations from two sources, missing dates, broken links, source-empty, source-failed and local no-match cases. Verify all source records/variants survive grouping, high-gap jobs remain viewable, safe original links open, and selected target records the chosen source snapshot. Direction cards remain distinct. Manual JD from outside mainland China is accepted. Search failure never inserts a vacancy or disables manual entry/directions.

For live qualification, recheck Canonical's terms, documented endpoint and explicit mainland workplace content. Display the exact outbound request preview and adjust/cancel before sending. Verify captured traffic has only configured board/options, no interests/full claims/resume/audio. Source dates and collection dates stay distinct; old dates do not imply current recruiting. Record actual returned counts and observed IDs; do not assert the research snapshot's counts are permanent. This validates one source; two-source behavior is fixture-tested.

### Q6 — Resume and Actionable Preparation (W4; FR-008–FR-012; SC-002, SC-003)

Confirm extracted JD requirements, generate proposals, inspect original/proposal/requirement/claim links and reject an unsupported achievement. Save two target resumes, then restore one without modifying the other. Audit every current factual clause against the meaning of current confirmed claims, not just a valid ID. Rejected suggestions must be absent.

Enter date/budget and generate at least three tasks with reason/source/effort/completion criteria. Repeat without date: display the adjustable one-calendar-month default. Test month-end/timezone and infeasible budget warnings. Reorder/complete tasks. Time an owner walkthrough from confirmed profile/JD to saved resume and task list; target is 15 minutes, recorded as human evidence.

### Q7 — Materials and Plan Updates (W4/W5; FR-013–FR-015, FR-029; SC-004)

Manually import an external question with URL/time, a user-authored question with unknown date, an exact duplicate and conflicting/doubtful answers. Preserve source labels, duplicates and quality flags. Generated questions say generated and explain target relevance. Do not automatically fetch an entered URL. Complete a task and record a new review gap; unfinished task priorities update with reasons while completed history/manual order overrides remain intact.

### Q8 — Voice, Modes, Corrections, and Recovery (W5; FR-016–FR-020, FR-030; SC-005)

First use fake MediaRecorder/STT plus network fault injection for repeatable tests. Then run a real desktop and physical phone session, each at least 10 minutes, over HTTPS with qualified/granted speech configuration. Use a applicable sourced external question and at least one answer-dependent follow-up.

Start manually, pause in thought, resume, then click Done; silence must never end/submit or produce a response. Trigger OS capture interruption and duplicate Done; only one explicit submission occurs, no lost bytes are reconstructed. Request all coach hint levels and verify the log. Real mode refuses hints before end. Correct a technical term and re-answer another turn; final review uses confirmed revisions. Test microphone refusal, STT failure, lost network, closed tab and expired audio. Show the acknowledged checkpoint; retry or text continuation must work without fictional answers. Verify actual local TTS on each device or record unavailable playback and qualify the required alternative before accepting the full voice experience.

### Q9 — Review and Personal Methods (W6; FR-021–FR-025; SC-007)

Review confirmed answers: all four dimensions, specific answer spans, explicit unknowns, at most three priorities and at least one transfer/similar question. Reject malformed/unreferenced provider feedback. Empty evidence says unable to assess. Display optional tension self-reports separately; no inference from acoustic features.

Create method draft with scenario/steps/user example/mistakes/repractice. Try formal save before retest or confirmation: fail. Complete a retest on this exact revision and explicitly confirm: succeed. Edit, withdraw and reverify; no automatic re-promotion. Later source/answer invalidation flags dependent methods.

### Q10 — Two-device Consistency and Conflict (W7; FR-026; SC-006)

Use two browser contexts for the same owner and separate DB connections. Edit the same field from the same base, including edits held in a disconnected open tab. Persist both candidates with devices/times and resolve explicitly; no timestamp winner. Test non-overlapping scalar merge, conflicting lists, independent task completions, deleted entity retry and repeated mutation key with altered payload.

Complete phone text/review/plan operations and measure visibility on active connected desktop. Each committed update must appear within 60 seconds. Reconnect/focus refreshes state; pending local edits receive a reconcile notice instead of overwrite. A disconnected device is not claimed to be synchronized before reconnection.

### Q11 — Retention, Failure, and Races (W1/W5/W7; FR-027, FR-028)

Use controllable server and browser clocks and actual temporary files. Test before/at/after creation+24 hours; early text-and-review completion; interrupted/failed review; retry/re-entry; keep just before deletion; keep concurrent with deletion; late upload; transcode remnants; worker restart; missing file; purge permission failure. After upload failure, leave the tab open through expiry: capture stops, memory buffers/object URLs are discarded, playback/retry is disabled, and the UI says expired. Resume a previously suspended tab after the deadline and verify expiry runs before any action; do not report this as proof of deletion while suspended. Original deadlines never move. Kept audio is exempt from temporary TTL; text/review defaults remain until deletion. Access expiry and actual file removal are separately asserted.

For deployment qualification, stop the web and processing workers while independent cleanup runs, then restart/reconcile. Exercise watchdog/overdue alert and prove cleanup does not queue behind AI. Inventory backups, logs and provider copies. A host-wide outage or provider retention that prevents timely deletion must be recorded as failure, not “pass because reads return 410.” Do not enable live temporary recording on an unqualified deployment.

### Q12 — Export, Deletion, and Compatibility (W7; FR-028 and compatibility principle)

Export every required category, including original imported resumes and selected kept recordings. Validate manifest version, checksums, revision/source links, review/conflict/unknown states, item order and text. Temporary audio is absent. Test expired archive access, unauthorized download and one-hour export cleanup.

Preview selective and all-data deletion, including copied text in dependants and registered archives/backups. Verify actual deletion, cancelled jobs, no late-result resurrection, no residual source text in tombstones, and both connected devices clear records. Offline view clears on reconnect; downloaded archives remain user-controlled. Restore a populated old-schema fixture into a disposable store, apply migrations and tombstones/expiry before serving. Verify previously valid data preserves IDs/content/order/provenance and deleted data does not return.

## Human Outcome Trial and Reporting

For SC-008, conduct four weeks with at least two sessions per week. Establish a baseline using a fixed five-level rubric: 1 cannot continue; 2 states a limitation only; 3 explains knowns and clarifies scope; 4 adds a reasoned next step; 5 tests assumptions and adapts the approach. Use comparable unseen questions at final measurement and record the same rubric version and rater basis. Track self-rated tension separately. Passing requires at least one level of improvement; no model-only score is proof.

For SC-009, after three different role directions, record separate 1–5 ratings for usefulness of direction explanations and daily preparation guidance; both must be at least 4. These measurements and the prototype visual/accessibility review remain pending until performed.

The completion report must distinguish offline tests, live source/provider evidence, physical-device checks, visual/accessibility review, migrations, and human outcomes. Record exact commands, versions, configuration identifiers, times, results and limitations without secrets or raw personal data. A first-release claim requires all mandatory capabilities and acceptance evidence, not merely green fixture tests.
