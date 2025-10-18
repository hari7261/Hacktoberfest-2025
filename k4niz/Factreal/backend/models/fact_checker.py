"""Optional fact checker using Wikipedia and/or NewsAPI.

This module contains lightweight stubs that contributors can extend. By default,
it attempts a simple Wikipedia summary presence check and returns references.
If disabled or offline, it safely returns a neutral response.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..utils.config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class FactCheckResult:
    veracity: str  # e.g., "unknown", "supported", "disputed"
    sources: List[str]
    notes: Optional[str] = None


class FactChecker:
    def __init__(self) -> None:
        self.enabled = settings.ENABLE_FACT_CHECK
        self.news_api_key = settings.NEWS_API_KEY

    def check(self, text: str) -> FactCheckResult:
        """Perform a minimal fact check of the input text.

        - If disabled, returns unknown.
        - Try Wikipedia search/summary presence as a naive signal.
        - NewsAPI can be wired later using self.news_api_key.
        """
        if not self.enabled:
            return FactCheckResult(veracity="unknown", sources=[], notes="disabled")

        sources: List[str] = []

        # 1) Try NewsAPI if configured
        if self.news_api_key:
            try:
                import requests

                # Very naive query: take first 5 tokens; contributors can improve NLP later
                terms = [t for t in text.split() if t.isalpha()][:5]
                query = " ".join(terms) or text[:64]
                resp = requests.get(
                    "https://newsapi.org/v2/everything",
                    params={"q": query, "pageSize": 3, "sortBy": "relevancy"},
                    headers={"X-Api-Key": self.news_api_key},
                    timeout=6,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    for art in data.get("articles", [])[:3]:
                        url = art.get("url")
                        if url:
                            sources.append(url)
                    if sources:
                        return FactCheckResult(veracity="supported", sources=sources)
                else:
                    logger.info("NewsAPI non-200: %s", resp.status_code)
            except Exception as e:  # noqa: BLE001
                logger.info("NewsAPI unavailable: %s", str(e))

        # 2) Fallback to Wikipedia signal
        try:
            import wikipedia

            # Very naive: search for a keyword from text and fetch a summary
            terms = text.split()
            if not terms:
                return FactCheckResult(veracity="unknown", sources=[], notes="empty")
            query = terms[0]
            results = wikipedia.search(query)
            if results:
                title = results[0]
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    sources.append(page.url)
                    return FactCheckResult(veracity="supported", sources=sources)
                except Exception:  # noqa: BLE001 for robustness
                    pass
        except Exception as e:  # noqa: BLE001
            logger.info("Wikipedia check unavailable: %s", str(e))

        return FactCheckResult(veracity="unknown", sources=sources)
