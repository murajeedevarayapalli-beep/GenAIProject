from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Delivery Support Resolution Agent"
    app_env: str = "development"
    debug: bool = True
    api_prefix: str = "/api"
    secret_key: str = "dev-secret-key"
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = ""
    postgres_url: str = "postgresql://postgres:postgres@localhost:5432/delivery_agent"
    redis_url: str = "redis://localhost:6379/0"
    chroma_persist_directory: str = "./data/chroma"
    rate_limit_per_minute: int = 60
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
