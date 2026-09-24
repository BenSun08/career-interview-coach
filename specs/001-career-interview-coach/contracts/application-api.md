# Application Interface Contract v1

**Status**: Phase 1 design, not an implemented API. **References**: [data model](../data-model.md), [lifecycle](./interaction-lifecycle.md), [external effects](./external-services.md).

## Transport, Identity, and Mutation Envelope

Same-origin HTTPS. Server-rendered forms and JSON endpoints call the same application functions; a form submission cannot bypass JSON validation or vice versa. All routes except login/static assets/minimal liveness require the configured active owner. JSON returns 401 when unauthenticated and 403 for a different authenticated account; private HTML redirects to login without leaking payloads. No public signup/admin/invite routes. Media, export and operation status require identical authorization.

Django session cookie is Secure, HttpOnly, SameSite=Lax, backed by the server. Every state-changing request requires CSRF and allowed Origin/Host checks. Logout is POST. Set private responses to `Cache-Control: no-store`; no service-worker personal-data cache. Rate-limit login attempts with generic errors and bounded lockout/retry information. Production requires DEBUG off and deployment checks.

- JSON fields use snake_case; IDs are opaque strings, timestamps ISO-8601 with explicit offsets; unknown values are null, displayed as unknown.
- Every command carries `mutation_id` and `device_id`; edits also carry `base_revision_id`. Device IDs are issued/registered within the authenticated owner session and never grant access.
- User-supplied timestamps remain metadata. Server timestamps govern record creation, retention and ordering.
- For synchronous writes, return `resource_id`, `revision_id`, `change_cursor`, and `outcome`. Creates use 201, updates 200, accepted durable work 202 with `operation_id`/status URL.
- Replaying the same mutation and payload returns the saved result without repeating an effect. Same key with a different payload returns 409 `idempotency_mismatch`.
- Invalid payloads have 422 plus field errors. Missing IDs are 404; private object lookup never exposes another owner. 410 identifies expired/deleted resources. 409 identifies revision conflict or stale evidence. 428 identifies missing base revision. 429 includes retry guidance. 503 means an unavailable dependency, never a fabricated successful result.
- Error body: `error.code`, safe `message`, `field_errors`, `retryable`, `operation_id` nullable, and `conflict_id` nullable. Do not include prompts, secrets, file paths or raw provider responses.

### Conflict response

On an overlapping stale edit, validate and persist the incoming candidate before returning 409 `edit_conflict`. Response includes conflict ID, base/current/proposed revision IDs, device labels and trusted receipt times, and differing fields. Fetch details only after owner authorization. Neither conflicting fact is eligible as a unique current generation input until explicit resolution. Non-overlapping scalar edits may merge from the common base; merge never deletes completed task/answer records.

## Endpoint Catalogue

Path IDs refer to entities in the data model. All POST/PATCH/DELETE commands use the mutation envelope; expected revision applies wherever a mutable aggregate exists. List GETs use stable cursor pagination, preserving recorded item order. `limit` defaults 50 and caps at 100; malformed cursors fail explicitly.

