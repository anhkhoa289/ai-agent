"""
Slack integration client
"""
from typing import List, Dict, Any, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from ..config.settings import settings


class SlackClient:
    """Client for interacting with Slack API"""

    def __init__(self):
        """Initialize Slack client"""
        self.client: Optional[WebClient] = None
        if settings.SLACK_BOT_TOKEN:
            self.client = WebClient(token=settings.SLACK_BOT_TOKEN)

    def send_message(self, channel: str, text: str, blocks: Optional[List[Dict]] = None) -> bool:
        """
        Send message to Slack channel

        Args:
            channel: Channel ID or name
            text: Message text
            blocks: Optional blocks for rich formatting

        Returns:
            Success status
        """
        if not self.client:
            raise ValueError("Slack client not configured")

        try:
            kwargs = {"channel": channel, "text": text}
            if blocks:
                kwargs["blocks"] = blocks

            response = self.client.chat_postMessage(**kwargs)
            return response["ok"]
        except SlackApiError as e:
            print(f"Error sending message: {e}")
            return False

    def send_standup_reminder(self, channel: str, team_members: List[str]) -> bool:
        """
        Send standup reminder to team

        Args:
            channel: Channel ID
            team_members: List of user IDs to mention

        Returns:
            Success status
        """
        mentions = " ".join([f"<@{member}>" for member in team_members])
        text = f"🌅 Good morning {mentions}! Time for our daily standup. Please share:\n" \
               "1️⃣ What did you do yesterday?\n" \
               "2️⃣ What will you do today?\n" \
               "3️⃣ Any blockers?"

        return self.send_message(channel, text)

    def collect_standup_updates(self, channel: str, thread_ts: str) -> List[Dict[str, Any]]:
        """
        Collect standup updates from thread

        Args:
            channel: Channel ID
            thread_ts: Thread timestamp

        Returns:
            List of updates
        """
        if not self.client:
            raise ValueError("Slack client not configured")

        try:
            response = self.client.conversations_replies(
                channel=channel,
                ts=thread_ts
            )

            updates = []
            for message in response["messages"][1:]:  # Skip the parent message
                updates.append({
                    "user": message.get("user"),
                    "text": message.get("text"),
                    "timestamp": message.get("ts")
                })

            return updates
        except SlackApiError as e:
            print(f"Error collecting updates: {e}")
            return []

    def send_sprint_report(self, channel: str, report: str) -> bool:
        """
        Send sprint report to channel

        Args:
            channel: Channel ID
            report: Formatted report text

        Returns:
            Success status
        """
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📊 Sprint Report"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": report
                }
            }
        ]

        return self.send_message(channel, "Sprint Report", blocks)

    def get_channel_members(self, channel: str) -> List[str]:
        """
        Get list of members in a channel

        Args:
            channel: Channel ID

        Returns:
            List of user IDs
        """
        if not self.client:
            raise ValueError("Slack client not configured")

        try:
            response = self.client.conversations_members(channel=channel)
            return response["members"]
        except SlackApiError as e:
            print(f"Error getting channel members: {e}")
            return []

    def create_poll(self, channel: str, question: str, options: List[str]) -> Optional[str]:
        """
        Create a poll in channel

        Args:
            channel: Channel ID
            question: Poll question
            options: List of options

        Returns:
            Message timestamp or None
        """
        if not self.client:
            raise ValueError("Slack client not configured")

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{question}*"
                }
            }
        ]

        for i, option in enumerate(options):
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{i+1}️⃣ {option}"
                }
            })

        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=question,
                blocks=blocks
            )
            return response["ts"]
        except SlackApiError as e:
            print(f"Error creating poll: {e}")
            return None
