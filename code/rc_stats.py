#!/usr/bin/env python3
"""Recompute release-candidate statistics from de-identified cluster aggregates."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path


def _rows(path: Path) -> list[dict[str, int | str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))
    required = {
        "cluster_token",
        "case_count",
        "wrong_count",
        "base_fc_count",
        "audit_fc_count",
        "covered_count",
        "positive_count",
        "refutation_count",
        "withholding_count",
    }
    if not records or set(records[0]) != required:
        raise ValueError("cluster summary schema mismatch")
    converted: list[dict[str, int | str]] = []
    for row in records:
        item: dict[str, int | str] = {"cluster_token": row["cluster_token"]}
        item.update({key: int(value) for key, value in row.items() if key != "cluster_token"})
        numeric = [int(value) for key, value in item.items() if key != "cluster_token"]
        if any(value < 0 for value in numeric):
            raise ValueError("cluster counts must be nonnegative")
        if item["case_count"] != item["positive_count"] + item["refutation_count"] + item["withholding_count"]:
            raise ValueError("cluster decision counts do not sum")
        if item["covered_count"] != item["positive_count"] + item["refutation_count"]:
            raise ValueError("cluster coverage counts do not sum")
        if item["base_fc_count"] > item["wrong_count"] or item["audit_fc_count"] > item["wrong_count"]:
            raise ValueError("false certifications exceed wrong answers")
        converted.append(item)
    if len(converted) != 15 or len({row["cluster_token"] for row in converted}) != 15:
        raise ValueError("expected 15 unique clusters")
    return converted


def _ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        raise ValueError("zero denominator")
    return numerator / denominator


def _summarize(rows: list[dict[str, int | str]]) -> dict[str, float | int]:
    total = lambda key: sum(int(row[key]) for row in rows)
    wrong_rows = [row for row in rows if int(row["wrong_count"]) > 0]
    return {
        "case_count": total("case_count"),
        "cluster_count": len(rows),
        "wrong_cluster_count": len(wrong_rows),
        "wrong_count": total("wrong_count"),
        "base_fc_count": total("base_fc_count"),
        "audit_fc_count": total("audit_fc_count"),
        "case_base_fcr": _ratio(total("base_fc_count"), total("wrong_count")),
        "case_audit_fcr": _ratio(total("audit_fc_count"), total("wrong_count")),
        "cluster_base_fcr": sum(_ratio(int(row["base_fc_count"]), int(row["wrong_count"])) for row in wrong_rows) / len(wrong_rows),
        "cluster_audit_fcr": sum(_ratio(int(row["audit_fc_count"]), int(row["wrong_count"])) for row in wrong_rows) / len(wrong_rows),
        "covered_count": total("covered_count"),
        "positive_count": total("positive_count"),
        "refutation_count": total("refutation_count"),
        "withholding_count": total("withholding_count"),
        "case_coverage": _ratio(total("covered_count"), total("case_count")),
        "cluster_coverage": sum(_ratio(int(row["covered_count"]), int(row["case_count"])) for row in rows) / len(rows),
    }


def _percentile(values: list[float], probability: float) -> float:
    values = sorted(values)
    position = (len(values) - 1) * probability
    lower, upper = math.floor(position), math.ceil(position)
    if lower == upper:
        return values[lower]
    return values[lower] + (values[upper] - values[lower]) * (position - lower)


def analyze(path: Path, replicates: int = 100_000, seed: int = 20261021) -> dict[str, object]:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rows = _rows(path)
    summary = _summarize(rows)
    loco = []
    for omitted in rows:
        result = _summarize([row for row in rows if row is not omitted])
        loco.append({"omitted_cluster": omitted["cluster_token"], **result})
    randomizer = random.Random(seed)
    fields = ("case_base_fcr", "case_audit_fcr", "cluster_base_fcr", "cluster_audit_fcr", "case_coverage", "cluster_coverage")
    samples = {field: [] for field in fields}
    skipped = 0
    for _ in range(replicates):
        sample = [randomizer.choice(rows) for _ in rows]
        if sum(int(row["wrong_count"]) for row in sample) == 0:
            skipped += 1
            continue
        result = _summarize(sample)
        for field in fields:
            samples[field].append(float(result[field]))
    bootstrap = {
        field: {"p2_5": _percentile(values, 0.025), "p50": _percentile(values, 0.5), "p97_5": _percentile(values, 0.975)}
        for field, values in samples.items()
    }
    return {
        "status": "POST_HOC_EXPLORATORY",
        "seed": seed,
        "replicates_requested": replicates,
        "replicates_used": replicates - skipped,
        "replicates_skipped_zero_wrong_denominator": skipped,
        "summary": summary,
        "loco": loco,
        "bootstrap": bootstrap,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clusters", required=True, type=Path)
    parser.add_argument("--replicates", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=20261021)
    args = parser.parse_args()
    print(json.dumps(analyze(args.clusters, args.replicates, args.seed), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
