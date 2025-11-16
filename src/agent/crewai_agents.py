"""CrewAI agents and crew configuration for scrum master tasks."""

from crewai import Agent, Crew, Task, Process
from crewai.llm import LLM
from typing import List, Dict, Any
from src.config import settings


def create_scrum_master_agents() -> Dict[str, Agent]:
    """
    Create and return a collection of AI agents for scrum master tasks.

    Returns:
        Dictionary of agent names to Agent objects
    """
    # Configure the LLM to use Anthropic Claude
    llm = LLM(
        model=f"anthropic/{settings.model_name}",
        api_key=settings.anthropic_api_key,
        temperature=settings.temperature
    )

    # Product Owner Agent - Focuses on backlog management and prioritization
    product_owner = Agent(
        role="Product Owner",
        goal="Manage and prioritize the product backlog effectively",
        backstory="""You are an experienced Product Owner with deep understanding
        of agile methodologies. You excel at understanding user needs, creating
        user stories, and prioritizing features based on business value.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # Scrum Master Agent - Facilitates scrum ceremonies and removes impediments
    scrum_master = Agent(
        role="Scrum Master",
        goal="Facilitate scrum ceremonies and help the team follow agile practices",
        backstory="""You are a certified Scrum Master with years of experience
        in facilitating agile teams. You are great at identifying and removing
        impediments, coaching teams, and ensuring scrum practices are followed.""",
        verbose=True,
        allow_delegation=True,
        llm=llm
    )

    # Developer Agent - Provides technical insights and estimations
    developer = Agent(
        role="Senior Developer",
        goal="Provide technical insights and realistic estimations",
        backstory="""You are a senior software developer with extensive experience
        in various technologies. You excel at breaking down complex features into
        technical tasks and providing accurate time estimations.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    # QA Agent - Focuses on quality assurance and testing
    qa_engineer = Agent(
        role="QA Engineer",
        goal="Ensure quality through comprehensive testing strategies",
        backstory="""You are an experienced QA engineer who believes in quality
        first. You excel at creating test plans, identifying edge cases, and
        ensuring comprehensive test coverage.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

    return {
        "product_owner": product_owner,
        "scrum_master": scrum_master,
        "developer": developer,
        "qa_engineer": qa_engineer
    }


def create_sprint_planning_crew() -> Crew:
    """
    Create a crew for sprint planning tasks.

    Returns:
        Configured Crew object for sprint planning
    """
    agents = create_scrum_master_agents()

    # Define tasks for sprint planning
    backlog_review_task = Task(
        description="""Review the product backlog and identify the highest
        priority items for the upcoming sprint. Consider business value,
        dependencies, and team capacity.""",
        agent=agents["product_owner"],
        expected_output="A prioritized list of user stories for the sprint"
    )

    technical_review_task = Task(
        description="""Review the selected user stories and break them down
        into technical tasks. Provide effort estimates for each task.""",
        agent=agents["developer"],
        expected_output="Technical breakdown with effort estimates"
    )

    testing_strategy_task = Task(
        description="""Create a testing strategy for the sprint including
        test cases, acceptance criteria, and quality gates.""",
        agent=agents["qa_engineer"],
        expected_output="Comprehensive testing strategy document"
    )

    sprint_plan_task = Task(
        description="""Based on the backlog review, technical breakdown, and
        testing strategy, create a comprehensive sprint plan.""",
        agent=agents["scrum_master"],
        expected_output="Complete sprint plan with goals and commitments"
    )

    # Create crew with sequential process
    crew = Crew(
        agents=list(agents.values()),
        tasks=[
            backlog_review_task,
            technical_review_task,
            testing_strategy_task,
            sprint_plan_task
        ],
        process=Process.sequential,
        verbose=True
    )

    return crew


def create_retrospective_crew() -> Crew:
    """
    Create a crew for sprint retrospective analysis.

    Returns:
        Configured Crew object for retrospectives
    """
    agents = create_scrum_master_agents()

    # Define tasks for retrospective
    feedback_collection_task = Task(
        description="""Collect and analyze feedback from team members about
        what went well, what didn't go well, and what can be improved.""",
        agent=agents["scrum_master"],
        expected_output="Organized feedback from all team perspectives"
    )

    improvement_suggestions_task = Task(
        description="""Based on the collected feedback, suggest concrete
        action items for improvement in the next sprint.""",
        agent=agents["scrum_master"],
        expected_output="List of actionable improvement items"
    )

    # Create crew
    crew = Crew(
        agents=[agents["scrum_master"]],
        tasks=[feedback_collection_task, improvement_suggestions_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


def create_standup_analysis_crew() -> Crew:
    """
    Create a crew for daily standup analysis.

    Returns:
        Configured Crew object for standup analysis
    """
    agents = create_scrum_master_agents()

    # Define task for standup analysis
    standup_analysis_task = Task(
        description="""Analyze the daily standup updates and identify:
        1. Progress made
        2. Potential blockers or impediments
        3. Tasks at risk of not being completed
        4. Team collaboration opportunities""",
        agent=agents["scrum_master"],
        expected_output="Daily standup analysis with actionable insights"
    )

    # Create crew
    crew = Crew(
        agents=[agents["scrum_master"]],
        tasks=[standup_analysis_task],
        process=Process.sequential,
        verbose=True
    )

    return crew
