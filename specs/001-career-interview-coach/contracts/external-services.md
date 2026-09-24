# External Service and File Contracts

**Parent**: [plan](../plan.md) | **Evidence**: [research](../research.md). These are narrow callable boundaries, not a provider framework or implementation.

## Common Boundary

All calls originate in server application jobs, after owner authorization and relevant processing choice. Inject only the concrete effect callable, clock and ID source for tests. No model can execute tools, choose arbitrary hosts or grant consent. Credentials remain server-side; imported text is escaped data and never instructions. Defaults use synthetic fixtures with external network denied.

Outcomes use a closed shape: `success(result, provenance)`, `unavailable(reason)`, `invalid_input(fields)`, `failed(code, retryable)`, or `stale_inputs(refs)`. Persist safe metadata, not raw prompts/audio/tokens in routine logs. Bounded reads, response size, connect/total timeout, redirect checks and one transient retry apply. Never disable TLS verification. Only configured HTTPS hosts are eligible; redirects must remain within the adapter's approved origin set. Document-provided URLs are stored as links, not fetched automatically.

## Document Extraction

`extract_resume(import_id, detected_type, private_file_handle, limits) → ExtractionResult`

- Input is an already authorized local PDF/DOCX handle, never an arbitrary path or URL. Filename extension alone is insufficient; validate magic/container structure.
- Initial operational limits: 10 MiB original upload, 100 PDF pages, 50 MiB total expanded DOCX entries, 1 MiB extracted text, 30-second subprocess deadline, 512 MiB process memory. These are explicit adjustable operational limits, not promises about all valid documents; show an actionable limit message and manual-entry path. Never truncate silently.
- Result: status complete/partial/unreadable, ordered `{segment_id, locator, text}` items, diagnostics and skipped/unsupported areas. Extraction cannot confirm facts, preserve original layout perfectly or invent missing text.
- Reject path traversal, unsafe ZIP entry names, external resource loads, macros, compressed bombs, parser hangs and invalid types. Kill/reap timed-out subprocesses and purge temporary material. Original upload follows its explicit retention policy.
- PDF pages with no extractable text and DOCX tracked/unsupported structures receive precise diagnostics. Preserve successfully extracted content; compare source order in fixtures.

## Job Acquisition: `greenhouse:canonical`

`fetch_published_jobs(approved_request, deadline) → SourceFetchResult`

**Fixed request**: GET `https://boards-api.greenhouse.io/v1/boards/canonical/jobs?content=true`. Optional recheck: documented `/v1/boards/canonical/jobs/{posting_id}`. No authenticated application POST, arbitrary board names, scraping fallback or background crawl. Preview exposes host, board and options; local interests/keywords remain inside the app. The UI can adjust local filters or cancel; any future external-query field requires an updated preview/hash.

