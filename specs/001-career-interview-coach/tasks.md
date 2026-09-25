---
description: "Requirement-traceable implementation tasks for the approved career interview coach"
---

# Tasks: Career Direction and Interview Growth Coach

**Feature**: 职业方向探索与面试成长助手 (`001-career-interview-coach`)
**Created**: 2026-09-25
**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md), [data-model.md](./data-model.md), [application contract](./contracts/application-api.md), [external-service contract](./contracts/external-services.md), [interaction lifecycle](./contracts/interaction-lifecycle.md), [quickstart.md](./quickstart.md), [prototype index](./prototype.md), [UX addendum](./ux-addendum.md), and [constitution](../../.specify/memory/constitution.md).
**Authority**: The user's 2026-09-25 instruction authorizes task generation from the approved spec and plan. The plan's earlier “proposed / no tasks in this command” wording describes its prior planning invocation; it does not override this authorization. This file is the canonical Spec Kit task breakdown, not a replacement plan. Implementation is not authorized by this generation run.
**Observed repository baseline**: `main`, HEAD `9895af7`, ahead of `origin/main` by one commit; no application scaffold exists. Reverify before later Git work. Task generation makes no branch, commit, push or PR.
**Tests**: Explicitly requested as first-class tasks. Write the listed focused tests first and observe meaningful failures before implementing the corresponding behavior. Finish each task with its stated checks; passing fixture tests never replaces live or human evidence.
**Organization**: Setup, blocking foundation, six story phases in spec priority order, then cross-cutting acceptance. Both P2 stories remain required for the approved first usable release.

## Format and execution rules

- Every task has an unchecked marker, sequential ID, optional `[P]`, story label where applicable, exact files, explicit dependencies, requirement/design basis, and observable completion criterion. All paths are relative to `/Users/ben/Documents/MyProj/career-helper`; they name planned files, not existing application code.
- `Depends` lists prerequisite tasks. All must be complete before starting that task; dependencies are transitive. Increasing IDs provide a safe serial execution order. A failing test-authoring task is complete only when its intended behavioral assertion fails, not merely because its file imports fail.
- `[P]` means the task may run alongside the other tasks in its named parallel batch **after their common prerequisites are complete**. It never bypasses dependencies. Unmarked tasks stay ordered; shared route/model registries, migrations and application modules are deliberately serialized.
- Each model task contains verbatim field/constraint quotations from `data-model.md`. These constraints apply to constructors, input validation and persistence as appropriate. Do not invent new product bounds for underspecified fields; document necessary operational bounds in the existing contract and resolve any behavior-changing question before the affected work.
- `Q1`–`Q12` refer to the quickstart's named validation scenarios; `FR`/`SC` refer to the spec; named contract sections supply the narrow technical justification for infrastructure work.
- [behavior-quality.md](./checklists/behavior-quality.md) remains reviewer-owned and unchecked. Task generation neither approves its criteria nor changes any checklist marker. Follow the later implementation workflow's review gates and resolve material contradictions before dependent implementation; checklist questions are not new requirements.
- Before UI work, inspect the approved prototype if accessible and reconcile it with the spec/UX addendum. Nonvisual work may continue under the prototype index's documented fallback; exact visual parity remains a separate acceptance gate.
- No live personal-data processing, paid provisioning, external deployment, Git mutation or automatic trial scheduling is authorized by this task list alone. Live qualification tasks use synthetic data and existing approved access; missing credentials, permissions or hardware remain explicit dependencies. Never store secrets or raw personal answers in repository evidence.
- Narrow helper modules and evidence documents listed below implement the approved responsibilities. They do not authorize new frameworks, generic repositories, extra job sources, OCR, public accounts, full offline replicas or expanded mobile editing.

## Phase 1: Setup — shared toolchain

**Goal**: Establish only the approved Django/Python and browser-test structure, with synthetic offline defaults.

**Independent verification**: A clean checkout can install locked dependencies and run the scaffold checks and offline harness; commands are documented as available only after they actually work.

### Setup

- [ ] T001 Create the Python 3.12/Django 5.2 application skeleton, lock supported runtime/dev patch versions with hashes, and default to loopback plus a separate private synthetic data root; do not bind live providers. Files: `manage.py`, `pyproject.toml`, `requirements.lock`, `requirements-dev.lock`, `config/settings.py`, `config/urls.py`, `config/wsgi.py`, `career_helper/apps.py`, `.gitignore`, `.env.example`. **Depends**: none. **Basis**: Plan Technical Context/Project Structure; Research R1; Quickstart Prerequisites. **Done**: Django check succeeds; locks include the runtime set and configuration contains no credentials.

- [ ] T002 [P] Configure Ruff and mypy for the planned Python folders and initialize discoverable unit/contract/integration/migration test packages. Files: `pyproject.toml`, `tests/__init__.py`, `tests/unit/__init__.py`, `tests/contract/__init__.py`, `tests/integration/__init__.py`, `tests/migrations/__init__.py`. **Depends**: T001. **Basis**: Plan Testing Strategy; Constitution IV. **Done**: The configured Python checks run on the scaffold.

- [ ] T003 [P] Configure Node 24, ES2022 checkJs, Node browser-rule tests and Playwright against a disposable fixture server; pin browser development dependencies. Files: `package.json`, `package-lock.json`, `jsconfig.json`, `playwright.config.js`, `tests/browser-unit/setup.test.mjs`, `tests/e2e/setup.spec.js`. **Depends**: T001. **Basis**: Plan Technical Context; Quickstart Canonical Verification Commands. **Done**: typecheck, Node tests and the fixture-server browser smoke check run without live network.

- [ ] T004 Add explicit clock/ID/effect fixtures, network-denial defaults, temporary private directories and file-backed SQLite connection helpers; avoid a generic provider/repository framework. Files: `tests/support.py`, `config/test_settings.py`, `tests/unit/test_test_boundaries.py`. **Depends**: T002, T003. **Basis**: Constitution IV; Plan Testing Strategy; External services Common Boundary. **Done**: Unexpected outbound calls fail tests; two independent database connections and controllable clocks are available.

- [ ] T005 Run the available scaffold checks and record exact commands and results; update only commands that now exist, leaving later commands labelled planned. Files: `AGENTS.md`, `specs/001-career-interview-coach/quickstart.md`, `specs/001-career-interview-coach/evidence/setup.md`. **Depends**: T004. **Basis**: Constitution VI; AGENTS.md Dependencies and checks. **Done**: Fresh setup evidence distinguishes runnable checks from later application acceptance.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 2: Foundational — blocking access, integrity and lifecycle primitives

**Goal**: Provide owner authorization, immutable revisions, explicit conflicts, processing choices, private storage and bounded jobs before personal-data features.

**Independent verification**: Q1 and focused file-backed concurrency, publication and storage tests pass offline; unauthenticated/other-user access and ungranted outbound effects fail closed.

### Tests first

- [ ] T006 [P] Write failing access-boundary tests for owner/second-account/anonymous access, login expiry/throttling, CSRF, Origin/Host, private no-store responses and safe errors. Files: `tests/contract/test_access.py`. **Depends**: T005. **Basis**: FR-026, FR-029, FR-030; API Transport; Q1. **Done**: Failures identify absent owner protections, including private-file and operation-route contract cases.

- [ ] T007 [P] Write failing real-connection transaction tests for revision membership, mutation replay/mismatch, overlapping candidates, scalar merge, ordered-content conflict, deleted-write rejection and cursor atomicity. Include forward/reverse schema checks with populated predecessor fixtures and the phase's declared model constraints. Files: `tests/integration/test_revisions.py`, `tests/migrations/test_core_schema.py`. **Depends**: T005. **Basis**: FR-002, FR-026; Data model Shared Rules/Concurrency; Q10. **Done**: Assertions use persisted outcomes, preserve both candidates and expose rollback/race failures.

- [ ] T008 [P] Write failing tests for denied/revoked/provider-changed processing choices, job leases, one bounded transient retry and stale/deleted/unauthorized result publication. Files: `tests/integration/test_processing_jobs.py`. **Depends**: T005. **Basis**: FR-020, FR-030; API Operation Publication and Failure; Q1. **Done**: Request capture proves no sends for blocked choices and no double publication after retries.

- [ ] T009 [P] Write failing storage/policy tests for owner-only files, registered copies, UTC deadlines, earlier completion/deletion triggers and visible purge failures with access revoked. Files: `tests/integration/test_private_storage.py`. **Depends**: T005. **Basis**: FR-027, FR-028; Interaction lifecycle Recording Retention; Q11. **Done**: Actual temporary files distinguish inaccessible, pending and physically removed states.

### Models and migrations

- [ ] T010 Create concrete owner/device, mutation/conflict/change and evidence-reference tables with an initial migration; apply shared ownership, revision and date constraints without introducing an arbitrary entity store. Files: `career_helper/models/core.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0001_core.py`. **Depends**: T006, T007. **Basis**: FR-002, FR-026; Data model Shared Rules/Dependency Validity. **Done**: Migration enforces owner/revision/operation uniqueness and explicit artifact kinds; core migration reverses on an empty fixture.

  Data-model constraints (verbatim; part of this task):

  > **OwnerBinding — fields**: Singleton `user_id`, `timezone`, configured_at; Django user/password/session data remains in Django auth tables.
  >
  > **OwnerBinding — validation/lifecycle**: Provision locally; active user must equal binding for every private operation. No public account creation.

  > **Device — fields**: `id`, owner, user-visible label, first/last seen.
  >
  > **Device — validation/lifecycle**: Metadata only; server receipt time wins over client time for deadlines.

  > **MutationReceipt — fields**: owner, mutation_id, request hash, outcome, resource revision/conflict ID.
  >
  > **MutationReceipt — validation/lifecycle**: Same key+same payload returns prior result; different payload is `idempotency_mismatch`. Keep content-free receipts/tombstones through client reconciliation.

  > **EditConflict — fields**: aggregate, base/current/proposed revisions, changed fields, both device IDs/timestamps, state, resolution_revision.
  >
  > **EditConflict — validation/lifecycle**: Persist both accepted candidates; no unique current factual result while conflicted. Resolve against expected conflict revision; another intervening change returns a new conflict.

  > **ChangeEntry — fields**: monotonic cursor, resource ID/type, revision, event (`updated`, `conflicted`, `deleted`), server time.
  >
  > **ChangeEntry — validation/lifecycle**: Same transaction as mutation; contains no duplicated sensitive text. Old cursor can require full refetch.
  > - IDs are opaque server-issued UUIDs except external posting IDs. Every private aggregate belongs to the configured owner. Device ID is a user-labelled provenance identifier, never authorization.
  > - Persist UTC timezone-aware timestamps; retain original source date strings/offsets alongside normalized values. Applicable career dates can be partial (`year`, `month`, `day` precision) or unknown; never invent day/month precision. Planning uses the owner's configured timezone, default Asia/Shanghai and visibly editable.
  > - Revisions have `id`, `aggregate_id`, `revision_number`, `previous_revision_id`, `created_at`, `device_id`, `origin`, `schema_version`. Unique aggregate/revision number; immutable content. Current pointers, job state and deletion metadata are operational fields, not overwritten historical content.
  > - Unknown is represented by null plus a reason where useful, not an empty fabricated value. Preserve original user text and ordered items. Comparison keys are separate derived fields; normalization never mutates source content.
  > - Stored foreign keys and uniqueness/check constraints enforce ownership, revision membership and idempotency where possible. Domain validation enforces semantic constraints. Client/provider input must not set confirmation, current status, trusted time or owner identity directly.
  > - `validity` is computed from current dependencies and unresolved conflicts: `current`, `needs_review`, `evidence_unavailable`. A saved historical payload does not become current through viewing, exporting, restoring or dismissing a warning.
  > - Concrete aggregates have concrete tables. Shared revision conventions do not imply a generic entity store, arbitrary JSON event log or polymorphic repository framework.

