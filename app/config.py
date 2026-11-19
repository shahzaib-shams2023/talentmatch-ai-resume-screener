from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "TalentMatch AI Resume Screening & Rubric Evaluator"
    host: str = "0.0.0.0"
    port: int = 8004
    environment: str = "development"

    min_passing_score: float = 70.0
    anonymize_default: bool = False

    llm_api_key: Optional[str] = None
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

