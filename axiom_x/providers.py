from __future__ import annotations

import json
import os
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Protocol

from .spec import FormalSpecification


@dataclass(frozen=True)
class GenerationRecord:
    provider: str
    model: str
    generation_id: str
    generated_at: str
    specification: FormalSpecification


class Provider(Protocol):
    def generate(self, problem_id: str, problem_text: str) -> GenerationRecord: ...


class FixtureProvider:
    def __init__(self, name: str, fixtures: dict[str, dict[str, Any]]) -> None:
        self.name = name
        self.fixtures = fixtures

    def generate(self, problem_id: str, problem_text: str) -> GenerationRecord:
        del problem_text
        raw = json.loads(json.dumps(self.fixtures[problem_id]))
        raw["generation_id"] = f"{self.name}-{problem_id}"
        specification = FormalSpecification.from_dict(raw)
        return GenerationRecord(
            provider=self.name, model="deterministic-fixture-v1",
            generation_id=specification.generation_id,
            generated_at="1970-01-01T00:00:00+00:00", specification=specification,
        )


class OpenAICompatibleProvider:
    """Optional JSON-only provider. It never receives Gold, labels, or another path's output."""

    def __init__(self, *, model: str, api_url: str = "https://api.openai.com/v1/chat/completions") -> None:
        self.model, self.api_url = model, api_url

    def generate(self, problem_id: str, problem_text: str) -> GenerationRecord:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured; real LLM experiment NOT RUN")
        generation_id = str(uuid.uuid4())
        prompt = (
            "Return only a JSON AXIOM-X finite-domain specification. Supported constraint kinds: "
            "all_different, equal, not_equal, sum_equal, count_equal, number_mod, less_than. "
            f"problem_id={problem_id}. Problem: {problem_text}"
        )
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0,
        }).encode()
        request = urllib.request.Request(
            self.api_url, data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.load(response)
        raw = json.loads(body["choices"][0]["message"]["content"])
        raw["generation_id"] = generation_id
        specification = FormalSpecification.from_dict(raw)
        return GenerationRecord(
            provider="openai-compatible", model=self.model, generation_id=generation_id,
            generated_at=datetime.now(timezone.utc).isoformat(), specification=specification,
        )


def generate_isolated(
    problem_id: str, problem_text: str, primary: Provider, secondary: Provider
) -> tuple[GenerationRecord, GenerationRecord]:
    """Two fresh calls receive only public problem fields; neither call receives Gold or peer state."""
    return primary.generate(problem_id, problem_text), secondary.generate(problem_id, problem_text)