- [ ] T011 Add the processing-choice, retention-policy, copy inventory, deletion and export operation tables; chain the migration after the core migration. Files: `career_helper/models/privacy.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0002_privacy.py`. **Depends**: T010, T009, T008. **Basis**: FR-027, FR-028, FR-030; Data model Concurrency, Processing Choice, and Privacy. **Done**: Defaults, state constraints and prior-schema preservation pass focused migration assertions.

  Data-model constraints (verbatim; part of this task):

  > **ProcessingChoice — fields**: provider/config version, purpose, data categories, disclosure version, choice, decided_at.
  >
  > **ProcessingChoice — validation/lifecycle**: Unknown/denied/revoked blocks sending. Scope/provider change requires a new choice. Consent is rechecked before retries, not just at job creation.

  > **RetentionPolicy — fields**: category, mode (`until_deleted`, `days`), days nullable, effective_at.
  >
  > **RetentionPolicy — validation/lifecycle**: Text/review defaults until_deleted; shortening requires affected-data preview. Temporary audio hard maximum cannot be extended. Imported files, resumes and methods remain visible until deletion unless configured otherwise.

  > **DeletionRequest — fields**: scope IDs/categories, requested_at, deletion generation, dependent-impact preview, state, failed-copy list.
  >
  > **DeletionRequest — validation/lifecycle**: `pending → running → complete/failed`; completion requires all registered copies removed, tombstones published and late output disabled.

  > **StoredCopy — fields**: kind (`original`, `audio`, `transcode_temp`, `export`, `backup`), private location, content references, created_at, expires_at nullable, deletion state.
  >
  > **StoredCopy — validation/lifecycle**: Enumerate product-controlled copies; no temporary audio in export/backups; export expiry and backup retention visible.

  > **ExportJob — fields**: selected scope/policy, manifest version, snapshot cursor, private archive ref, created/expires_at, state.
  >
  > **ExportJob — validation/lifecycle**: Snapshot is consistent; contains retention/review flags, checksums and selected kept recordings. The downloaded copy is user-controlled and cannot be remotely erased.

- [ ] T012 Add the fixed-operation ProcessingJob table and migration; store references and safe metadata rather than raw sensitive job logs. Files: `career_helper/models/jobs.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0003_jobs.py`. **Depends**: T011. **Basis**: FR-020, FR-030; Plan critical transactions 4; Data model ProcessingJob. **Done**: Lease/operation uniqueness and allowed state values are enforced.

  Data-model constraints (verbatim; part of this task):

  > **ProcessingJob — fields**: fixed kind, input refs, input hash, consent version, owner/deletion generation, created_at, state, attempt count, lease_until, result ref, safe error.
  >
  > **ProcessingJob — validation/lifecycle**: `queued → running → succeeded/failed/blocked/stale/cancelled`; lease expiry permits bounded retry, never fresh audio expiry. Unique operation key; no sensitive payloads in job logs.

### Implementation

- [ ] T013 Implement secure local owner provisioning, owner-bound sessions, login/logout, throttling and shared route protection with safe errors; exclude public registration/admin/invitation routes. Files: `career_helper/management/commands/provision_owner.py`, `career_helper/web/access.py`, `career_helper/web/auth.py`, `config/settings.py`, `config/urls.py`, `career_helper/templates/registration/login.html`. **Depends**: T012, T006. **Basis**: FR-026; Research R3; API Transport; Q1. **Done**: Access tests pass; password entry is secure and device labels never authorize access.

- [ ] T014 Implement immutable revision writes, receipts, trusted dates, conditional updates, short IMMEDIATE transactions, explicit overlap conflicts and content-free change cursors. Files: `career_helper/domain/evidence.py`, `career_helper/application/revisions.py`. **Depends**: T013, T007. **Basis**: FR-002, FR-003, FR-026; Plan critical transactions 1–3; Q10. **Done**: File-backed race/rollback tests pass; no external call occurs inside a write transaction.

- [ ] T015 Implement provider/config/purpose/category-scoped processing choices and capability availability, including disclosure, deny/revoke and change-of-scope handling. Files: `career_helper/application/processing.py`, `career_helper/web/processing.py`, `career_helper/templates/career_helper/processing_choices.html`, `config/urls.py`. **Depends**: T014, T008. **Basis**: FR-030; API /processing-choices; Q1. **Done**: Grant/deny/revoke routes preserve versions and leave unrelated manual capabilities available.

- [ ] T016 Implement authorized private-copy storage, retention decisions and independent cleanup with deadline scheduling, safe startup reconciliation and deletion-failure status. Files: `career_helper/application/storage.py`, `career_helper/domain/retention.py`, `career_helper/management/commands/run_retention.py`. **Depends**: T015, T009. **Basis**: FR-027, FR-028; Plan W1; Interaction lifecycle Recording Retention. **Done**: Storage tests pass; cleanup is independent of processing jobs and never extends a stored deadline.

- [ ] T017 Implement the finite job runner with bounded leases/retries, rechecking owner, grant, input validity and deletion generation both before dispatch and publication. Files: `career_helper/application/jobs.py`, `career_helper/management/commands/run_jobs.py`. **Depends**: T016, T008. **Basis**: FR-020, FR-030; API Operation Publication and Failure. **Done**: Processing tests pass with safe blocked/stale outcomes and no claim of exactly-once external delivery.

- [ ] T018 Implement the shared command/error envelope, session/capability and operation-status routes, stable pagination and concrete conflict-resolution detail/command paths. Files: `career_helper/web/protocol.py`, `career_helper/web/session.py`, `career_helper/web/operations.py`, `career_helper/web/conflicts.py`, `config/urls.py`. **Depends**: T017. **Basis**: FR-020, FR-026; API Transport/Endpoint Catalogue. **Done**: 422/404/410/409/428/429/503 and owner checks match the contract; list defaults 50, maximum 100, malformed cursors fail.

- [ ] T019 Create the approved desktop/mobile shell, semantic forms, focus/error summary and non-color asynchronous status patterns without adding out-of-scope mobile editing. Files: `career_helper/templates/career_helper/base.html`, `career_helper/templates/career_helper/conflicts.html`, `career_helper/static/career_helper/base.css`, `career_helper/static/career_helper/status.js`. **Depends**: T018. **Basis**: UX addendum Accessibility; Interaction lifecycle Screen and Device Boundaries. **Done**: Keyboard/focus/status smoke checks pass and no raw source HTML becomes executable content.

### Checkpoint and documentation

- [ ] T020 Run foundation tests and schema checks; document finite timeout/validation values chosen within the approved contracts and any unresolved product-level ambiguity before dependent work. Files: `specs/001-career-interview-coach/evidence/foundation.md`, `specs/001-career-interview-coach/contracts/application-api.md`, `specs/001-career-interview-coach/data-model.md`. **Depends**: T019. **Basis**: Constitution II–VI; Plan W1; Q1/Q10/Q11. **Done**: All foundation tests pass; no personal data or live recording is enabled by fixture success alone.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 3: User Story 1 — verify experience and explore directions (P1)

**Goal**: Import PDF/DOCX or enter facts manually, resolve provenance/conflicts, and explore three career domains without inventing history.

**Independent verification**: Q2–Q4 with three isolated synthetic profiles: ordered pending imports, confirmed/rejected/conflicted facts, at least three directions per domain, high-gap favorites and explicit unknowns. Future dependent artifact kinds are integrated in their owning stories.

### Tests first

- [ ] T021 [P] [US1] Write failing import contract tests and synthetic fixtures for readable PDF/DOCX, image-only/corrupt/oversized content, partial extraction, tracked changes, unsafe archives and embedded instructions. Files: `tests/contract/test_resume_imports.py`, `tests/fixtures/documents/build_fixtures.py`. **Depends**: T020. **Basis**: FR-001, FR-029; SC-010; Q2; External services Document Extraction. **Done**: Tests assert source order/locators, pending facts, diagnostics/manual fallback and bounded parser failure.

- [ ] T022 [P] [US1] Write failing claim lifecycle tests for partial dates, unknown numbers, work versus learning/interest, explicit edit-and-confirm, conflicting sources and dependent-content invalidation. Include forward/reverse schema checks with populated predecessor fixtures and the phase's declared model constraints. Files: `tests/integration/test_claims.py`, `tests/e2e/profile.spec.js`, `tests/migrations/test_profile_schema.py`. **Depends**: T020. **Basis**: FR-001–FR-003; SC-002; Q2/Q3. **Done**: Current eligibility and immutable history assertions cover direct invalid inputs and transaction rollback.

- [ ] T023 [P] [US1] Write failing catalog/filter/assessment tests across automotive, frontend and learning-only synthetic profiles, including unknown evidence and high-gap favorites. Files: `tests/unit/test_directions.py`, `tests/fixtures/profiles.json`. **Depends**: T020. **Basis**: FR-004–FR-006; SC-001; Q4. **Done**: Every profile expects three or more directions in each required domain without becoming multi-user support.

### Models and migrations

- [ ] T024 [US1] Add source/import/segment/claim/revision/source-conflict tables and the chained migration with exact provenance and confirmation constraints. Files: `career_helper/models/profile.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0004_profile.py`. **Depends**: T021, T022, T023. **Basis**: FR-001–FR-003; Data model Access, Sources, and Claims. **Done**: Populated core/privacy rows survive migration; imported facts cannot start confirmed.

  Data-model constraints (verbatim; part of this task):

  > **SourceRecord — fields**: `id`, type (`resume_file`, `manual_claim`, `manual_jd`, `job_board`, `manual_material`, `generated`), title, URI nullable, source times nullable, collected_at, original content/file reference, notices, content hash.
  >
  > **SourceRecord — validation/lifecycle**: Source content remains untrusted, never executable; original link is not evidence of current recruiting.

  > **ResumeImport — fields**: source_id, original filename, detected type, bytes, hash, private blob key, created_at, extraction status, diagnostics.
  >
  > **ResumeImport — validation/lifecycle**: `queued → extracting → complete/partial/unreadable/failed`; only PDF/DOCX allowed, no OCR. Partial results retain successful segments.

  > **ExtractionSegment — fields**: import_id, stable segment_id, source locator (PDF page or DOCX paragraph/table/cell path), order, raw text, warnings.
  >
  > **ExtractionSegment — validation/lifecycle**: Preserve sequence; identify unhandled sections rather than completing them with generated text.

  > **Claim — fields**: owner, nature (`work`, `education`, `learning_project`, `interest`), current_revision_id.
  >
  > **Claim — validation/lifecycle**: Interests and personal learning cannot be relabelled as employment by inference.

  > **ClaimRevision — fields**: claim_id, text, applicable_start/end with precision, source references/segment spans, factual fields, `confirmation` (`pending`, `confirmed`, `rejected`), confirmation actor/time, predecessor.
  >
  > **ClaimRevision — validation/lifecycle**: Any imported/generated claim starts pending. Editing creates a revision; direct user edit-and-confirm is one explicit command. Valid dates/numbers or explicit unknown.

  > **ClaimConflict — fields**: involved claim/revision IDs, disputed fields, source IDs, resolution_id nullable.
  >
  > **ClaimConflict — validation/lifecycle**: No automatic winning source. Related current facts remain ineligible until explicit selection/merge/rejection.