| Method/path | Input | Public outcome / rule |
| --- | --- | --- |
| POST `/login/`; POST `/logout/` | Django login/CSRF; logout token | Owner session or generic failure; no second-user access. |
| GET `/api/v1/session` | none | Owner display name, device, capability availability, CSRF bootstrap; no provider secret. |
| GET `/api/v1/changes?after=cursor` | last cursor | Ordered changed/conflicted/deleted resource IDs plus next cursor; expired cursor requires full refetch. |
| GET `/api/v1/operations/{id}` | none | queued/running/succeeded/failed/blocked/stale/cancelled, safe reason and result references. |
| POST `/api/v1/resume-imports` | multipart PDF/DOCX, original filename, mutation_id | Bounded upload and extraction job; 202. File type/size failure explicit. |
| GET `/api/v1/resume-imports/{id}` | none | Source, segments, partial/unreadable diagnostics, pending claim candidates. |
| GET/POST `/api/v1/claims` | query or manual text/nature/time/source | Ordered claim summaries or new pending/user-explicitly-confirmed manual claim. |
| POST `/api/v1/claims/{id}/decisions` | base revision, action confirm/reject/edit, revised content when editing | New claim revision and affected artifact IDs; invalidate dependencies atomically. |
| GET/PATCH `/api/v1/preferences` | base revision, explicit changed preference fields | Revisioned preferences and favorites; no skill confirmation. |
| GET `/api/v1/directions` | industry/interest/work/stage filters | Catalog plus assessments/unknowns; high-gap entries not silently removed. |
| POST `/api/v1/assessments` | direction/target ID, eligible claim/preference revisions | Bounded assessment operation; no auto-application. |
| POST `/api/v1/job-search-previews` | editable local filters; enabled source | Server-built exact outbound request and hash; explains local-only fields. |
| POST `/api/v1/job-searches` | preview_id, accepted request hash | User-initiated acquisition, 202. Changed/stale external request needs new preview. |
| GET `/api/v1/job-searches/{id}` | none | source status, local match status, listing groups, provenance and variants. |
| GET `/api/v1/listings/{id}` | none | All observations, differing fields, source dates/links, observed availability. |
| POST `/api/v1/listings/{id}/recheck` | selected source observation | Bounded source detail check; failure does not rewrite saved target. |
| POST `/api/v1/targets` | direction ID OR listing observation ID OR manual JD text/source/time | Exactly one type; preserve source snapshot. Manual location unrestricted. |
| POST `/api/v1/targets/{id}/requirements` | base revision, per-requirement confirm/edit/reject decisions | New target revision; no implicit extraction confirmation. |
| POST `/api/v1/resume-suggestions` | confirmed target and current claim refs | Proposals with original, clauses, evidence, requirement links; unsupported clauses blocked. |
| POST `/api/v1/resume-suggestions/{id}/decision` | accept/reject plus factual review of referenced clauses | Adoption permitted only after semantic review and current evidence check. New facts require separately confirmed claims. |
| POST `/api/v1/resumes` | target, accepted suggestion IDs/ordered sections | Immutable resume revision; rejected suggestions excluded. |
| GET `/api/v1/resumes/{id}/revisions` | pagination | History including current validity and review reasons. |
| POST `/api/v1/resumes/{id}/restore` | base revision, historical revision ID | New revision for this target only; current evidence revalidated, stale flags preserved. |
| POST `/api/v1/plans` | target/resume revisions, date nullable, weekly_minutes, adjustable horizon | At least three actionable tasks where feasible; visible budget/default assumptions; job or saved draft. |
| POST `/api/v1/plans/{id}/reorder` | base revision, unfinished task IDs, manual overrides | New order preserving completed records. |
| POST `/api/v1/tasks/{id}/progress` | base revision, state, completion evidence | Completion event/history preserved; rerank unfinished tasks. |
| GET/POST `/api/v1/materials` | query or manual content/type/source/date/role/topics | Source-aware questions/materials and duplicate/quality flags. No automatic web fetching. |
| POST `/api/v1/materials/{id}/quality` | base revision, doubt/answer-source/conflict decision | Versioned quality change; source variants preserved. |
| POST `/api/v1/interviews` | target/resume, mode, focus, optional pre-rating | Frozen eligible context, selected questions/source availability, session ID. |
| GET `/api/v1/interviews/{id}` | none | Saved questions/answers, current turn, hints, review, last acknowledged progress and expired-audio states. |
| POST `/api/v1/interviews/{id}/recordings` | turn ID | Reservation ID, immutable created_at/expires_at and accepted MIME/size limits; then browser capture may begin. |
| PUT `/api/v1/recordings/{id}/content` | bounded audio body, MIME/hash, mutation_id | Upload acknowledged only after durable private storage; no answer submission. Expired IDs reject bytes. |
| POST `/api/v1/turns/{id}/submit` | explicit Done action ID; uploaded recording ID OR typed text | Idempotent submitted answer; STT if authorized/qualified. No implicit submit endpoint driven by silence. |
| POST `/api/v1/turns/{id}/hints` | requested next level | Coach hint and logged level; real pre-end returns 409 `hint_unavailable_in_mode`. |
| POST `/api/v1/answers/{id}/confirm` | base revision, corrected text or selected re-answer revision | Final confirmed text for review; correction retains history. |
| POST `/api/v1/interviews/{id}/end` | base revision, optional post-rating | End session; display unanswered/unconfirmed gaps and required sourced-question status. |
| POST `/api/v1/interviews/{id}/reviews` | confirmed answer revisions | Evidence-bound review operation or insufficient-evidence outcome. Rechecks changed claims. |
| POST `/api/v1/methods` | review ID, required draft fields | Editable draft only. |
| PATCH `/api/v1/methods/{id}` | base revision, changed draft fields | New draft revision; cannot retain an old revision's verification. |
| POST `/api/v1/methods/{id}/verification` | completed retest reference, explicit user decision | Formal only when this method revision has valid retest and confirmed evidence. |
| POST `/api/v1/methods/{id}/withdraw` | base revision | Removes formal/current use; preserves permissible history. |
| GET/POST `/api/v1/conflicts/{id}/resolution` | GET detail; POST expected conflict revision and chosen/merged content | Explicit new resolution revision; rejects races and keeps both source candidates. |
| GET/POST `/api/v1/processing-choices` | purpose/provider/config/categories/disclosure, grant/deny/revoke | Versioned choice; no outbound work on absent/refused/revoked scope. |
| GET/PATCH `/api/v1/retention` | category policy, expected revision, affected-data confirmation | Defaults and expiry preview; temporary audio cannot exceed hard limit. |
| POST `/api/v1/recordings/{id}/retention` | keep/delete; base revision | Serialized transition; expired/deleting/deleted audio cannot be kept. |
| GET `/api/v1/files/{id}` | none | Owner-only attachment/recording if retained and authorized; 410 when expired/deleted. |
| POST `/api/v1/exports` | selected categories/IDs | Durable versioned archive operation; excludes non-kept audio. |
| GET `/api/v1/exports/{id}/download` | none | Owner-only unexpired archive; no public link. |
| POST `/api/v1/deletion-previews` | scope IDs/categories or all | Copies, dependants and consequences; no deletion yet. |
| POST `/api/v1/deletions` | accepted preview hash, explicit user action | Access revoked, jobs cancelled/staled, registered copies purged, tombstones returned. Completion reflects actual deletion. |

Resource detail/list GETs for targets, plans, tasks, materials, reviews and methods expose their data-model fields, exact revision IDs and current validity, never private storage keys. They apply the same owner/pagination rules. No unrestricted CRUD endpoint can mutate state-machine flags directly.

## Operation Publication and Failure

Jobs contain a fixed operation kind, immutable inputs and current consent. Retry at most once for a transient external error within the total deadline; retry never extends a recording deadline. Provider refusal/format errors and denied consent are terminal/blocked until a new explicit user action or configuration. Worker lease and idempotency prevent double publication; a network service can still receive a repeated request after uncertain transport failure, so never claim exactly-once external execution.

Before publication recheck owner binding, input existence/current validity, consent version, session/turn state and deletion generation. Stale inputs return `stale_inputs` and a review/retry path; the user must initiate regeneration. Requests cannot clear `needs_review` by setting a boolean.
