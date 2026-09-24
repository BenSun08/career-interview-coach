# Implementation Plan: Career Direction and Interview Growth Coach

**Git branch**: `main` | **Observed HEAD**: `f678297` | **Spec Kit feature**: `001-career-interview-coach` | **Date**: 2026-09-25 | **Spec**: [spec.md](./spec.md)

**Status**: Technical design proposed for review. Planning only; tasks and implementation are not authorized by this document.

**Input**: Approved [specification](./spec.md), [constitution v1.1.0](../../.specify/memory/constitution.md), [prototype index](./prototype.md), [UX addendum](./ux-addendum.md), and completed [requirements checklist](./checklists/requirements.md).

## Summary

Deliver the complete first usable release for one authenticated owner: verify imported career claims, explore directions, discover real mainland-China vacancies, prepare a fact-backed resume and learning plan, practise through manual-turn voice interviews, and turn evidence-based reviews into tested personal methods. Desktop supports the full workflow; phone supports practice, hints, short reviews, and shared progress. P2 stories remain part of this release.

Use one Django application with server-rendered screens, focused browser modules, SQLite, private files, and supervised processing/retention commands. Core decisions remain pure Python functions; application services own transactions, authorization, and effects. No application code, package manifest, separate approved technical architecture, persisted application data, or published API was found. This proposes the initial technical stack while preserving the repository's approved behavioral and data boundaries. If another approved architecture is supplied, reconcile it here before implementation.

This is the sole implementation plan. Research, data model, contracts, and validation guide support it. Stop after Spec Kit Phase 1 and plan review; do not create another plan or generate `tasks.md` in this command.

## Technical Context

| Item | Decision |
| --- | --- |
| Language/version | Python 3.12; ES2022 browser JavaScript modules with JSDoc/checkJs; HTML/CSS. |
| Primary dependencies | Django 5.2 LTS; Gunicorn for production; `pypdf` and `python-docx` for required extraction. Standard-library HTTP, UUIDs, hashing, ZIP and date utilities. Exact supported patch releases locked during foundation work. |
| Storage | One SQLite database on persistent local disk; private original documents and audio outside the static root. One host, short write transactions; no shared network filesystem. |
| Testing | Django/unittest, file-backed SQLite concurrency tests, Node built-in browser-rule tests, Playwright, Ruff, mypy for domain/application contracts, TypeScript checkJs. Node 24 LTS is development-only. |
| Platform | Continuously running Linux host with HTTPS and persistent disk; macOS/Linux development. Desktop Chrome/Edge/Safari and physical mobile Safari/Chrome acceptance. |
| Project type | Single-owner responsive web application; same codebase for web, bounded job worker, and independent retention command. No native app or general offline replica. |
| Performance goals | SC-006: saved phone changes visible on connected active desktop within 60 seconds; visible-tab polling every 10 seconds and immediate focus/reconnect refresh. SC-003: timed resume-plus-plan flow within 15 minutes. No invented model latency SLA. |
| Constraints | Owner-only access; immutable provenance; explicit conflicts; manual Done submission; processing choices; recording deletion at earlier of transcript-and-review completion or creation plus 24 hours. |
| Scale/scope | One owner, two primary devices; six stories, 35 FRs, 12 SCs; at least nine directions across automotive, robotics/embodied intelligence, and AI. Three acceptance profiles are isolated fixtures, not multi-user support. |

The selected job adapter is the public Greenhouse Job Board API for Canonical's published vacancies, limited to this owner's private personal use with attribution/notices. The permitted scope, live evidence and limitations are in [research.md](./research.md). Text-generation and STT deployment configurations must pass the qualification contract before live enablement; a fake adapter is test infrastructure, not a release substitute. This plan fixes their narrow interfaces without promising an unverified vendor/model, price, hosting region, or data-retention policy.

## Constitution Check

