# Executable Audit Extension (2026-10-22)

## Status and provenance

This is a new, AI-assisted implementation stage based on baseline commit
`708a0c8b9f834701a3ead2dfafef58e2bd163d97`. It does not reconstruct or replace
historical Studies A/B/C, their data, or their findings. The original tag
`v0.1.0-development`, preprint, aggregate data, correction record, and
`code/rc_stats.py` remain unchanged.

## Implemented scope

The extension accepts a deliberately small JSON-compatible finite-domain
language: equality/inequality, pairwise distinctness, sums, value counts,
ordered variables, and base-N divisibility. The schema caps variables, domain
sizes, constraints, and total search space. It never executes generated code.

Two independent implementations evaluate a specification: exhaustive Python
enumeration and Z3 model enumeration. Specification comparison first requires
an exact variable/domain mapping and asks Z3 for a symmetric-difference
witness. Equal counts and equal solution sets are reported separately.

The dual-formalization interface makes two isolated provider calls. A call sees
only the public problem ID/text, not Gold, the peer specification, labels, or
prior conversation. This is operational isolation, not statistical
independence. Deterministic fixtures work without credentials; the optional
real provider fails explicitly when `OPENAI_API_KEY` is unavailable.

Audit decisions are `PASS`, `FAIL`, or `INCONCLUSIVE` with stable reason codes.
`PASS` means only that the two mapped specifications have the same finite
solution set and any supplied answer has the verified count. It does not prove
that either specification is faithful to natural language.

## Gold-isolated evaluation

`axiom_x.experiment` serializes and hashes prediction-only records before Gold
is supplied to `evaluate_frozen`. The evaluator rejects changed payloads and
reports wrong-answer opportunities, false certifications, decision coverage,
abstention, and correct-answer acceptance. False-certification rate is `null`
with status `UNDEFINED_ZERO_DENOMINATOR` when there is no error opportunity.
The grouped paired bootstrap samples group IDs with a fixed seed.

The three intended strategies have different evidentiary meanings:

- Baseline checks a proposed answer without a second independently generated specification.
- Single formalization checks internal solver consistency for one specification.
- Dual formalization additionally checks agreement between two isolated specifications.

They are matched comparisons only in the limited sense of sharing cases and
frozen evaluation; they do not perform equivalent checks.

## Reproduce

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-extension.txt
pytest -q
python -m axiom_x.demo
python code/rc_stats.py --clusters data/cluster_summary.csv
```

## Evidence map

| Claim | Evidence | Level |
|---|---|---|
| bounded schema rejects executable/oversized input | `tests/test_extension.py` | VERIFIED only after local test run |
| Python and Z3 solve finite fixtures | `axiom_x/solver.py`, tests | VERIFIED only after local test run |
| equal counts can hide different sets | symmetric-difference fixture | VERIFIED only after local test run |
| Gold is absent from generation calls | provider spy/freeze tests | VERIFIED only after local test run |
| natural LLM reliability | no natural experiment run | NOT RUN |
| external or human Gold validity | no independent reviewer/data | NOT VERIFIED |

## Execution record

Executed locally on 2026-10-22 from the clean baseline and again from a fresh
temporary clone of branch `research-upgrade-20261022`:

- `python3 code/rc_stats.py --clusters data/cluster_summary.csv`: VERIFIED;
  preserved 40 cases, 17 wrong-answer opportunities, 13 Base false
  certifications, 1 audit false certification, and 17/40 decision coverage.
- `python -m pytest -q`: VERIFIED, `12 passed`.
- `python -m axiom_x.demo`: VERIFIED; deterministic synthetic output contained
  one `DEFINED_CHECKS_PASSED` and one counterexample-backed
  `SPECIFICATION_SET_DIFFERENCE`.
- Fresh-clone rerun: VERIFIED, `12 passed`; historical recomputation and demo
  also completed. Temporary outputs were not committed as research results.

The real-provider experiment, new natural dataset evaluation, and independent
human Gold review were NOT RUN because no credentials, approved unseen data,
or independent reviewer evidence was supplied.

## Failure analysis and limits

- Shared semantic omissions can pass dual formalization; a deterministic test
  demonstrates the resulting false certification after Gold is revealed.
- Timeout, unsupported mapping, and incomplete evidence become
  `INCONCLUSIVE`, never success or a count of zero.
- Enumeration is intentionally limited to one million assignments and is not a
  general mathematics engine.
- Real-model calls, new licensed natural data, and independent human review
  were unavailable in this execution and therefore were not run.
- Synthetic fixtures validate software mechanisms, not model reliability,
  external generalization, or human technical competency.

## AI assistance and authorship boundary

Codex implemented and documented this extension and its fixtures. That work is
AI-assisted implementation and is not evidence that the repository owner wrote
or independently mastered it. Human competency requires separate owner-run
exercises, explanation, modification, and review; none is claimed here.
