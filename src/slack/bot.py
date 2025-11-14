"""Slack bot implementation using Slack Bolt framework."""

import logging
from typing import Optional
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from ..agent.scrum_master import ScrumMasterAgent
from ..config import Config
from ..storage.database import Database

logger = logging.getLogger(__name__)


class ScrumMasterBot:
    """Slack bot for Scrum Master AI Agent."""

    def __init__(self, config: Config):
        """Initialize the Slack bot."""
        self.config = config
        self.app = App(
            token=config.slack_bot_token,
            signing_secret=config.slack_signing_secret
        )
        self.agent = ScrumMasterAgent(
            api_key=config.anthropic_api_key,
            model_name=config.model_name
        )
        self.db = Database(config.database_url)
        self._register_handlers()

    def _register_handlers(self):
        """Register Slack event handlers."""

        # Direct messages and mentions
        @self.app.event("app_mention")
        def handle_mention(event, say, client):
            """Handle when bot is mentioned."""
            self._handle_message(event, say, client)

        @self.app.event("message")
        def handle_dm(event, say, client):
            """Handle direct messages."""
            # Only respond to DMs (no channel or subtype)
            if event.get("channel_type") == "im" and not event.get("subtype"):
                self._handle_message(event, say, client)

        # Slash commands
        @self.app.command("/standup")
        def handle_standup_command(ack, command, client):
            """Handle /standup command."""
            ack()
            self._handle_standup(command, client)

        @self.app.command("/sprint-planning")
        def handle_sprint_planning(ack, command, client):
            """Handle /sprint-planning command."""
            ack()
            self._handle_sprint_planning(command, client)

        @self.app.command("/retrospective")
        def handle_retrospective(ack, command, client):
            """Handle /retrospective command."""
            ack()
            self._handle_retrospective(command, client)

        @self.app.command("/estimate")
        def handle_estimate(ack, command, client):
            """Handle /estimate command for story point estimation."""
            ack()
            self._handle_estimate(command, client)

        # Shortcuts for interactive features
        @self.app.shortcut("start_standup")
        def handle_standup_shortcut(ack, shortcut, client):
            """Handle standup shortcut."""
            ack()
            self._open_standup_modal(shortcut, client)

        # View submissions (modals)
        @self.app.view("standup_submission")
        def handle_standup_submission(ack, view, client):
            """Handle standup modal submission."""
            ack()
            self._process_standup_submission(view, client)

    def _handle_message(self, event, say, client):
        """Handle incoming messages."""
        try:
            user_id = event["user"]
            channel_id = event["channel"]
            text = event["text"]

            # Remove bot mention from text
            text = text.replace(f"<@{self.app.client.auth_test()['user_id']}>", "").strip()

            # Get user info for context
            user_info = client.users_info(user=user_id)
            user_name = user_info["user"]["real_name"]

            # Build conversation ID (per channel)
            conversation_id = f"slack_{channel_id}"

            # Get team/sprint context from database
            context = self._get_context(channel_id)
            context["user_name"] = user_name

            # Get response from agent
            response = self.agent.get_response(
                user_message=text,
                context=context,
                conversation_id=conversation_id
            )

            # Send response
            say(response)

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            say("Sorry, I encountered an error processing your message. Please try again.")

    def _handle_standup(self, command, client):
        """Handle standup command."""
        try:
            channel_id = command["channel_id"]
            user_id = command["user_id"]

            # Open modal for standup input
            client.views_open(
                trigger_id=command["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "standup_submission",
                    "title": {"type": "plain_text", "text": "Daily Standup"},
                    "submit": {"type": "plain_text", "text": "Submit"},
                    "blocks": [
                        {
                            "type": "input",
                            "block_id": "yesterday_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "yesterday_input",
                                "multiline": True,
                                "placeholder": {"type": "plain_text", "text": "What did you work on yesterday?"}
                            },
                            "label": {"type": "plain_text", "text": "Yesterday"}
                        },
                        {
                            "type": "input",
                            "block_id": "today_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "today_input",
                                "multiline": True,
                                "placeholder": {"type": "plain_text", "text": "What will you work on today?"}
                            },
                            "label": {"type": "plain_text", "text": "Today"}
                        },
                        {
                            "type": "input",
                            "block_id": "blockers_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "blockers_input",
                                "multiline": True,
                                "placeholder": {"type": "plain_text", "text": "Any blockers or impediments?"}
                            },
                            "label": {"type": "plain_text", "text": "Blockers"},
                            "optional": True
                        }
                    ],
                    "private_metadata": channel_id
                }
            )
        except Exception as e:
            logger.error(f"Error handling standup command: {e}")

    def _process_standup_submission(self, view, client):
        """Process standup modal submission."""
        try:
            values = view["state"]["values"]
            channel_id = view["private_metadata"]
            user_id = view["user"]["id"]

            yesterday = values["yesterday_block"]["yesterday_input"]["value"]
            today = values["today_block"]["today_input"]["value"]
            blockers = values["blockers_block"]["blockers_input"]["value"] or "None"

            # Get user info
            user_info = client.users_info(user=user_id)
            user_name = user_info["user"]["real_name"]

            # Save to database
            self.db.save_standup_update(channel_id, user_id, user_name, yesterday, today, blockers)

            # Post update to channel
            message = f"*Standup Update from {user_name}* :memo:\n\n*Yesterday:*\n{yesterday}\n\n*Today:*\n{today}\n\n*Blockers:*\n{blockers}"
            client.chat_postMessage(channel=channel_id, text=message)

        except Exception as e:
            logger.error(f"Error processing standup submission: {e}")

    def _handle_sprint_planning(self, command, client):
        """Handle sprint planning command."""
        try:
            channel_id = command["channel_id"]
            text = command.get("text", "")

            context = self._get_context(channel_id)

            if text:
                prompt = f"Help with sprint planning: {text}"
            else:
                prompt = "I'd like help with sprint planning. What should we discuss?"

            response = self.agent.get_response(
                user_message=prompt,
                context=context,
                conversation_id=f"slack_{channel_id}"
            )

            client.chat_postMessage(channel=channel_id, text=response)

        except Exception as e:
            logger.error(f"Error handling sprint planning: {e}")

    def _handle_retrospective(self, command, client):
        """Handle retrospective command."""
        try:
            channel_id = command["channel_id"]

            # Get sprint data
            context = self._get_context(channel_id)

            prompt = "Let's start a retrospective. What went well, what didn't, and what can we improve?"

            response = self.agent.get_response(
                user_message=prompt,
                context=context,
                conversation_id=f"slack_{channel_id}_retro"
            )

            client.chat_postMessage(channel=channel_id, text=response)

        except Exception as e:
            logger.error(f"Error handling retrospective: {e}")

    def _handle_estimate(self, command, client):
        """Handle story point estimation."""
        try:
            channel_id = command["channel_id"]
            user_story = command.get("text", "")

            if not user_story:
                client.chat_postMessage(
                    channel=channel_id,
                    text="Please provide a user story to estimate. Usage: `/estimate <user story>`"
                )
                return

            response = self.agent.suggest_story_points(user_story)
            client.chat_postMessage(channel=channel_id, text=response)

        except Exception as e:
            logger.error(f"Error handling estimate: {e}")

    def _open_standup_modal(self, shortcut, client):
        """Open standup modal from shortcut."""
        # Similar to _handle_standup but triggered from message shortcut
        pass

    def _get_context(self, channel_id: str) -> dict:
        """Get current context for a channel (sprint info, team data, etc.)."""
        # This would fetch from database
        return {
            "channel_id": channel_id,
            "sprint_data": self.db.get_current_sprint(channel_id),
            "team_velocity": self.db.get_team_velocity(channel_id),
        }

    def start(self):
        """Start the bot using Socket Mode."""
        handler = SocketModeHandler(self.app, self.config.slack_app_token)
        logger.info("Starting Scrum Master bot...")
        handler.start()
