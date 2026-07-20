# TRUST.md — Decision Record

Decisions that affect the scientific meaning of the convention. Status values:

- **Accepted** — settled for the v0.3 cycle (still reversible before release).
- **Proposed** — recommended by the planning analysis but **requires
  maintainer and/or methodology-contributor sign-off**. Nothing marked
  Proposed is silently decided; the validator and spec text must not assume it
  until accepted.

Context and evidence for all entries: `NEXT_VERSION_PLAN.md`.

---

## D-001 — Numerical vs ordinal assessment

**Status: Proposed.**
Keep the 0–100 integer scale as a valid, backward-compatible encoding, but
make the five **bands/ordinal levels the primary semantic**; the integer is an
optional refinement within a band. Band meanings are rewritten to describe
evidence support only (removing category vocabulary — defect D10), and the
spec states explicitly that the value is **not a probability** and carries
ordinal, not cardinal, information. Rejected alternatives: pure ordinal
replacement (breaking, no structural gain — plan §4 Option B); keeping 0–100
as primary with better prose only (leaves false precision structural — Option
A).

## D-002 — Optional vs mandatory aggregate

**Status: Proposed.**
No aggregate is ever mandatory. `corpus.average_trust` (mean of ordinal
judgements) is **deprecated but valid**; recommended summaries become
`band_distribution` (counts) and `median_band`. Any aggregate a tool displays
must keep the underlying dimensions one interaction away (principle 5). An
aggregate over the new dimensions is permitted only as explicitly
**experimental**, named, and non-default. Open sub-question for methodology
contributors: is `median_band` itself defensible, or should only
distributions be shown?

## D-003 — Supported assessment units

**Status: Proposed.**
Four units: repository declaration (default), artifact/document (`artifacts[]`),
individual claim (inline markup, only *summarised* in the manifest), and
claim–evidence relation (**external records only**, referenced via
`companions.claim_records`; TRUST.md defines no per-citation assessment
semantics). A claim-level assessment attaches to the claim, never
automatically to each citation relation. Repository-level-only adoption
remains fully conformant — no adopter needs a knowledge graph.

## D-004 — Missing-data semantics

**Status: Proposed.**
Four distinct states, normative in v0.3:
1. **Missing** (field absent) = not assessed, no statement made;
2. **`not-assessed`** (explicit) = considered, deliberately not assessed;
3. **`not-applicable`** = the dimension does not apply to this unit;
4. **Low support** (`none`, `unreviewed`, band "Speculative") = an assessment
   *result*, never a default.
`null` is not a valid assessment value (it remains valid only where already
specified, e.g. `companions.*`). Validators must not conflate these states.

## D-005 — Human and agent review states

**Status: Proposed.**
`review_status ∈ {unreviewed, agent-reviewed, human-reviewed, adjudicated}`,
strictly ordered. Agent agreement — including agreement among *multiple*
agents — caps at `agent-reviewed`: agreement is agreement, not scientific
validation (principle 6). `human-reviewed` requires an identifiable human in
`assessed_by`. `adjudicated` requires a recorded resolution of an actual
disagreement — its precise definition (who adjudicates, where recorded) is an
**open question** for methodology contributors (plan §12.4). Any status above
`unreviewed` requires assessor, protocol, and timestamp provenance
(principle 7); `independent_review: true` additionally requires a reviewer
independent of `produced_by`.

## D-006 — Conformance levels

**Status: Proposed.**
Keep three levels, redefined for v0.3:
- **Conformant** — MUST rules pass (unchanged in spirit; v0.1/v0.2 files stay
  conformant under their declared version);
- **Recommended** — Conformant + no warnings + the ten principles' declarable
  obligations met (e.g. no prestige/citation-count/p-value trust measures —
  which are auditable in spec-governed fields);
- **Extended** — Recommended + dimensions or claim-level summaries +
  `assessment` provenance block + documented inline encoding.
Renaming "Recommended" (ambiguous as a level name) is a bikeshed-level open
item; do not block on it.

## D-007 — Backward compatibility and version number

**Status: Accepted (planning-level; release itself is not authorised here).**
The next version is **v0.3, additive and non-breaking**. All v0.1/v0.2 files
remain valid; schemas are versioned and frozen (`schema/v0.1|v0.2|v0.3/`);
the validator dispatches on the declared `trust_md_version`; deprecations are
notices, not errors. Unknown *future* versions fail with a distinct
"unsupported version" error. A breaking v1.0 (e.g. removing `average_trust`
or making dimensions primary) is **deferred** — see D-010.

## D-008 — Canonical filename casing and discovery

**Status: Proposed (needs maintainer decision, coordinated with FAIR.md).**
Recommendation: canonical repository filename **`TRUST.md`** (uppercase,
matching README.md convention, this repo's name, and FAIR.md's de-facto repo
usage); canonical served web path lowercase **`/trust.md`**, servers
RECOMMENDED to treat the path case-insensitively; discovery order `/trust.md`
→ `/TRUST.md` → `/.well-known/trust.md` (redirect). Whatever is decided must
fix the current README/SPEC contradiction (defect D7) in both repos the same
way.

## D-009 — Unknown future fields

**Status: Proposed.**
Must-ignore policy: validators MUST NOT error on unknown top-level fields or
unknown keys inside extensible objects (info-level notice at most); the `x_`
prefix stays the recommendation for private extensions;
`additionalProperties: false` is removed from category/artifact/scale objects
(defect D8c) so documented extension points (e.g. `eco:` on categories)
are legal.

## D-010 — Deferred: promotion of dimensions to primary (v1.0)

**Status: Proposed (explicitly deferred).**
Whether a future v1.0 makes the dimensional model primary and removes the
0–100 integer and `average_trust` is *not decided in this cycle*. Adoption
data from v0.3 and methodology-contributor input (plan §12) are prerequisites.

## D-012 — Dimension set and acronym expansion

**Status: Proposed.**
The core dimension set is chosen by the **admission test** (plan §4 Option F:
self-assessable without expert appraisal of third-party science; distinct;
has a not-applicable state; no prestige/citation-count/p-value proxies) — the
acronym expansion follows the dimension set, never the reverse. Under that
test the core set is: statement type (existing categories),
`evidence_support`, `review_status`, `calibration` (uncertainty), and
`source_integrity` defined strictly as *citation integrity*; **traceability**
is realised as the `assessment` provenance block, which is recorded, not
scored. **Robustness** and **transferability** are excluded from the core:
they require expert appraisal of the underlying science (GRADE-style) and are
supported only by referencing an external appraisal via `assessment.protocol`
or as `x_` extensions. Additive per-letter subscores (5 × 20 summing to 100)
are rejected (plan §4 Option E; see also D-002 — no mandatory or
compensatory aggregate). Any re-expansion of the acronym must preserve
review status and evidence support as first-class dimensions. Worked preview:
`examples/dimensions-preview.trust.md`.

## D-011 — No calibration claims

**Status: Accepted (planning-level).**
The spec makes no claim that any scale or dimension is *calibrated* — there is
no benchmark. The word "calibration" appears only as the name of the optional
wording-vs-evidence dimension (whose viability for self-declaration is itself
an open question, plan §12.3), never as a validity claim.