- [ ] T025 [US1] Add preferences, career catalog and assessment revisions, initially scoped to directions; add the concrete target relationship in the US2 migration. Files: `career_helper/models/careers.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0005_careers.py`. **Depends**: T024. **Basis**: FR-004–FR-006; Data model Targets, Sources, and Assessments. **Done**: Allowed stage values and stable ordered favorites are preserved across migration.

  Data-model constraints (verbatim; part of this task):

  > **PreferencesRevision — fields**: industries, work_contents, interests, safe_choices, stable ordered favorites.
  >
  > **PreferencesRevision — validation/lifecycle**: Preference is not evidence of skill. Favorites can include high-gap directions.

  > **CareerDirection — fields**: catalog_version, stable direction_id, domain, title, typical work, skill_requirements, knowledge_topics.
  >
  > **CareerDirection — validation/lifecycle**: At least three directions in each of automotive, embodied/robotics and AI; catalog facts are general guidance, not personal history or vacancies.

  > **AssessmentRevision — fields**: target/direction, preferences_revision, input claim revision IDs, matched evidence, gaps, unknowns, suggested_stage, rationale.
  >
  > **AssessmentRevision — validation/lifecycle**: Stage enum `apply_now`, `short_preparation`, `long_exploration`; insufficient evidence explicitly shown. No guaranteed match score or auto-application.

### Implementation

- [ ] T026 [P] [US1] Implement bounded PDF extraction with ordered page segments and image-only/partial diagnostics; never synthesize missing text. Files: `career_helper/adapters/documents_pdf.py`. **Depends**: T025, T021. **Basis**: FR-001; Research R4; External services Document Extraction. **Done**: PDF fixture cases pass through a file-handle-only parser.

- [ ] T027 [P] [US1] Implement bounded DOCX paragraph/table/cell extraction with ordered locators and tracked/unsupported-structure diagnostics. Files: `career_helper/adapters/documents_docx.py`. **Depends**: T025, T021. **Basis**: FR-001; Research R4; External services Document Extraction. **Done**: DOCX fixture cases retain successful content and report omissions.

- [ ] T028 [US1] Wire parser subprocess isolation, detected types, upload/extraction jobs and private originals using 10 MiB upload, 100 PDF pages, 50 MiB expanded DOCX, 1 MiB text, 30 seconds and 512 MiB memory bounds. Files: `career_helper/adapters/documents.py`, `career_helper/application/imports.py`. **Depends**: T026, T027. **Basis**: FR-001, FR-029; External services Document Extraction. **Done**: Malicious/oversized/time-limited cases fail explicitly, subprocesses are reaped and temporary material is purged.

- [ ] T029 [US1] Implement manual and extracted pending claims, explicit confirm/edit/reject decisions and source-conflict selection/merge without an automatic winning source. Files: `career_helper/application/profile.py`. **Depends**: T028, T022. **Basis**: FR-001–FR-003; API claims/decisions; Q2. **Done**: Claim lifecycle tests pass with source spans and previous versions intact.

- [ ] T030 [US1] Implement concrete evidence-reference closure, atomic affected-unit annotations and use/restore/export/publication validity checks; add each later concrete artifact adapter in its owning story. Files: `career_helper/application/evidence.py`, `career_helper/domain/evidence.py`. **Depends**: T029. **Basis**: FR-002; Data model Dependency Validity and Corrections; Q3. **Done**: Claim and assessment fixtures cannot clear review requirements by acknowledgement or stale retry.

  Data-model constraints (verbatim; part of this task):
  > `EvidenceReference` maps a concrete artifact revision and content-unit ID to exact claim/target/answer/material revisions. Use explicit constrained artifact kinds; never accept arbitrary entity type strings. Index reverse claim lookups for invalidation. `ReviewRequirement` records affected revision/unit, changed dependency, reason and discovered_at; it is separate from the saved content payload.
  >
  > 1. Change/reject/conflict a claim: append the claim revision/event and all direct/transitive impact annotations in the same transaction; invalidate dependent assessments/resumes/plans/reviews and methods using those outputs.
  > 2. Recheck dependency closure at use, restore, export and job publication, including deleted and conflicted sources. Unaffected content and completed work remain retained.
  > 3. Acknowledging a warning does not clear it. A new corrected/regenerated version must use current confirmed facts; the owner reviews the affected clauses. Historical revisions retain their impact annotations.
  > 4. Correcting an answer after a review creates a new answer revision and marks the saved review/methods dependent on it for review; no silent historical rewrite.
  > 5. Correcting material question/answer content, or marking its answer unreliable, creates a MaterialRevision and marks dependent feedback/method content for review. Saved question and answer snapshots remain unchanged. A label-only topic edit does not invalidate substantive feedback, but retains its revision provenance. New question selection uses the latest eligible revision and displays unresolved quality flags.

- [ ] T031 [US1] Add a versioned nine-or-more-direction catalog, deterministic evidence/gap/stage assessments, editable preferences and high-gap favorites; add isolated-profile seeding for acceptance only. Files: `career_helper/domain/careers.py`, `career_helper/application/careers.py`, `career_helper/fixtures/directions.json`, `career_helper/management/commands/seed_acceptance.py`. **Depends**: T030, T023. **Basis**: FR-004–FR-006; SC-001; API preferences/directions/assessments; Q4. **Done**: Catalog/rule assessment works without AI; synthetic profile seed refuses non-synthetic data roots.

- [ ] T032 [US1] Expose import status, claim decisions, preferences, directions and assessment operations through protected forms/JSON using shared validators. Files: `career_helper/web/profile.py`, `career_helper/web/careers.py`, `config/urls.py`. **Depends**: T031. **Basis**: FR-001–FR-006; API Endpoint Catalogue. **Done**: Route contract tests preserve field errors, source diagnostics and owner checks.

- [ ] T033 [US1] Build desktop experience review and direction screens with source/confirmation/conflict labels, editable preferences, evidence/gaps/unknowns and manual fallback. Files: `career_helper/templates/career_helper/profile.html`, `career_helper/templates/career_helper/directions.html`, `career_helper/static/career_helper/profile.js`. **Depends**: T032. **Basis**: FR-001–FR-006; UX frames 01/02/12A. **Done**: Q2/Q4 browser journey handles empty, partial and failure states with accessible feedback.

### Checkpoint and documentation

- [ ] T034 [US1] Run Q2–Q4 offline and record import fidelity, three-profile direction coverage and current-fact restrictions; document the usable first increment and remaining full-release dependencies. Files: `specs/001-career-interview-coach/evidence/us1.md`, `specs/001-career-interview-coach/quickstart.md`. **Depends**: T033. **Basis**: FR-001–FR-006; SC-001, SC-002, SC-010. **Done**: All US1 tests pass; fixture results are not described as live service qualification.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 4: User Story 2 — discover concrete vacancies and select targets (P1)

**Goal**: Keep direction maps separate from sourced mainland-China vacancies and preserve unrestricted manual job-description entry.

**Independent verification**: Q5 distinguishes source-empty/failure/local-no-match, preserves duplicate/conflicting provenance, previews exact outbound fields and saves selected/manual targets. One qualified live source is required separately from offline aggregation tests.

### Tests first

- [ ] T035 [P] [US2] Write failing source boundary tests for fixed approved requests, disallowed redirects/hosts, malformed/oversized replies, deadlines/retries and absence of personal query content. Files: `tests/contract/test_job_source.py`, `tests/fixtures/jobs/responses.json`. **Depends**: T034. **Basis**: FR-029–FR-035; External services Job Acquisition; Q5. **Done**: Captured requests contain only board/options; exact error/freshness outcomes are asserted.

- [ ] T036 [P] [US2] Write failing aggregation/target tests for exact duplicates, two-source conflicts, unknown dates, location boundaries, high gaps, stale links and overseas manual descriptions. Include forward/reverse schema checks with populated predecessor fixtures and the phase's declared model constraints. Files: `tests/integration/test_listings_targets.py`, `tests/e2e/listings.spec.js`, `tests/migrations/test_targets_schema.py`. **Depends**: T034. **Basis**: FR-007, FR-031–FR-034; SC-004, SC-011, SC-012; Q5. **Done**: Uncertain identity stays separate and selecting a variant never silently blends a job description.

### Models and migrations

- [ ] T037 [US2] Add preview/search/fetch/observation/listing tables and source identity constraints; preserve every collection occurrence and source variant. Files: `career_helper/models/listings.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0006_listings.py`. **Depends**: T035, T036. **Basis**: FR-031–FR-035; Data model Targets, Sources, and Assessments. **Done**: Prior profile data survives migration and source-empty differs from local-no-match.

  Data-model constraints (verbatim; part of this task):

  > **SearchRequest — fields**: owner, preview_id, approved_request_hash, exact external fields, local filters, created_at, processing status.
  >
  > **SearchRequest — validation/lifecycle**: Changed external fields require a new preview; no full claim/resume/audio fields.

  > **SourceFetch — fields**: search_id, source_key, started/completed_at, status, response hash, error_code, returned_count.
  >
  > **SourceFetch — validation/lifecycle**: `succeeded`, `empty`, `failed`; local no-match separate from source-empty. Store errors without credentials/content.

  > **JobObservation — fields**: source_key/posting_id/internal_job_id, fetch_id, employer/title/location strings, offices, original_url, first_published/updated nullable, collected_at, description/source_id, status.
  >
  > **JobObservation — validation/lifecycle**: New observation on meaningful change; exact repeats can link existing content while retaining collection occurrence. Exclude prospect/general-interest postings from vacancy results.

  > **ListingGroup — fields**: id, member observation IDs, identity basis, field variants, mainland match evidence.
  >
  > **ListingGroup — validation/lifecycle**: Group exact identity/content matches for display; preserve all source records. Similar titles alone never prove identity. Conflicting fields remain alternatives.

- [ ] T038 [US2] Add target/revision tables and direction/listing/manual source relationships, including the assessment target reference. Files: `career_helper/models/targets.py`, `career_helper/models/careers.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0007_targets.py`. **Depends**: T037. **Basis**: FR-007, FR-008; Data model Targets, Sources, and Assessments. **Done**: Exactly-one target kind and per-requirement confirmation states are validated.

  Data-model constraints (verbatim; part of this task):

  > **Target — fields**: id, kind (`direction`, `listing`, `manual_jd`), direction/listing/source reference, current_revision_id.
  >
  > **Target — validation/lifecycle**: Exactly one kind; selecting a listing captures the chosen observation and visible variants, not a silent blended JD. Manual JD has no location restriction.

  > **TargetRevision — fields**: source text/version, title, extracted requirements, source/date metadata, confirmed requirement IDs.
  >
  > **TargetRevision — validation/lifecycle**: Each requirement has pending/confirmed/rejected status and source span. Only confirmed requirements drive adopted resume/plan facts.

