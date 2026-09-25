# Phase 0 Research: Career Interview Coach

**Date**: 2026-09-25 | **Parent**: [plan.md](./plan.md) | **Scope**: technical decisions for the approved first release; no implementation.

The repository was inspected directly. Earlier discovery notes are historical; the current specification/constitution govern this design. No separate approved stack or application exists. Decisions below resolve the architecture questions needed for Phase 1. Live training configuration and deployment qualification are explicit delivery gates; this document does not certify an untested provider.

## R1 — Application and toolchain

**Decision**: Python 3.12, Django 5.2 LTS, server templates with small ES2022 modules and CSS. Use built-in auth, sessions, forms, ORM, migrations and tests. Browser-only tooling uses Node 24 LTS, Playwright and checkJs; lock supported patch versions during implementation.

**Rationale**: The owner-only workflow requires durable records, authentication, forms and a small amount of intensive browser interaction. Django supplies those server facilities in one deployment; Figma layouts do not imply an SPA. Django's [support schedule](https://www.djangoproject.com/download/) lists 5.2 LTS through April 2028. [Node releases](https://nodejs.org/en/about/previous-releases) provide the development runtime baseline.

**Alternatives considered**: React/Vite plus FastAPI would add separate authentication, persistence/migration and client-state choices before an active requirement needs them. A browser-only app cannot share one durable owner record or enforce server retention. Native desktop/mobile apps multiply delivery work without a first-release need.

## R2 — Storage, jobs, and conflicts

**Decision**: SQLite on one persistent host, short IMMEDIATE write transactions and revision-conditional updates; immutable content revisions and explicit conflicts. A fixed-operation database job table plus one supervised worker handles imports, search and training; a separate retention command cannot be delayed by that queue.

**Rationale**: Two devices for one owner do not require a distributed store. SQLite locking is limited, and `select_for_update()` has no effect; test with separate real connections, keep network work outside transactions, and use a finite busy timeout. [Django SQLite notes](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes)

**Alternatives considered**: PostgreSQL remains a possible reviewed migration after measured contention/deployment needs. Redis/Celery, event sourcing and CRDTs are unnecessary. Last-writer-wins violates FR-026. Nonconflicting scalar edits may merge; semantic lists and overlapping fields require user resolution.

## R3 — Single owner and consent

**Decision**: Provision one ordinary Django user via a local management command and bind its immutable ID to the owner configuration. All private endpoints verify that exact identity, not merely login or staff status. No registration/admin/invitation pages. Use server sessions, HTTPS, CSRF and login throttling; no credentials in client storage. Record consent by provider, purpose and data categories, with explicit unknown/granted/denied states.

