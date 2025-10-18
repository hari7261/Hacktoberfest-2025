"""Application configuration using Pydantic Settings (v2).

This centralizes environment-based settings for model names,
thresholds, and optional feature toggles. Safe defaults are provided
to keep the app usable even without external configuration.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Model identifiers (Hugging Face)
    MODEL_BIAS: str = Field(
        default="facebook/bart-large-mnli",
        description="Zero-shot classification model for bias detection.",
    )
    MODEL_REASONING: str = Field(
        default="google/flan-t5-base",
        description="Text-to-text model for explanation generation.",
    )

    # Thresholds
    THRESHOLD_BIAS: float = Field(
        default=0.55, description="Confidence threshold to mark text as flagged."
    )

    # Feature toggles
    ENABLE_FACT_CHECK: bool = Field(
        default=False, description="Enable optional external fact checking."
    )

    # External APIs
    NEWS_API_KEY: str | None = Field(default=None, description="NewsAPI key.")

    # Pydantic v2 settings configuration
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
