# Interaction and Lifecycle Contract

**Authority**: [spec](../spec.md) decides behavior; [prototype index](../prototype.md) and [UX addendum](../ux-addendum.md) guide UX. Figma retrieval was quota-blocked, so exact visual parity is not verified. This contract does not add OCR, public accounts, automatic external question collection, real-time interruption or full mobile resume editing.

## Screen and Device Boundaries

| Flow / prototype reference | Desktop behavior | Phone boundary |
| --- | --- | --- |
| 01 Experience review | PDF/DOCX select, source/partial diagnostics, pending facts, conflict decisions, manual entry. | Existing context may be read for practice; complete import/edit workflow is desktop-first. |
| 02 Directions | Three domains; evidence/gaps/unknowns/stage, filters/favorites; high gaps remain. | No promised full exploration UI. |
| 02A Listings / 12A states | Query preview, deliberate fetch, separate real listing results, provenance/variants, target selection and manual JD. | No full search expansion. |
| Resume and preparation | Confirm requirements, compare/accept/reject proposals, save/restore, calendar/budget/task order. | Display selected target and current practice task. |
| Coach / real practice | Start/Done, question text/audio, hints by mode, text fallback, corrections, saved status. | Primary mobile workflow, touch targets and microphone support. |
| Review / methods | Four dimensions, answer links, next priorities/retest; draft/verify/edit/withdraw methods. | Short review and next practice; full editing remains desktop-first. |
| Data/privacy/conflict | Processing choices, recording status, export/delete and explicit version resolution. | Show applicable processing/recording controls and conflicts; avoid overwriting unresolved data. |

Direction cards are never presented as live vacancies. Demo employers and source A/B from Figma never enter production fixtures as verified live data. Import progress percentage/cancel are not required acceptance commitments. Unknowns, failures and unavailable capabilities use text, not just color.

First-use empty states follow the spec's existing-flow actions: import/manual experience; select a direction/listing/manual target; clear direction filters; generate a plan from a confirmed target; start practice before a review; create a method draft from a review. Keep prerequisite explanations visible and do not generate fake saved content. Source search separately exposes not-started, queued/running, empty, local-no-match, failed and previous-results-only states.

## Manual-Turn Protocol

1. Fetch a saved question and show the selected mode. Playback is local speech when available; question text always exists.
2. Before capture, disclose that unsaved browser audio is memory-only, cannot be recovered after loss, and cannot be guaranteed to clear while the browser/device is suspended. Clicking Start requests a server recording reservation with immutable creation/deadline. After acknowledgement and microphone permission, begin capture in memory. Show “recording; current answer not yet saved.” If reservation/network fails, offer text; do not pretend recording is recoverable.
3. Silence has no transition. Coach hint requests may run without submitting. In real mode the server rejects pre-end hints. OS interruption/track-ended becomes `interrupted_unsaved`, not Done.
4. Clicking Done records an explicit action ID, stops capture, uploads bytes under the reservation, then submits that recording ID. Upload acknowledgement and answer submission are distinct. Repeated clicks/retries reuse IDs; an upload failure does not start the next question.
5. After submission, authorized STT produces editable text and the interviewer may respond/follow up using that submitted provisional answer. Label provisional transcription. The user can correct/re-answer before review; corrected meaning can prompt an explicitly requested replacement follow-up while retaining earlier history. Do not claim earlier questions were generated from corrected text.
6. End the session deliberately. Confirm final answer revisions before creating a review. Skipped/unconfirmed turns remain visible and are excluded from assessed evidence; absence of evaluable evidence produces an explicit inability to assess.
7. Save checkpoints after each accepted command. A reopened session shows acknowledged questions, submitted text and unexpired stored recordings. Lost memory audio, deleted recordings or never-saved answers are never reconstructed.

No voice activity detection, silence timeout, automatic answer submission or realtime barge-in. A user can stop/retry or switch to text; limits/errors never submit automatically. Show which portion is saved and which must be re-entered.

## Corrections, Conflicts, and Sync

Poll resource changes every 10 seconds while visible, and immediately on focus/reconnect. Apply updates only to clean views; an unsaved draft retains its base revision and receives an update/conflict notice. First release keeps draft text only in page memory; an open tab may edit through a brief network interruption, but closed-tab offline editing is not promised.

