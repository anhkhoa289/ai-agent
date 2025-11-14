"""
Main orchestrator for coordinating AI agents using CrewAI
"""
from typing import Dict, Any, List, Optional
from crewai import Crew, Task, Process
from ..agents import StandupMasterAgent, TrackMasterAgent, ReportMasterAgent
from ..integrations import JiraClient, SlackClient, TrelloClient


class CrewOrchestrator:
    """Orchestrates multiple AI agents to perform scrum master tasks"""

    def __init__(self, use_jira: bool = True, use_trello: bool = False):
        """
        Initialize crew orchestrator

        Args:
            use_jira: Whether to use Jira integration
            use_trello: Whether to use Trello integration
        """
        # Initialize agents
        self.standup_agent = StandupMasterAgent()
        self.track_agent = TrackMasterAgent()
        self.report_agent = ReportMasterAgent()

        # Initialize integrations
        self.slack_client = SlackClient()
        self.jira_client = JiraClient() if use_jira else None
        self.trello_client = TrelloClient() if use_trello else None

    def run_daily_standup(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute daily standup workflow

        Args:
            context: Contains channel, team_members, etc.

        Returns:
            Standup results
        """
        # Send standup reminder
        channel = context.get("channel")
        team_members = context.get("team_members", [])

        if channel and team_members:
            self.slack_client.send_standup_reminder(channel, team_members)

        # Execute standup agent
        standup_result = self.standup_agent.execute(context)

        # Send summary to Slack
        if channel and standup_result.get("summary"):
            self.slack_client.send_message(channel, standup_result["summary"])

        return standup_result

    def track_sprint_progress(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track and analyze sprint progress

        Args:
            context: Contains sprint_id, board_id, etc.

        Returns:
            Tracking results with metrics and insights
        """
        # Fetch sprint data from project management tool
        sprint_data = self._fetch_sprint_data(context)

        # Add sprint data to context
        enhanced_context = {**context, **sprint_data}

        # Execute tracking agent
        track_result = self.track_agent.execute(enhanced_context)

        # Send alerts if sprint is at risk
        if track_result.get("sprint_health") in ["at_risk", "critical"]:
            self._send_sprint_alert(track_result, context)

        return track_result

    def generate_report(self, report_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sprint report or facilitate retrospective

        Args:
            report_type: Type of report (sprint_summary, retrospective, velocity_report)
            context: Report context data

        Returns:
            Generated report
        """
        # Add report type to context
        context["report_type"] = report_type

        # Fetch additional data if needed
        if report_type in ["sprint_summary", "velocity_report"]:
            sprint_data = self._fetch_sprint_data(context)
            context.update(sprint_data)

        # Execute report agent
        report_result = self.report_agent.execute(context)

        # Send report to Slack if channel specified
        channel = context.get("channel")
        if channel and report_result.get("formatted_report"):
            self.slack_client.send_sprint_report(channel, report_result["formatted_report"])

        return report_result

    def run_crew_workflow(self, workflow: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a complete crew workflow with multiple agents

        Args:
            workflow: Workflow type (sprint_end, sprint_start, etc.)
            context: Workflow context

        Returns:
            Workflow results
        """
        if workflow == "sprint_end":
            return self._sprint_end_workflow(context)
        elif workflow == "sprint_start":
            return self._sprint_start_workflow(context)
        elif workflow == "daily_routine":
            return self._daily_routine_workflow(context)
        else:
            return {"status": "error", "message": f"Unknown workflow: {workflow}"}

    def _sprint_end_workflow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute end-of-sprint workflow"""
        results = {}

        # Generate sprint summary
        results["summary"] = self.generate_report("sprint_summary", context)

        # Facilitate retrospective
        results["retrospective"] = self.generate_report("retrospective", context)

        # Update velocity report
        results["velocity"] = self.generate_report("velocity_report", context)

        return {
            "status": "completed",
            "workflow": "sprint_end",
            "results": results
        }

    def _sprint_start_workflow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute sprint start workflow"""
        results = {}

        # Get sprint planning data
        sprint_data = self._fetch_sprint_data(context)
        results["sprint_data"] = sprint_data

        # Send sprint kickoff message
        channel = context.get("channel")
        if channel:
            kickoff_msg = f"🚀 Sprint {sprint_data.get('sprint_name', 'New Sprint')} has started!\n" \
                         f"Duration: {sprint_data.get('sprint_length', 0)} days\n" \
                         f"Committed Points: {sprint_data.get('metrics', {}).get('total_points', 0)}"
            self.slack_client.send_message(channel, kickoff_msg)
            results["kickoff_sent"] = True

        return {
            "status": "completed",
            "workflow": "sprint_start",
            "results": results
        }

    def _daily_routine_workflow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute daily routine workflow"""
        results = {}

        # Run standup
        results["standup"] = self.run_daily_standup(context)

        # Track progress
        results["tracking"] = self.track_sprint_progress(context)

        return {
            "status": "completed",
            "workflow": "daily_routine",
            "results": results
        }

    def _fetch_sprint_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch sprint data from project management tool"""
        sprint_data = {}

        if self.jira_client:
            board_id = context.get("board_id")
            if board_id:
                active_sprint = self.jira_client.get_active_sprint(board_id)
                if active_sprint:
                    sprint_id = active_sprint["id"]
                    stories = self.jira_client.get_sprint_stories(sprint_id)

                    sprint_data = {
                        "sprint_name": active_sprint["name"],
                        "sprint_id": sprint_id,
                        "stories": stories,
                        "sprint_length": 14,  # Default, could be calculated
                        "days_elapsed": context.get("days_elapsed", 0)
                    }

        elif self.trello_client:
            board_id = context.get("board_id")
            sprint_label = context.get("sprint_label", "Current Sprint")
            if board_id:
                cards = self.trello_client.get_sprint_cards(board_id, sprint_label)

                sprint_data = {
                    "sprint_name": sprint_label,
                    "stories": cards,
                    "sprint_length": 14,
                    "days_elapsed": context.get("days_elapsed", 0)
                }

        return sprint_data

    def _send_sprint_alert(self, track_result: Dict[str, Any], context: Dict[str, Any]):
        """Send alert when sprint is at risk"""
        channel = context.get("channel")
        if not channel:
            return

        health = track_result.get("sprint_health")
        insights = track_result.get("insights", [])
        recommendations = track_result.get("recommendations", [])

        alert_emoji = "⚠️" if health == "at_risk" else "🚨"

        message = f"{alert_emoji} *Sprint Health Alert: {health.upper()}*\n\n"
        message += "*Insights:*\n" + "\n".join(insights) + "\n\n"

        if recommendations:
            message += "*Recommendations:*\n" + "\n".join(f"• {rec}" for rec in recommendations)

        self.slack_client.send_message(channel, message)