| Principle | Before Phase 0 | After Phase 1 design / enforcement |
| --- | --- | --- |
| I. Minimal architecture/scope | PASS | PASS: one app, local DB, bounded effects, no agent framework/Redis/vector store; worker is justified by recovery/expiry. Deferred capabilities are excluded. |
| II. Data integrity | PASS | PASS: immutable revisions, source spans, explicit conflicts, dependency invalidation, current-fact guards and reviewed clauses. |
| III. Security/privacy | PASS subject to source research | PASS at design level: researched private source use; owner gate; consent; safe imports; retention/deletion contract. Hosting/provider qualification remains a live-enablement gate. |
| IV. Testability/verification | PASS | PASS: controllable effects and clocks; offline boundary tests; real-device/live/longitudinal evidence separated. |
| V. Compatibility | PASS; no legacy application data | PASS: initial schema, versioned exports/API, migration/restore tests and deletion reconciliation. |
| VI. Clear code/documentation | PASS | PASS: module owners, FR/SC coverage and precise interfaces; future canonical checks listed as planned, not executed. |

No constitution waiver or amendment is proposed. A deployment/provider that cannot meet the contracts fails its gate. Research identifies no unresolved product-behavior clarification. Infrastructure credentials, provider qualification and physical-device evidence are implementation/release dependencies, not claims of completed integration.

## Project Structure

### Documentation (this feature)

```text
specs/001-career-interview-coach/
├── spec.md                     # Approved behavior, unchanged
├── prototype.md                # Approved UX reference
├── ux-addendum.md
├── checklists/requirements.md
├── plan.md                     # This canonical plan
├── research.md                 # Phase 0 decisions and primary sources
├── data-model.md               # Phase 1 entities/invariants
├── contracts/
│   ├── application-api.md
│   ├── external-services.md
│   └── interaction-lifecycle.md
└── quickstart.md               # Future validation/run guide
```

`tasks.md` is a later `$speckit-tasks` output, deliberately absent.

### Proposed source code (not created by planning)

```text
manage.py
pyproject.toml
requirements.lock
requirements-dev.lock
package.json                   # Browser tests/checks only
package-lock.json
config/                        # Django settings, URLs, WSGI
career_helper/
├── domain/                    # Pure dataclasses/rules, no Django/network imports
│   ├── evidence.py
│   ├── careers.py
│   ├── preparation.py
│   ├── interviews.py
│   └── methods.py
├── application/               # Explicit transactional use cases
│   ├── profile.py
│   ├── jobs.py
│   ├── preparation.py
│   ├── interviews.py
│   ├── reviews.py
│   └── privacy.py
├── models/                    # Concrete ORM entities/constraints
├── migrations/
├── adapters/                  # documents.py, job_source.py, coaching.py, speech.py
├── web/                       # Views/forms, JSON validation, owner gate
├── management/commands/       # Owner provisioning, jobs, retention
├── templates/                 # Full desktop and focused mobile flows
├── static/career_helper/      # CSS and recording/answers/conflicts/sync JS
└── fixtures/                  # Versioned direction catalog, no personal facts
tests/
├── unit/
├── integration/
├── contract/
├── migrations/
├── browser-unit/
├── e2e/
└── fixtures/                  # Synthetic documents/jobs/answers/failures
```

**Structure decision**: One Django app with responsibility folders avoids separate services or excessive apps. Domain functions accept explicit values and return decisions. Application functions use concrete persistence and narrow effect functions; no generic repository hierarchy, event bus, plugin registry or event sourcing. Data, secrets and generated exports stay outside source/static paths.

## Architecture and Affected Modules

