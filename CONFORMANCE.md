# TRUST.md v0.3 conformance matrix

| Obligation | Schema | CLI semantic check | Human review |
|---|:---:|:---:|:---:|
| Required fields and types | ✓ | | |
| Version-specific dispatch | | ✓ | |
| URI, date, ORCID, path formats | ✓ | | |
| Canonical five-band order | ✓ | ✓ | |
| Numeric bands cover 0–100; `100-100` valid | partial | ✓ | |
| Numeric refinement is not presented as probability | partial | | ✓ |
| Missing states remain distinct | ✓ | | ✓ |
| Human review names a human | partial | ✓ | |
| Agent agreement caps at agent-reviewed | | ✓ | ✓ |
| Adjudication records disagreement and resolution | partial | ✓ | ✓ |
| Independent reviewer differs from producers | | ✓ | ✓ |
| Reviewer competence and actual independence | | | ✓ |
| Claim–evidence records remain external | | ✓ | ✓ |
| Band counts and conservative median agree | partial | ✓ | |
| Unknown fields and deprecations are notices | | ✓ | |
| No prestige/citation-count/p-value trust proxy | | | ✓ |
| Scientific claims are valid and sources support them | | | ✓ |

Passing the schema or CLI establishes structural conformance only. It does not
certify scientific truth, source quality, reviewer competence, independence,
or replication.
