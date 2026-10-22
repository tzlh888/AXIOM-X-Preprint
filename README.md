# AXIOM-X

## Development-Stage / Exploratory / Non-Confirmatory Research

**Development-Stage Evidence on False Certification in LLM-Generated Mathematical Constraints**

AXIOM-X is an exploratory individual AI/CS research project about a specific verification failure mode: a symbolic solver can correctly verify a formal specification that does not faithfully represent the natural-language problem. This repository is a public preprint and reproducibility packet, not evidence that AXIOM-X is a generally reliable or independently validated system.

## Evidence summary

| Study | Scope | Result | Boundary |
|---|---:|---|---|
| A — real Development pilot | 20 problems | 20/20 initial answers correct; natural false-certification rate `0/0`, **undefined** | No natural wrong-answer opportunity was observed |
| B — controlled challenge | 40 cases, 15 base-problem clusters | 17 wrong-answer opportunities; Base FC 13/17; reference-backed audit FC 1/17 | Gold-referenced construction; not a natural deployment estimate |
| B — decision behavior | 40 cases | Audit decision coverage 17/40; 23/40 withheld | Lower FC coincided with substantial withholding |
| C — author review | 10 Development cases | 9/10 automatic matches; 10/10 only after same-author post-Gold adjudication | Independent human reviews: 0 |

## Important methodological boundary

In Study B, the Primary is a deterministic mutation of a Gold-derived specification. The Secondary is normally the unmodified Gold-derived specification, except in the shared-error condition. Study B does **not** use an independently generated LLM Secondary. Its controlled result is therefore affected by reference leakage, oracle assistance, and label endogeneity; it must not be interpreted as an estimate of natural LLM error frequency or deployed audit reliability.

## Research questions

The paper studies answer correctness, specification fidelity, false certification under controlled perturbations, audit withholding, and shared Primary/Secondary semantic errors. The central broad-reliability claim remains inconclusive.

## Known limitations

- Gold correctness has not been independently established.
- Natural-language-to-formal-specification equivalence has not been established.
- Held-out contamination remains `HIGH_UNRESOLVED`; there is no credible Held-out generalization result.
- Natural-error reliability is not estimable from Study A because its error-opportunity denominator is zero.
- Study C is an author evidence-provenance exercise, not independent blind review.
- The model alias is dynamic, so longitudinal response reproduction is not guaranteed.

## Paper and figures

- [Full preprint](paper_preprint.md)
- [Architecture](figures_rc2/fig_architecture.svg)
- [Evidence layers](figures_rc2/fig_evidence_layers.svg)
- [False-certification comparison](figures_rc2/fig_fc_comparison.svg)
- [Decision breakdown](figures_rc2/fig_decision_breakdown.svg)
- [Perturbation categories](figures_rc2/fig_perturbations.svg)
- [Cluster-aware results](figures_rc2/fig_cluster_results.svg)
- [Leave-one-cluster-out sensitivity](figures_rc2/fig_loco.svg)

## Reproducibility

Python 3.11+ and the standard library are sufficient for the aggregate statistical recomputation:

```bash
python3 code/rc_stats.py --clusters data/cluster_summary.csv
```

The included CSV files contain only public aggregate/case-level derived material. They do not contain private questions, Gold answers, model responses, reviewer identities, or private ledgers. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md), [METHOD.md](METHOD.md), [LIMITATIONS.md](LIMITATIONS.md), and [manifest_sha256.txt](manifest_sha256.txt).

## Research integrity and AI disclosure

ChatGPT and other AI tools assisted with code, analysis, field interpretation, and writing. The author retains responsibility for all claims and release decisions. The structured author-review ledger did not record all wording/field-guidance assistance; this is disclosed at report level and was not retroactively inserted into frozen evidence. See [DISCLOSURE.md](DISCLOSURE.md) and [PROVENANCE.md](PROVENANCE.md).

## Citation

Until an archival identifier exists, cite the repository release and version tag:

> @tzlh888. *AXIOM-X: Development-Stage Evidence on False Certification in LLM-Generated Mathematical Constraints*. Version `v0.1.0-development`, 2026.

## License and reuse

Copyright © 2026 @tzlh888. No additional reuse license is granted with this repository. Contact the author before redistribution, adaptation, or other reuse beyond rights provided by applicable law.
