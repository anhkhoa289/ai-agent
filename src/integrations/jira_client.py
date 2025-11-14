"""
Jira integration client
"""
from typing import List, Dict, Any, Optional
from jira import JIRA
from ..config.settings import settings


class JiraClient:
    """Client for interacting with Jira API"""

    def __init__(self):
        """Initialize Jira client"""
        self.client: Optional[JIRA] = None
        if settings.JIRA_URL and settings.JIRA_EMAIL and settings.JIRA_API_TOKEN:
            self.client = JIRA(
                server=settings.JIRA_URL,
                basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
            )

    def get_sprint_stories(self, sprint_id: str) -> List[Dict[str, Any]]:
        """
        Get all stories in a sprint

        Args:
            sprint_id: Sprint ID

        Returns:
            List of story dictionaries
        """
        if not self.client:
            raise ValueError("Jira client not configured")

        jql = f"sprint = {sprint_id}"
        issues = self.client.search_issues(jql, maxResults=100)

        stories = []
        for issue in issues:
            stories.append({
                "key": issue.key,
                "title": issue.fields.summary,
                "status": issue.fields.status.name,
                "points": getattr(issue.fields, "customfield_10016", 0) or 0,  # Story points
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",
                "type": issue.fields.issuetype.name
            })

        return stories

    def get_active_sprint(self, board_id: str) -> Optional[Dict[str, Any]]:
        """
        Get active sprint for a board

        Args:
            board_id: Jira board ID

        Returns:
            Sprint information or None
        """
        if not self.client:
            raise ValueError("Jira client not configured")

        sprints = self.client.sprints(board_id, state="active")

        if sprints:
            sprint = sprints[0]
            return {
                "id": sprint.id,
                "name": sprint.name,
                "state": sprint.state,
                "start_date": sprint.startDate,
                "end_date": sprint.endDate
            }

        return None

    def update_story_status(self, issue_key: str, status: str) -> bool:
        """
        Update story status

        Args:
            issue_key: Jira issue key
            status: New status

        Returns:
            Success status
        """
        if not self.client:
            raise ValueError("Jira client not configured")

        try:
            issue = self.client.issue(issue_key)
            transitions = self.client.transitions(issue)

            for transition in transitions:
                if transition["name"].lower() == status.lower():
                    self.client.transition_issue(issue, transition["id"])
                    return True

            return False
        except Exception as e:
            print(f"Error updating story status: {e}")
            return False

    def create_story(self, project_key: str, summary: str, description: str,
                    story_points: Optional[int] = None) -> Optional[str]:
        """
        Create a new story

        Args:
            project_key: Jira project key
            summary: Story summary
            description: Story description
            story_points: Story points estimate

        Returns:
            Created issue key or None
        """
        if not self.client:
            raise ValueError("Jira client not configured")

        try:
            issue_dict = {
                "project": {"key": project_key},
                "summary": summary,
                "description": description,
                "issuetype": {"name": "Story"}
            }

            if story_points:
                issue_dict["customfield_10016"] = story_points

            issue = self.client.create_issue(fields=issue_dict)
            return issue.key
        except Exception as e:
            print(f"Error creating story: {e}")
            return None