**Rationale**: Django already handles passwords and sessions; its [authentication system](https://docs.djangoproject.com/en/5.2/topics/auth/default/) is sufficient with a narrow owner restriction. It does not supply brute-force throttling by default, so implement a small bounded attempt policy at the login boundary. [Security documentation](https://docs.djangoproject.com/en/5.2/topics/security/)

**Alternatives considered**: Social login, multiple roles and user invitations are outside scope. A secret URL is not authentication. A single blanket consent cannot express rejection of one processing feature while preserving manual workflows.

## R4 — PDF and DOCX

**Decision**: `pypdf` for text PDF; `python-docx` for DOCX paragraph/table order. Parse in a subprocess with byte, expanded-ZIP, page, text, CPU/wall-time and memory limits. Preserve the original, extraction segments and diagnostics; candidates start pending. Report partial/unsupported regions and support manual entry.

**Rationale**: PDF image recognition is outside scope. PDF streams can expand dramatically; file size alone is not a sufficient bound. [pypdf text extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html) DOCX tracked changes or unsupported structures can be omitted by ordinary collections, so successful parsing must not imply complete extraction. [python-docx document API](https://python-docx.readthedocs.io/en/latest/api/document.html)

**Alternatives considered**: OCR and cloud document parsing add scope/privacy costs. A handwritten PDF/DOCX parser is less reliable than the two narrowly justified libraries. Layout-perfect Word/PDF resume export is not an approved requirement.

## R5 — A concrete mainland-China job source

**Decision**: One concrete adapter, `greenhouse:canonical`, reading Canonical's public job board and selecting explicit mainland-China workplace records locally. Use only for the owner's private personal, noncommercial access; preserve original descriptions/notices, attribution and links. Separate local assessments from source text.

**Access evidence**: The [official Greenhouse Job Board API](https://docs.greenhouse.io/job-board.html) documents unauthenticated GETs for published jobs. During this planning session a TLS-verified request to the [Canonical board](https://boards-api.greenhouse.io/v1/boards/canonical/jobs?content=true) returned HTTP 200 and 306 records at 2026-09-24T17:21:08Z (2026-09-25 01:21 Asia/Shanghai); eight named Beijing or Shanghai. The direct detail endpoint for job 5560784 also returned HTTP 200. No credentials or personal data were sent; TLS verification remained enabled.

| Live ID | Observed title/location | Independent employer reference |
| --- | --- | --- |
| 5560784 | Software Engineer, Ubuntu Commercial Computers; Beijing, China | [Canonical career page](https://canonical.com/careers/5560784) |
| 7561124 | Silicon Alliances Ecosystem Development Manager; Shanghai or Beijing | [Canonical career page](https://canonical.com/careers/7561124) |

**Permission evidence and interpretation**: [Canonical's terms](https://canonical.com/legal/terms) permit personal, educational and noncommercial display/download/printing with notices retained. Combined with the documented public endpoint, this supports the bounded personal acquisition proposed here. This is an interpretation of those terms, not an express third-party aggregation licence. It does not authorize public/commercial republication, arbitrary employer boards, model training on descriptions or bypassing restrictions. A scope change needs a new source assessment; failure to retain this permission basis disables acquisition.

**Freshness/quality**: Source `first_published` was 2023-12-11 for 5560784 and 2026-01-23 for 7561124. All eight shared `updated_at=2026-08-05T18:23:33-04:00`; a shared update is not proof of individual recruiter activity. Describe presence in the published source at collection time, never guarantee active recruitment. These records establish usable content and location coverage, not broad coverage of every desired industry or mainland network reachability.

**Privacy and resilience decision**: Show the exact external request preview: Canonical board identifier and descriptions option. Personal interests/keywords/facts remain in local filtering; the owner can adjust local filters or cancel before sending. One in-flight fetch; user-triggered only; bounded timeout, honor Retry-After, at most one transient retry. No numeric GET limit was found in the API docs, so no unlimited-access claim. API failures, valid empty results and local no-match results remain distinct. No background crawl or application-submission POST.

**Alternatives considered**: Veeva had Shanghai jobs but its [terms](https://www.veeva.com/terms/) restrict copying/derivatives/mirroring; MongoDB's [terms](https://www.mongodb.com/legal/terms-of-use) also restrict automated retrieval. Unverified Boss and other boards are not promised. The first release requires one usable source, not two live sources; synthetic two-source conflicts test aggregation independently.

## R6 — Fact-backed generation and speech boundaries

**Decision**: Finite server-side coaching operations and one transcription operation with validated inputs/outputs. No arbitrary tools, URLs, recursive agents, provider discovery or automatic vendor switching. Test using deterministic fixtures. Before live enablement, qualify and pin one text-generation configuration and one STT configuration (they may share a provider), recording endpoint/model version, region, formats, processing retention/deletion, purpose and credentials handling in deployment configuration. Missing qualification produces an explicit unavailable state, not simulated success.

**Rationale**: Core fact/mode/review/retention rules must not depend on a model. The product spec authorizes functionality but does not select a vendor or waive data rules. Model output remains inference; references to valid IDs do not prove semantic support. New personal facts need their own confirmed claim before adoption. The exact qualification checklist and finite operation signatures are in [external-services.md](./contracts/external-services.md).

**Alternatives considered**: Binding a paid vendor/model now without location, credentials and retention evidence would invent readiness. Self-hosted inference is allowed only if the selected host meets quality/resource requirements, not assumed free. Browser SpeechRecognition is excluded: support is limited and some implementations send audio to a browser-selected service. [MDN SpeechRecognition](https://developer.mozilla.org/en-US/docs/Web/API/SpeechRecognition)

**Research limit**: No live generation/STT provider was qualified or invoked. For example, Alibaba's [privacy notice](https://www.alibabacloud.com/help/en/model-studio/privacy-notice) states it stores model/application invocation data; a no-training statement is not evidence of zero retention or deletion within this product's limits. Coaching qualification is required before W4 live acceptance; STT qualification is required before W5 live acceptance. Both are release blockers until evidenced, even if all offline tests pass. A service whose copies cannot satisfy FR-027 cannot be enabled for recordings under the present specification.

## R7 — Manual-turn recording and playback

**Decision**: Use getUserMedia/MediaRecorder over HTTPS. Reserve server recording ID/time before capture; keep the active answer in memory, upload on explicit Done, and recover only acknowledged saved data. Select MIME types by feature detection. Silence and OS capture-stop events do not submit. Text continuation is always available. Under the owner-approved 2026-09-25 FR-027 boundary, unsaved buffers have no persistent cache: clear on upload acknowledgement, cancellation, page teardown or active expiry, and clear expired buffers before any audio action on resume. Disclose before capture that memory clearing during browser/device suspension is not guaranteed; actual-device qualification verifies these observable controls.

**Rationale**: [getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) requires a secure context and permission. [MediaRecorder dataavailable](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/dataavailable_event) timing can vary with browser/device state, so chunk count is not a clock. [isTypeSupported](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/isTypeSupported_static) is a capability test, not a guarantee of successful capture.

**Playback**: Prefer local browser TTS voices only when `localService` is true; otherwise disclose unavailable audio and show text. A remote TTS adapter needs its own qualification/consent and is added only if required to pass actual-device voice acceptance. [MDN localService](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService)

**Alternatives considered**: Realtime streaming/VAD/barge-in contradict or exceed manual-turn scope. IndexedDB audio and service-worker recording caches cannot reliably expire when the browser is closed. Incremental upload adds complexity not required to preserve already saved turns.

## R8 — Retention and recovery

**Decision**: For stored server/provider recording copies, fixed server creation time and hard deadline; independently supervised cleanup; read/upload/dispatch/keep guards; no temporary audio in backups, logs or generated exports. Keep choice and deletion are serialized. Distinguish access revocation, deletion pending, failed and verified deletion. Transcoding temporary files and external copies belong to the same lifecycle.

**Rationale**: An hourly timer or a request-time expiry flag cannot prove physical removal by 24 hours. Cleanup should schedule ahead of deadlines with retry margin; service startup reconciles pending deletions before serving data. A stopped host cannot unlink files: qualify continuously running monitored hosting and report actual failure rather than claiming success. If a proposed deployment cannot meet FR-027, reject that deployment or seek an explicit spec change; never silently weaken expiry.

**Alternatives considered**: Browser-only cleanup, enqueueing deletion behind model jobs, resetting creation on retry, and unconditional backups all violate the required lifetime. User-chosen retained recordings and default-until-deleted text/reviews follow separate policies.

## R9 — Compatibility and verification

**Decision**: Initial Django schema plus versioned exports; future migration tests on populated fixtures and restore reconciliation. Separate deterministic tests from live provider/device and four-week user outcomes. [Django migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/) support schema evolution, but SQLite changes can rebuild tables, so migrations run during maintenance after a verified backup. Apply [Django deployment checks](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/) before external access.

**Alternatives considered**: No legacy import/migration can be invented because there is no app data. Full offline sync, generalized portability and public SDK stability exceed the approved first release.

## UX Evidence and Gate Disposition

Figma screenshot/metadata calls for the approved file returned the Starter-plan MCP tool limit; browser search access also failed. The repository explicitly permits nonvisual planning from the spec and UX addendum. No visual parity claim is made. Exact screen review remains required before UI acceptance.

Historical Phase 0 conclusion: source research supported Phase 1 under the narrow personal-use interpretation above; deployment/cleanup, concrete generation/STT configuration, real device voice behavior, Figma review and longitudinal outcomes remained unqualified. The subsequent owner decision and consistency-remediation record in plan.md resolve C1 by distinguishing hard stored-copy deletion deadlines from disclosed memory-only browser cleanup and expiry-on-resume controls. This closes the documentation blocker without qualifying a deployment or authorizing implementation. None of the live gates may be treated as already passed by later tasks or implementation.