### Implementation

- [ ] T039 [US2] Implement the fixed Canonical/Greenhouse GET and detail recheck with attribution/notices, TLS/allowlisted redirects, 20-second deadline, 10 MiB response cap, one transient retry and Retry-After. Files: `career_helper/adapters/job_source.py`. **Depends**: T038. **Basis**: FR-031, FR-034; Research R5; External services Job Acquisition. **Done**: Source contract tests pass without arbitrary boards, application POSTs or crawling.

- [ ] T040 [US2] Implement explicit mainland-location selection, prospect exclusion, exact-identity grouping and conflict variants while preserving source times and local relevance/unknowns. Files: `career_helper/domain/listings.py`. **Depends**: T039. **Basis**: FR-031–FR-033; Data model ListingGroup; Q5. **Done**: Aggregation tests preserve all locations and do not infer vacancy identity from similar titles.

- [ ] T041 [US2] Implement preview/hash approval, user-triggered search/recheck, one in-flight fetch and 30-second refresh spacing with separate source/local statuses and prior observations. Files: `career_helper/application/jobs.py`. **Depends**: T040. **Basis**: FR-031–FR-035; API job-search-previews/job-searches/listings/recheck. **Done**: Changed external fields invalidate approval; source failure preserves existing records and manual routes.

- [ ] T042 [US2] Implement direction/listing/manual target selection and confirmed/edit/rejected requirement revisions, with frozen chosen observations and unrestricted manual location. Files: `career_helper/application/targets.py`. **Depends**: T041. **Basis**: FR-007, FR-008, FR-033; API targets/requirements. **Done**: Target tests pass; unconfirmed requirements cannot authorize adopted factual content.

- [ ] T043 [US2] Add protected search, listing/detail/recheck and target/requirement routes with paginated owner-only outcomes and safe original links. Files: `career_helper/web/listings.py`, `career_helper/web/targets.py`, `config/urls.py`. **Depends**: T042. **Basis**: FR-007, FR-031–FR-035; API Endpoint Catalogue. **Done**: Contract tests cover denial, validation and all search/target result shapes.

- [ ] T044 [US2] Build query preview, separate listing results/detail and manual-description/target requirement screens with source variants, freshness and empty/failure/manual fallback feedback. Files: `career_helper/templates/career_helper/listings.html`, `career_helper/templates/career_helper/target.html`, `career_helper/static/career_helper/listings.js`. **Depends**: T043. **Basis**: FR-007, FR-031–FR-035; UX 02A/12A. **Done**: Q5 browser path reaches a selected target without mislabelling directions or stale vacancies.

### Tests first

- [ ] T045 [US2] Write failing command tests for permission/coverage/endpoint evidence and refusal to certify fixture observations as live. Files: `tests/contract/test_source_qualification.py`. **Depends**: T044. **Basis**: FR-031; SC-011; Research R5; Q5. **Done**: Command assertions fail without the qualification implementation.

### Implementation

- [ ] T046 [US2] Add a read-only job-source qualification command that records permitted-use basis, endpoint, observed location coverage, dates/counts and exact non-personal request fields. Files: `career_helper/management/commands/qualify_job_source.py`. **Depends**: T045. **Basis**: FR-031; SC-011; Research R5; Q5. **Done**: Mocked command tests fail on missing permission/coverage; fixture records cannot be certified live.

### Checkpoint and documentation

- [ ] T047 [US2] Run Q5 offline and update source/target contract evidence; leave current live availability to the final authorized live qualification task. Files: `specs/001-career-interview-coach/evidence/us2.md`, `specs/001-career-interview-coach/contracts/external-services.md`. **Depends**: T046. **Basis**: FR-007, FR-031–FR-035; SC-004, SC-011, SC-012. **Done**: All offline search/target checks pass; one-source live gate is explicitly still outstanding.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 5: User Story 3 — tailored resumes and preparation (P1)

**Goal**: Produce reviewable, fact-backed resume suggestions and feasible preparation plans while preserving versions and completed work.

**Independent verification**: Q3/Q6: adopt only supported clauses, preserve two target resumes through restore, show the adjustable calendar-month default and budget shortfalls, and retain completion/manual ordering. SC-003 timing requires live-qualified generation in final acceptance.

### Tests first

- [ ] T048 [P] [US3] Write failing contract/integration/browser tests for semantic clause review, unsupported quantities/entities, accept/reject, two-target history, stale dependencies and restoration. Include forward/reverse schema checks with populated predecessor fixtures and the phase's declared model constraints. Files: `tests/contract/test_resumes.py`, `tests/integration/test_resume_history.py`, `tests/e2e/preparation.spec.js`, `tests/migrations/test_preparation_schema.py`. **Depends**: T047. **Basis**: FR-002, FR-008–FR-010; SC-002; Q3/Q6. **Done**: A valid citation attached to an unsupported fact is rejected and historical review markers persist.

- [ ] T049 [P] [US3] Write failing scheduler/progress tests for confirmed requirements, three task categories, invalid dates/budgets, month-end/timezone, shortfalls, manual override and preserved completion. Files: `tests/unit/test_preparation.py`, `tests/integration/test_task_progress.py`. **Depends**: T047. **Basis**: FR-011–FR-013; SC-003; Q6/Q7. **Done**: Tests cover input boundaries and ordered outcomes rather than repeating a ranking formula.

- [ ] T050 [P] [US3] Write failing coaching-boundary tests for finite operations, unknown fields/enums/citations, untrusted instructions, ungranted processing, new factual additions and stale publication. Files: `tests/contract/test_coaching.py`. **Depends**: T047. **Basis**: FR-009, FR-029, FR-030; External services Structured Coaching. **Done**: Request capture proves minimum scope and no hidden source-description transfer or tools.

### Models and migrations

- [ ] T051 [US3] Add suggestion/resume/revision tables with per-clause evidence and target-scoped restore constraints. Files: `career_helper/models/resumes.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0008_resumes.py`. **Depends**: T048, T049, T050. **Basis**: FR-008–FR-010; Data model Resume and Preparation. **Done**: Prior targets survive migration; clauses retain exact requirement/claim references.

  Data-model constraints (verbatim; part of this task):

  > **ResumeSuggestion — fields**: target_revision, original text, proposed ordered clauses, requirement references, claim-revision references per factual clause, explanation, decision.
  >
  > **ResumeSuggestion — validation/lifecycle**: `proposed → accepted/rejected`; unsupported fact means `blocked` and cannot be accepted. Acceptance is explicit clause-level factual review.

  > **Resume / ResumeRevision — fields**: target_id, ordered sections/clauses, accepted suggestion IDs, evidence references, creation provenance, restored_from nullable.
  >
  > **Resume / ResumeRevision — validation/lifecycle**: Save/restore appends a revision and rechecks evidence. Original source file and other target resumes remain unchanged.

- [ ] T052 [US3] Add plans, revisions, tasks, progress and order revisions with positive estimate validation and explicit completion/override history. Files: `career_helper/models/preparation.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0009_preparation.py`. **Depends**: T051. **Basis**: FR-011–FR-013; Data model Resume and Preparation. **Done**: Prior resumes survive migration; unfinished membership and progress constraints hold.

  Data-model constraints (verbatim; part of this task):

  > **PreparationPlan / PlanRevision — fields**: target_revision, resume_revision nullable, interview_date nullable, horizon_start/end, timezone, default_horizon flag, weekly_minutes, task references, dependency refs.
  >
  > **PreparationPlan / PlanRevision — validation/lifecycle**: Missing interview date gives one calendar month, clamped month-end; user can change it. Insufficient budget produces a visible shortfall, not fabricated feasibility.

  > **PreparationTask — fields**: plan_id, category (`role_knowledge`, `resume_followup`, `external_question`), title, reason, reference sources, estimate_minutes, completion_criterion, dependencies.
  >
  > **PreparationTask — validation/lifecycle**: Explicit source or unknown/generated status; positive bounded estimate; no implied external source if none exists.

  > **TaskProgress — fields**: task_id, state (`todo`, `in_progress`, `completed`), completion evidence/time, mutation_id.
  >
  > **TaskProgress — validation/lifecycle**: Completed record survives reranking and conflicts. Reopening is an explicit user command preserving prior completion history.

  > **TaskOrderRevision — fields**: unfinished task IDs, rank reasons, manual override positions, triggered_by review/completion/user.
  >
  > **TaskOrderRevision — validation/lifecycle**: Unique task membership; deterministic tie-breaks; automatic reranking respects explicit user overrides until cleared. Completed items excluded from remaining-order replacement.

### Implementation

- [ ] T053 [US3] Implement finite structured coaching dispatch with injected fixtures and validators for resume_suggestions/preparation_tasks; keep later operations disabled until their story validators exist. Files: `career_helper/adapters/coaching.py`, `career_helper/domain/coaching.py`, `tests/fixtures/coaching.json`. **Depends**: T052. **Basis**: FR-009, FR-029, FR-030; Research R6; External services Structured Coaching. **Done**: Coaching tests pass with explicit unavailable capability and no fixture output labelled live.

- [ ] T054 [US3] Implement clause review/adopt/reject, immutable save/history/restore and current-evidence rechecks; new personal facts remain separate pending claims. Files: `career_helper/application/resumes.py`, `career_helper/domain/resumes.py`. **Depends**: T053. **Basis**: FR-002, FR-008–FR-010; API resume routes; Q3/Q6. **Done**: Resume tests pass and other target versions/original imports are unchanged.

- [ ] T055 [US3] Implement calendar-month horizons, invalid-input diagnostics, bounded positive estimates, visible shortfalls and deterministic ordering with manual overrides. Files: `career_helper/domain/preparation.py`. **Depends**: T054. **Basis**: FR-011–FR-013; Plan critical transactions 7; Q6. **Done**: Month-end/timezone tests pass; absent external material cannot acquire a fabricated source.

- [ ] T056 [US3] Implement plans from confirmed targets/current resume context, progress/reopen and unfinished reordering, preserving source records and completed history. Files: `career_helper/application/preparation.py`. **Depends**: T055. **Basis**: FR-011–FR-013; API plans/reorder/tasks/progress. **Done**: Progress tests pass; supplied source references work now, with material-entity integration in US4.

- [ ] T057 [US3] Register concrete resume/plan dependencies and atomic invalidation at claim changes, restore and publication, preserving unaffected units and completed work. Files: `career_helper/application/evidence.py`. **Depends**: T056. **Basis**: FR-002, FR-010, FR-013; SC-002; Q3. **Done**: Correction during generation cannot publish a stale current resume/plan.

- [ ] T058 [US3] Add suggestion decisions, resume history/restore, plans/reorder/progress and target/task detail routes using shared owner/validation/mutation rules. Files: `career_helper/web/preparation.py`, `config/urls.py`. **Depends**: T057. **Basis**: FR-008–FR-013; API Endpoint Catalogue. **Done**: Preparation contract tests cover each declared route and invalid input outcome.

