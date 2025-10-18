"""Explainability service using ReasoningModel."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..models.reasoning_model import ReasoningModel, ReasoningResult


@dataclass
class Explanation:
    text: str


class ExplainabilityService:
    def __init__(self, model: Optional[ReasoningModel] = None) -> None:
        self.model = model or ReasoningModel()

    def explain(self, text: str, label: str) -> Explanation:
        res: ReasoningResult = self.model.explain(text, label)
        return Explanation(text=res.explanation)