**Permission scope**: The [Canonical personal-use terms](https://canonical.com/legal/terms) and [public API documentation](https://docs.greenhouse.io/job-board.html) support the private personal-use interpretation in research. Retain source wording/notices and attribution. No public/commercial redistribution or model-training rights are claimed. In-app source snapshots and separate local assessments stay owner-only; sending third-party full descriptions to an external model requires checking that processing use separately and is disabled by default. Confirmed user-entered requirement labels can drive tailoring without transmitting the source description.

**Mapping**:

| API field | Stored meaning |
| --- | --- |
| `id` plus configured board | Unique source posting key. |
| `internal_job_id` | Related source identity; null denotes a prospect/general-interest post, excluded from vacancy results. |
| `title`, `company_name` | Original title/employer strings; unknown when absent. |
| `location.name`, `offices` | Verbatim locations plus a separate explicit mainland-workplace match. |
| `absolute_url` | Original application/source link, displayed safely. |
| `first_published`, `updated_at` | Nullable source dates; never substituted with collection time. |
| server clock | `collected_at`, the observation time. |
| `content` | Untrusted original description; retain private snapshot/notices and display safe plain text. |

Require an explicit mainland work location. Beijing or Shanghai qualifies; “Worldwide”, “APAC”, nationality or remote eligibility alone does not. Preserve all listed alternatives, including non-mainland locations on a multi-location posting. Do not exclude an international employer. Compare exact posting IDs or exact employer/title/location/content keys; uncertain similarities remain separate. Preserve all source observations and conflicting fields; never overwrite one with a preferred version.

**Status**: valid nonempty result=`success`; valid empty list=`source_empty`; locally no matching jobs=`no_matches`; HTTP/network/malformed response=`source_failed`; recheck 404=`detail_unavailable`; link failure=`link_unavailable`. Keep prior observations with original timestamps during failure. Published-list presence means observed at collection, not guaranteed current recruitment.

**Operational policy**: one in-flight fetch, at least 30 seconds between user refreshes, 20-second request deadline, 10 MiB maximum response, one transient retry only if within remaining budget, honor Retry-After. These are local limits, not claimed Greenhouse quotas. No result means no fabricated listings. Source terms/access/coverage are rechecked before live enablement and when errors or permission changes appear.

## Structured Coaching

`generate_result(operation, input_snapshot, processing_grant, configured_model) → ValidatedProposal`

Finite operation enum:

| Operation | Minimum inputs | Required output validation |
| --- | --- | --- |
| claim_candidates | Authorized extraction segments | Candidate text/source spans/nature; confirmation always pending. Manual candidate entry remains available without a provider. |
| role_assessment | Direction requirements, interests, eligible claim refs | Evidence IDs, gaps, unknowns, allowed preparation stage and explanation. Catalog/rule assessment remains usable without AI. |
| resume_suggestions | Confirmed requirement labels, current claim refs, existing selected text | Original/proposed clauses, requirement/evidence per factual clause, edit rationale; unsupported factual additions blocked. |
| preparation_tasks | Target requirements, eligible resume context, time budget | Task category/reason/source/estimate/criterion; deterministic scheduler assigns order/time. |
| generated_question | Target/focus/eligible context | Question text, generated label, role/evidence rationale. Never masquerades as an external question. |
| followup | Submitted answer revision, parent question and target context | Context-related follow-up and parent answer ref; unavailable before submission. |
| requested_hint | Coach mode, explicit requested level, current question | Exactly requested level, no unsolicited promotion or answer submission. |
| review | Final confirmed answers, questions/hints and eligible context | Four dimensions, answer-span citations, unknowns, at most three priorities, at least one retest. |
| method_draft | Review evidence and retest proposal | Scenario/steps/user example/common mistakes/practice method; draft state only. |

Each request includes the minimum relevant immutable content, provenance IDs and a bounded output schema. Runtime parsing rejects missing fields, unknown enum values, unresolvable citations, oversized content and tool/action instructions. Imported instructions cannot alter prompts, allowed operations, data scope or provider. Raw source HTML never reaches executable UI.

**Factual support**: Citation validity is necessary but insufficient. Clauses remain proposals until the owner reviews their actual meaning against confirmed facts. New dates, quantities, employers, responsibilities or achievements first become independent pending claims and cannot enter an adoptable resume. Reject unsupported numeric/entity changes rather than treating an AI-written citation as proof.

**Offline behavior**: File extraction/manual entry, catalog/filtering, saved content, deterministic scheduling of known tasks and imported questions remain available. A capability requiring generation reports unavailable if no qualified/granted configuration exists; fixtures are visible test mode, never a production substitute.

## Speech Input and Output

`transcribe(recording_id, actual_mime, language, permitted_glossary, grant, deadline) → {text, optional_segments, provider_metadata}`

Resolve bytes through the authorized recording store, not a public URL. Check retained/unexpired state, explicit submission and STT grant immediately before sending. The glossary can contain only approved relevant terms. Transcript is provisional; allow correction/re-answer and require final confirmation for review. Ignore any provider emotion/psychological inference fields. An empty or failed transcription does not fabricate an answer.

Browser capture uses MediaRecorder format negotiation; the chosen STT configuration must accept actual WebM/Opus and MP4/AAC emitted by supported devices, or justify one bounded transcoder with equally controlled temporary files. Do not split arbitrary recorder bytes into assumed independent audio files. Upload bound starts at 64 MiB per answer and is disclosed before capture; hitting it interrupts without submission and offers retry/text. Ten-minute session acceptance is not a per-answer limit.

Question playback uses a user-selected local browser speech voice (`localService=true`) with text/replay controls. No remote browser SpeechRecognition or undisclosed remote voice. If local playback fails, text remains. Any required remote TTS is a separately scoped, qualified capability with explicit data choice; it does not receive recordings or unrelated profile data.

## Live Training Qualification Gate

Before W4 live coaching acceptance and W5 live STT acceptance, respectively, record one concrete configuration per required capability with all of:

1. Provider/service and model/version, allowlisted endpoint, supported region/account, and credentials supplied securely by the owner during configuration. No key is requested or consumed in this planning task.
2. Current primary documentation/terms for intended personal-data processing; disclosed data categories/purpose; no unreviewed automatic fallback or training use.
3. Storage, logs, backups and subprocessors relevant to recording copies. Evidence that temporary audio can be deleted at the required earlier trigger and at most 24 hours; a generic no-training statement is insufficient. If not possible, reject the STT configuration under this spec.
4. Real synthetic Chinese/English-term audio and structured-output qualification, actual browser MIME compatibility, bounded timeout/retry and error mapping. A successful text fixture does not qualify speech.
5. Exact processing disclosure persisted in ProcessingChoice; refusal/revocation tested with a request recorder proving zero further personal-data sends. A new provider or expanded scope needs new choice.
6. No hidden transmission of full source job descriptions where their processing rights have not been established; use user-confirmed requirement labels instead.

There is no qualified live generation/STT service at planning time. Interface design and offline implementation can proceed after plan approval; the first usable release cannot pass with this gate unmet. Hosting, model pricing and regional availability are verified when selecting the concrete deployment, not guessed here.
