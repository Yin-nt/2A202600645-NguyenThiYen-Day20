"""Application configuration.

Keep config small and explicit. Do not read environment variables directly in agents.
"""

from functools import lru_cache
from os import getenv

from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Runtime settings loaded from environment variables or `.env`."""

    app_env: str = Field(default_factory=lambda: getenv("APP_ENV", "local"))
    log_level: str = Field(default_factory=lambda: getenv("LOG_LEVEL", "INFO"))

    openai_api_key: str | None = Field(default_factory=lambda: getenv("OPENAI_API_KEY"))
    openai_model: str = Field(default_factory=lambda: getenv("OPENAI_MODEL", "gpt-4o-mini"))

    langsmith_api_key: str | None = Field(default_factory=lambda: getenv("LANGSMITH_API_KEY"))
    langsmith_project: str = Field(
        default_factory=lambda: getenv("LANGSMITH_PROJECT", "multi-agent-research-lab")
    )

    tavily_api_key: str | None = Field(default_factory=lambda: getenv("TAVILY_API_KEY"))

    max_iterations: int = Field(
        default_factory=lambda: int(getenv("MAX_ITERATIONS", "6")),
        ge=1,
        le=20,
    )
    timeout_seconds: int = Field(
        default_factory=lambda: int(getenv("TIMEOUT_SECONDS", "60")),
        ge=5,
        le=600,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()
