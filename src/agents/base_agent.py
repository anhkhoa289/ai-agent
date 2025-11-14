"""
Base agent class for all scrum master agents
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from crewai import Agent


class BaseAgent(ABC):
    """Base class for all scrum master agents"""

    def __init__(self, name: str, role: str, goal: str, backstory: str):
        """
        Initialize base agent

        Args:
            name: Agent name
            role: Agent's role in the crew
            goal: Agent's goal
            backstory: Agent's backstory/context
        """
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self._agent: Optional[Agent] = None

    def create_agent(self, **kwargs) -> Agent:
        """
        Create and return CrewAI agent instance

        Args:
            **kwargs: Additional arguments for Agent creation

        Returns:
            CrewAI Agent instance
        """
        self._agent = Agent(
            name=self.name,
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            verbose=True,
            allow_delegation=False,
            **kwargs
        )
        return self._agent

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent's primary task

        Args:
            context: Execution context with relevant data

        Returns:
            Execution result
        """
        pass

    @property
    def agent(self) -> Agent:
        """Get the CrewAI agent instance"""
        if self._agent is None:
            self._agent = self.create_agent()
        return self._agent