On concurrent overlapping edits, preserve base/current/proposed versions and both device/timestamp labels. Let the owner select or manually merge, then submit a resolution against the current conflict revision. No silent latest-timestamp winner. Non-overlapping scalar changes can merge only by the documented three-way rule; task completion and answer history are independent records, not replaceable arrays.

Correcting/rejecting a used fact flags affected resume/plan/review/method content and prevents current reuse. Show impact reasons and a user-initiated correction/regeneration action. Dismissing a notice, restoring a resume, exporting a history item or retrying an old job cannot clear the guard. Keep unaffected content and completed work.

## Recording Retention

- The immutable reservation time precedes capture and conservatively bounds all accepted audio. `expires_at = created_at + 24 hours`. Show whether audio is temporary, explicitly kept, unavailable, pending deletion, failed deletion or deleted, with actual expiry.
- Temporary audio stored by the server or external processing provider is physically purged when confirmed text and its review complete, or by expiry, whichever comes first; interrupted/failed jobs cannot extend it. User delete can trigger earlier removal. Keep is accepted only before the terminal deletion trigger and while bytes exist. Unsaved browser buffers follow the separately approved rule below.
- Check deadline on upload, playback, download, keep, STT dispatch and retry. An expired object returns 410 even if physical cleanup is still failing. Report physical deletion separately and retry failures; never show expired data as recoverable.
- Independent supervised cleanup uses deadline scheduling and periodic reconciliation; it cannot wait behind inference. Include upload staging, transcoding, exports, registered backups and any provider copy in lifecycle accounting. Temporary audio is excluded from backups/exports by design.
- The deployment must prove physical cleanup under worker/web crashes and monitor overdue deletion. A stopped host or uncooperative provider cannot satisfy strict deletion by an application flag alone; this remains a deployment qualification failure. Startup purges overdue remnants before serving private data.
- Browser audio uses no persistent cache; discard buffers/URLs after upload acknowledgement, cancellation or page teardown. Also enforce a client expiry transition at the reservation deadline: stop capture, discard buffers/object URLs, disable playback/retry/upload and show expired status. Check on an active timer, before every audio action and immediately on visibility/resume; upload failure does not extend it. The owner's 2026-09-25 decision in spec FR-027 explicitly excludes a guarantee of memory clearing while the browser/device is suspended. Disclose this limit before capture. On resume, expired buffers must be cleared before any audio action, and unsaved buffers must never be presented as recoverable stored records. Real-device qualification must verify active cleanup, acknowledgement/cancellation cleanup, expiry-before-action on resume, no persistent cache and the disclosure; it must not claim proof of physical deletion during suspension. This boundary does not relax server/provider deletion deadlines.

Text and reviews default to until-user-deletion, independently of audio. Expose category policy settings and impact preview when shortening retention. Explicit retained audio follows its chosen policy; deleting audio does not implicitly delete the text/review.

## Export and Deletion

Export a consistent snapshot to an owner-only ZIP with `manifest.json` (`format=career-helper-export`, `version=1`, snapshot cursor, selected categories, policy/review states and checksums), UTF-8 structured records and retained original files/audio. Include imported resume files, confirmed and selected historical claims, resume versions, plans, text answers, reviews and methods. Preserve source/version links and unknown/conflict/review flags. No temporary audio or hidden credentials.

Generated exports are temporary product-controlled copies, expiring after one hour by default and included in deletion inventory. Owner-downloaded archives are outside product control; state that plainly. Backups require documented retention and selective purge or retirement on deletion; first release must not make untracked copies.

Deletion preview shows selected items, registered copies and dependent material containing copied personal text. Delete-all includes those derivatives. Accepted deletion revokes access immediately, cancels/stales related jobs, removes copies, publishes content-free tombstones and reconciles stale clients. Only mark complete when removal is verified. Retained dependants after selective source deletion receive evidence-unavailable flags and cannot reuse removed facts. Offline screens clear on reconnect; no claim of remotely erasing a disconnected display or user-downloaded file.

## Accessibility and Evidence

Use native labels/buttons, visible focus, keyboard-operable import/query/source expansion, meaningful link names, and non-color status text. Async updates use polite live status without stealing focus; errors place focus at an error summary with links to controls. Recorder Start/Done, hint level and saved status must be announced and usable on touch/keyboard. Text alternatives cover speech failure.

Before UI acceptance, compare actual screens with accessible Figma frames and log any conflict against the specification. Browser emulation does not prove actual microphone or screen-reader behavior. Real desktop/phone sessions and keyboard/focus/status checks are required validation evidence.