- [ ] T059 [US3] Build original/proposed/evidence review and preparation task screens with acceptance controls, history warnings, defaults, feasibility and progress feedback. Files: `career_helper/templates/career_helper/resumes.html`, `career_helper/templates/career_helper/preparation.html`, `career_helper/static/career_helper/preparation.js`. **Depends**: T058. **Basis**: FR-008–FR-013; Interaction lifecycle Screen and Device Boundaries. **Done**: Offline Q6 browser journey saves valid fixtures and exposes stale/unavailable states.

### Tests first

- [ ] T060 [US3] Write failing qualification-command tests for missing configurations, unapproved scope, absent retention evidence and fixture/live separation. Files: `tests/contract/test_training_qualification.py`. **Depends**: T059. **Basis**: FR-027, FR-030; External services Live Training Qualification Gate; Quickstart. **Done**: No missing gate can be converted to a successful live qualification.

### Implementation

- [ ] T061 [US3] Add qualification/configuration validation and the synthetic-only training qualification command, requiring permission, region, formats, retention and scope evidence before live capability enablement. Files: `career_helper/management/commands/qualify_training.py`, `career_helper/application/qualification.py`, `.env.example`. **Depends**: T060. **Basis**: FR-027, FR-030; External services Live Training Qualification Gate; Quickstart. **Done**: Command tests reject unqualified configurations; no vendor is auto-selected or credentials printed.

### Checkpoint and documentation

- [ ] T062 [US3] Run Q3/Q6 and task-order checks with fixtures; update contracts and record live-generation/15-minute acceptance dependencies separately. Files: `specs/001-career-interview-coach/evidence/us3.md`, `specs/001-career-interview-coach/contracts/application-api.md`, `specs/001-career-interview-coach/contracts/external-services.md`. **Depends**: T061. **Basis**: FR-008–FR-013; SC-002, SC-003. **Done**: All offline resume/plan tests pass; SC-003 human timing is still pending.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 6: User Story 4 — manual-turn desktop/phone practice (P1)

**Goal**: Provide sourced questions, both interview modes, explicit Start/Done, requested hints, corrections and honest saved-progress recovery.

**Independent verification**: Q7/Q8 with synthetic services: sourced-question quota, submission-only follow-ups, mode hints, answer revisions, text fallback and retention failures. Physical-device SC-005 includes the US5 review and remains a final integrated gate.

### Tests first

- [ ] T063 [P] [US4] Write failing material import/quality/provenance tests for exact duplicates, conflicting/missing answers, unknown fields and embedded instructions without automatic URL fetching. Files: `tests/contract/test_materials.py`. **Depends**: T062. **Basis**: FR-014, FR-015, FR-029; SC-004; Q7. **Done**: Sources/independent flags survive import; substantive edits append immutable revisions.

- [ ] T064 [P] [US4] Write failing interview/answer/hint tests for eligible frozen context, sourced-question quota, both modes, explicit submit, final confirmation and incomplete end states. Include forward/reverse schema checks with populated predecessor fixtures and the phase's declared model constraints. Files: `tests/contract/test_interviews.py`, `tests/unit/test_interviews.py`, `tests/migrations/test_interviews_schema.py`. **Depends**: T062. **Basis**: FR-016–FR-020, FR-023; Q8; API interview routes. **Done**: Before-submit follow-ups and real-mode hints fail; acoustic inference is excluded.

- [ ] T065 [P] [US4] Write failing recording/STT tests for trusted reservation deadlines, duplicate Done, partial uploads, expiry, early completion, purge failure, late retries and revoked grants. Files: `tests/integration/test_recordings.py`, `tests/contract/test_speech.py`. **Depends**: T062. **Basis**: FR-017, FR-020, FR-027, FR-030; Q8/Q11. **Done**: Actual files and request capture distinguish upload, submission, access revocation and physical removal.

- [ ] T066 [P] [US4] Write failing browser-rule/journey tests for silence, OS interruption, microphone denial, 64 MiB bound, failed upload, active expiry, suspend/resume, text fallback and local-only playback. Files: `tests/browser-unit/recorder.test.mjs`, `tests/browser-unit/playback.test.mjs`, `tests/e2e/interviews.spec.js`. **Depends**: T062. **Basis**: FR-017–FR-020, FR-027; Interaction lifecycle Manual-Turn Protocol/Recording Retention. **Done**: Unsaved memory differs from acknowledged data; tests do not certify deletion while suspended.

### Models and migrations

- [ ] T067 [US4] Add material identity/revision tables before their first interview consumer, preserving independent quality flags and exact source revisions. Files: `career_helper/models/materials.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0010_materials.py`. **Depends**: T063, T064, T065, T066. **Basis**: FR-014–FR-016; Plan W5; Data model Materials, Interviews, and Recordings. **Done**: Prior plans survive migration; edits never overwrite past question text.

  Data-model constraints (verbatim; part of this task):

  > **LearningMaterial — fields**: owner, type question/reference, current_revision_id.
  >
  > **LearningMaterial — validation/lifecycle**: Stable material identity; content and quality edits append a MaterialRevision. Duplicate notice never discards provenance.

  > **MaterialRevision — fields**: material_id, source_id, original prompt/content, answer variants, role/topic tags, exact fingerprint, quality flags, predecessor.
  >
  > **MaterialRevision — validation/lifecycle**: Source type/address/known time explicit; `missing_answer_source`, `conflicting_answers`, `user_doubt` independently representable. Interviews and dependencies bind this exact immutable revision.

- [ ] T068 [US4] Add sessions, turns, answer revisions and hint events with sequence uniqueness, allowed modes/states, frozen context and optional self-ratings. Files: `career_helper/models/interviews.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0011_interviews.py`. **Depends**: T067. **Basis**: FR-016–FR-020, FR-023; Data model Materials, Interviews, and Recordings. **Done**: Prior material history survives migration; answer confirmation/submission rules hold.

  Data-model constraints (verbatim; part of this task):

  > **InterviewSession — fields**: target_revision, eligible resume/claim refs, mode (`coach`, `real`), selected material refs, state, before/after self-rating nullable, rubric version.
  >
  > **InterviewSession — validation/lifecycle**: `ready → active → ended → review_pending → reviewed`; `interrupted` is resumable saved state. Source/claim changes add review requirements; frozen context remains visible history.

  > **InterviewTurn — fields**: session_id, sequence, question text/source or generated rationale, parent_turn_id for follow-up, submission_id nullable.
  >
  > **InterviewTurn — validation/lifecycle**: Unique session/sequence; complete session uses at least one applicable sourced external question if available. Availability/quota failure cannot be labelled complete.

  > **AnswerRevision — fields**: turn_id, original transcript/text, revised text, source (`typed`, `transcribed`, `user_corrected`, `reanswered`), recording_id nullable, submitted_at, confirmation actor/time, previous revision.
  >
  > **AnswerRevision — validation/lifecycle**: Only submitted answers can trigger follow-up; review uses final confirmed revision. Re-answer keeps prior history. No confirmed answer means review cannot evaluate it.

  > **HintEvent — fields**: turn_id, requested_at, level (`understand`, `structure`, `knowledge`), content, operation_id.
  >
  > **HintEvent — validation/lifecycle**: Coach only while active, explicit requests, sequential escalation. Real-mode pre-end requests fail server-side.

- [ ] T069 [US4] Add recording reservations/private-copy references with immutable reservation time, separate processing completion and terminal deletion transitions. Files: `career_helper/models/recordings.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0012_recordings.py`. **Depends**: T068. **Basis**: FR-027; Data model Recording; Q11. **Done**: Lifecycle constraints hold and session history survives migration.

  Data-model constraints (verbatim; part of this task):

  > **Recording — fields**: session/turn, reserved_at, capture_started_at metadata, immutable created_at=reservation time, expires_at, MIME, bytes/hash, private key, keep choice, retention policy, lifecycle state.
  >
  > **Recording — validation/lifecycle**: Reservation immediately before capture conservatively starts lifetime no later than capture. `reserved → uploaded → deletion_pending → deleted`; processing tracked separately. Explicit kept state is policy, not resurrection.
  > Recording processing status references final transcript and review completion separately. Temporary deletion trigger is the earliest of user deletion, `created_at + 24 hours`, or both text-and-review completion. After a terminal trigger, keep/upload/read/dispatch commands fail; deletion failure is visible, access stays revoked, cleanup retries. Retained recordings have no temporary TTL but remain user-deletable. Local browser audio is not persistent recovery storage.

### Implementation

- [ ] T070 [US4] Implement manual material import/search/quality routes and a minimal desktop import form, preserving duplicates/unknowns and linking supplied material references to preparation tasks. Files: `career_helper/application/materials.py`, `career_helper/web/materials.py`, `career_helper/templates/career_helper/material_import.html`, `career_helper/application/preparation.py`, `config/urls.py`. **Depends**: T069. **Basis**: FR-014–FR-016; API materials/quality; Q7. **Done**: US4 can acquire sourced questions without depending on later US5 review features.

- [ ] T071 [US4] Implement eligibility/selection, generated-question labels/rationale, mode transitions and complete-session sourced-question quota checks. Files: `career_helper/domain/interviews.py`, `career_helper/application/interviews.py`, `career_helper/adapters/coaching.py`. **Depends**: T070. **Basis**: FR-016, FR-018; External services generated_question; Q8. **Done**: Selection/mode tests pass; missing quota is never silently certified complete.

- [ ] T072 [US4] Implement reservation, durable bounded upload, private reads and serialized keep/delete; register copies and reject expired IDs before access/processing. Files: `career_helper/application/recordings.py`, `career_helper/application/storage.py`. **Depends**: T071. **Basis**: FR-017, FR-027; API recordings/files; Q11. **Done**: Tests pass through late upload, keep/delete races and failed physical purge.

- [ ] T073 [US4] Implement the qualified-config STT callable with actual MIME, granted glossary, bounded timeout, provisional text and empty/failure outcomes; discard emotion fields. Files: `career_helper/adapters/speech.py`. **Depends**: T072. **Basis**: FR-017, FR-019, FR-020, FR-030; External services Speech Input and Output. **Done**: Speech tests prove zero sends for unsubmitted/expired/deleted/ungranted audio.

- [ ] T074 [US4] Implement explicit Done/typed submit, sequential requested hints, contextual follow-ups, correction/reanswer/final confirmation and end/self-rating commands with saved checkpoints. Files: `career_helper/application/interviews.py`, `career_helper/adapters/coaching.py`. **Depends**: T073. **Basis**: FR-016–FR-020, FR-023; API turns/answers/end; Q8. **Done**: Tests preserve answer history and cite the actual submitted revision for follow-ups.

- [ ] T075 [US4] Expose protected session/detail/recording/upload/submit/hint/confirm/end/file routes with validation, retention states and common form/JSON rules. Files: `career_helper/web/interviews.py`, `career_helper/web/files.py`, `config/urls.py`. **Depends**: T074. **Basis**: FR-017–FR-020, FR-027; API Endpoint Catalogue. **Done**: Contract tests distinguish durable upload, submission and processing.

