# Scrum Master AI Agent - FastAPI

An intelligent Scrum Master assistant built with FastAPI and powered by Anthropic Claude AI. This RESTful API helps agile teams manage sprints, facilitate standups, conduct retrospectives, and improve team productivity.

## Features

- **RESTful API**: Clean, modern FastAPI-based REST API
- **AI-Powered Insights**: Leverage Claude AI for intelligent scrum assistance
- **Sprint Management**: Create and track sprints with goals and velocity metrics
- **Daily Standups**: Record and analyze standup updates with blocker detection
- **Retrospectives**: Conduct retrospectives with AI-generated insights
- **Story Estimation**: Get AI-assisted story point estimation guidance
- **SQLite Database**: Simple, file-based persistence
- **Buildpack Support**: Deploy with Cloud Native Buildpacks or Google Cloud Build
- **Interactive Docs**: Auto-generated Swagger UI and ReDoc documentation

## Quick Start

### Prerequisites

- Python 3.11+
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd ai-agent
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

5. **Run the application:**
```bash
python main.py
```

The API will start at `http://localhost:8000`

### Development with PostgreSQL (Docker Compose)

For local development with PostgreSQL database:

1. **Start PostgreSQL database:**
```bash
docker-compose up -d
```

2. **Update `.env` file with PostgreSQL connection:**
```bash
DATABASE_URL=postgresql://scrum_user:scrum_password@localhost:5432/scrum_master
```

3. **Run the application locally:**
```bash
python main.py
```

4. **Stop database:**
```bash
docker-compose down
```

5. **Stop and remove volumes (clean database):**
```bash
docker-compose down -v
```

The docker-compose provides:
- **PostgreSQL 16** database with persistent volume
- Accessible at `localhost:5432`
- Default credentials: `scrum_user` / `scrum_password`
- Database name: `scrum_master`

## API Documentation

Once running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Project Structure

```
ai-agent/
├── src/
│   ├── api/
│   │   └── routes/
│   │       ├── health.py          # Health check endpoints
│   │       ├── sprints.py         # Sprint CRUD operations
│   │       ├── standups.py        # Standup management
│   │       └── retrospectives.py  # Retrospective endpoints
│   ├── agent/
│   │   └── scrum_master.py        # AI agent logic
│   ├── models/
│   │   ├── base.py                # SQLAlchemy base
│   │   ├── sprint.py              # Sprint model
│   │   ├── standup.py             # Standup model
│   │   └── retrospective.py       # Retrospective model
│   ├── schemas/
│   │   ├── sprint.py              # Sprint Pydantic schemas
│   │   ├── standup.py             # Standup Pydantic schemas
│   │   └── retrospective.py       # Retrospective Pydantic schemas
│   ├── storage/
│   │   └── database.py            # Database configuration
│   ├── config.py                  # Application settings
│   └── main.py                    # FastAPI app factory
├── main.py                        # Application entry point
├── requirements.txt               # Python dependencies
├── Procfile                       # Process definition for buildpack
├── makefile                       # Build and deployment commands
├── docker-compose.yml             # PostgreSQL for local dev
├── .env.example                   # Example environment variables
└── README.md                      # This file
```

## API Endpoints

### Health Check
- `GET /health` - Health check with app info
- `GET /` - Root endpoint with API information

### Sprints
- `POST /api/v1/sprints` - Create a new sprint
- `GET /api/v1/sprints` - List all sprints (with optional filters)
- `GET /api/v1/sprints/{sprint_id}` - Get sprint details
- `PATCH /api/v1/sprints/{sprint_id}` - Update a sprint
- `DELETE /api/v1/sprints/{sprint_id}` - Delete a sprint

### Standups
- `POST /api/v1/standups` - Submit a standup update
- `GET /api/v1/standups` - List standups (with filters: user, sprint, blockers, date range)
- `GET /api/v1/standups/{standup_id}` - Get standup details
- `DELETE /api/v1/standups/{standup_id}` - Delete a standup

### Retrospectives
- `POST /api/v1/retrospectives` - Create retrospective with AI insights
- `GET /api/v1/retrospectives` - List retrospectives (with sprint filter)
- `GET /api/v1/retrospectives/{retro_id}` - Get retrospective details
- `DELETE /api/v1/retrospectives/{retro_id}` - Delete a retrospective

## Usage Examples

### Create a Sprint

```bash
curl -X POST "http://localhost:8000/api/v1/sprints" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sprint 1",
    "goal": "Implement user authentication",
    "start_date": "2025-11-15T00:00:00",
    "end_date": "2025-11-29T00:00:00",
    "team_capacity": 80,
    "committed_points": 34
  }'
```

### Submit a Standup

```bash
curl -X POST "http://localhost:8000/api/v1/standups" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "user_name": "John Doe",
    "yesterday": "Completed user login API endpoint",
    "today": "Working on password reset functionality",
    "blockers": "Need database migration approval",
    "sprint_id": 1
  }'
```

### Create a Retrospective

```bash
curl -X POST "http://localhost:8000/api/v1/retrospectives" \
  -H "Content-Type: application/json" \
  -d '{
    "sprint_id": 1,
    "conducted_by": "Scrum Master",
    "went_well": {
      "items": ["Good team collaboration", "Met sprint goals"]
    },
    "went_wrong": {
      "items": ["Some tasks took longer than estimated"]
    },
    "improvements": {
      "items": ["Better story breakdown", "More frequent code reviews"]
    },
    "action_items": {
      "items": ["Schedule estimation workshop", "Set up automated testing"]
    }
  }'
```

