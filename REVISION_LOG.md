# AXIOM-X Preprint RC2 — Targeted Revision Log

RC2 is derived from RC1 SHA-256 `48174e4fa024b130bff480cc565c501194080cefc63a016da00563fe989e23a6`. RC1 and earlier papers remain unchanged.

| Location | RC1 scientific risk | RC2 correction | Evidence | Remaining issue |
|---|---|---|---|---|
| Abstract and RQ2 | “secondary audit” could imply an independent LLM channel | Names Study B a Gold-referenced, reference-backed condition | `src/probe_v2.py:928–950`; frozen preregistration | Natural independent-Secondary effect untested |
| Architecture and Figures 1–2 | Study A and Study B Secondary provenance visually conflated | Separates model-generated Study A from Gold-derived Study B | public execution code and protocol | Study A has zero natural error opportunities |
| Methods 6.2.1 | Gold-derived Secondary disclosed but methodological consequences understated | Adds direct reference leakage, oracle assistance, label endogeneity, and rationale | public execution code; sample-plan protocol | Gold lacks independent blind validation |
| Methods 6.2.2–6.2.3 | Source checker and `PASS` could be read too broadly | Specifies regex-derived expectations, solution-set comparison, exact FAIL/PASS/INCONCLUSIVE rules, and negative meaning of PASS | `condition_audit.py`, `specification_normalizer.py`, `translation_audit.py` | Unsupported language patterns can be missed |
| Results 7.2 and Figures 3–7 | Controlled effect could be attributed to an independent translator | Labels every effect and sensitivity result reference-backed | formal review and post-hoc report | External validity remains untested |
| Failure modes and Discussion | “cross-translation” and prompt-diversity wording did not match Study B construction | Recasts as specification agreement under a Gold-derived channel | public execution code | Heterogeneous translator baseline absent |
| Threats to Validity | Oracle/reference-label dependence not isolated as a primary threat | Adds dedicated reference leakage and label-endogeneity threat | execution and sample-plan code | Cannot be repaired with existing data |
| Conclusion | “demonstrates” risked generalization beyond the controlled condition | Limits conclusion to a recorded mechanism under Gold reference support | Study A/B/C evidence map | Broad reliability remains inconclusive |
| Disclosure | Synthetic Reviewer status and human accountability could be clearer | States synthetic tests are not human evidence and author retains full responsibility | public protocol/status documents | Independent human review remains zero |
| References | Local consistency could be mistaken for publisher revalidation | Retains 17 entries and records the final official-source cross-check | local BibTeX, reference register, and official public pages | Targeted rather than systematic literature review |

No frozen result, denominator, experiment, or historic ledger was changed. RC2 changes interpretation and publication packaging only.
