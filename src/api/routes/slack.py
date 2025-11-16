"""Slack webhook endpoints for receiving events."""

import hmac
import hashlib
import time
from typing import Dict, Any
from fastapi import APIRouter, Request, HTTPException, Header
from fastapi.responses import JSONResponse

from src.config import settings
from src.agent.scrum_master import ScrumMasterAgent

router = APIRouter()

# Initialize the Scrum Master agent
scrum_agent = ScrumMasterAgent()


def verify_slack_signature(
    body: bytes,
    timestamp: str,
    signature: str,
    signing_secret: str
) -> bool:
    """
    Verify that the request comes from Slack.

    Args:
        body: Raw request body
        timestamp: X-Slack-Request-Timestamp header
        signature: X-Slack-Signature header
        signing_secret: Slack signing secret from environment

    Returns:
        True if signature is valid, False otherwise
    """
    # Prevent replay attacks
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    # Compute the signature
    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    my_signature = 'v0=' + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    # Compare signatures
    return hmac.compare_digest(my_signature, signature)


@router.post("/events")
async def slack_events(
    request: Request,
    x_slack_request_timestamp: str = Header(...),
    x_slack_signature: str = Header(...)
):
    """
    Handle Slack event subscriptions.

    This endpoint receives events from Slack's Event API including:
    - app_mention: When the bot is mentioned in a channel
    - message.im: Direct messages to the bot
    - Other subscribed events
    """
    # Get raw body for signature verification
    body = await request.body()

    # Verify the request is from Slack
    if not settings.slack_signing_secret:
        raise HTTPException(
            status_code=500,
            detail="Slack signing secret not configured"
        )

    if not verify_slack_signature(
        body,
        x_slack_request_timestamp,
        x_slack_signature,
        settings.slack_signing_secret
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse JSON body
    data = await request.json()

    # Handle URL verification challenge
    if data.get("type") == "url_verification":
        return JSONResponse(content={"challenge": data.get("challenge")})

    # Handle event callbacks
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        event_type = event.get("type")

        # Ignore bot messages to prevent loops
        if event.get("bot_id"):
            return JSONResponse(content={"ok": True})

        # Handle app mentions
        if event_type == "app_mention":
            await handle_app_mention(event)

        # Handle direct messages
        elif event_type == "message" and event.get("channel_type") == "im":
            await handle_direct_message(event)

        return JSONResponse(content={"ok": True})

    return JSONResponse(content={"ok": True})


@router.post("/interactions")
async def slack_interactions(
    request: Request,
    x_slack_request_timestamp: str = Header(...),
    x_slack_signature: str = Header(...)
):
    """
    Handle Slack interactive components (buttons, modals, etc.).

    This endpoint receives interactions from:
    - Button clicks
    - Modal submissions
    - Select menu choices
    - Other interactive components
    """
    # Get raw body for signature verification
    body = await request.body()

    # Verify the request is from Slack
    if not settings.slack_signing_secret:
        raise HTTPException(
            status_code=500,
            detail="Slack signing secret not configured"
        )

    if not verify_slack_signature(
        body,
        x_slack_request_timestamp,
        x_slack_signature,
        settings.slack_signing_secret
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse form data (Slack sends interactions as form-encoded)
    form_data = await request.form()
    payload = form_data.get("payload")

    if payload:
        import json
        interaction_data = json.loads(payload)

        # Handle different interaction types
        interaction_type = interaction_data.get("type")

        if interaction_type == "block_actions":
            await handle_block_actions(interaction_data)
        elif interaction_type == "view_submission":
            await handle_modal_submission(interaction_data)

        return JSONResponse(content={"ok": True})

    return JSONResponse(content={"ok": True})


@router.post("/commands")
async def slack_commands(
    request: Request,
    x_slack_request_timestamp: str = Header(...),
    x_slack_signature: str = Header(...)
):
    """
    Handle Slack slash commands.

    This endpoint receives slash command invocations:
    - /standup
    - /sprint-planning
    - /retrospective
    - /estimate
    """
    # Get raw body for signature verification
    body = await request.body()

    # Verify the request is from Slack
    if not settings.slack_signing_secret:
        raise HTTPException(
            status_code=500,
            detail="Slack signing secret not configured"
        )

    if not verify_slack_signature(
        body,
        x_slack_request_timestamp,
        x_slack_signature,
        settings.slack_signing_secret
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse form data
    form_data = await request.form()
    command = form_data.get("command")
    text = form_data.get("text", "")
    user_id = form_data.get("user_id")
    channel_id = form_data.get("channel_id")

    # Route to appropriate handler
    if command == "/standup":
        return await handle_standup_command(user_id, channel_id, text)
    elif command == "/sprint-planning":
        return await handle_sprint_planning_command(user_id, channel_id, text)
    elif command == "/retrospective":
        return await handle_retrospective_command(user_id, channel_id, text)
    elif command == "/estimate":
        return await handle_estimate_command(user_id, channel_id, text)

    return JSONResponse(content={
        "response_type": "ephemeral",
        "text": f"Unknown command: {command}"
    })


# Event handlers
async def handle_app_mention(event: Dict[str, Any]):
    """Handle when the bot is mentioned in a channel."""
    text = event.get("text", "")
    channel = event.get("channel")
    user = event.get("user")

    # Remove bot mention from text
    import re
    clean_text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()

    # Generate response using AI
    if clean_text.lower() in ["help", "?", ""]:
        response = get_help_message()
    else:
        response = await scrum_agent.chat(clean_text)

    # Send response back to channel (requires Slack API client)
    # This is a placeholder - actual implementation would use Slack SDK
    print(f"Would send to {channel}: {response}")


async def handle_direct_message(event: Dict[str, Any]):
    """Handle direct messages to the bot."""
    text = event.get("text", "")
    channel = event.get("channel")
    user = event.get("user")

    # Generate response using AI
    response = await scrum_agent.chat(text)

    # Send response back (requires Slack API client)
    print(f"Would send DM to {user}: {response}")


# Command handlers
async def handle_standup_command(user_id: str, channel_id: str, text: str):
    """Handle /standup command."""
    if not settings.enable_daily_standup:
        return JSONResponse(content={
            "response_type": "ephemeral",
            "text": "Daily standup feature is currently disabled."
        })

    # Return a modal for standup submission
    modal = {
        "type": "modal",
        "callback_id": "standup_modal",
        "title": {"type": "plain_text", "text": "Daily Standup"},
        "submit": {"type": "plain_text", "text": "Submit"},
        "blocks": [
            {
                "type": "input",
                "block_id": "yesterday",
                "label": {"type": "plain_text", "text": "What did you do yesterday?"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "yesterday_input",
                    "multiline": True
                }
            },
            {
                "type": "input",
                "block_id": "today",
                "label": {"type": "plain_text", "text": "What will you do today?"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "today_input",
                    "multiline": True
                }
            },
            {
                "type": "input",
                "block_id": "blockers",
                "label": {"type": "plain_text", "text": "Any blockers or impediments?"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "blockers_input",
                    "multiline": True
                },
                "optional": True
            }
        ]
    }

    return JSONResponse(content={
        "response_type": "ephemeral",
        "text": "Opening standup form...",
        # Note: To actually show a modal, you need to use the Slack Web API
        # This would require a POST to https://slack.com/api/views.open
    })


async def handle_sprint_planning_command(user_id: str, channel_id: str, text: str):
    """Handle /sprint-planning command."""
    if not settings.enable_sprint_planning:
        return JSONResponse(content={
            "response_type": "ephemeral",
            "text": "Sprint planning feature is currently disabled."
        })

    # Generate sprint planning guidance
    response = await scrum_agent.assist_sprint_planning(
        capacity=80,
        velocity=30,
        backlog_items=[]
    )

    return JSONResponse(content={
        "response_type": "in_channel",
        "text": f"🎯 Sprint Planning Assistance:\n\n{response}"
    })


async def handle_retrospective_command(user_id: str, channel_id: str, text: str):
    """Handle /retrospective command."""
    if not settings.enable_retrospectives:
        return JSONResponse(content={
            "response_type": "ephemeral",
            "text": "Retrospective feature is currently disabled."
        })

    return JSONResponse(content={
        "response_type": "ephemeral",
        "text": "🔄 Let's start a retrospective! Please share:\n" +
               "1. What went well?\n" +
               "2. What could be improved?\n" +
               "3. Action items for next sprint?"
    })


async def handle_estimate_command(user_id: str, channel_id: str, text: str):
    """Handle /estimate command."""
    if not text:
        return JSONResponse(content={
            "response_type": "ephemeral",
            "text": "Please provide a user story description.\n" +
                   "Example: `/estimate Implement user authentication with JWT`"
        })

    # Get estimation from AI
    response = await scrum_agent.estimate_story(text)

    return JSONResponse(content={
        "response_type": "in_channel",
        "text": f"📊 Story Estimation:\n\n{response}"
    })


# Interactive component handlers
async def handle_block_actions(data: Dict[str, Any]):
    """Handle button clicks and other block actions."""
    actions = data.get("actions", [])
    for action in actions:
        action_id = action.get("action_id")
        # Handle specific button actions here
        print(f"Button clicked: {action_id}")


async def handle_modal_submission(data: Dict[str, Any]):
    """Handle modal form submissions."""
    view = data.get("view", {})
    callback_id = view.get("callback_id")

    if callback_id == "standup_modal":
        # Extract values from modal
        values = view.get("state", {}).get("values", {})
        yesterday = values.get("yesterday", {}).get("yesterday_input", {}).get("value", "")
        today = values.get("today", {}).get("today_input", {}).get("value", "")
        blockers = values.get("blockers", {}).get("blockers_input", {}).get("value", "")

        # Save standup to database (implementation needed)
        print(f"Standup submitted: {yesterday}, {today}, {blockers}")


def get_help_message() -> str:
    """Get help message for the bot."""
    return """
🤖 **Scrum Master AI Assistant - Help**

**Available Commands:**
• `/standup` - Submit your daily standup update
• `/sprint-planning` - Get help with sprint planning
• `/retrospective` - Start a retrospective session
• `/estimate <story>` - Get story point estimation

**How to use:**
• Mention me in any channel: `@ScrumMaster help`
• Send me a direct message with your question
• Use slash commands for quick actions

**Features:**
✅ AI-powered sprint planning assistance
✅ Daily standup tracking and analysis
✅ Retrospective facilitation
✅ Story point estimation
✅ Team velocity tracking

Need more help? Just ask me anything about agile or scrum!
"""