The API will automatically generate AI insights for the retrospective!

### List Sprints with Filters

```bash
# Get only active sprints
curl "http://localhost:8000/api/v1/sprints?status_filter=active"

# Get all sprints with pagination
curl "http://localhost:8000/api/v1/sprints?skip=0&limit=10"
```

### Get Standups with Blockers

```bash
curl "http://localhost:8000/api/v1/standups?has_blockers=true"
```

## AI Agent Capabilities

The Scrum Master AI agent (`src/agent/scrum_master.py`) provides:

### 1. Standup Analysis
Analyzes daily standup updates to identify:
- Progress patterns and team focus
- Potential risks or concerns
- Blocker resolution strategies
- Actionable next steps

### 2. Sprint Planning Assistance
Helps with:
- Capacity and velocity planning
- Story prioritization
- Risk and dependency identification
- Sprint goal setting

### 3. Retrospective Insights
Generates:
- Pattern and theme identification
- Root cause analysis
- Improvement suggestions
- Action item prioritization
- Success metrics recommendations

### 4. Story Estimation
Provides:
- Story point estimates (Fibonacci scale)
- Complexity factor analysis
- Clarifying questions
- Story breakdown suggestions

## Configuration

All configuration is managed through environment variables in `.env`:

```bash
# FastAPI Settings
DEBUG=false                          # Enable debug mode
HOST=0.0.0.0                        # Server host
PORT=8000                           # Server port

# AI Configuration
ANTHROPIC_API_KEY=sk-ant-xxx        # Your Anthropic API key (required)
MODEL_NAME=claude-sonnet-4-5-20250929  # Claude model to use
MAX_TOKENS=4096                     # Max response tokens
TEMPERATURE=0.7                     # Response creativity (0-1)

# Database
# For local development with SQLite (simple, no setup required)
# DATABASE_URL=sqlite:///./scrum_master.db

# For local development with PostgreSQL (recommended, use docker-compose)
DATABASE_URL=postgresql://scrum_user:scrum_password@localhost:5432/scrum_master

# For production (use environment-specific credentials)
# DATABASE_URL=postgresql://user:password@host:port/database

# Feature Flags
ENABLE_DAILY_STANDUP=true
ENABLE_SPRINT_PLANNING=true
ENABLE_RETROSPECTIVES=true

# CORS
CORS_ORIGINS=*                      # Allowed CORS origins
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

### Database Migrations

The application uses SQLAlchemy and creates tables automatically on startup. For production, consider using Alembic:

```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Deployment

### Google Cloud Build

Build and deploy to Google Artifact Registry using Cloud Build:

```bash
# Build and push to artifact registry
make gcloud-build

# Or with full command
gcloud builds submit --async --tag <region>-docker.pkg.dev/<project-id>/<repository>/<image-name>:<version>
```

### Cloud Native Buildpacks

Build using Paketo buildpacks locally:

```bash
# Build with buildpacks
make pack-load

# Or with full command
pack build <image-name>:<version> --builder paketobuildpacks/builder-jammy-base
```

### Manual Deployment

1. Set up Python 3.11+ environment
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run with production server: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### Production Considerations

- Use a production database (PostgreSQL recommended)
- Set `DEBUG=false`
- Configure proper CORS origins
- Use HTTPS/TLS
- Set up monitoring and logging
- Configure rate limiting
- Use environment secrets management (Google Secret Manager)
- Set up database backups
- Deploy to Cloud Run or Google Kubernetes Engine

## Extending the API

### Adding a New Endpoint

1. **Create a schema** in `src/schemas/`:
```python
from pydantic import BaseModel

class MyFeatureCreate(BaseModel):
    name: str
    description: str
```

2. **Create a model** in `src/models/`:
```python
from src.models.base import Base, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column

class MyFeature(Base, TimestampMixin):
    __tablename__ = "my_features"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
```

3. **Create a router** in `src/api/routes/`:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.storage.database import get_db

router = APIRouter()

@router.post("/")
async def create_feature(feature: MyFeatureCreate, db: Session = Depends(get_db)):
    # Implementation
    pass
```

4. **Register the router** in `src/main.py`:
```python
from src.api.routes import my_feature
app.include_router(my_feature.router, prefix="/api/v1/my-features", tags=["MyFeature"])
```

## Troubleshooting

**API doesn't start:**
- Check that port 8000 is available
- Verify Python version (3.11+)
- Ensure all dependencies are installed

**Database errors:**
- Database file is created automatically
- Check file permissions in the working directory
- For production, use PostgreSQL with proper connection string

**AI responses fail:**
- Verify `ANTHROPIC_API_KEY` is set correctly
- Check API key has sufficient credits
- Ensure internet connectivity for API calls

**Buildpack deployment issues:**
- Ensure Python version is specified correctly (3.11+)
- Check that `requirements.txt` is in the root directory
- Verify Procfile syntax is correct
- For Google Cloud Build, ensure proper project permissions

## Documentation

See the `/docs` folder for additional documentation:
- [Slack Integration Guide](docs/SLACK_SETUP.md)
- [Jira API Integration](docs/JIRA_API.md)
- [Trello API Integration](docs/TRELLO_API.md)
- [CrewAI Integration](docs/CREWAI.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the existing documentation in `/docs` folder

---

**Built with FastAPI, Claude AI, and SQLAlchemy**
