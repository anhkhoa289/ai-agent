"""Configuration management for Scrum Master AI Agent."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # API Settings
    app_name: str = "Scrum Master AI Agent"
    app_version: str = "0.1.0"
    debug: bool = False
    api_prefix: str = "/api/v1"

    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000

    # Slack Configuration
    slack_bot_token: Optional[str] = None
    slack_app_token: Optional[str] = None
    slack_signing_secret: Optional[str] = None

    # AI Configuration - LLM Provider Settings
    # Supported providers: anthropic, openai, gemini, groq, ollama
    llm_provider: str = "anthropic"  # Choose: anthropic, openai, gemini, groq, ollama

    # API Keys for different providers (only the one matching llm_provider is required)
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None  # For Gemini
    groq_api_key: Optional[str] = None

    # Model configuration
    # Anthropic: claude-sonnet-4-5-20250929, claude-3-5-sonnet-20241022, claude-3-opus-20240229
    # OpenAI: gpt-4o, gpt-4o-mini, gpt-4-turbo
    # Gemini: gemini-1.5-pro, gemini-1.5-flash, gemini-2.0-flash-exp
    # Groq: llama-3.1-70b-versatile, mixtral-8x7b-32768
    # Ollama: llama2, mistral, codellama (for local models)
    model_name: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    temperature: float = 0.7

    # Database Configuration
    database_url: str = "sqlite:///./scrum_master.db"

    # Feature Flags
    enable_daily_standup: bool = True
    enable_sprint_planning: bool = True
    enable_retrospectives: bool = True

    # CORS Settings
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]


# Global settings instance
settings = Settings()