- [ ] T076 [US4] Implement browser reservation/capture, feature-detected MIME, explicit Done upload/submit, memory-only buffers and size/OS/timer/action/resume expiry handling. Files: `career_helper/static/career_helper/recorder.js`. **Depends**: T075. **Basis**: FR-017, FR-020, FR-027; Interaction lifecycle Manual-Turn Protocol. **Done**: Browser-rule tests pass; silence never submits and expired buffers cannot be replayed/retried.

- [ ] T077 [US4] Implement user-selected localService voice playback with text/replay controls and explicit unavailable audio; no hidden remote speech recognition/playback. Files: `career_helper/static/career_helper/playback.js`. **Depends**: T076. **Basis**: FR-017, FR-020, FR-030; Research R7. **Done**: Playback tests reject non-local voices and preserve text alternatives.

- [ ] T078 [US4] Build desktop/phone setup/practice screens with mode, Start/Done, hints, corrections, saved/unsaved status, recording retention controls and accessible recovery feedback. Files: `career_helper/templates/career_helper/interview.html`, `career_helper/templates/career_helper/interview_setup.html`, `career_helper/static/career_helper/answers.js`. **Depends**: T077. **Basis**: FR-016–FR-020, FR-023, FR-027; Interaction lifecycle Screen and Device Boundaries. **Done**: Offline browser journey covers both modes and failure paths.

### Checkpoint and documentation

- [ ] T079 [US4] Run Q7/Q8 and recording Q11 offline; document MIME/recovery contracts and carry provider-copy, physical-device and suspended-browser qualification forward. Files: `specs/001-career-interview-coach/evidence/us4.md`, `specs/001-career-interview-coach/contracts/interaction-lifecycle.md`, `specs/001-career-interview-coach/contracts/external-services.md`. **Depends**: T078. **Basis**: FR-014–FR-020, FR-023, FR-027; SC-004, SC-005. **Done**: No fixture check is reported as live speech qualification or end-to-end reviewed-session acceptance.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 7: User Story 5 — evidence-based review and personal methods (P2)

**Goal**: Turn confirmed answers and sourced material into bounded feedback, next practice and explicitly verified method revisions.

**Independent verification**: Q7/Q9: final-answer feedback covers four dimensions with at most three priorities and a retest; absent evidence is unassessable; only unfinished work is reranked; only the retested and confirmed method revision becomes formal.

### Tests first

- [ ] T080 [P] [US5] Write failing review tests for four dimensions, exact final-answer spans, unknowns, malformed output, zero evidence, zero-to-three priorities and one-or-more retests. Include forward/reverse schema checks with populated predecessor fixtures and the phase's declared model constraints. Files: `tests/contract/test_reviews.py`, `tests/integration/test_review_evidence.py`, `tests/migrations/test_reviews_schema.py`. **Depends**: T079. **Basis**: FR-019, FR-021–FR-023; SC-007; Q9. **Done**: False citations, unconfirmed answers and acoustic inference are rejected.

- [ ] T081 [P] [US5] Write failing method lifecycle/journey tests for draft fields, same-revision completed retest, explicit confirmation, edit/new draft, withdrawal and evidence invalidation. Files: `tests/unit/test_methods.py`, `tests/integration/test_methods.py`, `tests/e2e/review_methods.spec.js`. **Depends**: T079. **Basis**: FR-024, FR-025; Q9. **Done**: Practice alone cannot promote a draft or carry verification to an edited revision.

- [ ] T082 [P] [US5] Write failing tests for review-gap reprioritization, completed-task/manual-order preservation and transitive invalidation from corrected answers or substantive material changes. Files: `tests/integration/test_review_plan_invalidation.py`. **Depends**: T079. **Basis**: FR-002, FR-013, FR-019, FR-025; Q3/Q7. **Done**: Tests distinguish substantive source changes from label-only topic edits.

### Models and migrations

- [ ] T083 [US5] Add review/revision tables with exact answer/claim dependencies, four feedback dimensions, zero-to-three priorities and retest fields. Files: `career_helper/models/reviews.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0013_reviews.py`. **Depends**: T080, T081, T082. **Basis**: FR-021–FR-023; Data model Reviews and Personal Methods. **Done**: Prior answers/recording states survive migration; insufficient evidence remains a distinct outcome.

  Data-model constraints (verbatim; part of this task):

  > **Review / ReviewRevision — fields**: session, exact confirmed answer IDs, claim dependencies, four feedback dimensions, answer spans, unknowns, zero-to-three priorities, one-or-more retest questions, self-ratings.
  >
  > **Review / ReviewRevision — validation/lifecycle**: Dimensions: knowledge, answer structure, experience evidence, unfamiliar-question handling. Complete feedback must cite answer evidence. No evidence produces `insufficient_evidence`, not fabricated assessment.

- [ ] T084 [US5] Add method/revision/verification/status tables with revision-specific retest confirmation and explicit withdrawal/reverification. Files: `career_helper/models/methods.py`, `career_helper/models/__init__.py`, `career_helper/migrations/0014_methods.py`. **Depends**: T083. **Basis**: FR-024, FR-025; Data model Reviews and Personal Methods. **Done**: Prior reviews survive migration; formal/draft history persists without automatic promotion.

  Data-model constraints (verbatim; part of this task):

  > **PersonalMethod / MethodRevision — fields**: scenario, steps, user example refs, common mistakes, practice instructions, originating review, state.
  >
  > **PersonalMethod / MethodRevision — validation/lifecycle**: `draft → eligible_for_confirmation → formal`; latter requires a completed retest on this revision plus explicit user confirmation.

  > **MethodVerification — fields**: method_revision, session/turn/retest refs, outcome evidence, user confirmation/time.
  >
  > **MethodVerification — validation/lifecycle**: Practice results do not promote automatically. Editing a formal method creates a new draft; previous version remains historical.

  > **MethodStatusEvent — fields**: method/revision, action (`withdraw`, `reverify`, `confirm`), actor/time.
  >
  > **MethodStatusEvent — validation/lifecycle**: Withdrawal removes current formal use without deleting history; privacy deletion can remove history. Changed/invalid evidence adds needs-review and prevents current reuse.

### Implementation

- [ ] T085 [US5] Implement review generation/publication against confirmed answers with evidence-bound dimensions, bounded priorities/retests and the completed transcript-plus-review retention signal. Files: `career_helper/application/reviews.py`, `career_helper/domain/reviews.py`, `career_helper/adapters/coaching.py`. **Depends**: T084. **Basis**: FR-019, FR-021–FR-023, FR-027; API reviews; Q9/Q11. **Done**: Review tests pass and early cleanup uses actual completion of both transcript and review.

- [ ] T086 [US5] Implement method draft generation/edit, completed-retest verification, explicit formal confirmation, withdrawal and reverification. Files: `career_helper/application/methods.py`, `career_helper/domain/methods.py`, `career_helper/adapters/coaching.py`. **Depends**: T085. **Basis**: FR-024, FR-025; API methods; Q9. **Done**: Lifecycle tests pass with revision-specific evidence and no automatic promotion.

- [ ] T087 [US5] Connect review gaps/completed verification to preparation reprioritization and extend evidence invalidation to changed answers/materials and dependent methods. Files: `career_helper/application/preparation.py`, `career_helper/application/evidence.py`. **Depends**: T086. **Basis**: FR-002, FR-013, FR-019, FR-025; Data model Dependency Validity; Q3/Q7. **Done**: Completed/manual-order records persist; substantive changes flag affected history without rewriting it.

- [ ] T088 [US5] Add review/detail and method draft/edit/verify/withdraw routes, plus material detail/quality management, preserving exact revisions and validity. Files: `career_helper/web/reviews.py`, `career_helper/web/methods.py`, `career_helper/web/materials.py`, `config/urls.py`. **Depends**: T087. **Basis**: FR-014, FR-015, FR-021–FR-025; API Endpoint Catalogue. **Done**: Owner-only contract checks reject direct mutation of lifecycle state flags.

- [ ] T089 [US5] Build full desktop/short phone review, material library/quality and desktop method-editing screens with evidence, unknowns, retests and draft/formal status. Files: `career_helper/templates/career_helper/review.html`, `career_helper/templates/career_helper/materials.html`, `career_helper/templates/career_helper/methods.html`, `career_helper/static/career_helper/methods.js`. **Depends**: T088. **Basis**: FR-014, FR-015, FR-021–FR-025; Interaction lifecycle Screen and Device Boundaries. **Done**: Browser journey completes a retest and explicit formal confirmation.

### Checkpoint and documentation

- [ ] T090 [US5] Run Q3/Q7/Q9 and early-retention integration; document final-answer, material-revision and method lifecycle behavior. Files: `specs/001-career-interview-coach/evidence/us5.md`, `specs/001-career-interview-coach/contracts/application-api.md`, `specs/001-career-interview-coach/data-model.md`. **Depends**: T089. **Basis**: FR-013–FR-015, FR-019, FR-021–FR-025; SC-004, SC-007. **Done**: Offline review/method checks pass; human outcome scores remain unmeasured.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 8: User Story 6 — cross-device continuity and data control (P2)

**Goal**: Complete synchronized changes/conflicts and export/deletion/policy controls across every concrete data type.

**Independent verification**: Q10–Q12: two devices preserve conflicting versions/completed records; connected changes appear within 60 seconds; archives preserve context; deletion covers registered copies; old restores cannot revive deleted data.

### Tests first

- [ ] T091 [P] [US6] Write failing two-device sync/conflict tests for missed cursors, reconnect, unsaved drafts, independent completions and stale writes after deletion. Files: `tests/integration/test_sync.py`, `tests/e2e/sync.spec.js`. **Depends**: T090. **Basis**: FR-026; SC-006; Q10. **Done**: Measure committed-change visibility and reject silent local-draft overwrites.

- [ ] T092 [P] [US6] Write failing export/delete/policy tests across all FR-028 categories, archive authorization/expiry, copied dependant text, registered backups, retained audio and purge failures. Files: `tests/contract/test_privacy.py`, `tests/integration/test_exports_deletion.py`, `tests/e2e/privacy.spec.js`. **Depends**: T090. **Basis**: FR-027, FR-028; Q11/Q12; API privacy routes. **Done**: Manifest integrity and actual removal are distinct from access revocation.

- [ ] T093 [P] [US6] Write populated prior-schema migration and interrupted-upgrade/restore tests preserving IDs/order/provenance/review flags and reconciling deletion/expiry before private access. Files: `tests/migrations/test_upgrade_restore.py`, `tests/fixtures/migrations/build_fixture.py`. **Depends**: T090. **Basis**: Constitution V; Plan Migrations and Compatibility; Q12. **Done**: Use actual earlier migrations, refuse newer schemas and avoid invented legacy import data.

### Implementation

- [ ] T094 [US6] Implement owner-only ordered change feeds/full-refetch guidance and concrete conflict resolution across profiles, targets, plans, answers and methods. Files: `career_helper/web/changes.py`, `career_helper/web/conflicts.py`, `career_helper/application/revisions.py`, `config/urls.py`. **Depends**: T091, T092, T093. **Basis**: FR-026; API changes/conflicts; Q10. **Done**: Transaction tests retain both candidates and trusted receipt times.

