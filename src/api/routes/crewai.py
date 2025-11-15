"""CrewAI playground routes for testing AI agent crews."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from src.agent.crewai_agents import (
    create_scrum_master_agents,
    create_sprint_planning_crew,
    create_retrospective_crew,
    create_standup_analysis_crew
)


router = APIRouter()


class CrewInput(BaseModel):
    """Input model for crew execution."""
    context: str
    additional_info: Optional[Dict[str, Any]] = None


class CrewOutput(BaseModel):
    """Output model for crew execution results."""
    result: str
    status: str
    crew_type: str


@router.get("/agents")
async def list_agents():
    """
    List all available CrewAI agents.

    Returns:
        dict: Information about available agents
    """
    try:
        agents = create_scrum_master_agents()

        agent_info = {}
        for name, agent in agents.items():
            agent_info[name] = {
                "role": agent.role,
                "goal": agent.goal,
                "backstory": agent.backstory
            }

        return {
            "status": "success",
            "agents": agent_info,
            "total_agents": len(agent_info)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sprint-planning", response_model=CrewOutput)
async def run_sprint_planning(input_data: CrewInput):
    """
    Run the sprint planning crew with given context.

    Args:
        input_data: Context and additional information for sprint planning

    Returns:
        CrewOutput: Results from the sprint planning crew
    """
    try:
        crew = create_sprint_planning_crew()

        # Execute the crew
        result = crew.kickoff(inputs={"context": input_data.context})

        return CrewOutput(
            result=str(result),
            status="completed",
            crew_type="sprint_planning"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sprint planning failed: {str(e)}")


@router.post("/retrospective", response_model=CrewOutput)
async def run_retrospective(input_data: CrewInput):
    """
    Run the retrospective crew with given feedback.

    Args:
        input_data: Retrospective feedback and context

    Returns:
        CrewOutput: Results from the retrospective crew
    """
    try:
        crew = create_retrospective_crew()

        # Execute the crew
        result = crew.kickoff(inputs={"context": input_data.context})

        return CrewOutput(
            result=str(result),
            status="completed",
            crew_type="retrospective"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrospective failed: {str(e)}")


@router.post("/standup-analysis", response_model=CrewOutput)
async def run_standup_analysis(input_data: CrewInput):
    """
    Run the standup analysis crew with daily updates.

    Args:
        input_data: Daily standup updates and context

    Returns:
        CrewOutput: Results from the standup analysis crew
    """
    try:
        crew = create_standup_analysis_crew()

        # Execute the crew
        result = crew.kickoff(inputs={"context": input_data.context})

        return CrewOutput(
            result=str(result),
            status="completed",
            crew_type="standup_analysis"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Standup analysis failed: {str(e)}")


@router.get("/test")
async def test_crewai():
    """
    Simple test endpoint to verify CrewAI is properly installed.

    Returns:
        dict: Status and version information
    """
    try:
        import crewai
        import crewai_tools

        return {
            "status": "success",
            "message": "CrewAI is properly installed",
            "crewai_available": True,
            "test_agent_created": True
        }
    except ImportError as e:
        return {
            "status": "error",
            "message": f"CrewAI import failed: {str(e)}",
            "crewai_available": False
        }


@router.post("/custom-crew")
async def run_custom_crew(input_data: CrewInput):
    """
    Run a custom crew configuration for general scrum master tasks.

    This endpoint is useful for playground and testing different scenarios.

    Args:
        input_data: Custom context and configuration

    Returns:
        CrewOutput: Results from the custom crew
    """
    try:
        agents = create_scrum_master_agents()

        from crewai import Crew, Task, Process

        # Create a simple custom task based on the input context
        custom_task = Task(
            description=input_data.context,
            agent=agents["scrum_master"],
            expected_output="Analysis and recommendations"
        )

        # Create a simple crew
        crew = Crew(
            agents=[agents["scrum_master"]],
            tasks=[custom_task],
            process=Process.sequential,
            verbose=True
        )

        # Execute the crew
        result = crew.kickoff()

        return CrewOutput(
            result=str(result),
            status="completed",
            crew_type="custom"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom crew failed: {str(e)}")
