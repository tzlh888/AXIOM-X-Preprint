# AXIOM-X Preprint RC2 — Method-to-Code Check

The public Study B implementation shows that Primary is a deterministic mutation of project Gold and Secondary is the unmodified Gold-derived specification except in shared-error cases. The audit compares implemented source-text patterns and canonical or complete finite solution sets; it returns `FAIL` for an implemented source discrepancy, `PASS` only for equivalent specifications with both implemented coverage checks consistent, and otherwise `INCONCLUSIVE`. Only `PASS` preserves the Base decision.

This is a Gold-referenced, reference-backed controlled condition. It is not an independent LLM Secondary evaluation. A `PASS` means that implemented checks found no conflict; it does not prove project Gold correctness or natural-language equivalence.

## Public code identities

| Public implementation file | SHA-256 |
|---|---|
| `src/probe_v2.py` | `e45d7645668a8850eecc685b02f0c7eb8c814d9ab5cf29126dec313076bf1dce` |
| `src/axiom_x/condition_audit.py` | `85cc315eae37d5d2d3a73983967c64ce070a1ef035f2f1f11dcd965e6559563f` |
| `src/axiom_x/translation_audit.py` | `e6279e37018787801bb04dc35486760824b80af7ad13eadd3bb37d037bd3e2d6` |
| `src/axiom_x/specification_normalizer.py` | `22502e7d4c7c564e7984babace90d9416e0ebce19387e9d1da8f9f32240ceb23` |

## Correspondence findings

1. `probe_v2.py:928–930` constructs Primary by mutating `record.gold_specification`; Secondary is the same mutation only for shared error and otherwise the unmodified Gold specification. No LLM translation call occurs in this loop.
2. `condition_audit.py:82–300` derives supported expectations from source text with regular expressions. It cannot enumerate every unsupported language pattern.
3. `specification_normalizer.py:99–273` uses canonical fingerprints and, when needed, complete finite solution-set comparison. Equal counts alone do not establish equivalence.
4. `translation_audit.py:102–169` implements the stated FAIL/PASS/INCONCLUSIVE triage. Only PASS preserves the Base result; FAIL and INCONCLUSIVE yield Unknown.

Residual risks are independent Gold validity, unestablished source equivalence, shared-error survival, and the absence of an independent translator evaluation on natural errors.

**Result: METHOD_TO_CODE_MATCH_WITH_DISCLOSED_LIMITS.**
