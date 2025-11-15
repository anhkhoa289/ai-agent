"""Scrum Master AI Agent using Anthropic Claude."""

import json
from typing import Dict, Any, Optional
from anthropic import Anthropic

from src.config import settings


class ScrumMasterAgent:
    """
    AI-powered Scrum Master agent that provides intelligent assistance
    for agile project management tasks.
    """

    SYSTEM_PROMPT = """You are an experienced Scrum Master assistant with deep knowledge of agile
methodologies, sprint planning, team facilitation, and continuous improvement practices.

Your role is to:
- Help teams with sprint planning and backlog refinement
- Facilitate daily standups and identify blockers
- Guide retrospectives and suggest actionable improvements
- Provide estimation guidance using story points
- Track team velocity and suggest optimizations
- Identify potential risks and dependencies
- Promote agile best practices

Always be:
- Constructive and supportive
- Data-driven in your recommendations
- Clear and concise in communication
- Focused on team empowerment
- Mindful of Scrum values: commitment, courage, focus, openness, and respect
"""

    def __init__(self):
        """Initialize the Scrum Master agent."""
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set in environment")

        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.model_name
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature

    def get_response(self, user_message: str, context: Optional[str] = None) -> str:
        """
        Get a response from the AI agent.

        Args:
            user_message: The user's message or question
            context: Optional additional context for the conversation

        Returns:
            str: AI-generated response
        """
        messages = []

        if context:
            messages.append({
                "role": "user",
                "content": f"Context: {context}"
            })
            messages.append({
                "role": "assistant",
                "content": "I understand the context. How can I help?"
            })

        messages.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.SYSTEM_PROMPT,
            messages=messages
        )

        return response.content[0].text

    def analyze_standup(self, standup_data: Dict[str, Any]) -> str:
        """
        Analyze a standup update and provide insights.

        Args:
            standup_data: Dictionary containing standup information

        Returns:
            str: Analysis and recommendations
        """
        prompt = f"""Analyze this daily standup update:

**Team Member:** {standup_data.get('user_name', 'Unknown')}
**Yesterday:** {standup_data.get('yesterday', 'N/A')}
**Today:** {standup_data.get('today', 'N/A')}
**Blockers:** {standup_data.get('blockers', 'None')}

Provide:
1. Key observations about progress and focus
2. Any risks or concerns identified
3. Suggestions for addressing blockers (if any)
4. Encouragement or actionable next steps

Keep the response concise and actionable."""

        return self.get_response(prompt)

    def assist_sprint_planning(self, planning_data: Dict[str, Any]) -> str:
        """
        Provide assistance with sprint planning.

        Args:
            planning_data: Dictionary containing sprint planning information

        Returns:
            str: Sprint planning recommendations
        """
        context = json.dumps(planning_data, indent=2)
        prompt = f"""Help with sprint planning based on this data:

{context}

Provide guidance on:
1. Sprint capacity and velocity considerations
2. Story prioritization recommendations
3. Potential risks or dependencies
4. Tips for setting a clear sprint goal
5. Recommended team discussions

Be specific and actionable."""

        return self.get_response(prompt)

    def generate_retrospective_insights(self, retro_data: Dict[str, Any]) -> str:
        """
        Generate insights for a retrospective.

        Args:
            retro_data: Dictionary containing retrospective data

        Returns:
            str: AI-generated insights and recommendations
        """
        prompt = f"""Analyze this sprint retrospective data:

**What Went Well:**
{json.dumps(retro_data.get('went_well', {}), indent=2)}

**What Went Wrong:**
{json.dumps(retro_data.get('went_wrong', {}), indent=2)}

**Proposed Improvements:**
{json.dumps(retro_data.get('improvements', {}), indent=2)}

**Action Items:**
{json.dumps(retro_data.get('action_items', {}), indent=2)}

Provide:
1. Key patterns and themes identified
2. Root cause analysis of issues
3. Additional improvement suggestions
4. Prioritization recommendations for action items
5. Specific metrics to track improvement

Be constructive and focus on continuous improvement."""

        return self.get_response(prompt)

    def estimate_story(self, story_description: str) -> str:
        """
        Help estimate story points for a user story.

        Args:
            story_description: Description of the user story

        Returns:
            str: Estimation guidance
        """
        prompt = f"""Help estimate this user story:

{story_description}

Provide:
1. Suggested story point range (using Fibonacci: 1, 2, 3, 5, 8, 13, 21)
2. Key complexity factors to consider
3. Questions to clarify for better estimation
4. Suggestions for breaking down if too large (>13 points)
5. Potential technical considerations

Use your best judgment based on typical software development patterns."""

        return self.get_response(prompt)


# Singleton instance
_agent_instance: Optional[ScrumMasterAgent] = None


def get_scrum_master_agent() -> ScrumMasterAgent:
    """
    Get or create the singleton Scrum Master agent instance.

    Returns:
        ScrumMasterAgent: The agent instance
    """
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ScrumMasterAgent()
    return _agent_instance


async def get_ai_insights(retro_data: Dict[str, Any]) -> str:
    """
    Async wrapper to get AI insights for retrospectives.

    Args:
        retro_data: Retrospective data

    Returns:
        str: AI-generated insights
    """
    agent = get_scrum_master_agent()
    return agent.generate_retrospective_insights(retro_data)