| Module | Responsibility | Boundary |
| --- | --- | --- |
| Evidence domain + profile application | File extraction, source spans, claim states, revisions, conflicts, dependency impacts. | Imports/inferences never confirm themselves; no OCR or silent replacement. |
| Careers domain + jobs application | Direction catalog, evidence/gaps/stage, safe query, acquisition, exact duplicates and target snapshots. | Direction is not vacancy; high-gap interests remain visible. |
| Preparation | Confirmed JD requirements, clause-backed suggestions, target resume history, time-budget plans. | No new personal facts; preserve completed tasks and other target versions. |
| Interviews + speech | Two modes, manual turns, hint history, answer corrections, saved checkpoints. | No silence submission, live barge-in or psychological inference. |
| Reviews + methods | Four feedback dimensions, citations, bounded priorities, retest, draft/verification/withdrawal. | No promotion without retest and user confirmation. |
| Privacy + persistence + workers | Authorization, consent, recording lifetimes, version conflicts, export/deletion, retry. | No silent fallback, deadline reset or resurrection from late output. |
| Web/templates/browser modules | Approved navigation, semantic controls, keyboard/focus/status, recording/save state. | Server owns current-fact validity, deadlines, consent and conflict outcomes. |

### Critical transactions and algorithms

1. Claim change creates a revision, affected-content review annotations and change cursor atomically. Content payloads stay immutable. Every later use rechecks dependencies; cached stale flags alone cannot authorize reuse.
2. Writes carry base revision and idempotency key. Stale overlapping edits preserve both candidates and their devices/times in a conflict. Three-way merge is limited to independently edited scalar fields; ordered content and answer text conflict as a unit. Client clocks do not choose winners.
3. SQLite uses short `transaction.atomic()` blocks, `transaction_mode=IMMEDIATE`, bounded busy timeout and revision-conditional updates. `select_for_update()` is not a lock on SQLite. No database transaction spans parsing or external requests.
4. Jobs capture immutable input references and processing-choice version. Recheck authorization, consent, deletion generation and dependency validity before dispatch, retry and result acceptance. Late invalid output cannot become current.
5. Start recording reserves an immutable server recording ID/time/deadline. The current answer is held in browser memory; Done stops and uploads it under that reservation, then explicitly submits. An OS stop, silence or lost tab never submits. This satisfies recovery for acknowledged saved data without inventing offline audio durability.
6. Keep/delete is serialized; expiry, user deletion and completed transcript-plus-review can trigger purge. Reject late uploads and retries for expired/deleted IDs. Cleanup runs independently of slow provider jobs.
7. Direction assessments use a versioned nine-or-more-direction catalog with explicit skill requirements and preparation stages. Expose matched claim IDs, gaps and unknowns. Plans use a deterministic score from requirement relevance, gap and interview horizon, with stable ID tie-breaks; preserve manual order overrides and completed records. Default horizon is one calendar month in the user's timezone, clamped at month end.

## Requirement-to-Work Mapping

W1–W8 are implementation work packages, not a second task list. Q1–Q12 refer to [quickstart.md](./quickstart.md).

