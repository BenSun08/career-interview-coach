# Phase 1 Data Model

**Parent**: [plan.md](./plan.md) | **Requirements**: [spec.md](./spec.md) | **Status**: proposed contracts; no schema/code generated.

## Shared Rules

- IDs are opaque server-issued UUIDs except external posting IDs. Every private aggregate belongs to the configured owner. Device ID is a user-labelled provenance identifier, never authorization.
- Persist UTC timezone-aware timestamps; retain original source date strings/offsets alongside normalized values. Applicable career dates can be partial (`year`, `month`, `day` precision) or unknown; never invent day/month precision. Planning uses the owner's configured timezone, default Asia/Shanghai and visibly editable.
- Revisions have `id`, `aggregate_id`, `revision_number`, `previous_revision_id`, `created_at`, `device_id`, `origin`, `schema_version`. Unique aggregate/revision number; immutable content. Current pointers, job state and deletion metadata are operational fields, not overwritten historical content.
- Unknown is represented by null plus a reason where useful, not an empty fabricated value. Preserve original user text and ordered items. Comparison keys are separate derived fields; normalization never mutates source content.
- Stored foreign keys and uniqueness/check constraints enforce ownership, revision membership and idempotency where possible. Domain validation enforces semantic constraints. Client/provider input must not set confirmation, current status, trusted time or owner identity directly.
- `validity` is computed from current dependencies and unresolved conflicts: `current`, `needs_review`, `evidence_unavailable`. A saved historical payload does not become current through viewing, exporting, restoring or dismissing a warning.
- Concrete aggregates have concrete tables. Shared revision conventions do not imply a generic entity store, arbitrary JSON event log or polymorphic repository framework.

## Access, Sources, and Claims

| Entity | Principal fields and relationships | Validation/lifecycle |
| --- | --- | --- |
| OwnerBinding | Singleton `user_id`, `timezone`, configured_at; Django user/password/session data remains in Django auth tables. | Provision locally; active user must equal binding for every private operation. No public account creation. |
| Device | `id`, owner, user-visible label, first/last seen. | Metadata only; server receipt time wins over client time for deadlines. |
| SourceRecord | `id`, type (`resume_file`, `manual_claim`, `manual_jd`, `job_board`, `manual_material`, `generated`), title, URI nullable, source times nullable, collected_at, original content/file reference, notices, content hash. | Source content remains untrusted, never executable; original link is not evidence of current recruiting. |
| ResumeImport | source_id, original filename, detected type, bytes, hash, private blob key, created_at, extraction status, diagnostics. | `queued → extracting → complete/partial/unreadable/failed`; only PDF/DOCX allowed, no OCR. Partial results retain successful segments. |
| ExtractionSegment | import_id, stable segment_id, source locator (PDF page or DOCX paragraph/table/cell path), order, raw text, warnings. | Preserve sequence; identify unhandled sections rather than completing them with generated text. |
| Claim | owner, nature (`work`, `education`, `learning_project`, `interest`), current_revision_id. | Interests and personal learning cannot be relabelled as employment by inference. |
| ClaimRevision | claim_id, text, applicable_start/end with precision, source references/segment spans, factual fields, `confirmation` (`pending`, `confirmed`, `rejected`), confirmation actor/time, predecessor. | Any imported/generated claim starts pending. Editing creates a revision; direct user edit-and-confirm is one explicit command. Valid dates/numbers or explicit unknown. |
| ClaimConflict | involved claim/revision IDs, disputed fields, source IDs, resolution_id nullable. | No automatic winning source. Related current facts remain ineligible until explicit selection/merge/rejection. |
| PreferencesRevision | industries, work_contents, interests, safe_choices, stable ordered favorites. | Preference is not evidence of skill. Favorites can include high-gap directions. |

A claim is a current factual input only if its exact revision is current, confirmed, owned, not deleted and not involved in an unresolved conflict. A prior confirmed revision does not stay eligible after the current claim changes.

