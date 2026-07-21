# Validator usage

The reference validator checks TRUST.md structure and locally testable semantic
relationships. It does not certify evidence or scientific conclusions.

## Install

Python 3.10 or newer is recommended.

```sh
python -m pip install pyyaml jsonschema
```

Install `pytest` as well when running the repository test suite:

```sh
python -m pip install pyyaml jsonschema pytest
```

## Validate a declaration

```sh
python tools/validate.py TRUST.md
```

Pass another path to validate a fixture or example:

```sh
python tools/validate.py examples/v04-multiple-assessments.trust.md
```

The command dispatches only from the exact quoted `trust_md_version` and never
rewrites the file.

## Diagnostics and exit codes

- **Error:** a required schema or semantic rule was violated. Exit code 1.
- **Warning:** a recommended or reviewable condition needs attention. Exit code
  remains 0 when there are no errors.
- **Notice:** a deprecated or ignored unknown field was found. Exit code remains
  0 when there are no errors.
- **Usage/dependency failure:** exit code 2.

Private extension keys should begin `x_`. Standard-looking unknown fields are
ignored for conformance but reported, including nested locations.

## Repository checks

Run the same main test command used by CI:

```sh
python -m pytest -q
```

Compile the validator:

```sh
python -m py_compile tools/validate.py
```

Validate all public examples on a POSIX shell:

```sh
find examples -name '*.trust.md' -print0 | while IFS= read -r -d '' file; do
  python tools/validate.py "$file"
done
```

Some historical examples intentionally emit documented notices. Tests encode
the expected diagnostics. All v0.4 public examples validate without errors,
warnings, or notices.

## Validation boundary

Successful validation establishes only structural conformance, declared
provenance, identifier shape, and locally checkable relationships. It does not
verify evidence truth, protocol adequacy, reviewer competence, actual
independence, reproducibility, or fitness for an undeclared purpose.
