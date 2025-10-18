"""Classification service that wraps the BiasModel.

Responsible for applying thresholds, shaping the response, and logging.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from ..models.bias_model import BiasModel, BiasPrediction
from ..utils.config import settings


@dataclass
class ClassificationResult:
    label: str
    confidence: float
    scores: Dict[str, float]
    flagged: bool


class ClassificationService:
    def __init__(self, model: Optional[BiasModel] = None) -> None:
        self.model = model or BiasModel()

    def classify(self, text: str) -> ClassificationResult:
        pred: BiasPrediction = self.model.predict(text)
        flagged = pred.score >= settings.THRESHOLD_BIAS and pred.label != "neutral"
        return ClassificationResult(
            label=pred.label, confidence=pred.score, scores=pred.details, flagged=flagged
        )
