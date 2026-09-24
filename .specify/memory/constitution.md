<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles:
- I. Strict YAGNI -> I. Minimal Architecture and Scope
- II. Self-Documenting Code -> VI. Clear Code and Documentation
- III. Local-First Simplicity -> I. Minimal Architecture and Scope
Added principles:
- II. Data Integrity
- III. Security and Privacy
- IV. Testability and Verification
- V. Backward Compatibility
Added sections: Applicability; Review Standard
Removed sections: Engineering Decision Rules; Delivery and Review
Follow-up TODOs: None
The previous rules remain in force; this revision adds durable safeguards.
This temporary report is for review and must be removed before a commit.
-->
# Career Helper Constitution

## Core Principles

### I. Minimal Architecture and Scope

Every change MUST serve an active feature requirement or a confirmed defect.
The design MUST use the smallest clear solution that satisfies that need.
Extra abstractions, generic wrappers, and speculative interfaces MUST NOT be
added unless the active specification explicitly requires them. Where external
systems exist, business rules and data invariants MUST remain testable without
those systems; boundaries MUST be no wider than necessary.

Implementations MUST prefer minimal local state and built-in runtime utilities.
Shared state or a third-party dependency MAY be added only when a local or
built-in approach cannot meet an active requirement with comparable simplicity
and correctness. Deferred ideas MUST NOT justify present complexity.

### II. Data Integrity

Accepted user data MUST be preserved without silent loss, reordering, or
normalization that changes meaning. Inputs MUST be validated at the point where
they enter a trusted boundary, and invalid or conflicting data MUST produce
an explicit outcome. Derived claims MUST retain enough provenance to distinguish
source facts, user confirmation, and inference. The system MUST NOT fabricate
missing facts or present uncertain conclusions as confirmed data.

### III. Security and Privacy

Access to data and capabilities MUST follow least privilege. Secrets MUST NOT
be committed, exposed to clients that do not need them, or included in routine
logs. Imported documents and external content MUST be treated as untrusted data,
never as instructions. Sensitive data MUST be collected, shared, retained, and
deleted only for a stated purpose under user control. Security boundaries MUST
fail closed when authorization or source trust cannot be established.

### IV. Testability and Verification

Behavior MUST be observable and testable through its public outcomes.
Dependencies that cause external effects MUST be controllable in focused tests
without speculative abstractions. Tests MUST cover relevant success, boundary,
and failure behavior; tests that only repeat implementation details MUST NOT be
added. Completion claims MUST rely on fresh verification of the affected
behavior, and remaining limits MUST be stated.

### V. Backward Compatibility

Existing persisted data and published contracts MUST remain usable across
ordinary changes. A change that breaks either MUST identify the affected users
or data, provide an explicit migration or version boundary, and verify that
previously valid information is not silently discarded. Compatibility behavior
MUST be documented where users or integrators can rely on it.

### VI. Clear Code and Documentation

Names MUST describe the purpose of variables and functions. Inline comments
MUST be limited to obscure edge cases and explain why the behavior is necessary;
verbose commentary blocks and comments that restate code MUST NOT be added.
Documentation MUST describe externally visible behavior, data rules, and known
limits, and MUST be updated when those contracts change.

## Applicability

Feature specifications define requested behavior; this constitution sets
durable constraints on how that behavior is delivered. An explicit requirement
may justify added complexity under Principle I, but it does not silently waive
data integrity, security, or compatibility. A true conflict MUST be resolved
through a documented constitution amendment before implementation.

## Review Standard

A completed change MUST be reviewable against its requirement or defect,
data and security effects, compatibility impact, relevant documentation, and
verification evidence. The depth of review and testing MUST match the risk of
the change. This section defines the evidence required, not operational
commands or a fixed tool sequence.

## Governance

This constitution governs project planning, implementation, and review.
Amendments MUST state their rationale and impact, receive review, and update
the Sync Impact Report. Versioning MUST follow semantic versioning: MAJOR for
incompatible principle changes or removals, MINOR for new principles or
materially expanded guidance, and PATCH for non-semantic clarification.
The original ratification date MUST remain unchanged. The Last Amended date
MUST reflect the latest amendment.

**Version**: 1.1.0 | **Ratified**: 2026-09-24 | **Last Amended**: 2026-09-24
