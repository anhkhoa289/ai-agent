#!/bin/bash

# Start development environment with FastAPI and ngrok in parallel
# This script runs both the FastAPI server and ngrok tunnel

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Starting Development Environment${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if Python virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Warning: No virtual environment detected${NC}"
    echo "Checking for venv..."

    if [ -d "venv" ]; then
        echo "Activating venv..."
        source venv/bin/activate
    else
        echo -e "${RED}Error: venv not found${NC}"
        echo "Run: python -m venv venv"
        exit 1
    fi
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo -e "${GREEN}Please configure .env with your credentials${NC}"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip install -q -r requirements.txt

echo ""
echo -e "${GREEN}Starting FastAPI server on port 8000...${NC}"
echo ""

# Start FastAPI in background
python main.py &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 3

# Check if FastAPI is running
if ! kill -0 $FASTAPI_PID 2>/dev/null; then
    echo -e "${RED}Error: FastAPI failed to start${NC}"
    exit 1
fi

echo -e "${GREEN}FastAPI is running (PID: $FASTAPI_PID)${NC}"
echo ""
echo -e "${YELLOW}Starting ngrok tunnel...${NC}"
echo ""

# Start ngrok (this will run in foreground)
ngrok http 8000

# Cleanup on exit
echo ""
echo "Stopping FastAPI server..."
kill $FASTAPI_PID
echo -e "${GREEN}Shutdown complete${NC}"