## Targets, Sources, and Assessments

| Entity | Principal fields/relationships | Validation/lifecycle |
| --- | --- | --- |
| CareerDirection | catalog_version, stable direction_id, domain, title, typical work, skill_requirements, knowledge_topics. | At least three directions in each of automotive, embodied/robotics and AI; catalog facts are general guidance, not personal history or vacancies. |
| SearchRequest | owner, preview_id, approved_request_hash, exact external fields, local filters, created_at, processing status. | Changed external fields require a new preview; no full claim/resume/audio fields. |
| SourceFetch | search_id, source_key, started/completed_at, status, response hash, error_code, returned_count. | `succeeded`, `empty`, `failed`; local no-match separate from source-empty. Store errors without credentials/content. |
| JobObservation | source_key/posting_id/internal_job_id, fetch_id, employer/title/location strings, offices, original_url, first_published/updated nullable, collected_at, description/source_id, status. | New observation on meaningful change; exact repeats can link existing content while retaining collection occurrence. Exclude prospect/general-interest postings from vacancy results. |
| ListingGroup | id, member observation IDs, identity basis, field variants, mainland match evidence. | Group exact identity/content matches for display; preserve all source records. Similar titles alone never prove identity. Conflicting fields remain alternatives. |
| Target | id, kind (`direction`, `listing`, `manual_jd`), direction/listing/source reference, current_revision_id. | Exactly one kind; selecting a listing captures the chosen observation and visible variants, not a silent blended JD. Manual JD has no location restriction. |
| TargetRevision | source text/version, title, extracted requirements, source/date metadata, confirmed requirement IDs. | Each requirement has pending/confirmed/rejected status and source span. Only confirmed requirements drive adopted resume/plan facts. |
| AssessmentRevision | target/direction, preferences_revision, input claim revision IDs, matched evidence, gaps, unknowns, suggested_stage, rationale. | Stage enum `apply_now`, `short_preparation`, `long_exploration`; insufficient evidence explicitly shown. No guaranteed match score or auto-application. |

For two-source acceptance fixtures, known shared posting identity or exact content/employer/location equality can group records. Conflicting observations for a known identity are retained in the same display group with variants; uncertain identity is displayed separately with a possible-duplicate notice. No fuzzy automatic merge is required.

## Resume and Preparation

| Entity | Fields/relationships | Validation/lifecycle |
| --- | --- | --- |
| ResumeSuggestion | target_revision, original text, proposed ordered clauses, requirement references, claim-revision references per factual clause, explanation, decision. | `proposed → accepted/rejected`; unsupported fact means `blocked` and cannot be accepted. Acceptance is explicit clause-level factual review. |
| Resume / ResumeRevision | target_id, ordered sections/clauses, accepted suggestion IDs, evidence references, creation provenance, restored_from nullable. | Save/restore appends a revision and rechecks evidence. Original source file and other target resumes remain unchanged. |
| PreparationPlan / PlanRevision | target_revision, resume_revision nullable, interview_date nullable, horizon_start/end, timezone, default_horizon flag, weekly_minutes, task references, dependency refs. | Missing interview date gives one calendar month, clamped month-end; user can change it. Insufficient budget produces a visible shortfall, not fabricated feasibility. |
| PreparationTask | plan_id, category (`role_knowledge`, `resume_followup`, `external_question`), title, reason, reference sources, estimate_minutes, completion_criterion, dependencies. | Explicit source or unknown/generated status; positive bounded estimate; no implied external source if none exists. |
| TaskProgress | task_id, state (`todo`, `in_progress`, `completed`), completion evidence/time, mutation_id. | Completed record survives reranking and conflicts. Reopening is an explicit user command preserving prior completion history. |
| TaskOrderRevision | unfinished task IDs, rank reasons, manual override positions, triggered_by review/completion/user. | Unique task membership; deterministic tie-breaks; automatic reranking respects explicit user overrides until cleared. Completed items excluded from remaining-order replacement. |

