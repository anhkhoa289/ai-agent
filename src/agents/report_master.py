"""
Report Master Agent - Generates sprint reports and retrospectives
"""
from typing import Any, Dict, List
from datetime import datetime
from .base_agent import BaseAgent


class ReportMasterAgent(BaseAgent):
    """Agent responsible for generating reports and facilitating retrospectives"""

    def __init__(self):
        super().__init__(
            name="Report Master",
            role="Sprint Reporter and Retrospective Facilitator",
            goal="Generate comprehensive sprint reports, facilitate retrospectives, and document lessons learned",
            backstory="""You are a thoughtful Scrum Master who excels at synthesizing
            information and facilitating meaningful retrospectives. You know how to
            present data in actionable ways and guide teams through productive
            discussions about what went well, what didn't, and what to improve."""
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute report generation or retrospective facilitation

        Args:
            context: Contains sprint_data, metrics, feedback, report_type, etc.

        Returns:
            Generated report or retrospective summary
        """
        report_type = context.get("report_type", "sprint_summary")

        if report_type == "sprint_summary":
            return self._generate_sprint_summary(context)
        elif report_type == "retrospective":
            return self._facilitate_retrospective(context)
        elif report_type == "velocity_report":
            return self._generate_velocity_report(context)
        else:
            return {"status": "error", "message": f"Unknown report type: {report_type}"}

    def _generate_sprint_summary(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate sprint summary report"""
        sprint_data = context.get("sprint_data", {})
        metrics = context.get("metrics", {})
        stories = context.get("stories", [])

        completed_stories = [s for s in stories if s.get("status") == "done"]
        incomplete_stories = [s for s in stories if s.get("status") != "done"]

        summary = {
            "sprint_name": sprint_data.get("name", "Unknown Sprint"),
            "date_generated": datetime.now().isoformat(),
            "duration": f"{sprint_data.get('sprint_length', 0)} days",
            "team_size": sprint_data.get("team_size", 0),
            "metrics": {
                "committed_points": metrics.get("total_points", 0),
                "completed_points": metrics.get("completed_points", 0),
                "completion_rate": f"{metrics.get('completion_rate', 0):.1f}%",
                "velocity": metrics.get("velocity", 0)
            },
            "completed_stories": len(completed_stories),
            "incomplete_stories": len(incomplete_stories),
            "key_achievements": self._extract_achievements(completed_stories),
            "challenges": self._extract_challenges(context),
            "sprint_health": metrics.get("sprint_health", "unknown")
        }

        return {
            "status": "completed",
            "report_type": "sprint_summary",
            "report": summary,
            "formatted_report": self._format_sprint_summary(summary)
        }

    def _facilitate_retrospective(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Facilitate retrospective discussion"""
        feedback = context.get("feedback", {})
        metrics = context.get("metrics", {})

        retrospective = {
            "date": datetime.now().isoformat(),
            "participants": context.get("participants", []),
            "went_well": feedback.get("went_well", []),
            "needs_improvement": feedback.get("needs_improvement", []),
            "action_items": self._generate_action_items(feedback, metrics),
            "team_sentiment": self._analyze_sentiment(feedback)
        }

        return {
            "status": "completed",
            "report_type": "retrospective",
            "retrospective": retrospective,
            "formatted_report": self._format_retrospective(retrospective)
        }

    def _generate_velocity_report(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate velocity trend report"""
        sprint_history = context.get("sprint_history", [])

        velocity_data = [
            {
                "sprint": sprint.get("name"),
                "completed_points": sprint.get("completed_points", 0),
                "committed_points": sprint.get("committed_points", 0)
            }
            for sprint in sprint_history
        ]

        avg_velocity = (sum(s["completed_points"] for s in velocity_data) / len(velocity_data)
                       if velocity_data else 0)

        return {
            "status": "completed",
            "report_type": "velocity_report",
            "velocity_data": velocity_data,
            "average_velocity": avg_velocity,
            "trend": self._analyze_velocity_trend(velocity_data),
            "formatted_report": self._format_velocity_report(velocity_data, avg_velocity)
        }

    def _extract_achievements(self, completed_stories: List[Dict]) -> List[str]:
        """Extract key achievements from completed stories"""
        return [story.get("title", "Unnamed story") for story in completed_stories[:5]]

    def _extract_challenges(self, context: Dict[str, Any]) -> List[str]:
        """Extract challenges from context"""
        blockers = context.get("blockers", [])
        return [blocker.get("description", str(blocker)) for blocker in blockers[:3]]

    def _generate_action_items(self, feedback: Dict, metrics: Dict) -> List[Dict[str, str]]:
        """Generate action items from retrospective feedback"""
        action_items = []

        improvements = feedback.get("needs_improvement", [])
        for improvement in improvements:
            action_items.append({
                "item": improvement,
                "priority": "high",
                "owner": "team"
            })

        return action_items

    def _analyze_sentiment(self, feedback: Dict) -> str:
        """Analyze team sentiment from feedback"""
        positive = len(feedback.get("went_well", []))
        negative = len(feedback.get("needs_improvement", []))

        if positive > negative * 2:
            return "positive"
        elif negative > positive * 2:
            return "needs_attention"
        else:
            return "neutral"

    def _analyze_velocity_trend(self, velocity_data: List[Dict]) -> str:
        """Analyze velocity trend"""
        if len(velocity_data) < 2:
            return "insufficient_data"

        recent_avg = sum(s["completed_points"] for s in velocity_data[-3:]) / min(3, len(velocity_data))
        overall_avg = sum(s["completed_points"] for s in velocity_data) / len(velocity_data)

        if recent_avg > overall_avg * 1.1:
            return "improving"
        elif recent_avg < overall_avg * 0.9:
            return "declining"
        else:
            return "stable"

    def _format_sprint_summary(self, summary: Dict) -> str:
        """Format sprint summary as readable text"""
        return f"""
📊 Sprint Summary: {summary['sprint_name']}

Duration: {summary['duration']}
Team Size: {summary['team_size']}

Metrics:
- Committed: {summary['metrics']['committed_points']} points
- Completed: {summary['metrics']['completed_points']} points
- Completion Rate: {summary['metrics']['completion_rate']}
- Velocity: {summary['metrics']['velocity']} points/day

Stories:
- Completed: {summary['completed_stories']}
- Incomplete: {summary['incomplete_stories']}

Sprint Health: {summary['sprint_health'].upper()}
"""

    def _format_retrospective(self, retro: Dict) -> str:
        """Format retrospective as readable text"""
        went_well = "\n".join(f"  ✅ {item}" for item in retro['went_well'])
        improvements = "\n".join(f"  ⚠️ {item}" for item in retro['needs_improvement'])
        actions = "\n".join(f"  🎯 {item['item']}" for item in retro['action_items'])

        return f"""
🔄 Sprint Retrospective

Team Sentiment: {retro['team_sentiment'].upper()}
Participants: {len(retro['participants'])}

What Went Well:
{went_well}

Needs Improvement:
{improvements}

Action Items:
{actions}
"""

    def _format_velocity_report(self, velocity_data: List[Dict], avg_velocity: float) -> str:
        """Format velocity report as readable text"""
        sprints = "\n".join(
            f"  {sprint['sprint']}: {sprint['completed_points']}/{sprint['committed_points']} points"
            for sprint in velocity_data[-5:]
        )

        return f"""
📈 Velocity Report

Recent Sprints:
{sprints}

Average Velocity: {avg_velocity:.1f} points
"""