- [ ] T095 [US6] Implement 10-second visible-tab sync and focus/reconnect refresh, preserving unsaved drafts and showing explicit conflict/delete/reconcile notices. Files: `career_helper/static/career_helper/sync.js`, `career_helper/static/career_helper/conflicts.js`, `career_helper/templates/career_helper/conflicts.html`, `career_helper/templates/career_helper/base.html`. **Depends**: T094. **Basis**: FR-026; SC-006; Interaction lifecycle Corrections, Conflicts, and Sync. **Done**: Two-context checks meet 60 seconds when connected; no persistent personal-data browser cache exists.

- [ ] T096 [US6] Implement category retention settings/impact previews with text/review defaults, hard temporary-audio cap and truthful pending/failed/deleted copy state. Files: `career_helper/application/privacy.py`, `career_helper/web/privacy.py`. **Depends**: T095. **Basis**: FR-027, FR-028; API retention; Q11. **Done**: Policy tests retain independent choices and require impact preview for shortening.

- [ ] T097 [US6] Implement consistent owner-only career-helper-export/v1 archives with checksums, ordered records/provenance/review/conflict state, original imports and selected kept audio; set one-hour generated-archive expiry. Files: `career_helper/application/exports.py`. **Depends**: T096. **Basis**: FR-028; Plan Migrations and Compatibility; Q12. **Done**: All categories are covered without temporary audio, credentials or private storage keys.

- [ ] T098 [US6] Implement accepted-preview deletion, immediate revocation, cancelled/stale jobs, registered-copy purge, content-free tombstones and dependant evidence-unavailable marking. Files: `career_helper/application/deletion.py`, `career_helper/application/evidence.py`. **Depends**: T097. **Basis**: FR-002, FR-028; Data model Concurrency, Processing Choice, and Privacy; Q12. **Done**: Delete-all covers copied text; late outputs cannot resurrect data and failed removal stays visibly incomplete.

  Data-model constraints (verbatim; part of this task):
  > Deletion of a source/claim preserves permitted dependent content only with `evidence_unavailable`/needs-review marking; it must not silently retain deleted source text in a supposedly content-free reference. Show copied personal text in a deletion impact preview so the user can include dependent artifacts. Delete-all purges all such payloads and registered copies. On reconnect, deletion tombstones invalidate stale edits and remove displayed/cache copies; first release keeps no persistent browser personal-data cache. A disconnected screen cannot be remotely erased, so no claim of instantaneous removal from an offline device.

- [ ] T099 [US6] Expose protected retained-file/export/download/deletion-preview/deletion and retention routes, including invalid previews, partial failures and expired archives. Files: `career_helper/web/privacy.py`, `career_helper/web/files.py`, `config/urls.py`. **Depends**: T098. **Basis**: FR-027, FR-028; API Endpoint Catalogue. **Done**: Privacy route tests enforce authorization and true completion for each category.

- [ ] T100 [US6] Build data-control screens with scope/impact previews, independent retention choices and explicit offline-device/user-downloaded-copy limits. Files: `career_helper/templates/career_helper/privacy.html`, `career_helper/static/career_helper/privacy.js`. **Depends**: T099. **Basis**: FR-027, FR-028; Interaction lifecycle Export and Deletion. **Done**: Browser tests show consequences, saved choices and actionable incomplete-purge feedback.

- [ ] T101 [US6] Implement operator-only backup/restore maintenance and schema guards with registered backups, paused writers, policy-compliant copies and tombstone/expiry reconciliation before service resumes. Files: `career_helper/management/commands/backup_private.py`, `career_helper/management/commands/restore_private.py`, `career_helper/application/maintenance.py`, `specs/001-career-interview-coach/operations.md`. **Depends**: T100. **Basis**: Constitution V; Plan Migrations and Compatibility; Q12. **Done**: Upgrade/restore tests pass without adding generic user archive import or temporary-audio backups.

### Tests first

- [ ] T102 [US6] Write failing audit-command tests against real temporary copies for expired, unknown, failed and physically removed states. Files: `tests/integration/test_retention_audit.py`. **Depends**: T101. **Basis**: FR-027, FR-028; Quickstart audit_retention; Q11. **Done**: Inaccessible copies cannot pass the physical-removal assertion.

### Implementation

- [ ] T103 [US6] Add the retention audit command with overdue/copy inventory and content-free reports distinguishing physical deletion from unknown, pending or inaccessible copies. Files: `career_helper/management/commands/audit_retention.py`. **Depends**: T102. **Basis**: FR-027, FR-028; Quickstart audit_retention; Q11. **Done**: Audit tests cannot certify unverified provider copies or failed physical removal.

### Checkpoint and documentation

- [ ] T104 [US6] Run Q10–Q12 including populated migrations, failed-upgrade recovery, private media/export authorization and stale-device writes; update contracts/operations guidance. Files: `specs/001-career-interview-coach/evidence/us6.md`, `specs/001-career-interview-coach/contracts/application-api.md`, `specs/001-career-interview-coach/operations.md`. **Depends**: T103. **Basis**: FR-026–FR-030; SC-006; Constitution V. **Done**: Offline continuity/privacy checks pass; host/device qualification remains a separate gate.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Phase 9: Cross-cutting verification, qualification and release evidence

**Goal**: Complete application verification and the explicitly separate live-service, deployment, device, visual and human-outcome gates.

**Independent verification**: All Q1–Q12 and SC-001–SC-012 evidence is attributable to actual runs; missing live configuration, physical-device proof, visual review or four-week outcomes remains an unmet release gate.

### Tests first

- [ ] T105 Add cross-story adversarial tests for altered claims/answers/materials during generation, consent revocation, delete-versus-late-output, resume restore and early transcript-plus-review deletion. Files: `tests/integration/test_full_lifecycle.py`, `tests/contract/test_all_private_routes.py`. **Depends**: T104. **Basis**: FR-002, FR-010, FR-019, FR-026–FR-030; SC-002; Q1/Q3/Q11/Q12. **Done**: Assertions cover every concrete artifact/private endpoint and detect missing integration rather than duplicate unit rules.

### Verification

- [ ] T106 Run the canonical Python/browser/type/lint/schema/static checks and integrated Q1–Q12 with external network denied; close failures within the owning tasks before continuing. Files: `specs/001-career-interview-coach/evidence/offline-suite.md`. **Depends**: T105. **Basis**: Plan Testing Strategy; Constitution IV; Quickstart Canonical Verification Commands. **Done**: Record exact versions/commands/results; migrations and real-connection concurrency checks pass separately from browser fixtures.

### Deployment preparation

- [ ] T107 [P] Create reviewed Linux host service/proxy configuration for HTTPS, Gunicorn, independent jobs/retention/watchdog and persistent private storage with production guards and maintenance instructions. Files: `deploy/career-helper-web.service`, `deploy/career-helper-jobs.service`, `deploy/career-helper-retention.service`, `deploy/career-helper-watchdog.service`, `deploy/reverse-proxy.conf`, `specs/001-career-interview-coach/operations.md`. **Depends**: T106. **Basis**: Plan Technical Context/W8; Research R8; Quickstart Prerequisites. **Done**: Configuration validation and check --deploy pass with synthetic configuration; applying it to an external host requires deployment authorization.

### Visual/accessibility verification

- [ ] T108 [P] Compare implemented screens to accessible approved Figma frames and perform keyboard/focus/status/screen-reader and desktop/phone-boundary review; resolve actual mismatches in the owning story. Files: `specs/001-career-interview-coach/evidence/ux-accessibility.md`. **Depends**: T106. **Basis**: Prototype review gate; UX addendum; Interaction lifecycle Accessibility and Evidence. **Done**: Record frame/device evidence; inaccessible Figma or absent assistive-technology review remains pending rather than assumed correct.

### Live source qualification

- [ ] T109 Revalidate the one configured job source through the qualification command, current permission basis, non-personal request preview and observed mainland workplace content. Files: `specs/001-career-interview-coach/evidence/job-source-live.md`. **Depends**: T107, T108. **Basis**: FR-031–FR-035; SC-011, SC-012; Research R5; Q5. **Done**: Record actual endpoint/time/counts/IDs and limitations; do not reuse historical research counts or claim broad market coverage.

### Live configuration decision

- [ ] T110 Qualify candidate coaching and STT configurations against current terms, region/access, structured Chinese output, actual formats and recording-copy deletion; document the chosen minimum configuration and disclosure. Files: `specs/001-career-interview-coach/evidence/training-configuration.md`, `specs/001-career-interview-coach/contracts/external-services.md`. **Depends**: T109. **Basis**: FR-017, FR-027, FR-030; Research R6; External services Live Training Qualification Gate. **Done**: No personal payload or live enablement yet; missing owner-supplied configuration/permission evidence or incompatible retention is an explicit gate, not an invented provider.

### Tests first

- [ ] T111 [P] Write contract tests for the selected coaching transport using recorded synthetic response shapes and a local request recorder, including limits, grants and safe failures. Files: `tests/contract/test_coaching_service.py`. **Depends**: T110. **Basis**: FR-009, FR-021, FR-029, FR-030; External services Structured Coaching. **Done**: Tests fail until the selected concrete callable satisfies existing operation contracts.

- [ ] T112 [P] Write contract tests for the selected STT transport with WebM/Opus and MP4/AAC inputs, grant/expiry guards, transient failures and provider-copy lifecycle evidence requirements. Files: `tests/contract/test_speech_service.py`. **Depends**: T110. **Basis**: FR-017, FR-019, FR-020, FR-027, FR-030; External services Speech Input and Output. **Done**: Tests fail until the selected callable satisfies MIME/privacy/lifetime boundaries.

### Implementation

- [ ] T113 Implement the one selected server-side coaching service callable and bind it behind existing validators/qualification guards, using server-only secrets and the finite operation set. Files: `career_helper/adapters/coaching_service.py`, `config/settings.py`, `.env.example`. **Depends**: T111, T112. **Basis**: FR-009, FR-011, FR-016, FR-018, FR-021, FR-024, FR-030; Research R6. **Done**: Transport tests pass; fixture/live modes stay distinct, with no vendor discovery or automatic fallback.

- [ ] T114 Implement the one selected STT service callable and configuration binding without speculative transcoding; add a bounded transcoder only if the qualified formats actually require it and document its deletion lifecycle. Files: `career_helper/adapters/speech_service.py`, `config/settings.py`, `.env.example`. **Depends**: T113. **Basis**: FR-017, FR-019, FR-020, FR-027, FR-030; External services Speech Input and Output. **Done**: Transport tests pass; every actual audio copy follows the existing deadline and copy inventory.

### Live training qualification

- [ ] T115 Run qualify_training with synthetic Chinese/English-term samples for all implemented operations/MIMEs, record model/config/disclosure versions and prove revoke/deny yields zero further sends. Files: `specs/001-career-interview-coach/evidence/training-live.md`. **Depends**: T114. **Basis**: FR-009, FR-017–FR-025, FR-027, FR-030; External services Live Training Qualification Gate. **Done**: Actual configuration passes quality/scope/copy-retention checks; fixtures and no-training statements alone cannot satisfy qualification.

### Deployment/lifetime qualification

