#!/usr/bin/env python3
"""
Scrum Master AI Agent - Main Entry Point

This script starts the FastAPI application using Uvicorn.
"""

import uvicorn
from src.config import settings


def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
    )


if __name__ == "__main__":
    main()
