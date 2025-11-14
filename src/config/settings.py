"""
Application configuration settings
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""

    # AI/LLM Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Integration Settings
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_APP_TOKEN: str = os.getenv("SLACK_APP_TOKEN", "")
    JIRA_URL: str = os.getenv("JIRA_URL", "")
    JIRA_EMAIL: str = os.getenv("JIRA_EMAIL", "")
    JIRA_API_TOKEN: str = os.getenv("JIRA_API_TOKEN", "")
    TRELLO_API_KEY: str = os.getenv("TRELLO_API_KEY", "")
    TRELLO_TOKEN: str = os.getenv("TRELLO_TOKEN", "")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./scrum_agent.db")

    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present"""
        required = ["OPENAI_API_KEY", "SLACK_BOT_TOKEN"]
        missing = [key for key in required if not getattr(cls, key)]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return True


settings = Settings()
