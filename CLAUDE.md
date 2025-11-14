# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Scrum Master AI Agent project designed to assist with agile project management tasks.

## Development Setup

Since this is a new project, the codebase is currently empty. When implementing this project, consider the following architecture decisions:

### Recommended Project Structure

- **Agent Core**: Main AI agent logic for scrum master functionality
- **Task Management**: Handling user stories, sprints, and backlog items
- **Communication**: Interfaces for team interaction (chat, notifications, etc.)
- **Integration**: Connectors for project management tools (Jira, GitHub, etc.)
- **Storage**: Persistence layer for sprint data and team metrics

### Technology Considerations

When selecting technologies for this project:
- Choose a language/framework suitable for AI/LLM integration (Python, TypeScript/Node.js, etc.)
- Consider LLM API integration (OpenAI, Anthropic Claude, etc.)
- Plan for asynchronous task processing
- Design for extensibility with different project management platforms

## Development Workflow

Once the codebase is established, this section should be updated with:
- Build commands
- Test execution commands
- Linting and formatting commands
- Deployment procedures

## Architecture Notes

Key architectural considerations for a Scrum Master AI Agent:

### Core Responsibilities
- Sprint planning assistance
- Daily standup facilitation
- Retrospective analysis
- Backlog refinement
- Team velocity tracking
- Impediment identification and resolution

### Integration Points
- Project management systems
- Communication platforms (Slack, Teams, etc.)
- Version control systems
- CI/CD pipelines

### Data Model
- Teams and team members
- Sprints and sprint cycles
- User stories and tasks
- Metrics and analytics