| Requirement | Work / affected module | Verification |
| --- | --- | --- |
| FR-001 | W2 profile/document extraction/manual entry | Q2 valid, partial, corrupt, image-only imports; source/time and pending status. |
| FR-002 | W1/W2/W4/W6 evidence dependencies/history | Q3 changed/rejected fact invalidates all affected content; no automatic rewrite. |
| FR-003 | W2 claim conflicts | Q2 retain contradictory dates, duties and numbers until resolution. |
| FR-004 | W2 preferences | Q4 editable interests/work/industry/safe choices, distinct from work facts. |
| FR-005 | W3 direction catalog/filter/favorite | Q4 three domains, nine directions, high-gap visibility. |
| FR-006 | W3 assessment | Q4 evidence/gaps/unknowns/stage; insufficient evidence stays uncertain. |
| FR-007 | W3 target/manual JD | Q5 overseas manual import; source/link/time-or-unknown. |
| FR-008 | W4 JD requirement confirmation | Q6 pending requirements/claims cannot support adoption. |
| FR-009 | W4 clause-backed resume proposals | Q6 original/proposal/requirement/evidence; unsupported facts blocked. |
| FR-010 | W4 decisions/version/restore | Q3/Q6 selected target only; stale history remains flagged. |
| FR-011 | W4 scheduling | Q6 explicit date/budget or adjustable calendar-month default; three task types. |
| FR-012 | W4 task metadata/order/completion | Q6 reason/source/estimate/criterion plus manual changes. |
| FR-013 | W4/W6 gap-based reranking | Q7 preserve completed work and explain unfinished priority changes. |
| FR-014 | W5 material import | Q7 source type/address/time, role/topics, unknowns. |
| FR-015 | W5 duplicates/quality/generated origin | Q7 exact duplicate, missing/conflicting answer sources, user doubt. |
| FR-016 | W5 question selection/follow-up | Q8 sourced-question quota when applicable; contextual follow-up. |
| FR-017 | W5 recording/text/manual turns | Q8 two real 10-minute sessions; silence never submits. |
| FR-018 | W5 mode/hint rules | Q8 requested sequential coach hints; real mode refuses pre-end hints. |
| FR-019 | W5/W6 corrections and hint events | Q8/Q9 review uses final confirmed answer revision. |
| FR-020 | W5 saved checkpoints/retry | Q8 microphone/network/provider failure and text continuation. |
| FR-021 | W6 feedback dimensions | Q9 answer citations and explicit inability to assess. |
| FR-022 | W6 priorities/retest | Q9 at most three priorities and at least one similar/transfer question. |
| FR-023 | W5/W6 optional self-ratings | Q9 before/after ratings never presented as acoustic inference. |
| FR-024 | W6 method drafts/verification | Q9 required fields, completed retest and user confirmation before formal save. |
| FR-025 | W6 edit/withdraw/reverify | Q9 revised method needs verification; no automatic promotion. |
| FR-026 | W1/W7 auth/revisions/conflicts/sync | Q1/Q10 deny other users; preserve both device versions; 60-second sync. |
| FR-027 | W1/W5/W7 recording lifecycle | Q11 earlier-of expiry, interrupted processing, retries and keep/delete races. |
| FR-028 | W7 export/deletion/policies | Q11/Q12 all data categories; text/review default until deletion. |
| FR-029 | W1/W2/W3/W5 untrusted inputs | Q2/Q5/Q7 embedded instructions cannot change rules or cause sending. |
| FR-030 | W1/W5/W6 processing grants | Q1/Q8 denied/unknown/revoked choice means zero outbound personal data. |
| FR-031 | W3 qualified Canonical/Greenhouse source | Q5 live mainland-China vacancies including international employer. |
| FR-032 | W3 observations/relevance | Q5 every entry exposes source/link/times/unknowns and evidence. |
| FR-033 | W3 duplicates/variants/selection | Q5 all source records and differences preserved; high-gap target selectable. |
| FR-034 | W3 source status/fallback | Q5 distinguish empty/failure/link unavailable; no invented vacancies. |
| FR-035 | W3 exact query preview | Q5 edit invalidates approval; no resume/full-claim/audio query fields. |

## Implementation Sequence

| Package | Dependencies | Deliverable and exit evidence |
| --- | --- | --- |
| W1 Integrity/access foundation | Plan review and later tasks approval | Project/toolchain, owner auth, revision/conflict/dependency model, grants, private storage, jobs/retention primitives. Q1 and critical transaction tests before personal data use. |
| W2 Confirmed profile | W1 | Import/review/manual entry, conflicting facts, current-data invalidation. Q2–Q3. |
| W3 Directions and listings | W2; source research | Catalog, assessments, safe query, live source, aggregation and targets. Q4–Q5; live evidence distinct from fixtures. |
| W4 Resume and preparation | W2/W3; qualified coaching configuration before live acceptance | Requirement confirmation, proposals/history, scheduling and task completion. Q6; timed SC-003 with live generation. Offline implementation can use fixtures. |
| W5 Materials and practice | W1/W4; qualified STT configuration before live voice acceptance | Manual materials, both modes, voice/text, hints, corrections/recovery. Q7–Q8; real devices. |
| W6 Review and methods | W5 | Evidence feedback, retest, self-ratings, method lifecycle, plan update. Q9. |
| W7 Sync/privacy completion | W2–W6 | Integrated conflicts, retention, exports/deletions and restore safety. Q10–Q12; W1 security is not postponed. |
| W8 Release validation | W1–W7 | Regression/accessibility/visual review, live qualifications, timed usability and four-week outcome evidence. |

