#!/bin/bash

# Script to start ngrok tunnel for Slack webhook development
# This creates a public HTTPS URL that forwards to your local FastAPI server

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}Starting ngrok for Slack webhooks${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}Error: ngrok is not installed${NC}"
    echo ""
    echo "To install ngrok:"
    echo "1. Visit: https://ngrok.com/download"
    echo "2. Download for your platform"
    echo "3. Install and add to PATH"
    echo ""
    echo "Alternative installation methods:"
    echo "  - macOS: brew install ngrok"
    echo "  - Linux: snap install ngrok"
    echo "  - Or download directly from ngrok.com"
    echo ""
    exit 1
fi

# Get port from .env or use default
PORT=${PORT:-8000}

echo -e "${YELLOW}Configuration:${NC}"
echo "  Local port: $PORT"
echo "  Protocol: HTTP"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}Created .env file. Please update it with your credentials.${NC}"
    else
        echo -e "${RED}Error: .env.example not found${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Starting ngrok tunnel...${NC}"
echo ""
echo -e "${YELLOW}Next steps after ngrok starts:${NC}"
echo "1. Copy the HTTPS URL (e.g., https://abc123.ngrok.io)"
echo "2. Go to https://api.slack.com/apps"
echo "3. Select your app"
echo "4. Configure Event Subscriptions:"
echo "   - Request URL: <ngrok-url>/slack/events"
echo "5. Configure Interactivity & Shortcuts:"
echo "   - Request URL: <ngrok-url>/slack/interactions"
echo "6. Configure Slash Commands:"
echo "   - Request URL: <ngrok-url>/slack/commands"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop ngrok${NC}"
echo ""
echo "======================================"
echo ""

# Start ngrok
ngrok http $PORT
