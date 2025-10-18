"""High-level API service orchestrating preprocessing, classification,
explanation, and optional fact checking.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

from .preprocessing_service import preprocess_text
from .classification_service import ClassificationService, ClassificationResult
from .explainability_service import ExplainabilityService
from ..models.fact_checker import FactChecker, FactCheckResult
from ..utils.config import settings


@dataclass
class FullAnalysis:
    classification: ClassificationResult
    explanation: str
    fact_check: Dict[str, Any] | None

    def to_json(self) -> Dict[str, Any]:
        payload = {
            "classification": asdict(self.classification),
            "explanation": self.explanation,
        }
        if self.fact_check is not None:
            payload["fact_check"] = self.fact_check
        return payload


class ApiService:
    def __init__(
        self,
        classifier: Optional[ClassificationService] = None,
        explainer: Optional[ExplainabilityService] = None,
        fact_checker: Optional[FactChecker] = None,
    ) -> None:
        self.classifier = classifier or ClassificationService()
        self.explainer = explainer or ExplainabilityService()
        self.fact_checker = fact_checker or FactChecker()

    def analyze(self, text: str) -> FullAnalysis:
        pre = preprocess_text(text)
        cls: ClassificationResult = self.classifier.classify(pre.text)
        exp = self.explainer.explain(pre.text, cls.label)

        fc: Dict[str, Any] | None = None
        if settings.ENABLE_FACT_CHECK:
            fr: FactCheckResult = self.fact_checker.check(pre.text)
            fc = {
                "veracity": fr.veracity,
                "sources": fr.sources,
                "notes": fr.notes,
            }

        return FullAnalysis(classification=cls, explanation=exp.text, fact_check=fc)