- [ ] T116 On an authorized qualification host, exercise independent cleanup with stopped web/jobs, watchdog/overdue detection, restart reconciliation and the complete backup/provider-copy inventory. Files: `specs/001-career-interview-coach/evidence/hosting-retention.md`. **Depends**: T115. **Basis**: FR-027, FR-028; Research R8; Q11. **Done**: Record physical deletion evidence and host-wide failure limits; an incompatible host/provider stays unqualified for live recording.

### Physical-device verification

- [ ] T117 Run real desktop Chrome/Edge/Safari and physical iOS Safari/Android Chrome voice paths, including manual turns, silence, hints, corrected terminology, saved review, text fallback and suspend/expiry handling. Files: `specs/001-career-interview-coach/evidence/devices-voice.md`. **Depends**: T116. **Basis**: FR-017–FR-020, FR-027; SC-005; Q8/Q11. **Done**: Desktop and phone each complete at least 10 minutes with actual audio; unsupported playback or unproven suspended-device deletion is not waived by emulation.

### Human/timing verification

- [ ] T118 Measure confirmed-profile/JD to saved resume plus at least three tasks, connected phone-to-desktop text/review/plan visibility, and the two usefulness ratings after three distinct directions. Files: `specs/001-career-interview-coach/evidence/usability-sync.md`. **Depends**: T117. **Basis**: SC-003, SC-006, SC-009; Q6/Q10; Quickstart Human Outcome Trial. **Done**: Record start/end conditions: at most 15 minutes, at most 60 seconds, and both ratings at least 4/5; failures stay visible.

### Human outcome protocol

- [ ] T119 Record the fixed five-level rubric, baseline, rater basis, unseen comparable questions, schedule and separate tension self-report method before starting the four-week trial. Files: `specs/001-career-interview-coach/evidence/trial-protocol.md`. **Depends**: T118. **Basis**: FR-023; SC-008; Quickstart Human Outcome Trial. **Done**: Protocol uses the existing rubric and at least two sessions weekly; no retrospective baseline or invented scores.

### Human outcome verification

- [ ] T120 Conduct and record the four-week trial against the fixed protocol and final unseen-question reassessment; keep personal answers outside repository evidence. Files: `specs/001-career-interview-coach/evidence/four-week-outcomes.md`. **Depends**: T119. **Basis**: SC-008; Quickstart Human Outcome Trial. **Done**: At least two sessions per week and at least one rubric-level improvement are evidenced; elapsed time or green code checks alone cannot complete this task.

### Documentation and final review

- [ ] T121 Rerun affected canonical checks after live-adapter/integration changes, reconcile FR/SC evidence, update actual commands and contract/operations limits, and review changed files for scope/security/compatibility. Files: `AGENTS.md`, `specs/001-career-interview-coach/quickstart.md`, `specs/001-career-interview-coach/operations.md`, `specs/001-career-interview-coach/evidence/release-readiness.md`. **Depends**: T120. **Basis**: All FR-001–FR-035 and SC-001–SC-012; Constitution Review Standard/VI. **Done**: Report offline/live/device/UX/migration/human gates separately; any failed or unavailable mandatory gate prevents a first-release completion claim.

**Checkpoint**: Complete the phase checks before its dependent tasks; leave live/human evidence outstanding until actually obtained.

---

## Dependencies and execution order

```mermaid
flowchart LR
  S[Setup] --> F[Foundation]
  F --> U1[US1 Facts and directions]
  U1 --> U2[US2 Vacancies and targets]
  U2 --> U3[US3 Resume and preparation]
  U3 --> U4[US4 Materials and practice]
  U4 --> U5[US5 Review and methods]
  U5 --> U6[US6 Sync and privacy completion]
  U6 --> R[Offline regression]
  R --> L[Live source and service qualification]
  L --> D[Hosting and physical devices]
  D --> H[Timed usability and four-week outcomes]
  H --> A[Release evidence review]
```

Story phase ordering is intentional: these journeys share provenance and saved state, so they are not declared independent development tracks. Each phase has its own fixture-based verification boundary. Runtime manual workflows remain usable when external services are unavailable; a dependency on US2's target contract does not make live job search a prerequisite for using a manually imported target.

- **Foundation is early protection**: owner/consent/storage/deadline/conflict primitives precede every story. US6 completes the cross-device and all-category privacy experience; it does not introduce security for the first time.
- **Earliest consumer placement**: US1 owns direction catalog/assessment despite part of W3 being described with listings in the plan. US2 owns target requirement confirmation used by US3. US4 implements the sourced-material import/revision primitive from FR-014/FR-015 before interview selection; US5 extends its library/quality experience and evidence invalidation. Preparation can reference supplied source records before that material table exists.
- **Review handoff without a cycle**: US4's offline checkpoint ends at confirmed, recoverable answers and a review-ready session. US5 supplies the actual review. Final SC-005 explicitly requires both; no story checkpoint silently waives the full-release criterion.
- **Provider readiness**: synthetic interfaces unblock development, while actual adapters/configuration qualification remain mandatory before W4/W5 live acceptance. US3/US4 checkpoints are offline implementation evidence only. Source terms/access, host deletion, actual devices and outcome trials are not inferred from fixtures.
- **Migrations are serial**: the initial core migration through the method migration form a single chain. Each phase's tests cover its new constraints and populated predecessor data. US6 adds full upgrade/restore/recovery evidence. Shared registries and `config/urls.py` have one writer at a time.

## Parallel execution examples

Only the batches below carry `[P]`. All their prerequisites must already be complete; each task writes disjoint files within its batch. This is a scheduling guide, not an instruction to launch agents during task generation.

| Batch | Prerequisite | Tasks eligible together | Why independent |
| --- | --- | --- | --- |
| Setup tools | T001 | T002, T003 | Python config/test packages versus browser toolchain files. |
| Foundation tests | T005 | T006, T007, T008, T009 | Separate access, revision, job and copy-lifecycle suites. |
| US1 test authoring | T020 | T021, T022, T023 | Separate document fixtures, claim/migration/browser tests and catalog fixtures. |
| US1 extraction helpers | T025 | T026, T027 | Different format-specific modules; integration wrapper follows both. |
| US2 test authoring | T034 | T035, T036 | Transport/source fixtures versus aggregation/target/migration tests. |
| US3 test authoring | T047 | T048, T049, T050 | Resume, scheduler and coaching suites have separate files. |
| US4 test authoring | T062 | T063, T064, T065, T066 | Material, interview, server recording and browser suites are disjoint. |
| US5 test authoring | T079 | T080, T081, T082 | Review output, method lifecycle and plan-invalidation suites are disjoint. |
| US6 test authoring | T090 | T091, T092, T093 | Sync/browser, privacy and maintenance migration fixtures are separate. |
| Release preparation | T106 | T107, T108 | Deployment files/operations guidance versus visual-accessibility evidence. |
| Selected transport tests | T110 | T111, T112 | Separate coaching and speech transport suites. |

## Requirement and acceptance traceability

Every task carries its own basis. This index identifies the primary implementation and verification owners without treating a reference as completion.

| Requirements | Primary task owners | Verification |
| --- | --- | --- |
| FR-001–FR-003 | T024, T028, T029, T030 | T021, T022, T105 |
| FR-004–FR-006 | T025, T031, T033 | T023, T034 |
| FR-007, FR-031–FR-035 | T039, T040, T041, T042, T044 | T035, T036, T109 |
| FR-008–FR-010 | T042, T054, T057 | T048, T105 |
| FR-011–FR-013 | T055, T056, T087 | T049, T082, T118 |
| FR-014–FR-015 | T070, T088, T089 | T063, T082 |
| FR-016–FR-020 | T071, T072, T073, T074, T078 | T064, T065, T066, T117 |
| FR-021–FR-023 | T085, T074, T089 | T080, T117, T120 |
| FR-024–FR-025 | T086, T087 | T081, T082 |
| FR-026 | T013, T014, T094, T095 | T006, T007, T091, T118 |
| FR-027–FR-028 | T016, T072, T096, T097, T098, T101 | T009, T065, T092, T093, T116, T117 |
| FR-029–FR-030 | T015, T017, T053, T073 | T008, T050, T063, T115, T105 |
| SC-001 / SC-010 | T031, T028 | T034 |
| SC-002 | T030, T054, T087 | T048, T105 |
| SC-003 / SC-006 / SC-009 | T059, T095 | T118 |
| SC-004 / SC-011 / SC-012 | T044, T070 | T047, T079, T109 |
| SC-005 / SC-007 | T078, T085 | T080, T117 |
| SC-008 | T119 | T120 |
| Constitution V / migration compatibility | T010, T011, T012, T024, T025, T037, T038, T051, T052, T067, T068, T069, T083, T084, T101 | T093, T104 |

## Implementation strategy

1. After implementation is separately authorized, apply the required checklist/review workflow, then complete setup and foundation. Preserve approved scope and document any material contract conflict before dependent changes.
2. Deliver **US1 as the first demonstrable increment**: verified import/manual facts and three-domain exploration. This is the suggested MVP milestone for feedback, not a reduced interpretation of the approved complete first release.
3. Add US2 through US6 in the dependency order above, with tests first, migrations reviewed and checkpoint evidence at each phase. Use fixtures to isolate a story's behavior; keep the entire first-release scope, including both P2 stories.
4. Complete offline regression, then qualified live services, hosting, actual devices, visual/accessibility review and timed outcomes. A missing resource does not prevent unrelated offline work, but the affected live task stays unchecked.
5. Establish the baseline before the four-week trial. Do not compress elapsed-time requirements, infer improvement from model scores, or mark that task complete in a coding session.
6. Review the full evidence set and updated operational/contract documentation. Report completion only at the corresponding milestone; deployments and Git operations require their own task-specific authorization.

## Notes

- All tasks start unchecked. They describe future work; no implementation or acceptance execution occurred during generation.
- Exact file paths within a task are its review surface, not permission to edit unrelated files. Test and production paths have separate purposes.
- An implementation task is complete when its focused previously failing checks pass and its stated public outcome is evidenced. A phase checkpoint records checks already defined; it does not silently add new behavior.
- For later changes, run the appropriate fresh checks rather than repeatedly rerunning unrelated suites. Final integration checks are justified by new adapters, concrete artifact interactions and release evidence.
- Hook checks before/after generation found no `.specify/extensions.yml`; no extension commands were dispatched.

## Task inventory

| Phase | Tasks | Count |
| --- | --- | --- |
| Phase 1: Setup — shared toolchain | T001–T005 | 5 |
| Phase 2: Foundational — blocking access, integrity and lifecycle primitives | T006–T020 | 15 |
| Phase 3: User Story 1 — verify experience and explore directions (P1) | T021–T034 | 14 |
| Phase 4: User Story 2 — discover concrete vacancies and select targets (P1) | T035–T047 | 13 |
| Phase 5: User Story 3 — tailored resumes and preparation (P1) | T048–T062 | 15 |
| Phase 6: User Story 4 — manual-turn desktop/phone practice (P1) | T063–T079 | 17 |
| Phase 7: User Story 5 — evidence-based review and personal methods (P2) | T080–T090 | 11 |
| Phase 8: User Story 6 — cross-device continuity and data control (P2) | T091–T104 | 14 |
| Phase 9: Cross-cutting verification, qualification and release evidence | T105–T121 | 17 |

**Total**: 121 tasks; **parallel-marked**: 30; **first-class test-authoring tasks**: 28.
