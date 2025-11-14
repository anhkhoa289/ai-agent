# Scrum Master AI Agent

An intelligent Scrum Master assistant that communicates through Slack to help agile teams manage sprints, facilitate standups, and improve team productivity.

## Features

- **Slack Integration**: Natural conversation through Slack with slash commands and interactive modals
- **Daily Standup Management**: Collect and summarize team updates with blocker identification
- **Sprint Planning Assistance**: Help with story estimation, sprint goal setting, and backlog refinement
- **Retrospective Facilitation**: Guide teams through retrospectives with AI-powered insights
- **Team Velocity Tracking**: Monitor and analyze team performance over time
- **Intelligent Responses**: Powered by Claude AI for context-aware assistance

## Architecture

The system uses a clean, modular architecture:

```
┌─────────────────────────────────────────┐
│           Slack Interface               │
│   (Messages, Commands, Modals)          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Scrum Master AI Agent             │
│      (Claude AI Integration)            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Storage Layer                   │
│    (Sprint Data, Team Metrics)          │
└─────────────────────────────────────────┘
```

**Key Components:**
- **Slack Bot** (src/slack/bot.py): Handles Slack events, commands, and interactions
- **AI Agent** (src/agent/scrum_master.py): Core intelligence using Claude for responses
- **Database** (src/storage/database.py): Stores sprint data, standups, and metrics
- **Configuration** (src/config.py): Environment-based configuration management

## Setup

### Prerequisites

- Python 3.9+
- Slack workspace with admin access
- Anthropic API key for Claude

### Step 1: Slack App Configuration

1. Go to [api.slack.com/apps](https://api.slack.com/apps) and create a new app
2. Choose "From scratch" and name it (e.g., "Scrum Master")
3. Under "OAuth & Permissions", add these Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `commands`
   - `im:history`
   - `im:read`
   - `im:write`
   - `users:read`
   - `channels:read`
   - `groups:read`

4. Under "Event Subscriptions", enable events and subscribe to:
   - `app_mention`
   - `message.im`

5. Under "Interactivity & Shortcuts":
   - Enable Interactivity
   - Add a Request URL (you can use ngrok for local development)

6. Under "Slash Commands", create these commands:
   - `/standup` - "Submit daily standup update"
   - `/sprint-planning` - "Get help with sprint planning"
   - `/retrospective` - "Start a retrospective"
   - `/estimate` - "Estimate story points"

7. Enable "Socket Mode" under "Socket Mode" section (for local development)
8. Install the app to your workspace

### Step 2: Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-agent
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
# Get these from your Slack app settings
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
SLACK_SIGNING_SECRET=your-signing-secret

# Get this from Anthropic Console (console.anthropic.com)
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### Step 3: Run the Bot

```bash
python main.py
```

You should see:
```
INFO - Configuration loaded successfully
INFO - Using model: claude-sonnet-4-5-20250929
INFO - Scrum Master AI Agent is starting...
```

## Usage

### Slack Commands

**Slash Commands:**

- `/standup` - Opens a modal to submit your daily standup update
  - What did you work on yesterday?
  - What will you work on today?
  - Any blockers or impediments?

- `/sprint-planning [topic]` - Get help with sprint planning
  - Example: `/sprint-planning capacity planning for 2-week sprint`

- `/retrospective` - Start a retrospective session
  - The bot will guide you through what went well, what didn't, and improvements

- `/estimate <user story>` - Get AI-assisted story point estimation
  - Example: `/estimate Add user authentication with OAuth`

**Direct Messages:**

You can also directly message the bot or mention it in channels:

- `@ScrumMaster help me plan the next sprint`
- `@ScrumMaster what's our team velocity?`
- `@ScrumMaster analyze yesterday's standup updates`

**Example Conversations:**

```
You: @ScrumMaster How should we approach sprint planning for a new team?

Bot: Great question! For a new team, I recommend:

*Sprint Planning Approach:*
1. Start with a shorter sprint (1 week) to establish baseline velocity
2. Focus on team capacity and working agreements first
3. Keep initial commitments conservative

*Key Activities:*
- Review and refine backlog items together
- Ensure everyone understands the Definition of Done
- Break down stories to similar sizes (3-5 points)
- Leave buffer time for unknowns (~20%)

Would you like help with any specific aspect?
```

## Development

### Project Structure

```
.
├── src/
│   ├── agent/
│   │   ├── scrum_master.py      # Core AI agent logic with Claude
│   │   └── __init__.py
│   ├── slack/
│   │   ├── bot.py               # Slack event handlers and commands
│   │   └── __init__.py
│   ├── storage/
│   │   ├── database.py          # SQLite database manager
│   │   └── __init__.py
│   ├── config.py                # Configuration management
│   └── __init__.py
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
└── README.md                    # This file
```

### Key Files

**src/agent/scrum_master.py** - The core AI agent that:
- Maintains conversation context per channel
- Provides specialized methods for standup, sprint planning, and retrospectives
- Uses Claude with a custom system prompt for Scrum Master behavior

**src/slack/bot.py** - The Slack integration that:
- Registers event handlers for messages and mentions
- Implements slash commands with interactive modals
- Manages the connection between Slack and the AI agent

**src/storage/database.py** - Data persistence for:
- Standup updates and history
- Sprint information and tracking
- Team velocity calculations
- User stories and backlog items

### Extending the Bot

**Add a new slash command:**

1. Register the command in Slack App settings
2. Add a handler in `src/slack/bot.py`:

```python
@self.app.command("/your-command")
def handle_your_command(ack, command, client):
    ack()
    # Your logic here
```

**Add new AI capabilities:**

Add methods to `ScrumMasterAgent` class in `src/agent/scrum_master.py`:

```python
def your_new_feature(self, data: Dict[str, Any]) -> str:
    prompt = f"Analyze this data: {json.dumps(data)}"
    return self.get_response(prompt)
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-mock

# Run tests
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Check style
flake8 src/

# Type checking
mypy src/
```

## Troubleshooting

**Bot doesn't respond:**
- Check that Socket Mode is enabled in Slack App settings
- Verify all tokens in `.env` are correct
- Check bot has required OAuth scopes
- Look for errors in console output

**Database errors:**
- The SQLite database is created automatically on first run
- Check file permissions in the working directory
- Database location: `scrum_master.db`

**API rate limits:**
- Slack has rate limits on API calls
- Anthropic Claude API has usage limits based on your plan
- Consider implementing caching for frequently accessed data

## Future Enhancements

Potential features to add:
- Integration with Jira/Linear for automatic story tracking
- Scheduled standup reminders
- Burndown chart generation
- Team mood tracking and analytics
- Multi-language support
- Voice/video standup transcription

## License

MIT
