"""FastAPI application factory and configuration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.config import settings
from src.api.routes import health, sprints, standups, retrospectives, crewai, slack
from src.storage.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Debug mode: {settings.debug}")
    print(f"AI Model: {settings.model_name}")

    # Initialize database
    init_db()
    print("Database initialized")

    yield

    # Shutdown
    print("Shutting down application")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="An intelligent Scrum Master assistant powered by AI",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # Include routers
    app.include_router(health.router, tags=["Health"])
    app.include_router(
        sprints.router,
        prefix=f"{settings.api_prefix}/sprints",
        tags=["Sprints"]
    )
    app.include_router(
        standups.router,
        prefix=f"{settings.api_prefix}/standups",
        tags=["Standups"]
    )
    app.include_router(
        retrospectives.router,
        prefix=f"{settings.api_prefix}/retrospectives",
        tags=["Retrospectives"]
    )
    app.include_router(
        crewai.router,
        prefix=f"{settings.api_prefix}/crewai",
        tags=["CrewAI Playground"]
    )
    app.include_router(
        slack.router,
        prefix="/slack",
        tags=["Slack Integration"]
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Global exception handler."""
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc) if settings.debug else "An error occurred"
            }
        )

    return app


# Create app instance
app = create_app()
