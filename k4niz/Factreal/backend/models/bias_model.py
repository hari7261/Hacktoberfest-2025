"""Bias detection model wrapper.

Uses a Hugging Face zero-shot classification pipeline with a model like
"facebook/bart-large-mnli". If transformers or model weights are not available,
falls back to a simple keyword heuristic so the API remains usable.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class BiasPrediction:
    label: str
    score: float
    details: Dict[str, float]


class BiasModel:
    """Encapsulates a zero-shot bias classification pipeline.

    The candidate labels are fixed for now but can be extended easily by
    contributors. The class exposes a simple `predict(text)` method.
    """

    CANDIDATE_LABELS = ["neutral", "biased", "misleading", "propaganda"]

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or settings.MODEL_BIAS
        self.pipeline = None

        try:
            from transformers import pipeline  # defer import for faster startup

            logger.info("Loading zero-shot classification model: %s", self.model_name)
            self.pipeline = pipeline(
                "zero-shot-classification", model=self.model_name, device_map="auto"
            )
        except Exception as e:  # noqa: BLE001 broad but safe for offline demo
            logger.warning(
                "Falling back to heuristic bias detection (reason: %s)", str(e)
            )
            self.pipeline = None

    def predict(self, text: str) -> BiasPrediction:
        """Return the most likely label with confidence and per-label scores.

        If the transformer pipeline is unavailable, a keyword-based heuristic is used.
        """
        if not text.strip():
            return BiasPrediction(label="neutral", score=1.0, details={"neutral": 1.0})

        if self.pipeline is None:
            # Simple heuristic: look for charged words to flag as biased/propaganda
            charged = ["fake", "hoax", "never", "always", "disaster", "enemy", "traitor"]
            score = 0.7 if any(w in text.lower() for w in charged) else 0.2
            label = "propaganda" if score >= 0.65 else "neutral"
            return BiasPrediction(label=label, score=score, details={label: score})

        res: Dict[str, Any] = self.pipeline(
            sequences=[text], candidate_labels=self.CANDIDATE_LABELS
        )
        # transformers returns a dict when single input but we passed list; unwrap
        if isinstance(res, list):
            res = res[0]
        labels: List[str] = list(res.get("labels", []))
        scores: List[float] = list(res.get("scores", []))
        best_label = labels[0] if labels else "neutral"
        best_score = float(scores[0]) if scores else 0.0
        details = {lbl: float(scr) for lbl, scr in zip(labels, scores)}
        return BiasPrediction(label=best_label, score=best_score, details=details)
