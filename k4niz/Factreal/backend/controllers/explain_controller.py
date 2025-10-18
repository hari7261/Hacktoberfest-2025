"""Controllers for explanation endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field

from ..services.explainability_service import ExplainabilityService


class ExplainRequest(BaseModel):
    text: str = Field(..., description="Input text to explain")
    label: str = Field(..., description="Label to explain, e.g., biased")


class ExplainResponse(BaseModel):
    explanation: str


class ExplainController:
    def __init__(self, service: ExplainabilityService | None = None) -> None:
        self.service = service or ExplainabilityService()

    def explain(self, req: ExplainRequest) -> ExplainResponse:
        res = self.service.explain(req.text, req.label)
        return ExplainResponse(explanation=res.text)