Each package begins with relevant invariant and boundary tests, then application outcomes and UI integration. Fixtures keep core development independent of paid or unavailable services. Live service qualification remains mandatory for required release capabilities. This sequence authorizes neither implementation now nor omission of a later package.

## Interfaces and Contracts

- [Data model](./data-model.md): entities, fields, revision/dependency relationships, validation, state transitions and deletion.
- [Application API](./contracts/application-api.md): owner-facing endpoints, inputs/outputs, revision/idempotency/errors/conflicts.
- [External services](./contracts/external-services.md): exact boundaries for documents, jobs, structured coaching and speech; qualification/consent.
- [Interaction lifecycle](./contracts/interaction-lifecycle.md): approved desktop/mobile flows, manual turns, sync, retention/export/deletion and accessibility.

`/api/v1/` and `career-helper-export/v1` establish client/export compatibility boundaries. There is no public SDK or generalized extension API.

## Testing Strategy

1. **Pure rules**: controllable clocks/IDs; current-fact and dependency guards, conflicts, stable ranking, month-end planning, mode/hints, review limits and method promotion. No database/network/AI/microphone required.
2. **Persistence/application**: file-backed SQLite with separate connections; CAS concurrency, rollback, duplicate requests, worker lease expiry, crashes, invalidation during generation and deletion versus late output. In-memory tests alone do not prove locking behavior.
3. **Boundary contracts**: hostile/oversized documents, partial extraction, source unknowns/duplicates/conflicts, malformed or unsupported generated clauses/citations, denied consent, timeouts, CSRF, non-owner media/export access. Default tests block external network.
4. **Browser**: same owner in two browser contexts, overlapping edits, mode enforcement, manual Done, silence, permission/network failures, answer correction, keyboard/focus/live status. Playwright Chromium/Firefox/WebKit plus actual iOS/Android microphones.
5. **Live/human**: actual source access/permission/coverage, provider region/retention/quality, real speech/playback, 60-second sync, timed flow, ratings and longitudinal practice. These cannot be established by stubs or screenshot inspection.

| Criterion | Required evidence |
| --- | --- |
| SC-001 | Three separate synthetic profiles × three domains × three-or-more directions; high gaps visible. |
| SC-002 | Every current factual resume clause backed by current confirmed claims; zero rejected facts; complete history invalidation/restore checks. |
| SC-003 | Owner saves resume draft and at least three actionable tasks within 15 minutes. |
| SC-004 | Every test JD/question/material displays source and known time or explicit unknown. |
| SC-005 | Desktop and physical phone each complete at least 10 minutes; manual turns, long pause, hint, corrected term, saved review. |
| SC-006 | Committed phone text/review/plan becomes visible on connected active desktop within 60 seconds. |
| SC-007 | Complete reviews cite answers, have at most three priorities and a retest; empty evidence is unevaluable. |
| SC-008 | Four-week trial, at least twice weekly; fixed five-level rubric, unseen equal-difficulty retest, at least one-level improvement, separate tension self-ratings. |
| SC-009 | After three role directions, owner rates explanation and daily plan usefulness at least 4/5 each. |
| SC-010 | Text PDF and DOCX imports plus unreadable fallback without invented claims. |
| SC-011 | Qualified live mainland-China source; 100% of displayed listings have provenance/link/time-or-unknown and preserve duplicate sources. |
| SC-012 | Empty and failure states differ; directions/manual JD remain usable; zero fabricated listings. |

Future canonical commands and Q1–Q12 are in [quickstart.md](./quickstart.md). No application checks were runnable at planning time. A four-week outcome cannot be labeled passed when software tests pass.

## Migrations and Compatibility

