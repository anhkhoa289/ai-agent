"""
Web dashboard for scrum master AI agent
"""
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ..orchestrator import CrewOrchestrator
from ..config.settings import settings

app = FastAPI(title="Scrum Master AI Dashboard")
orchestrator = CrewOrchestrator()


# Request/Response Models
class StandupRequest(BaseModel):
    channel: str
    team_members: list[str]


class SprintTrackingRequest(BaseModel):
    board_id: str
    days_elapsed: int = 0
    channel: Optional[str] = None


class ReportRequest(BaseModel):
    report_type: str
    board_id: Optional[str] = None
    channel: Optional[str] = None
    sprint_history: Optional[list] = None
    feedback: Optional[Dict[str, Any]] = None


class WorkflowRequest(BaseModel):
    workflow: str
    context: Dict[str, Any]


# Health check
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Scrum Master AI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Standup endpoints
@app.post("/standup")
async def run_standup(request: StandupRequest):
    """Run daily standup"""
    try:
        context = {
            "channel": request.channel,
            "team_members": request.team_members
        }
        result = orchestrator.run_daily_standup(context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Sprint tracking endpoints
@app.post("/sprint/track")
async def track_sprint(request: SprintTrackingRequest):
    """Track sprint progress"""
    try:
        context = {
            "board_id": request.board_id,
            "days_elapsed": request.days_elapsed,
            "channel": request.channel
        }
        result = orchestrator.track_sprint_progress(context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sprint/status/{board_id}")
async def get_sprint_status(board_id: str):
    """Get current sprint status"""
    try:
        context = {"board_id": board_id}
        result = orchestrator.track_sprint_progress(context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Report endpoints
@app.post("/reports/generate")
async def generate_report(request: ReportRequest):
    """Generate sprint report"""
    try:
        context = {
            "board_id": request.board_id,
            "channel": request.channel,
            "sprint_history": request.sprint_history or [],
            "feedback": request.feedback or {}
        }
        result = orchestrator.generate_report(request.report_type, context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports/types")
async def get_report_types():
    """Get available report types"""
    return {
        "success": True,
        "data": {
            "types": [
                {
                    "id": "sprint_summary",
                    "name": "Sprint Summary",
                    "description": "Comprehensive sprint summary with metrics"
                },
                {
                    "id": "retrospective",
                    "name": "Retrospective",
                    "description": "Sprint retrospective report"
                },
                {
                    "id": "velocity_report",
                    "name": "Velocity Report",
                    "description": "Team velocity trends"
                }
            ]
        }
    }


# Workflow endpoints
@app.post("/workflow/run")
async def run_workflow(request: WorkflowRequest):
    """Run a crew workflow"""
    try:
        result = orchestrator.run_crew_workflow(request.workflow, request.context)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflow/types")
async def get_workflow_types():
    """Get available workflow types"""
    return {
        "success": True,
        "data": {
            "workflows": [
                {
                    "id": "sprint_end",
                    "name": "Sprint End",
                    "description": "Complete sprint end workflow with summary and retrospective"
                },
                {
                    "id": "sprint_start",
                    "name": "Sprint Start",
                    "description": "Sprint kickoff workflow"
                },
                {
                    "id": "daily_routine",
                    "name": "Daily Routine",
                    "description": "Daily standup and progress tracking"
                }
            ]
        }
    }


# Agent information
@app.get("/agents")
async def get_agents():
    """Get information about available agents"""
    return {
        "success": True,
        "data": {
            "agents": [
                {
                    "name": "Standup Master",
                    "role": "Daily Standup Facilitator",
                    "capabilities": [
                        "Conduct daily standups",
                        "Collect team updates",
                        "Identify blockers"
                    ]
                },
                {
                    "name": "Track Master",
                    "role": "Sprint Progress Tracker",
                    "capabilities": [
                        "Monitor sprint progress",
                        "Calculate velocity",
                        "Analyze burndown",
                        "Assess sprint health"
                    ]
                },
                {
                    "name": "Report Master",
                    "role": "Reporter and Retrospective Facilitator",
                    "capabilities": [
                        "Generate sprint reports",
                        "Facilitate retrospectives",
                        "Track velocity trends"
                    ]
                }
            ]
        }
    }


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the web server"""
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
