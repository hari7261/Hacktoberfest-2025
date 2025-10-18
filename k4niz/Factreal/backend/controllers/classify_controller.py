"""Controllers for classification endpoints.

Defines request/response schemas close to HTTP layer and calls services.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from ..services.api_service import ApiService


class ClassifyRequest(BaseModel):
    text: str = Field(..., description="Input text to analyze")


class ClassifyResponse(BaseModel):
    label: str
    confidence: float
    scores: dict
    flagged: bool
    explanation: str
    fact_check: dict | None = None


class ClassifyController:
    def __init__(self, api: ApiService | None = None) -> None:
        self.api = api or ApiService()

    def classify(self, req: ClassifyRequest) -> ClassifyResponse:
        analysis = self.api.analyze(req.text)
        payload = analysis.to_json()
        return ClassifyResponse(
            label=payload["classification"]["label"],
            confidence=payload["classification"]["confidence"],
            scores=payload["classification"]["scores"],
            flagged=payload["classification"]["flagged"],
            explanation=payload["explanation"],
            fact_check=payload.get("fact_check"),
        )