- **Baseline**: no legacy application data/API exists. The approved spec's old non-Git header is historical metadata: Git was initially observed as unborn `main`, then reverified at initial commit `f678297` during this session. That commit was created outside this planning agent's actions. No feature branch, commit, push or PR was created by this workflow; final corrections remain in the working tree.
- **Initial schema**: reviewed Django migrations cover owner binding, provenance/revisions/conflicts, dependencies, targets/jobs, resumes/plans, materials/interviews/reviews/methods, jobs/grants/retention. Seed catalog separately; never seed personal facts or prototype vacancies as real records.
- **Later migrations**: maintenance mode, paused web writers/workers, policy-compliant backup, migrate a copy, verify IDs/order/content/provenance/review flags, then apply. Test populated prior-schema fixtures and rollback/recovery. Refuse newer unsupported schema. SQLite table rebuilds require measured maintenance time.
- **Exports**: versioned manifest/checksums, all selected content/revisions/provenance/known conflicts/review flags, original imports and retained audio. Viewing/exporting history does not certify current validity. No generic archive-import feature; operator restore validates schema, then applies deletion tombstones and expiry before service resumes.
- **Deletion wins over history**: purge selected sensitive payloads and annotate retained dependants as evidence unavailable. Keep minimal content-free tombstones to reject old writes. Exclude temporary audio from backups/exports. Backups and generated archives are registered copies subject to deletion/retention, not a way to retain deleted content forever.
- **Clients**: stale revision/contract errors are explicit; no silent field discard or last-writer-wins. Display reload/reconcile guidance.

## Dependencies, Risks, and Gates

| Dependency/risk | Mitigation and gate |
| --- | --- |
| Source availability/permission/coverage | Research verified Canonical published Beijing/Shanghai jobs via official public API and personal-use terms. Limit to private noncommercial use with notices; source status can change. Revalidate before live enablement; no global coverage claim. |
| No approved stack document located | Preserve approved behavior; review the initial stack here. Additional architecture must be reconciled in this plan. |
| Figma quota | MCP returned Starter-plan call limit; web access failed. Nonvisual planning is allowed by prototype.md. Screen fidelity/interaction review remains pending before UI acceptance. |
| Generation/STT configuration | Implement finite ports with fixtures, then qualify concrete provider or local service for availability, Chinese quality, allowed processing, formats and deletion. No silent vendor fallback; dependent features and first-release acceptance remain gated until live evidence exists. |
| Strict 24-hour audio deletion | Trusted reservation time, deadline checks, independent cleanup and no temp backups. Stopped hardware cannot prove timely physical deletion; qualify monitored hosting/cleanup and disclose any failure. Do not equate inaccessible with physically removed. |
| SQLite contention | Short IMMEDIATE transactions/CAS, finite retries, unique operation IDs; test two devices plus worker. Scale only after measured failure or approved deployment change. |
| Import fidelity/exhaustion | Bounded parser subprocess; explicit partial/unreadable diagnostics and manual entry. No OCR/layout-fidelity promise. |
| Semantic hallucination | Clause-level references and user review; reject unknown IDs/new unsupported facts. A valid citation ID alone is not proof of semantic support. |
| Mobile lifecycle | MIME feature detection, HTTPS, explicit unsaved state and physical-device checks. No background/offline recording promise. |
| User outcomes | SC-008/SC-009 are measured separately; neither is inferred from passing code tests. |

## Planning Completion Record

Pre-plan and post-plan extension checks: `.specify/extensions.yml` absent; no hooks registered to dispatch. Setup used the existing feature directory and persisted `.specify/feature.json`; its `BRANCH` value is the feature identifier, not Git branch creation. Research and Phase 1 outputs remain within Spec Kit. There are no justified constitution violations to list under Complexity Tracking.

Document verification on 2026-09-25: Spec Kit prerequisite discovery succeeds; all 35 FRs and 12 SCs have explicit table rows; Q1–Q12 exist; seven generated design documents have valid local links, balanced code fences and no template placeholders/trailing whitespace. Hash comparison confirms the specification, constitution, prototype index, UX addendum and requirements checklist are unchanged. A design review identified browser-buffer expiry, provider qualification sequencing and missing material revisions; all three were corrected. No `tasks.md`, application scaffold, dependency installation or application test execution occurred. These checks establish planning artifact consistency, not application behavior or live release readiness.
