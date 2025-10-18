"""Reasoning (explanation) model wrapper.

Uses a text-to-text model (e.g., FLAN-T5) to generate short natural language
explanations for a given text and predicted label. If transformers/models are
unavailable, falls back to a template-based heuristic explanation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ReasoningResult:
    explanation: str


class ReasoningModel:
    def __init__(self, model_name: Optional[str] = None) -> None:
        self.model_name = model_name or settings.MODEL_REASONING
        self.pipeline = None
        try:
            from transformers import pipeline

            logger.info("Loading reasoning model: %s", self.model_name)
            self.pipeline = pipeline(
                "text2text-generation",
                model=self.model_name,
                device_map="auto",
            )
        except Exception as e:  # noqa: BLE001
            logger.warning(
                "Falling back to template-based reasoning (reason: %s)", str(e)
            )
            self.pipeline = None

    def explain(self, text: str, label: str) -> ReasoningResult:
        """Generate a concise explanation for a given text and predicted label."""
        prompt = (
            "Explain in 1-2 sentences why the following text may be {label}:\n"
            "Text: {text}\nExplanation:"
        ).format(label=label, text=text)

        if self.pipeline is None:
            # Fallback: simple template
            explanation = (
                f"The text is labeled as '{label}' based on its wording and context. "
                f"This is a heuristic explanation because the full model is unavailable."
            )
            return ReasoningResult(explanation=explanation)

        try:
            outs = self.pipeline(prompt, max_new_tokens=80, num_return_sequences=1)
            if isinstance(outs, list) and outs:
                # Different models return 'generated_text' or 'summary_text'
                generated = (
                    outs[0].get("generated_text")
                    or outs[0].get("summary_text")
                    or ""
                )
                explanation = generated.strip()
            else:
                explanation = "No explanation generated."
        except Exception as e:  # noqa: BLE001
            logger.error("Reasoning generation error: %s", str(e))
            explanation = "Explanation generation failed due to an internal error."
        return ReasoningResult(explanation=explanation)
