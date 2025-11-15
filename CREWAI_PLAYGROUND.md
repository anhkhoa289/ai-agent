# CrewAI Playground

This document provides information about the CrewAI routes added to the Scrum Master AI Agent.

## Overview

CrewAI has been integrated into this project to enable AI agent collaboration for various scrum master tasks. The agents work together to provide comprehensive insights and recommendations.

## Available Agents

The system includes four specialized agents:

1. **Product Owner**: Manages and prioritizes product backlog
2. **Scrum Master**: Facilitates scrum ceremonies and removes impediments
3. **Senior Developer**: Provides technical insights and estimations
4. **QA Engineer**: Ensures quality through comprehensive testing strategies

## API Endpoints

All CrewAI endpoints are available under `/api/v1/crewai/`

### 1. List Available Agents

```
GET /api/v1/crewai/agents
```

Returns information about all available AI agents including their roles, goals, and backstories.

### 2. Test CrewAI Installation

```
GET /api/v1/crewai/test
```

Simple endpoint to verify that CrewAI is properly installed and working.

### 3. Sprint Planning Crew

```
POST /api/v1/crewai/sprint-planning
```

Runs the sprint planning crew with all four agents collaborating to create a comprehensive sprint plan.

**Request Body:**
```json
{
  "context": "We need to plan the next sprint for our e-commerce platform. We have 15 user stories in the backlog ranging from adding new payment methods to improving search functionality.",
  "additional_info": {}
}
```

### 4. Retrospective Analysis

```
POST /api/v1/crewai/retrospective
```

Runs the retrospective crew to analyze sprint feedback and suggest improvements.

**Request Body:**
```json
{
  "context": "Last sprint we completed 8 out of 10 stories. Team mentioned issues with unclear requirements and too many meetings interrupting deep work time.",
  "additional_info": {}
}
```

### 5. Daily Standup Analysis

```
POST /api/v1/crewai/standup-analysis
```

Analyzes daily standup updates to identify blockers, risks, and collaboration opportunities.

**Request Body:**
```json
{
  "context": "John: Completed user authentication, working on API integration today, blocked by missing API keys. Sarah: Finished UI mockups, starting implementation today, no blockers. Mike: Bug fixing in payment module, will continue today, concerned about timeline.",
  "additional_info": {}
}
```

### 6. Custom Crew

```
POST /api/v1/crewai/custom-crew
```

Runs a custom crew configuration for general scrum master tasks. Useful for playground and testing.

**Request Body:**
```json
{
  "context": "Analyze our team velocity over the last 3 sprints and provide recommendations for improvement.",
  "additional_info": {}
}
```

## Example Usage with curl

```bash
# Test CrewAI installation
curl http://localhost:8000/api/v1/crewai/test

# List agents
curl http://localhost:8000/api/v1/crewai/agents

# Run custom analysis
curl -X POST http://localhost:8000/api/v1/crewai/custom-crew \
  -H "Content-Type: application/json" \
  -d '{
    "context": "What are best practices for managing technical debt in an agile team?"
  }'
```

## Configuration

CrewAI agents use the LLM configuration from your environment variables. Make sure you have set up your API keys:

```bash
# For OpenAI (default)
export OPENAI_API_KEY="your-api-key-here"

# Or for Anthropic Claude
export ANTHROPIC_API_KEY="your-api-key-here"
```

## Notes

- The crews run sequentially by default, meaning each agent completes their task before the next one starts
- Crew execution may take some time depending on the complexity of the task and the LLM response time
- All crew results are returned as structured text outputs
- The agents are configured with verbose=True for detailed execution logs

## Future Enhancements

Potential improvements for the CrewAI integration:

- [ ] Add support for parallel crew execution
- [ ] Implement custom tool integration
- [ ] Add memory and context persistence across crew runs
- [ ] Create specialized crews for backlog grooming
- [ ] Implement user story generation crews
- [ ] Add metrics and analytics tracking for crew performance
