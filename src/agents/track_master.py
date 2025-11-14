"""
Track Master Agent - Monitors sprint progress and team velocity
"""
from typing import Any, Dict, List
from .base_agent import BaseAgent


class TrackMasterAgent(BaseAgent):
    """Agent responsible for tracking sprint progress and team metrics"""

    def __init__(self):
        super().__init__(
            name="Track Master",
            role="Sprint Progress Tracker",
            goal="Monitor sprint progress, track team velocity, analyze burndown, and provide insights on sprint health",
            backstory="""You are a data-driven Scrum Master who excels at tracking
            metrics and identifying trends. You understand story points, velocity,
            burndown charts, and can spot risks early. You provide actionable insights
            to help teams stay on track and continuously improve."""
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute sprint tracking and analysis

        Args:
            context: Contains sprint_data, stories, completed_points, etc.

        Returns:
            Sprint tracking report with metrics and insights
        """
        sprint_data = context.get("sprint_data", {})
        stories = context.get("stories", [])

        metrics = self._calculate_metrics(sprint_data, stories)
        insights = self._generate_insights(metrics, sprint_data)
        recommendations = self._generate_recommendations(metrics, insights)

        return {
            "status": "completed",
            "metrics": metrics,
            "insights": insights,
            "recommendations": recommendations,
            "sprint_health": self._assess_sprint_health(metrics)
        }

    def _calculate_metrics(self, sprint_data: Dict, stories: List[Dict]) -> Dict[str, Any]:
        """Calculate sprint metrics"""
        total_points = sum(story.get("points", 0) for story in stories)
        completed_points = sum(
            story.get("points", 0) for story in stories if story.get("status") == "done"
        )
        in_progress_points = sum(
            story.get("points", 0) for story in stories if story.get("status") == "in_progress"
        )

        days_elapsed = sprint_data.get("days_elapsed", 0)
        sprint_length = sprint_data.get("sprint_length", 14)
        days_remaining = sprint_length - days_elapsed

        return {
            "total_points": total_points,
            "completed_points": completed_points,
            "in_progress_points": in_progress_points,
            "remaining_points": total_points - completed_points,
            "completion_rate": (completed_points / total_points * 100) if total_points > 0 else 0,
            "days_elapsed": days_elapsed,
            "days_remaining": days_remaining,
            "velocity": completed_points / days_elapsed if days_elapsed > 0 else 0
        }

    def _generate_insights(self, metrics: Dict, sprint_data: Dict) -> List[str]:
        """Generate insights from metrics"""
        insights = []

        if metrics["completion_rate"] < 30 and metrics["days_remaining"] < 5:
            insights.append("⚠️ Sprint is at risk - low completion rate with few days remaining")

        if metrics["velocity"] > 0:
            projected_completion = metrics["remaining_points"] / metrics["velocity"]
            if projected_completion > metrics["days_remaining"]:
                insights.append(
                    f"📊 Current velocity suggests {int(projected_completion)} more days needed, "
                    f"but only {metrics['days_remaining']} days remain"
                )

        if metrics["in_progress_points"] > metrics["completed_points"]:
            insights.append("🔄 More work in progress than completed - consider focusing efforts")

        return insights

    def _generate_recommendations(self, metrics: Dict, insights: List[str]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if metrics["completion_rate"] < 50 and metrics["days_remaining"] < metrics["days_elapsed"]:
            recommendations.append("Consider scope reduction or sprint extension discussion")

        if metrics["in_progress_points"] > metrics["total_points"] * 0.5:
            recommendations.append("Encourage team to complete in-progress items before starting new work")

        return recommendations

    def _assess_sprint_health(self, metrics: Dict) -> str:
        """Assess overall sprint health"""
        completion_rate = metrics["completion_rate"]
        time_elapsed_rate = (metrics["days_elapsed"] /
                            (metrics["days_elapsed"] + metrics["days_remaining"]) * 100)

        if completion_rate >= time_elapsed_rate - 10:
            return "healthy"
        elif completion_rate >= time_elapsed_rate - 25:
            return "at_risk"
        else:
            return "critical"
