"""
Slack bot interface for interacting with scrum master AI
"""
import re
from typing import Dict, Any
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from ..orchestrator import CrewOrchestrator
from ..config.settings import settings


class ScrumMasterBot:
    """Slack bot for scrum master AI agent"""

    def __init__(self):
        """Initialize Slack bot"""
        self.orchestrator = CrewOrchestrator()
        self.client = None

        if settings.SLACK_APP_TOKEN:
            self.client = SocketModeClient(
                app_token=settings.SLACK_APP_TOKEN,
                web_client=self.orchestrator.slack_client.client
            )

    def start(self):
        """Start the bot"""
        if not self.client:
            raise ValueError("Slack client not configured")

        # Register event handlers
        self.client.socket_mode_request_listeners.append(self._handle_events)

        print("⚡️ Scrum Master Bot is running!")
        self.client.connect()

    def _handle_events(self, client: SocketModeClient, req: SocketModeRequest):
        """Handle incoming Slack events"""
        if req.type == "events_api":
            # Acknowledge the event
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

            # Process the event
            event = req.payload["event"]
            self._process_event(event)

        elif req.type == "slash_commands":
            # Handle slash commands
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

            command = req.payload
            self._process_command(command)

    def _process_event(self, event: Dict[str, Any]):
        """Process Slack event"""
        event_type = event.get("type")

        if event_type == "app_mention":
            self._handle_mention(event)
        elif event_type == "message":
            self._handle_message(event)

    def _handle_mention(self, event: Dict[str, Any]):
        """Handle bot mention"""
        text = event.get("text", "").lower()
        channel = event.get("channel")
        user = event.get("user")

        # Parse intent from message
        if "standup" in text:
            context = {
                "channel": channel,
                "team_members": self.orchestrator.slack_client.get_channel_members(channel)
            }
            self.orchestrator.run_daily_standup(context)

        elif "sprint" in text and "status" in text:
            context = {
                "channel": channel,
                "board_id": self._get_board_id(channel)
            }
            result = self.orchestrator.track_sprint_progress(context)
            if result.get("formatted_report"):
                self.orchestrator.slack_client.send_message(channel, result["formatted_report"])

        elif "report" in text:
            context = {
                "channel": channel,
                "board_id": self._get_board_id(channel)
            }
            self.orchestrator.generate_report("sprint_summary", context)

        elif "help" in text:
            self._send_help_message(channel)

        else:
            self.orchestrator.slack_client.send_message(
                channel,
                "I'm your Scrum Master AI! Mention me with 'help' to see what I can do."
            )

    def _handle_message(self, event: Dict[str, Any]):
        """Handle regular message"""
        # Only process messages in threads or direct messages
        if event.get("thread_ts") or event.get("channel_type") == "im":
            # Process as potential standup update
            pass

    def _process_command(self, command: Dict[str, Any]):
        """Process slash command"""
        command_text = command.get("command", "")
        channel = command.get("channel_id")

        if command_text == "/standup":
            context = {
                "channel": channel,
                "team_members": self.orchestrator.slack_client.get_channel_members(channel)
            }
            self.orchestrator.run_daily_standup(context)

        elif command_text == "/sprint-status":
            context = {
                "channel": channel,
                "board_id": self._get_board_id(channel)
            }
            self.orchestrator.track_sprint_progress(context)

        elif command_text == "/sprint-report":
            context = {
                "channel": channel,
                "board_id": self._get_board_id(channel)
            }
            self.orchestrator.generate_report("sprint_summary", context)

        elif command_text == "/retrospective":
            context = {
                "channel": channel,
                "board_id": self._get_board_id(channel)
            }
            self.orchestrator.generate_report("retrospective", context)

    def _send_help_message(self, channel: str):
        """Send help message"""
        help_text = """
*Scrum Master AI - Commands*

*Slash Commands:*
• `/standup` - Start daily standup
• `/sprint-status` - Get current sprint status
• `/sprint-report` - Generate sprint report
• `/retrospective` - Start retrospective

*Mention Commands:*
• `@ScrumBot standup` - Start standup
• `@ScrumBot sprint status` - Get sprint status
• `@ScrumBot report` - Generate report
• `@ScrumBot help` - Show this message

I can help you with:
✅ Daily standup facilitation
✅ Sprint progress tracking
✅ Report generation
✅ Retrospective facilitation
"""
        self.orchestrator.slack_client.send_message(channel, help_text)

    def _get_board_id(self, channel: str) -> str:
        """Get board ID for channel (placeholder - should be configured per channel)"""
        # This should be stored in a database or configuration
        # For now, return a placeholder
        return "default-board"


def main():
    """Main entry point for Slack bot"""
    bot = ScrumMasterBot()
    bot.start()


if __name__ == "__main__":
    main()
