from __future__ import annotations

from dataclasses import dataclass

from .solver import compare_specifications, enumerate_specification, solve_z3
from .spec import FormalSpecification


@dataclass(frozen=True)
class AuditDecision:
    decision: str
    reason_code: str
    evidence: dict[str, object]


def audit(
    primary: FormalSpecification,
    secondary: FormalSpecification,
    *,
    proposed_answer: int | None = None,
    timeout_ms: int = 5_000,
) -> AuditDecision:
    comparison = compare_specifications(primary, secondary, timeout_ms=timeout_ms)
    if comparison.status == "INCONCLUSIVE":
        return AuditDecision("INCONCLUSIVE", "UNCOMPARABLE_OR_TIMEOUT", {"reason": comparison.reason})
    if comparison.status == "DIFFERENT":
        return AuditDecision(
            "FAIL", "SPECIFICATION_SET_DIFFERENCE",
            {"counterexample": comparison.counterexample, "count_equal": comparison.count_equal},
        )
    primary_result = solve_z3(primary, timeout_ms=timeout_ms)
    if primary_result.status != "COMPLETE":
        return AuditDecision("INCONCLUSIVE", "SOLVER_NOT_COMPLETE", {"reason": primary_result.reason})
    reference_result = enumerate_specification(primary)
    if reference_result.status != "COMPLETE":
        return AuditDecision("INCONCLUSIVE", "REFERENCE_NOT_COMPLETE", {"reason": reference_result.reason})
    if primary_result.solutions != reference_result.solutions:
        return AuditDecision(
            "INCONCLUSIVE", "SOLVER_DISAGREEMENT",
            {"z3_count": primary_result.count, "python_count": reference_result.count},
        )
    if proposed_answer is not None and proposed_answer != primary_result.count:
        return AuditDecision(
            "FAIL", "ANSWER_COUNT_MISMATCH",
            {"proposed_answer": proposed_answer, "verified_count": primary_result.count},
        )
    return AuditDecision(
        "PASS", "DEFINED_CHECKS_PASSED",
        {
            "verified_count": primary_result.count,
            "solver_cross_check": "Python enumeration and Z3 solution sets agree",
            "claim_boundary": "No claim of natural-language semantic fidelity",
        },
    )