## Materials, Interviews, and Recordings

| Entity | Fields/relationships | Validation/lifecycle |
| --- | --- | --- |
| LearningMaterial | owner, type question/reference, current_revision_id. | Stable material identity; content and quality edits append a MaterialRevision. Duplicate notice never discards provenance. |
| MaterialRevision | material_id, source_id, original prompt/content, answer variants, role/topic tags, exact fingerprint, quality flags, predecessor. | Source type/address/known time explicit; `missing_answer_source`, `conflicting_answers`, `user_doubt` independently representable. Interviews and dependencies bind this exact immutable revision. |
| InterviewSession | target_revision, eligible resume/claim refs, mode (`coach`, `real`), selected material refs, state, before/after self-rating nullable, rubric version. | `ready → active → ended → review_pending → reviewed`; `interrupted` is resumable saved state. Source/claim changes add review requirements; frozen context remains visible history. |
| InterviewTurn | session_id, sequence, question text/source or generated rationale, parent_turn_id for follow-up, submission_id nullable. | Unique session/sequence; complete session uses at least one applicable sourced external question if available. Availability/quota failure cannot be labelled complete. |
| AnswerRevision | turn_id, original transcript/text, revised text, source (`typed`, `transcribed`, `user_corrected`, `reanswered`), recording_id nullable, submitted_at, confirmation actor/time, previous revision. | Only submitted answers can trigger follow-up; review uses final confirmed revision. Re-answer keeps prior history. No confirmed answer means review cannot evaluate it. |
| HintEvent | turn_id, requested_at, level (`understand`, `structure`, `knowledge`), content, operation_id. | Coach only while active, explicit requests, sequential escalation. Real-mode pre-end requests fail server-side. |
| Recording | session/turn, reserved_at, capture_started_at metadata, immutable created_at=reservation time, expires_at, MIME, bytes/hash, private key, keep choice, retention policy, lifecycle state. | Reservation immediately before capture conservatively starts lifetime no later than capture. `reserved → uploaded → deletion_pending → deleted`; processing tracked separately. Explicit kept state is policy, not resurrection. |
| ProcessingJob | fixed kind, input refs, input hash, consent version, owner/deletion generation, created_at, state, attempt count, lease_until, result ref, safe error. | `queued → running → succeeded/failed/blocked/stale/cancelled`; lease expiry permits bounded retry, never fresh audio expiry. Unique operation key; no sensitive payloads in job logs. |

Recording processing status references final transcript and review completion separately. Temporary deletion trigger is the earliest of user deletion, `created_at + 24 hours`, or both text-and-review completion. After a terminal trigger, keep/upload/read/dispatch commands fail; deletion failure is visible, access stays revoked, cleanup retries. Retained recordings have no temporary TTL but remain user-deletable. Local browser audio is not persistent recovery storage.

## Reviews and Personal Methods

| Entity | Fields/relationships | Validation/lifecycle |
| --- | --- | --- |
| Review / ReviewRevision | session, exact confirmed answer IDs, claim dependencies, four feedback dimensions, answer spans, unknowns, zero-to-three priorities, one-or-more retest questions, self-ratings. | Dimensions: knowledge, answer structure, experience evidence, unfamiliar-question handling. Complete feedback must cite answer evidence. No evidence produces `insufficient_evidence`, not fabricated assessment. |
| PersonalMethod / MethodRevision | scenario, steps, user example refs, common mistakes, practice instructions, originating review, state. | `draft → eligible_for_confirmation → formal`; latter requires a completed retest on this revision plus explicit user confirmation. |
| MethodVerification | method_revision, session/turn/retest refs, outcome evidence, user confirmation/time. | Practice results do not promote automatically. Editing a formal method creates a new draft; previous version remains historical. |
| MethodStatusEvent | method/revision, action (`withdraw`, `reverify`, `confirm`), actor/time. | Withdrawal removes current formal use without deleting history; privacy deletion can remove history. Changed/invalid evidence adds needs-review and prevents current reuse. |

