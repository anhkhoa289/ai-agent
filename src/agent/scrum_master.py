"""Core Scrum Master AI Agent logic."""

from typing import Optional, Dict, Any, List
from anthropic import Anthropic
import json


class ScrumMasterAgent:
    """AI Agent for Scrum Master assistance."""

    SYSTEM_PROMPT = """You are an experienced Scrum Master AI assistant integrated with Slack. Your role is to help agile teams with:

1. **Sprint Planning**: Help teams plan sprints, estimate story points, and set sprint goals
2. **Daily Standups**: Facilitate daily standup meetings, track blockers and progress
3. **Backlog Management**: Assist with grooming, prioritizing, and refining the product backlog
4. **Retrospectives**: Guide teams through retrospective meetings and identify improvements
5. **Metrics & Analytics**: Track team velocity, burndown charts, and sprint health
6. **Impediment Resolution**: Identify blockers and suggest solutions

**Communication Style**:
- Be concise and actionable
- Use Slack formatting (bold, lists, code blocks)
- Ask clarifying questions when needed
- Provide structured responses
- Be supportive and encouraging

**Slack Format Guidelines**:
- Use *bold* for emphasis
- Use `code` for technical terms
- Use bullet points for lists
- Use numbered lists for action items
- Keep messages brief and scannable

Remember: You're a facilitator, not a dictator. Help the team self-organize and improve."""

    def __init__(self, api_key: str, model_name: str = "claude-sonnet-4-5-20250929"):
        """Initialize the Scrum Master agent."""
        self.client = Anthropic(api_key=api_key)
        self.model_name = model_name
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}

    def get_response(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None,
        conversation_id: Optional[str] = None
    ) -> str:
        """
        Get a response from the AI agent.

        Args:
            user_message: The user's message
            context: Additional context (sprint info, team data, etc.)
            conversation_id: ID to track conversation history

        Returns:
            The agent's response
        """
        # Build context information
        context_str = ""
        if context:
            context_str = f"\n\n**Current Context**:\n{json.dumps(context, indent=2)}"

        # Get or initialize conversation history
        if conversation_id:
            history = self.conversation_history.get(conversation_id, [])
        else:
            history = []

        # Add user message to history
        history.append({
            "role": "user",
            "content": user_message + context_str
        })

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=2000,
                system=self.SYSTEM_PROMPT,
                messages=history
            )

            # Extract response text
            assistant_message = response.content[0].text

            # Add assistant response to history
            history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Store updated history
            if conversation_id:
                # Keep only last 20 messages to manage context length
                self.conversation_history[conversation_id] = history[-20:]

            return assistant_message

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    def clear_conversation(self, conversation_id: str):
        """Clear conversation history for a given ID."""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]

    def get_sprint_summary(self, sprint_data: Dict[str, Any]) -> str:
        """Generate a sprint summary."""
        prompt = f"""Based on this sprint data, provide a concise summary:

{json.dumps(sprint_data, indent=2)}

Include:
- Sprint goal progress
- Key accomplishments
- Blockers and risks
- Team velocity
- Recommendations"""

        return self.get_response(prompt)

    def facilitate_standup(self, team_updates: List[Dict[str, str]]) -> str:
        """Facilitate daily standup and provide summary."""
        updates_text = "\n".join([
            f"*{update['member']}*:\n- Yesterday: {update.get('yesterday', 'N/A')}\n- Today: {update.get('today', 'N/A')}\n- Blockers: {update.get('blockers', 'None')}"
            for update in team_updates
        ])

        prompt = f"""Here are today's standup updates:

{updates_text}

Provide:
1. A brief summary
2. Identified blockers that need attention
3. Suggested follow-ups"""

        return self.get_response(prompt)

    def suggest_story_points(self, user_story: str, historical_data: Optional[List[Dict]] = None) -> str:
        """Suggest story points for a user story."""
        historical_context = ""
        if historical_data:
            historical_context = f"\n\nHistorical similar stories:\n{json.dumps(historical_data, indent=2)}"

        prompt = f"""Help estimate story points for this user story:

{user_story}
{historical_context}

Provide:
- Suggested story point range
- Complexity factors to consider
- Questions to clarify requirements"""

        return self.get_response(prompt)
