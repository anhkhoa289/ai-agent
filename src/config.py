"""Configuration management for the Scrum Master AI Agent."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Application configuration."""

    # Slack configuration
    slack_bot_token: str
    slack_app_token: str
    slack_signing_secret: str

    # AI configuration
    anthropic_api_key: str
    model_name: str = "claude-sonnet-4-5-20250929"

    # Database configuration
    database_url: str = "sqlite:///scrum_master.db"

    # Feature flags
    enable_daily_standup: bool = True
    enable_sprint_planning: bool = True
    enable_retrospectives: bool = True

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            slack_bot_token=os.getenv("SLACK_BOT_TOKEN", ""),
            slack_app_token=os.getenv("SLACK_APP_TOKEN", ""),
            slack_signing_secret=os.getenv("SLACK_SIGNING_SECRET", ""),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            model_name=os.getenv("MODEL_NAME", "claude-sonnet-4-5-20250929"),
            database_url=os.getenv("DATABASE_URL", "sqlite:///scrum_master.db"),
        )

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate configuration."""
        if not self.slack_bot_token:
            return False, "SLACK_BOT_TOKEN is required"
        if not self.slack_app_token:
            return False, "SLACK_APP_TOKEN is required"
        if not self.slack_signing_secret:
            return False, "SLACK_SIGNING_SECRET is required"
        if not self.anthropic_api_key:
            return False, "ANTHROPIC_API_KEY is required"
        return True, None
