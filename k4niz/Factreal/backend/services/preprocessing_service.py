"""Text preprocessing service.

Keeps preprocessing minimal and transparent. Contributors can add more advanced
normalization, token cleaning, or language detection here.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PreprocessResult:
    text: str


def preprocess_text(text: str) -> PreprocessResult:
    """Trim and normalize whitespace for now.

    Notes: Minimal by design to avoid altering semantics before classification.
    """
    cleaned = " ".join(text.split())
    return PreprocessResult(text=cleaned)