## Dependency Validity and Corrections

`EvidenceReference` maps a concrete artifact revision and content-unit ID to exact claim/target/answer/material revisions. Use explicit constrained artifact kinds; never accept arbitrary entity type strings. Index reverse claim lookups for invalidation. `ReviewRequirement` records affected revision/unit, changed dependency, reason and discovered_at; it is separate from the saved content payload.

1. Change/reject/conflict a claim: append the claim revision/event and all direct/transitive impact annotations in the same transaction; invalidate dependent assessments/resumes/plans/reviews and methods using those outputs.
2. Recheck dependency closure at use, restore, export and job publication, including deleted and conflicted sources. Unaffected content and completed work remain retained.
3. Acknowledging a warning does not clear it. A new corrected/regenerated version must use current confirmed facts; the owner reviews the affected clauses. Historical revisions retain their impact annotations.
4. Correcting an answer after a review creates a new answer revision and marks the saved review/methods dependent on it for review; no silent historical rewrite.
5. Correcting material question/answer content, or marking its answer unreliable, creates a MaterialRevision and marks dependent feedback/method content for review. Saved question and answer snapshots remain unchanged. A label-only topic edit does not invalidate substantive feedback, but retains its revision provenance. New question selection uses the latest eligible revision and displays unresolved quality flags.

## Concurrency, Processing Choice, and Privacy

| Entity | Fields/relationships | Validation/lifecycle |
| --- | --- | --- |
| MutationReceipt | owner, mutation_id, request hash, outcome, resource revision/conflict ID. | Same key+same payload returns prior result; different payload is `idempotency_mismatch`. Keep content-free receipts/tombstones through client reconciliation. |
| EditConflict | aggregate, base/current/proposed revisions, changed fields, both device IDs/timestamps, state, resolution_revision. | Persist both accepted candidates; no unique current factual result while conflicted. Resolve against expected conflict revision; another intervening change returns a new conflict. |
| ChangeEntry | monotonic cursor, resource ID/type, revision, event (`updated`, `conflicted`, `deleted`), server time. | Same transaction as mutation; contains no duplicated sensitive text. Old cursor can require full refetch. |
| ProcessingChoice | provider/config version, purpose, data categories, disclosure version, choice, decided_at. | Unknown/denied/revoked blocks sending. Scope/provider change requires a new choice. Consent is rechecked before retries, not just at job creation. |
| RetentionPolicy | category, mode (`until_deleted`, `days`), days nullable, effective_at. | Text/review defaults until_deleted; shortening requires affected-data preview. Temporary audio hard maximum cannot be extended. Imported files, resumes and methods remain visible until deletion unless configured otherwise. |
| DeletionRequest | scope IDs/categories, requested_at, deletion generation, dependent-impact preview, state, failed-copy list. | `pending → running → complete/failed`; completion requires all registered copies removed, tombstones published and late output disabled. |
| StoredCopy | kind (`original`, `audio`, `transcode_temp`, `export`, `backup`), private location, content references, created_at, expires_at nullable, deletion state. | Enumerate product-controlled copies; no temporary audio in export/backups; export expiry and backup retention visible. |
| ExportJob | selected scope/policy, manifest version, snapshot cursor, private archive ref, created/expires_at, state. | Snapshot is consistent; contains retention/review flags, checksums and selected kept recordings. The downloaded copy is user-controlled and cannot be remotely erased. |

Deletion of a source/claim preserves permitted dependent content only with `evidence_unavailable`/needs-review marking; it must not silently retain deleted source text in a supposedly content-free reference. Show copied personal text in a deletion impact preview so the user can include dependent artifacts. Delete-all purges all such payloads and registered copies. On reconnect, deletion tombstones invalidate stale edits and remove displayed/cache copies; first release keeps no persistent browser personal-data cache. A disconnected screen cannot be remotely erased, so no claim of instantaneous removal from an offline device.
