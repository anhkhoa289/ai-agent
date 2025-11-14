"""Main entry point for the Scrum Master AI Agent."""

import logging
import sys
from src.config import Config
from src.slack.bot import ScrumMasterBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("scrum_master.log")
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to start the Scrum Master bot."""
    try:
        # Load configuration
        config = Config.from_env()

        # Validate configuration
        is_valid, error_message = config.validate()
        if not is_valid:
            logger.error(f"Configuration error: {error_message}")
            logger.error("Please check your .env file and ensure all required variables are set.")
            sys.exit(1)

        logger.info("Configuration loaded successfully")
        logger.info(f"Using model: {config.model_name}")

        # Initialize and start bot
        bot = ScrumMasterBot(config)
        logger.info("Scrum Master AI Agent is starting...")

        # Start the bot (blocks until terminated)
        bot.start()

    except KeyboardInterrupt:
        logger.info("Shutting down Scrum Master bot...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
