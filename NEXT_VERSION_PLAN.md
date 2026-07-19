# TRUST.md — Next Version Plan (toward v0.3)

**Status:** planning document — no release is made by this document.
**Date:** 2026-07-19
**Scope:** audit of v0.2 as shipped, confirmed defects, methodological analysis of
the epistemic model, compared alternatives, recommended direction, compatibility
strategy, implementation sequence, and open questions for methodology contributors.

Guiding constraint (unchanged): TRUST.md is a **lightweight, human- and
machine-readable epistemic manifest**. It must not grow into an
evidence-management platform. Everything below is filtered through that
constraint.

---

## 1. Current-state audit

What exists today (v0.2, commit `9e38fc6` and later):

| Component | State |
|---|---|
| `README.md` | v0.2 status line; 30-second example; adoption steps; lineage |
| `TRUST.md` (template) | Placeholder template, front matter `trust_md_version: "0.2"` |
| `SPEC.md` | Formal spec v0.2: 15 MUST rules, 7 warning checks, 3 conformance levels |
| `schema/trust.schema.json` | JSON Schema draft 2020-12 for the front matter |
| `tools/validate.py` | Standalone PyYAML-only CLI implementing the 15 rules + 7 warnings |
| `examples/neuronautix.trust.md` | Reference implementation (passes CLI and schema) |
| `.github/workflows/validate.yml` | CI: runs CLI over `examples/*.trust.md` |
| `CHANGELOG.md` | Keep-a-Changelog format, entries for 0.1 and 0.2 |
| Issues / PRs | No open issues; one merged PR (#1, review improvements) |
| Tags / releases | One tag+release `v0.2` — **mis-tagged, see D5** |
| Tests | **None.** No test suite exists for the validator or schema |

Related ecosystem:

- **`Neuronautix/FAIR.md`** (v0.2) — companion convention; same front-matter
  style (`fair_md_version`, `last_reviewed`, `companions` cross-link); uses a
  categorical self-assessment vocabulary (`yes | partial | planned | no | n/a`)
  — notably *ordinal/categorical, not numeric*. Its repo also exhibits the same
  uppercase-repo-file / lowercase-served-file split as this one.
- **`Neuronautix/ComputationalReviewTemplate_trust-knowledge`** ("TRUST
  Knowledge" template) — a claim-level pipeline with its own
  `claim_context.schema.json`, `trust_score.schema.json`,
  `claim_graph.schema.json` and a mechanical `TRUST_RUBRIC.md` (component
  scores, score caps, VERIFIED-requires-verbatim-passage). It operates at the
  **claim and claim–evidence level**; TRUST.md operates at the
  **repository/corpus level**. Neither currently names the other's scores, and
  their numeric scales are *not* the same quantity.
- **ORAtlas** — no public specification could be located at the time of this
  audit. It is treated here as a planned downstream consumer. **No semantic
  alignment with ORAtlas is claimed anywhere in this plan**; the only
  requirement recorded is directional (see §8).

## 2. Confirmed defects

All defects below were reproduced against the working tree at `317b98b`
(validator behaviour verified by execution; schema behaviour verified with
`jsonschema` 2020-12).

### Blocking / code

- **D1 — Validator crash (NameError).** `tools/validate.py:123` references
  `expected_start`, which is never defined (the variable is `expected_next`).
  Any file whose confidence bands do not end at 100 makes the validator crash
  with a traceback instead of reporting the W7 warning. Reproduced.
- **D2 — Single-point bands rejected.** `check_band_coverage` treats
  `lo >= hi` as malformed, so a legitimate band like `"100-100"` is reported
  as a problem — and then triggers the D1 crash because coverage ends early.
  Reproduced.

### Documentation / examples

- **D3 — README 30-second example is invalid.** It uses
  `TRUST_md_version` (wrong capitalisation of the key) and `average_:` (a
  truncated `average_trust`). The showcase example fails the project's own
  schema with two errors. Reproduced with `jsonschema`.
- **D4 — v0.1/v0.2 wording drift.** All confirmed:
  - `SPEC.md` §5.1 still states `trust_md_version` "Allowed values: `"0.1"`",
    contradicting its own §7 rule 4 and the schema enum (`0.1 | 0.2`);
  - `README.md` §Formal specification says "the complete **v0.1**
    specification"; the 30-second example declares `"0.1"`;
  - the template's prose says "It is a **proposed convention (v0.1)**" and its
    changelog stub says v0.1, while its front matter says `"0.2"`;
  - `examples/neuronautix.trust.md` header comment (line 3) and prose
    (line 129) say v0.1 with front matter `"0.2"`; its prose changelog has no
    v0.2 entry;
  - `tools/validate.py` docstring says "specification **v0.1**" and the Rule 4
    code comment says `== "0.1"`.
- **D5 — Release/tag hygiene.** The GitHub release `v0.2` tags commit
  `1b2ec8e`, whose tree is entirely v0.1 (SPEC header, README status, template
  version all say 0.1) — the actual bump commit `9e38fc6` is untagged. Also,
  `CHANGELOG.md` links `[0.1]` to a `v0.1` tag that does not exist. Verified
  via `git show 1b2ec8e:SPEC.md` and the tag list.
- **D6 — Broken example link.** `README.md` links
  `examples/neuronautix.TRUST.md`; the file is `examples/neuronautix.trust.md`
  (404 on GitHub's case-sensitive paths).
- **D7 — Casing and discovery inconsistency.** README says "Serve the file at
  `https://yourdomain/TRUST.md`" and gives the reference URL as
  `https://neuronautix.com/TRUST.md`; SPEC §3.1 and the template mandate
  lowercase `https://<domain>/trust.md`. The repo's own root file is uppercase
  `TRUST.md` while the template instructs adopters to copy it "as `trust.md`".
  No canonical-casing statement exists anywhere. (Decision D-008 in
  DECISIONS.md.)

### Schema ↔ CLI ↔ SPEC enforcement drift

All reproduced with fixtures:

- **D8a** — Schema requires `trust_md_version` to be a *string*; the CLI
  coerces with `str()` so an unquoted YAML `0.1` (a float) passes the CLI but
  fails the schema.
- **D8b** — Schema errors on a malformed ORCID (regex); the CLI never checks
  ORCID format, only presence (warning).
- **D8c** — Schema sets `additionalProperties: false` on category entries, so
  an extension key such as `eco: "ECO:0000204"` — explicitly invited by
  README ("ECO codes are a natural extension of TRUST.md's category IDs") and
  SPEC §5.3 — is a schema **error**. Same problem on `artifacts` entries and
  `confidence_scale`.
- **D8d** — Schema band `range` pattern accepts only the ASCII hyphen
  (`^[0-9]+-[0-9]+$`); the CLI also accepts an en-dash (`0–29`). A file can
  pass one and fail the other.
- **D8e** — `corpus.average_trust` out of [0,100] is a schema **error**
  (min/max) but a SPEC §7 / CLI **warning**. Same input, different severity.
- **D8f** — The CLI checks nothing about `corpus` structure, `artifacts`
  structure, `companions` path format, `canonical` URI shape, or category `id`
  charset — all schema-only rules. Conversely, prose presence, band
  contiguity, and canonical-category warnings are CLI-only.
- **D8g** — **Nothing ever runs the JSON Schema.** CI runs only the CLI. The
  schema and CLI have therefore drifted with no signal. Additionally, `format:
  "uri"` / `format: "date"` are annotation-only in draft 2020-12 default
  behaviour, so `canonical: "not a uri"` passes everything.
- **D9 — CI redundancy.** `validate.yml` validates the reference example
  explicitly and then again inside the `examples/*` loop.

### Methodological (also defects, fix requires spec text)

- **D10 — Band meanings conflate category with confidence.** The 0–29 band is
  *defined* as "normative/opinion/vision with little direct evidence" — i.e.
  membership of the `view`/`hypothesis` categories is written into the
  confidence scale. Under these definitions a `view` can never legitimately
  score above ~29, which directly contradicts
  `independent_of_category: true` — a MUST in the same spec. The two axes are
  declared independent and defined dependently.
- **D11 — README contradicts the schema on adjustability.** README step 3
  says "the 0–100 scale can be adjusted for your domain"; the schema and SPEC
  make `[0, 100]` + `type: integer` a hard MUST (`const`).
- **D12 — `$id` is not a resolvable schema URL.** It points at a GitHub
  `/blob/` HTML page, not raw JSON; and it is version-pinned to v0.2 in a way
  that will need a real versioning scheme (see §7).

## 3. Methodological problems with the current model

### 3.1 What the single 0–100 "confidence" score conflates

The current per-claim annotation is `(category, confidence 0–100)`. The number
is asked to carry at least four distinct meanings at once:

1. **Evidence support** — how directly and strongly sources support the claim
   (the band *meanings* are written in these terms);
2. **Author calibration/uncertainty** — how confident the author feels and
   whether the wording matches the evidence (the field *name* says this);
3. **Review status** — the governance prose implies reviewed claims, but the
   number does not say whether anyone checked it;
4. **A soft probability reading** — a reader who sees "confidence 85/100"
   will, absent instruction, read it as "85% likely true". Nothing in v0.2
   forbids that reading. The reference implementation's own `limitations`
   already concedes the conflation ("a planned second axis would separate
   them").

### 3.2 False precision

A 101-point integer scale implies distinctions (73 vs 74) that no author or
reviewer can reproduce. In practice every published value is chosen *by band*
and then given a number inside it. The information content is ordinal (5
levels); the encoding is pseudo-cardinal. Worse, `corpus.average_trust`
computes an **arithmetic mean of ordinal judgements** — a statistically
dubious operation — and presents it as the headline corpus statistic.

### 3.3 Missing states are indistinguishable

v0.2 cannot distinguish: *no assessment was made*, *assessment was attempted
but not applicable*, *assessed with low support*, and *field simply omitted*.
An unmarked claim and a claim assessed at 0 are different epistemic states; the
format currently collapses them.

### 3.4 No assessment provenance

`produced_by` covers who produced the *content*; nothing records who produced
an *assessment*, under what protocol, or when — so an agent-generated score and
an adjudicated human score are indistinguishable on the page.

## 4. Model alternatives compared

The methodological question: keep, replace, or decompose the 0–100 score.

### Option A — Keep 0–100, tighten definitions only

Redefine the number as "graded evidence support", rewrite band meanings to
remove category language (fixes D10), add the "not a probability" principles.

- *Pros:* zero migration; no schema change; existing tooling (Trust Lens,
  `data-trust`) untouched.
- *Cons:* false precision remains; conflation of support/calibration/review
  remains structural, not verbal; `average_trust` stays statistically dubious;
  readers still see a number that looks like a probability.

### Option B — Replace with a single ordinal scale

Replace the integer with the five band labels as an enum
(`speculative | tentative | moderate | high | very-high`).

- *Pros:* honest about information content; removes false precision; matches
  FAIR.md's categorical style; trivially machine-readable.
- *Cons:* **breaking** for every existing file and for inline `data-trust`
  markup; still a single axis, so the conflation of §3.1 survives with fewer
  digits; loses back-compat for no structural gain.

### Option C — Multidimensional profile, no aggregate at all

Per assessed unit: `statement_type` (existing categories), `evidence_support`
(ordinal), `review_status` (enum), optional `calibration` note, plus assessor
provenance. Remove the numeric score entirely.

- *Pros:* each dimension means one thing; nothing masquerades as probability;
  averaging becomes impossible by construction.
- *Cons:* **breaking**; heavier authoring cost per claim (against the
  lightweight mandate if all dimensions were required); orphans every v0.1/v0.2
  file and the entire inline-markup installed base at once.

### Option D — Multidimensional profile + optional, explicitly experimental aggregate

Option C's dimensions introduced as **optional** structures, while the existing
0–100 `confidence` is retained as a *legacy summary*: still valid, redefined
as an author-declared ordinal-in-spirit gradation, explicitly labelled **not a
probability**, and **deprecated as the sole assessment for new adopters**.
Aggregate corpus statistics move from `average_trust` (deprecated) to a
band/level **distribution** (medians and counts, no means).

- *Pros:* fully backward-compatible (v0.1/v0.2 files remain valid v0.3 files);
  separates the four concepts for anyone who wants them; existing tooling keeps
  working during migration; the false-precision object is contained and
  labelled rather than silently blessed; consistent with FAIR.md's categorical
  precedent.
- *Cons:* two ways to say related things during the transition (mitigated by
  clear deprecation text and validator hints); slightly larger spec.

## 5. Recommended direction

**Adopt Option D, released as v0.3 (additive, non-breaking).** Rationale:

- It is the only option that fixes the conflation (§3.1) **and** honours the
  compatibility requirement **and** stays lightweight (all new dimensions
  optional; a minimal repository-level TRUST.md gets *no* longer).
- The 0–100 scale's real, defensible content is its five bands. v0.3 makes the
  bands/ordinal levels the primary semantic and demotes the integer to an
  optional refinement within a band, explicitly experimental as an aggregate.
- FAIR.md already demonstrated the categorical style in the same ecosystem.

### 5.1 Sketch of the v0.3 additions (all optional unless noted)

```yaml
epistemic_model:
  categories: [...]            # unchanged; docs retitle this "statement type"
  confidence_scale: {...}      # unchanged; meanings rewritten (D10); redefined
                               # as "graded evidence support", NOT probability
  dimensions:                  # NEW, optional
    evidence_support:          # ordinal enum
      levels: [direct, indirect, partial, contested, none]
    review_status:
      levels: [unreviewed, agent-reviewed, human-reviewed, adjudicated]
    calibration:               # does the wording match the evidence?
      levels: [understated, matched, overstated, not-assessed]

assessment:                    # NEW, optional — provenance of the assessment
  unit: repository             # repository | artifact | claim | claim-evidence
  protocol: "<name/URL of rubric or protocol, e.g. TRUST_RUBRIC v1>"
  assessed_by:                 # humans and/or agents, same shape as produced_by
    humans: [...]
    agents: [...]
  date: "YYYY-MM-DD"
  supersedes: null             # URL/path of a previous assessment, if any
  independent_review: false    # false = self-declaration (default)
```

Missing-data semantics (normative in v0.3): an **absent** optional field means
*not assessed*; the explicit value `not-assessed` means *considered and
deliberately not assessed*; `not-applicable` (where a level list includes it)
means *the dimension does not apply*; the lowest ordinal level (`none`,
`unreviewed`) is an *assessment result*, never a default. `null` is not a valid
assessment value.

Corpus aggregation in v0.3: `corpus.average_trust` is **deprecated** (still
valid). New optional `corpus.band_distribution` (claim counts per band/level)
and `corpus.median_band` replace it as the recommended summary. No mandatory
aggregate of any kind.

### 5.2 Required principles (normative text for SPEC v0.3)

The next version MUST state, in a dedicated "What a TRUST.md assessment is and
is not" section, that a TRUST.md assessment:

1. is **not a probability** that a claim is true;
2. is **not a score for an author, institution, journal, or laboratory** — it
   attaches to statements and corpora, never to persons or venues;
3. **must not use prestige, citation counts, or p-values** as direct trust
   measures;
4. distinguishes **missing**, **not assessed**, **not applicable**, and **low
   support** as four different states;
5. **preserves individual dimensions** — tools MUST NOT display an aggregate
   without the dimensions being one interaction away;
6. treats **agent agreement as agreement**, not scientific validation —
   multiple AI reviewers concurring raises `review_status` at most to
   `agent-reviewed`;
7. preserves **assessor, protocol, timestamp, and evidence provenance** for
   any assessment that claims more than self-declaration;
8. allows assessments to be **challenged or superseded** (`supersedes`, and a
   documented dispute path);
9. is never **silently translated into another assessment protocol** — exports
   MUST carry the source protocol identifier;
10. remains a **self-declaration unless independently reviewed**
    (`independent_review: true` requires naming the reviewer).

## 6. Assessment units

v0.3 defines four units explicitly (today they are implicit and muddled):

| Unit | Where it lives | Status in v0.3 |
|---|---|---|
| **Repository declaration** | the TRUST.md file itself | the default; what every adopter gets with zero extra work |
| **Artifact/document** | `artifacts[]` entries | supported (exists today); gains optional `review_status` |
| **Individual claim** | inline markup in content (`data-epi`, `data-trust`, optionally `data-support`, `data-review`) | supported; TRUST.md only *summarises* it — the manifest never enumerates claims |
| **Claim–evidence relation** | external claim records (e.g. the TRUST Knowledge template's `claim_context` / `trust_score` files, nanopublications) | **referenced, not contained**: an optional `companions.claim_records` pointer. TRUST.md does NOT define per-citation assessment semantics |

Explicit rule: a claim-level assessment is **not** attached to every citation
relation. A claim may cite several sources; the assessment attaches to the
claim (or, in external records only, to a claim–evidence pair whose semantics
that record format defines). This is the boundary that keeps TRUST.md a
manifest and not a knowledge graph: **richer claim-level records live outside
the file and are pointed to, never embedded.** Adopters who stop at the
repository level are fully conformant.

## 7. Compatibility strategy

- **Version number: v0.3** (minor, additive). No confirmed defect or accepted
  recommendation requires breaking v0.1/v0.2 files, so a breaking version is
  not justified. A future v1.0 may promote the dimensions; that decision is
  explicitly deferred (DECISIONS.md D-010).
- **Old files remain valid:** the v0.3 validator accepts
  `trust_md_version: "0.1" | "0.2" | "0.3"`; every rule added in v0.3 applies
  only to v0.3 declarations or to optional fields when present.
- **Deprecated (not removed) in v0.3:**
  - `corpus.average_trust` → `corpus.band_distribution` / `corpus.median_band`
    (validator: deprecation notice, not a warning-level defect);
  - the bare 0–100 number as the *only* assessment for new adopters →
    band/ordinal levels (+ optional dimensions). `data-trust` inline attribute
    stays valid.
- **Versioned schemas:** move to `schema/v0.1/`, `schema/v0.2/`, `schema/v0.3/`
  (v0.1 and v0.2 reconstructed from tags/history and frozen; the current
  drifted file becomes the corrected v0.2). `$id` becomes a raw, resolvable
  URL. The validator selects the schema by the file's declared
  `trust_md_version` and grows a `--spec-version` override.
- **Unknown future fields:** must-ignore policy, stated normatively — a
  validator encountering an unknown top-level field or an unknown key inside
  extensible objects MUST NOT error (info-level notice at most). Extension
  fields keep the `x_` prefix recommendation. A file declaring an *unknown
  version* (e.g. `"0.9"`) fails with a distinct "unsupported version" error,
  not a generic one. `additionalProperties: false` is removed from category,
  artifact, and confidence-scale objects (fixes D8c/D9-adjacent) — known keys
  stay typed, unknown keys pass.
- **Migration guide:** `MIGRATION.md` (v0.2 → v0.3): no mandatory edits; a
  checklist for opting into dimensions; before/after fixtures (which double as
  test inputs).
- **Filename/discovery:** proposal (D-008, needs owner sign-off): canonical
  *repository* filename is **`TRUST.md`** (uppercase, matching README.md
  convention and this repo's name); the *served web path* is lowercase
  `/trust.md`, with servers RECOMMENDED to treat the path case-insensitively;
  discovery order documented as `/trust.md`, then `/TRUST.md`, then
  `/.well-known/trust.md` (redirect). All prose brought into line (fixes D7).

## 8. Interoperability boundaries

| System | Boundary in v0.3 | What v0.3 does / does not claim |
|---|---|---|
| **FAIR.md** | Sibling convention, disjoint concern (findability vs epistemic status). Shared surface: `*_md_version` naming, `last_reviewed`, mutual `companions` links, the same casing decision. | Coordinate casing + companions wording; no field overlap |
| **TRUST Knowledge template** (`ComputationalReviewTemplate_trust-knowledge`) | It is a claim/claim–evidence **producer**; TRUST.md is the repository-level **summary**. Its mechanical `TRUST_score` is a different quantity from `confidence` and MUST NOT be copied into it silently — a manifest summarising its output names the rubric via `assessment.protocol` and uses `review_status: agent-reviewed` (or higher if humans adjudicated). | A written mapping doc is a backlog item (B-022); until it exists, no equivalence is claimed |
| **ORAtlas** | No public spec located; treated as a future consumer. Directional requirement only: TRUST.md native fields must be exportable *as TRUST.md fields with their protocol identifier attached*, so ORAtlas (or any platform) cannot silently reinterpret them as its own native criteria (principle 9). | **No alignment claimed** |
| **W3C PROV** | `produced_by` / `assessed_by` are informal renderings of prov:Agent / prov:Activity. | "Informed by", not "conformant to", until a JSON-LD context exists (B-023) |
| **SEPIO / ECO** | Optional per-category extension keys (e.g. `eco:`) become schema-legal (D8c fix). | Spec wording downgraded from "aligns with" to "designed to map; mapping table pending" until a term-level table is published |
| **Nanopublications** | Export target for claim records (external unit, §6). | No conformance claim |
| **schema.org ClaimReview** | Possible emission target for claim-level markup; note honestly that ClaimReview's `reviewRating` is a rating of a *claim by a reviewer* — closest to `review_status ≥ human-reviewed` records, not to self-declared confidence. | Export sketch only; "planned" stays "planned" |

## 9. Implementation sequence

Ordered; IDs reference BACKLOG.md.

1. **Repair the validator and build the missing test suite** (B-001…B-004):
   fix D1/D2, add pytest suite + fixtures, run schema *and* CLI in CI.
2. **Documentation consistency pass** (B-005…B-009): fix D3, D4, D6, D9;
   record D5/D7 resolutions (tag hygiene needs owner action on GitHub).
3. **Schema/CLI reconciliation within v0.2 semantics** (B-010…B-013): one
   source of truth for severity (D8a–D8g), extensibility fix (D8c), versioned
   schema layout.
4. **Spec v0.3 draft** (B-014…B-018): principles section, assessment units,
   dimensions + missing-data semantics, deprecations, casing/discovery text.
5. **Examples + migration** (B-019…B-021): v0.1/v0.2 back-compat fixtures, a
   dimensions-based example with *no* numeric aggregate, MIGRATION.md.
6. **Interoperability** (B-022…B-024): TRUST-Knowledge mapping doc, PROV
   context sketch, export round-trip tests.
7. **Release decision** — explicitly out of scope for this plan; requires
   maintainer sign-off on DECISIONS.md items marked *Proposed*.

## 10. Test plan (required coverage)

To live under `tests/` (pytest) with fixtures under `tests/fixtures/`:

1. **Schema/validator agreement** — every fixture is run through both; any
   verdict divergence (error/warn/pass) fails the suite (catches D8-class
   drift permanently).
2. **Every supported spec version** — a minimal and a full fixture for 0.1,
   0.2, 0.3 each pass their versioned schema and the CLI.
3. **Invalid and future versions** — `"0.9"`, `1`, unquoted `0.1` (float),
   missing version: each yields the specific "unsupported/invalid version"
   error.
4. **Missing vs null fields** — absent optional field (pass, "not assessed"),
   `null` where disallowed (error), explicit `not-assessed` (pass) are three
   distinct outcomes.
5. **Malformed confidence bands** — non-numeric ranges, en-dash vs hyphen
   (one canonical answer in both schema and CLI), reversed `lo>hi`,
   single-point `100-100` (must be *valid*), missing `range` key.
6. **Gaps and overlaps** — bands `0-29/40-100` (gap), `0-50/40-100`
   (overlap), bands ending at 90 (regression for D1 — must warn, not crash).
7. **Empty or invalid assessor records** — `assessment.assessed_by` present
   but empty; agent assessor without `oversight`; unknown protocol shape.
8. **Invalid review states** — `review_status: peer-reviewed` (not in enum)
   errors; case sensitivity pinned.
9. **Backward-compatible v0.1/v0.2 examples** — the exact examples shipped
   with those versions (from git history) validate forever.
10. **Migration fixtures** — each MIGRATION.md before/after pair validates
    under its declared version.
11. **Unknown extension fields** — unknown top-level key, `x_` key, unknown
    key inside a category entry: all pass (info at most).
12. **No-aggregate examples** — a v0.3 file using dimensions with no numeric
    confidence and no `average_trust` passes with zero warnings.

## 11. Non-goals (restated for this cycle)

No ORAtlas features in this repo; no claim database; no invented expert
validation data; no calibration claims without a benchmark (there is none —
any "calibrated" language is banned from spec text); no domain-specific
requirements; no requirement that adopters use AI; no new field without a use
case named in its backlog item; **no release published during this cycle**.

## 12. Unresolved decisions requiring expert input

Tracked as *Proposed* in DECISIONS.md; summarised:

1. Band thresholds (90/70/50/30) — are five bands and these cut-points
   defensible, or should levels be purely nominal-ordinal without numeric
   anchors at all?
2. `evidence_support` level vocabulary (`direct/indirect/partial/contested/
   none`) — is `contested` a support level or a separate flag?
3. Is `calibration` (wording vs evidence) reliably assessable by authors, or
   should it be reserved to reviewers/agents and dropped from self-declaration?
4. What exactly qualifies as `adjudicated` (who resolves disagreement between
   reviewers, and where is that recorded)?
5. Should `average_trust` be deprecated (recommended here) or hard-removed at
   v1.0? Is a median over ordinal bands acceptable as the headline statistic?
6. Claim–evidence records: is pointing to external records (nanopub /
   TRUST-Knowledge files) sufficient, or does any adopter need in-file
   claim-level entries badly enough to justify the weight?
7. Does multi-agent agreement ever justify more than `agent-reviewed` (this
   plan says no — principle 6) — confirm with methodology contributors.
8. Canonical casing (D-008) — needs the maintainer's decision jointly with
   FAIR.md, since both repos share the pattern.
