# Ngrok + Slack Webhook Setup Guide

Complete guide for setting up ngrok tunnels and Slack webhooks to receive real-time events from your Slack app.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Step-by-Step Setup](#step-by-step-setup)
- [Configuration](#configuration)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)

---

## Overview

This guide shows you how to:
1. Set up ngrok to create a public HTTPS URL for your local development server
2. Configure Slack webhooks to send events to your FastAPI application
3. Test and debug webhook events

### What is ngrok?

Ngrok creates a secure tunnel from a public URL to your localhost, allowing external services (like Slack) to send webhooks to your development machine.

### Architecture

```
Slack API → ngrok Public URL → ngrok Tunnel → Your Local FastAPI (localhost:8000)
```

---

## Prerequisites

Before starting, ensure you have:

- ✅ Python 3.11+ installed
- ✅ FastAPI application running locally
- ✅ Slack workspace with admin access
- ✅ Slack app created (see [SLACK_SETUP.md](./SLACK_SETUP.md))
- ✅ Anthropic API key
- ✅ Internet connection

---

## Quick Start

### 1. Install ngrok

**macOS:**
```bash
brew install ngrok
```

**Linux (Ubuntu/Debian):**
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok
```

**Windows (PowerShell):**
```powershell
choco install ngrok
```

**Or download directly:**
Visit [ngrok.com/download](https://ngrok.com/download)

### 2. Sign up for ngrok (Optional but Recommended)

1. Visit [ngrok.com](https://ngrok.com) and sign up
2. Get your auth token from the dashboard
3. Configure ngrok with your auth token:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

**Benefits of authentication:**
- Longer session times
- Custom subdomains (paid plans)
- More concurrent tunnels
- Better stability

### 3. Set up environment

```bash
# Clone repository
cd ai-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Edit `.env` and add your credentials:
```bash
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token  # Only for Socket Mode
SLACK_SIGNING_SECRET=your-signing-secret

# AI Configuration
ANTHROPIC_API_KEY=sk-ant-your-api-key

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 4. Start the development environment

**Option A: Automated (Recommended)**
```bash
./scripts/start-dev.sh
```
This script starts both FastAPI and ngrok automatically.

**Option B: Manual**

Terminal 1 - Start FastAPI:
```bash
python main.py
```

Terminal 2 - Start ngrok:
```bash
./scripts/start-ngrok.sh
# Or manually:
ngrok http 8000
```

### 5. Configure Slack webhooks

After ngrok starts, you'll see output like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

Copy the HTTPS URL (`https://abc123.ngrok.io`) and configure Slack:

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Select your app
3. Configure the following:

**Event Subscriptions:**
- Enable Events: ON
- Request URL: `https://abc123.ngrok.io/slack/events`
- Subscribe to bot events:
  - `app_mention`
  - `message.im`

**Interactivity & Shortcuts:**
- Enable Interactivity: ON
- Request URL: `https://abc123.ngrok.io/slack/interactions`

**Slash Commands:**
For each command, set Request URL to:
- `/standup` → `https://abc123.ngrok.io/slack/commands`
- `/sprint-planning` → `https://abc123.ngrok.io/slack/commands`
- `/retrospective` → `https://abc123.ngrok.io/slack/commands`
- `/estimate` → `https://abc123.ngrok.io/slack/commands`

4. Click **Save Changes**
5. **Reinstall your app** (if prompted)

---

## Step-by-Step Setup

### Step 1: Install and Configure ngrok

#### 1.1 Install ngrok

Choose your platform and install ngrok using the methods in [Quick Start](#quick-start).

#### 1.2 Verify installation

```bash
ngrok version
```

Expected output:
```
ngrok version 3.x.x
```

#### 1.3 Create ngrok account (Optional)

1. Visit [ngrok.com](https://ngrok.com)
2. Sign up for a free account
3. Go to [dashboard.ngrok.com/get-started/your-authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
4. Copy your authtoken
5. Add it to ngrok:

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

#### 1.4 Verify configuration

```bash
ngrok config check
```

### Step 2: Prepare Your FastAPI Application

#### 2.1 Ensure all dependencies are installed

```bash
pip install -r requirements.txt
```

#### 2.2 Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:
```bash
# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here

# AI Configuration
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
MODEL_NAME=claude-sonnet-4-5-20250929
```

**Important:**
- `SLACK_SIGNING_SECRET` is required for webhook signature verification
- `SLACK_BOT_TOKEN` is needed to send responses back to Slack

#### 2.3 Test FastAPI locally

```bash
python main.py
```

Visit http://localhost:8000/docs to verify the API is running.

You should see the Slack endpoints:
- `/slack/events`
- `/slack/interactions`
- `/slack/commands`

### Step 3: Start ngrok Tunnel

#### 3.1 Start ngrok

```bash
ngrok http 8000
```

Or use the provided script:
```bash
./scripts/start-ngrok.sh
```

#### 3.2 Understand ngrok output

```
ngrok

Session Status                online
Account                       your-email@example.com (Plan: Free)
Version                       3.5.0
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Key information:**
- **Forwarding URL**: `https://abc123.ngrok.io` - This is your public URL
- **Web Interface**: http://127.0.0.1:4040 - ngrok's request inspector

#### 3.3 Keep ngrok running

**Important:** Keep this terminal window open. If you close it, the tunnel will stop and Slack won't be able to reach your app.

**Note:** Free ngrok URLs change every time you restart ngrok. You'll need to update Slack configuration each time.

### Step 4: Configure Slack App

#### 4.1 Go to Slack App Dashboard

1. Visit [api.slack.com/apps](https://api.slack.com/apps)
2. Select your app (or create one following [SLACK_SETUP.md](./SLACK_SETUP.md))

#### 4.2 Configure Event Subscriptions

1. Click **Event Subscriptions** in the left sidebar
2. Toggle **Enable Events** to **ON**
3. Enter **Request URL**:
   ```
   https://abc123.ngrok.io/slack/events
   ```
   Replace `abc123` with your actual ngrok subdomain

4. Wait for verification ✅ - You should see "Verified"

   **If verification fails:**
   - Check that FastAPI is running
   - Check that ngrok is forwarding correctly
   - Visit ngrok inspector at http://127.0.0.1:4040
   - Check the FastAPI logs for errors

5. Scroll to **Subscribe to bot events**
6. Click **Add Bot User Event** and add:
   - `app_mention` - When someone @mentions your bot
   - `message.im` - Direct messages to your bot

7. Click **Save Changes**

#### 4.3 Configure Interactivity & Shortcuts

1. Click **Interactivity & Shortcuts** in the left sidebar
2. Toggle **Interactivity** to **ON**
3. Enter **Request URL**:
   ```
   https://abc123.ngrok.io/slack/interactions
   ```

4. Click **Save Changes**

#### 4.4 Configure Slash Commands

1. Click **Slash Commands** in the left sidebar
2. For each existing command (or create new ones):

   **Command: `/standup`**
   - Request URL: `https://abc123.ngrok.io/slack/commands`
   - Short Description: Submit your daily standup update

   **Command: `/sprint-planning`**
   - Request URL: `https://abc123.ngrok.io/slack/commands`
   - Short Description: Get help with sprint planning

   **Command: `/retrospective`**
   - Request URL: `https://abc123.ngrok.io/slack/commands`
   - Short Description: Start a retrospective session

   **Command: `/estimate`**
   - Request URL: `https://abc123.ngrok.io/slack/commands`
   - Short Description: Estimate story points for a user story

3. Click **Save** for each command

#### 4.5 Reinstall App (if needed)

If you see a yellow banner saying "You need to reinstall your app":

1. Click **Install App** in the left sidebar
2. Click **Reinstall to Workspace**
3. Click **Allow**

### Step 5: Get Slack Tokens

#### 5.1 Get Bot Token

1. Click **OAuth & Permissions** in the left sidebar
2. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
3. Add to `.env`:
   ```bash
   SLACK_BOT_TOKEN=xoxb-your-token-here
   ```

#### 5.2 Get Signing Secret

1. Click **Basic Information** in the left sidebar
2. Scroll to **App Credentials**
3. Click **Show** next to **Signing Secret**
4. Copy the value
5. Add to `.env`:
   ```bash
   SLACK_SIGNING_SECRET=your-secret-here
   ```

#### 5.3 Restart FastAPI

After updating `.env`:
```bash
# Stop the current process (Ctrl+C)
# Restart
python main.py
```

---

## Configuration

### Environment Variables

Required variables in `.env`:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Slack Configuration (for Webhooks)
SLACK_BOT_TOKEN=xoxb-...           # Required for sending messages
SLACK_SIGNING_SECRET=...            # Required for verifying webhooks

# AI Configuration
ANTHROPIC_API_KEY=sk-ant-...
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
TEMPERATURE=0.7

# Database
DATABASE_URL=sqlite:///./scrum_master.db

# Feature Flags
ENABLE_DAILY_STANDUP=true
ENABLE_SPRINT_PLANNING=true
ENABLE_RETROSPECTIVES=true
```

### ngrok Configuration File

Create `~/.ngrok2/ngrok.yml`:

```yaml
version: "2"
authtoken: YOUR_AUTH_TOKEN

tunnels:
  slack:
    proto: http
    addr: 8000
    bind_tls: true
    inspect: true
```

Start with:
```bash
ngrok start slack
```

---

## Testing

### 1. Test Webhook Endpoint

Visit the ngrok inspector at http://127.0.0.1:4040

You should see all incoming requests from Slack here.

### 2. Test Event Subscriptions

#### Test App Mention:

1. Invite your bot to a channel:
   ```
   /invite @YourBotName
   ```

2. Mention the bot:
   ```
   @YourBotName help
   ```

3. Check:
   - ngrok inspector shows POST to `/slack/events`
   - FastAPI logs show the event
   - Bot responds in the channel

#### Test Direct Message:

1. Find your bot in Slack's Apps section
2. Send a message: "Hello!"
3. Bot should respond

### 3. Test Slash Commands

Try each command:

```
/standup
/sprint-planning
/retrospective
/estimate Implement user authentication
```

Check:
- ngrok inspector shows POST to `/slack/commands`
- FastAPI processes the command
- Response appears in Slack

### 4. Debug with ngrok Inspector

1. Open http://127.0.0.1:4040
2. Click on any request to see:
   - Request headers
   - Request body
   - Response status
   - Response body
3. Use "Replay" to resend requests for testing

### 5. Check FastAPI Logs

Your terminal running FastAPI should show:
```
INFO:     127.0.0.1:xxxxx - "POST /slack/events HTTP/1.1" 200 OK
```

### 6. Verify Signature Verification

The webhook endpoint verifies Slack signatures. If verification fails:
- Check `SLACK_SIGNING_SECRET` is correct
- Check system time is accurate
- Check request timestamp is recent (< 5 minutes)

---

## Troubleshooting

### Slack can't verify my URL

**Symptoms:**
- "Your URL didn't respond with the challenge parameter"
- Request times out

**Solutions:**
1. ✅ Verify FastAPI is running: `curl http://localhost:8000/health`
2. ✅ Verify ngrok is running: Check for "Forwarding" line
3. ✅ Check ngrok inspector at http://127.0.0.1:4040
4. ✅ Ensure the URL is exactly: `https://your-subdomain.ngrok.io/slack/events`
5. ✅ Check firewall isn't blocking ngrok

### Events not reaching my app

**Symptoms:**
- No requests in ngrok inspector
- Bot doesn't respond

**Solutions:**
1. ✅ Verify Event Subscriptions are configured
2. ✅ Check bot has required OAuth scopes:
   - `app_mentions:read`
   - `chat:write`
   - `im:history`
3. ✅ Reinstall the app after making changes
4. ✅ Invite bot to the channel: `/invite @BotName`

### Invalid signature errors

**Symptoms:**
```
ERROR: Invalid signature
401 Unauthorized
```

**Solutions:**
1. ✅ Verify `SLACK_SIGNING_SECRET` in `.env`
2. ✅ Restart FastAPI after changing `.env`
3. ✅ Check system time is accurate
4. ✅ Verify request is recent (< 5 minutes)

### ngrok URL keeps changing

**Issue:** Free ngrok URLs change on restart

**Solutions:**
1. **Keep ngrok running** during development
2. **Paid ngrok plans** offer custom subdomains
3. **Use Socket Mode** for development (see [SLACK_SETUP.md](./SLACK_SETUP.md))
4. **Deploy to production** for stable URLs

### Commands return errors

**Symptoms:**
- Slash commands show "dispatch_failed"
- Modal doesn't open

**Solutions:**
1. ✅ Check command Request URL is correct
2. ✅ Verify endpoint returns 200 OK
3. ✅ Check FastAPI logs for errors
4. ✅ Use ngrok inspector to see actual request/response

### Bot responds to itself (infinite loop)

**Solution:**
The code already handles this:
```python
if event.get("bot_id"):
    return JSONResponse(content={"ok": True})
```

If you still see loops:
1. ✅ Check this code is not commented out
2. ✅ Verify bot events don't include bot messages

---

## Production Deployment

### Don't use ngrok in production!

Ngrok is for development only. For production:

### Option 1: Deploy to Cloud Platform

**Google Cloud Run:**
```bash
gcloud run deploy scrum-master-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Heroku:**
```bash
git push heroku main
```

**AWS Lambda / Azure Functions:**
Use FastAPI with Mangum adapter.

### Option 2: Your Own Server

1. Get a domain name
2. Set up HTTPS with Let's Encrypt
3. Deploy FastAPI with gunicorn/uvicorn
4. Configure reverse proxy (nginx)
5. Update Slack URLs to your domain

### Option 3: Continue with ngrok (Paid)

Ngrok paid plans offer:
- Custom subdomains (static URLs)
- Better uptime
- More features

---

## Best Practices

### Development Workflow

1. **Start environment:**
   ```bash
   ./scripts/start-dev.sh
   ```

2. **Make changes** to code

3. **Restart FastAPI** (keep ngrok running)

4. **Test** using Slack and ngrok inspector

5. **Debug** using logs and inspector

### Security

1. **Never commit `.env`**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Verify all webhook signatures**
   (Already implemented in the code)

3. **Use HTTPS only** (ngrok provides this)

4. **Rotate tokens periodically**

### Monitoring

1. **Watch ngrok inspector** during development
2. **Check FastAPI logs** for errors
3. **Monitor Slack API rate limits**
4. **Use structured logging** in production

---

## Additional Resources

### ngrok Documentation
- [ngrok Docs](https://ngrok.com/docs)
- [ngrok API](https://ngrok.com/docs/api)
- [ngrok Pricing](https://ngrok.com/pricing)

### Slack Documentation
- [Events API](https://api.slack.com/apis/connections/events-api)
- [Slash Commands](https://api.slack.com/interactivity/slash-commands)
- [Interactive Components](https://api.slack.com/interactivity)
- [Request Verification](https://api.slack.com/authentication/verifying-requests-from-slack)

### FastAPI Documentation
- [FastAPI Webhooks](https://fastapi.tiangolo.com/)
- [Deployment](https://fastapi.tiangolo.com/deployment/)

---

## Quick Reference

### Endpoints

| Endpoint | Purpose | Slack Configuration |
|----------|---------|---------------------|
| `/slack/events` | Event subscriptions | Event Subscriptions → Request URL |
| `/slack/interactions` | Interactive components | Interactivity & Shortcuts → Request URL |
| `/slack/commands` | Slash commands | Each command → Request URL |

### Required Slack Scopes

- `app_mentions:read`
- `chat:write`
- `commands`
- `im:history`
- `im:read`
- `im:write`
- `users:read`
- `channels:read`

### Environment Variables

- `SLACK_BOT_TOKEN` - Send messages
- `SLACK_SIGNING_SECRET` - Verify webhooks
- `ANTHROPIC_API_KEY` - AI responses

### Useful Commands

```bash
# Start FastAPI
python main.py

# Start ngrok
ngrok http 8000
./scripts/start-ngrok.sh

# Start both
./scripts/start-dev.sh

# View ngrok inspector
open http://127.0.0.1:4040

# Test health endpoint
curl http://localhost:8000/health

# Check logs
tail -f logs/app.log  # if you set up file logging
```

---

**Last Updated:** 2025-01-15
**Version:** 1.0
**Author:** Scrum Master AI Agent Team
