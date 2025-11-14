"""
Standup Master Agent - Facilitates daily standup meetings
"""
from typing import Any, Dict, List
from .base_agent import BaseAgent


class StandupMasterAgent(BaseAgent):
    """Agent responsible for facilitating daily standup meetings"""

    def __init__(self):
        super().__init__(
            name="Standup Master",
            role="Daily Standup Facilitator",
            goal="Conduct efficient and productive daily standup meetings, collect updates from team members, and identify blockers",
            backstory="""You are an experienced Scrum Master who excels at facilitating
            daily standup meetings. You know how to keep discussions focused, ensure
            everyone participates, and identify impediments that need attention. You
            follow the classic three questions: What did you do yesterday? What will
            you do today? Are there any blockers?"""
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute standup meeting facilitation

        Args:
            context: Contains team_members, previous_updates, etc.

        Returns:
            Standup summary with updates and blockers
        """
        team_members = context.get("team_members", [])
        updates = []
        blockers = []

        # Process standup updates
        for member in team_members:
            update = self._collect_update(member, context)
            updates.append(update)

            if update.get("blockers"):
                blockers.extend(update["blockers"])

        return {
            "status": "completed",
            "updates": updates,
            "blockers": blockers,
            "summary": self._generate_summary(updates, blockers)
        }

    def _collect_update(self, member: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Collect update from a team member"""
        # This would integrate with Slack/messaging to collect actual updates
        return {
            "member": member.get("name"),
            "yesterday": member.get("yesterday", ""),
            "today": member.get("today", ""),
            "blockers": member.get("blockers", [])
        }

    def _generate_summary(self, updates: List[Dict], blockers: List[Any]) -> str:
        """Generate standup summary"""
        summary_parts = [
            f"Standup completed with {len(updates)} team members.",
            f"Identified {len(blockers)} blocker(s)." if blockers else "No blockers reported."
        ]
        return " ".join(summary_parts)
