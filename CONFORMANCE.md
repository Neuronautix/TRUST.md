# TRUST.md v0.4 conformance matrix

| Obligation | Schema | CLI semantic check | Human/scientific review |
|---|:---:|:---:|:---:|
| Required fields and exact version dispatch | ✓ | ✓ | |
| URI, date-time, digest, ORCID, and path formats | ✓ | | |
| Non-empty subject registry | ✓ | | |
| Exact subject version or immutable snapshot | ✓ | ✓ | |
| Unique assessment IDs and series/version pairs | | ✓ | |
| Assessment subject resolves locally | | ✓ | |
| Protocol identity and version | ✓ | | ✓ |
| Fitness requires a declared purpose | ✓ | | ✓ |
| Active reviewed assessment links a basis | ✓ | ✓ | ✓ |
| Human review has human provenance | partial | ✓ | ✓ |
| Agent-only review is not human review | | ✓ | ✓ |
| Adjudication links disagreement and resolution | ✓ | ✓ | ✓ |
| Independence uses a declared state | ✓ | ✓ | |
| Actual assessor independence or competence | | | ✓ |
| Missing and assessed-low states remain distinct | ✓ | | ✓ |
| Optional numeric refinement is not probability | ✓ | | ✓ |
| Review and impact metrics cannot be dimensions | partial | ✓ | ✓ |
| Supersession stays in one series and subject | | ✓ | |
| Supersession graph is acyclic | | ✓ | |
| Withdrawal/retraction leaves subject unchanged | partial | ✓ | ✓ |
| Conflicting assessments remain separate | ✓ | ✓ | ✓ |
| No top-level aggregation across assessments | | ✓ | ✓ |
| Unknown fields and deprecations are notices | | ✓ | |
| Frozen v0.1–v0.3 behavior is preserved | | ✓ | |
| Evidence truth, methods, reproducibility, conclusions | | | ✓ |

## What conformance means

Schema and CLI conformance establish that a declaration has the required
structure, attributable provenance, identifiers, and internally checkable
relationships for its declared version.

They do **not** certify evidence, methodological quality, source truth,
reviewer competence, independence, reproducibility, replication, or downstream
scientific conclusions. TRUST.md v0.4 is an experimental proposed convention,
not an assessment authority. Human scientific work remains separate and cannot
be replaced by schema validation or agreement among automated agents.
