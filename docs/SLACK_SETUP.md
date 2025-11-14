# Slack App Setup Guide - Scrum Master AI Agent

This comprehensive guide will walk you through creating and configuring a Slack app for the Scrum Master AI Agent from scratch.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Create a Slack App](#step-1-create-a-slack-app)
- [Step 2: Configure OAuth & Permissions](#step-2-configure-oauth--permissions)
- [Step 3: Enable Event Subscriptions](#step-3-enable-event-subscriptions)
- [Step 4: Configure Interactivity](#step-4-configure-interactivity)
- [Step 5: Create Slash Commands](#step-5-create-slash-commands)
- [Step 6: Enable Socket Mode](#step-6-enable-socket-mode)
- [Step 7: Install App to Workspace](#step-7-install-app-to-workspace)
- [Step 8: Configure Environment Variables](#step-8-configure-environment-variables)
- [Step 9: Test the Installation](#step-9-test-the-installation)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- **Slack Workspace Admin Access**: You need admin privileges to create and install apps
- **Anthropic API Key**: Get one from [console.anthropic.com](https://console.anthropic.com)
- **Python 3.9+**: Installed on your system
- **Git**: For cloning the repository

---

## Step 1: Create a Slack App

### 1.1 Navigate to Slack API Dashboard

1. Open your web browser and go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click the **"Create New App"** button

### 1.2 Choose Creation Method

You have two options:
- **From scratch** (Recommended for this guide)
- From an app manifest (Advanced)

**Select "From scratch"**

### 1.3 Configure Basic Information

1. **App Name**: Enter a descriptive name
   - Example: `Scrum Master` or `Agile Assistant`

2. **Workspace**: Select the workspace where you want to develop the app
   - Choose your development/testing workspace first

3. Click **"Create App"**

### 1.4 Customize App Display

1. In the left sidebar, go to **"Basic Information"**
2. Scroll to **"Display Information"**
3. Fill in the following (optional but recommended):
   - **Short Description**: "AI-powered Scrum Master to help manage agile teams"
   - **Long Description**: Add a detailed description of features
   - **App Icon**: Upload a 512x512 px icon (optional)
   - **Background Color**: Choose a color that matches your icon

4. Click **"Save Changes"**

---

## Step 2: Configure OAuth & Permissions

OAuth scopes define what your bot can do in Slack.

### 2.1 Navigate to OAuth & Permissions

1. In the left sidebar, click **"OAuth & Permissions"**
2. Scroll down to **"Scopes"** section
3. Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"**

### 2.2 Add Required Bot Token Scopes

Add the following scopes one by one:

| Scope | Purpose |
|-------|---------|
| `app_mentions:read` | Detect when the bot is mentioned in channels |
| `chat:write` | Send messages as the bot |
| `chat:write.public` | Send messages to channels the bot isn't in |
| `commands` | Enable slash commands |
| `im:history` | Read message history in direct messages |
| `im:read` | View basic information about direct messages |
| `im:write` | Start direct message conversations |
| `users:read` | View users in the workspace |
| `channels:read` | View basic information about public channels |
| `channels:history` | View messages in public channels (if needed) |
| `groups:read` | View basic information about private channels |

### 2.3 Optional Scopes (for extended features)

If you plan to add these features later:

| Scope | Purpose |
|-------|---------|
| `channels:join` | Join public channels automatically |
| `files:write` | Upload files (for reports, charts) |
| `reactions:write` | Add emoji reactions to messages |
| `reminders:write` | Create reminders for team members |

**Note**: Don't install the app to your workspace yet. We need to configure more settings first.

---

## Step 3: Enable Event Subscriptions

Event subscriptions allow your bot to receive events from Slack in real-time.

### 3.1 Navigate to Event Subscriptions

1. In the left sidebar, click **"Event Subscriptions"**
2. Toggle **"Enable Events"** to **ON**

### 3.2 Configure Request URL (Two Options)

#### Option A: Using Socket Mode (Recommended for Development)

**Skip the Request URL for now** if you're using Socket Mode (we'll enable this in Step 6).

Socket Mode doesn't require a public URL and is perfect for:
- Local development
- Testing
- Development environments

#### Option B: Using HTTP Mode (For Production)

If deploying to production, you need a public HTTPS URL:

1. **For local development with HTTP mode**:
   - Install ngrok: `npm install -g ngrok`
   - Run: `ngrok http 3000`
   - Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
   - Add `/slack/events` to the end: `https://abc123.ngrok.io/slack/events`

2. **For production deployment**:
   - Use your production server URL
   - Example: `https://your-domain.com/slack/events`

3. Enter the URL in **"Request URL"** field
4. Wait for verification (the app must be running)

### 3.3 Subscribe to Bot Events

Scroll down to **"Subscribe to bot events"** and add:

| Event Name | Description |
|------------|-------------|
| `app_mention` | When someone mentions @YourBot |
| `message.im` | Direct messages sent to the bot |

**Optional events** (add if needed):
| Event Name | Description |
|------------|-------------|
| `message.channels` | Messages in public channels (bot must be in channel) |
| `message.groups` | Messages in private channels (bot must be in channel) |

### 3.4 Save Changes

1. Click **"Save Changes"** at the bottom
2. You'll see a yellow banner saying you need to reinstall the app (do this later)

---

## Step 4: Configure Interactivity

Interactivity enables modals, buttons, and select menus.

### 4.1 Navigate to Interactivity & Shortcuts

1. In the left sidebar, click **"Interactivity & Shortcuts"**
2. Toggle **"Interactivity"** to **ON**

### 4.2 Set Request URL

#### For Socket Mode (Development):
- Leave blank or enter a placeholder
- Socket Mode will handle this

#### For HTTP Mode (Production):
- Enter: `https://your-domain.com/slack/interactions`
- Or with ngrok: `https://abc123.ngrok.io/slack/interactions`

### 4.3 Save Changes

Click **"Save Changes"**

---

## Step 5: Create Slash Commands

Slash commands provide quick access to bot features.

### 5.1 Navigate to Slash Commands

1. In the left sidebar, click **"Slash Commands"**
2. Click **"Create New Command"**

### 5.2 Create Each Command

Add the following commands one by one:

#### Command 1: Daily Standup

- **Command**: `/standup`
- **Request URL**:
  - Socket Mode: Leave blank or use placeholder
  - HTTP Mode: `https://your-domain.com/slack/commands`
- **Short Description**: `Submit your daily standup update`
- **Usage Hint**: (leave blank)
- Click **"Save"**

#### Command 2: Sprint Planning

- **Command**: `/sprint-planning`
- **Request URL**: Same as above
- **Short Description**: `Get help with sprint planning`
- **Usage Hint**: `[topic]`
- Click **"Save"**

#### Command 3: Retrospective

- **Command**: `/retrospective`
- **Request URL**: Same as above
- **Short Description**: `Start a retrospective session`
- **Usage Hint**: (leave blank)
- Click **"Save"**

#### Command 4: Story Estimation

- **Command**: `/estimate`
- **Request URL**: Same as above
- **Short Description**: `Estimate story points for a user story`
- **Usage Hint**: `<user story description>`
- Click **"Save"**

### 5.3 Optional Additional Commands

Consider adding:

- `/sprint-status` - Check current sprint progress
- `/velocity` - View team velocity
- `/backlog` - Manage product backlog
- `/impediment` - Report a blocker or impediment

---

## Step 6: Enable Socket Mode

Socket Mode is the easiest way to develop and run your bot without a public URL.

### 6.1 Navigate to Socket Mode

1. In the left sidebar, click **"Socket Mode"**
2. Toggle **"Enable Socket Mode"** to **ON**

### 6.2 Generate App-Level Token

1. A popup will appear asking you to create an app-level token
2. **Token Name**: Enter a descriptive name (e.g., `scrum-master-socket-token`)
3. **Scopes**: Select `connections:write`
4. Click **"Generate"**

### 6.3 Save the Token

⚠️ **IMPORTANT**: Copy the token immediately!

- It starts with `xapp-`
- Format: `xapp-1-A123456789-1234567890123-abc...`
- **Save this token securely** - you'll need it for your `.env` file
- You won't be able to see it again

### 6.4 Click Done

After copying the token, click **"Done"**

---

## Step 7: Install App to Workspace

Now that everything is configured, install the app.

### 7.1 Navigate to Install App

1. In the left sidebar, click **"Install App"**
2. Review the permissions the app will request
3. Click **"Install to Workspace"**

### 7.2 Authorize the App

1. A Slack authorization page will open
2. Review the permissions:
   - What channels it can access
   - What data it can read/write
3. Select a channel where the bot should post (optional)
4. Click **"Allow"**

### 7.3 Copy Bot Token

After installation, you'll see:

- **Bot User OAuth Token**: Starts with `xoxb-`
  - Example: `xoxb-1234567890123-1234567890123-abc...`
  - **Copy and save this token** - you'll need it for your `.env` file

### 7.4 Find Your Signing Secret

1. Go back to **"Basic Information"** in the left sidebar
2. Scroll to **"App Credentials"**
3. Find **"Signing Secret"**
4. Click **"Show"** and copy the value
5. **Save this secret** - you'll need it for your `.env` file

---

## Step 8: Configure Environment Variables

### 8.1 Clone the Repository

```bash
git clone <repository-url>
cd ai-agent
```

### 8.2 Create Environment File

```bash
cp .env.example .env
```

### 8.3 Edit the `.env` File

Open `.env` in your text editor and fill in the values:

```bash
# Slack Configuration
# Bot User OAuth Token (from Step 7.3)
SLACK_BOT_TOKEN=xoxb-your-actual-bot-token-here

# App-Level Token for Socket Mode (from Step 6.3)
SLACK_APP_TOKEN=xapp-your-actual-app-token-here

# Signing Secret (from Step 7.4)
SLACK_SIGNING_SECRET=your-actual-signing-secret-here

# AI Configuration
# Get your API key from console.anthropic.com
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
MODEL_NAME=claude-sonnet-4-5-20250929

# Database Configuration
DATABASE_URL=sqlite:///scrum_master.db

# Optional: Feature Flags
ENABLE_DAILY_STANDUP=true
ENABLE_SPRINT_PLANNING=true
ENABLE_RETROSPECTIVES=true
```

### 8.4 Verify Your Tokens

Double-check that:
- ✅ `SLACK_BOT_TOKEN` starts with `xoxb-`
- ✅ `SLACK_APP_TOKEN` starts with `xapp-`
- ✅ `SLACK_SIGNING_SECRET` is a 32-character hex string
- ✅ `ANTHROPIC_API_KEY` starts with `sk-ant-`
- ✅ No extra spaces or quotes around values

---

## Step 9: Test the Installation

### 9.1 Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 9.2 Run the Bot

```bash
python main.py
```

### 9.3 Verify Startup

You should see output like:

```
INFO - Configuration loaded successfully
INFO - Using model: claude-sonnet-4-5-20250929
INFO - Database initialized successfully
INFO - Scrum Master AI Agent is starting...
INFO - Socket Mode connection established
INFO - ⚡️ Bolt app is running!
```

### 9.4 Test in Slack

#### Test 1: Direct Message

1. Open Slack
2. Find your bot in the Apps section (left sidebar)
3. Send a message: `Hello!`
4. The bot should respond

#### Test 2: Slash Command

1. In any channel or DM, type: `/standup`
2. A modal should open with form fields
3. Fill out the form and submit
4. You should get a confirmation

#### Test 3: Mention in Channel

1. Invite the bot to a channel: `/invite @ScrumMaster`
2. Mention the bot: `@ScrumMaster help`
3. The bot should respond with help information

### 9.5 Check Logs

If something doesn't work:
1. Check the terminal where `main.py` is running
2. Look for error messages
3. Refer to the Troubleshooting section below

---

## Troubleshooting

### Bot doesn't respond to messages

**Check 1: Verify tokens**
```bash
# Check if tokens are set (don't print actual values)
python -c "
from src.config import Config
config = Config()
print(f'Bot Token set: {bool(config.slack_bot_token)}')
print(f'App Token set: {bool(config.slack_app_token)}')
print(f'Signing Secret set: {bool(config.slack_signing_secret)}')
"
```

**Check 2: Verify Socket Mode is enabled**
- Go to [api.slack.com/apps](https://api.slack.com/apps)
- Select your app
- Check that Socket Mode is ON

**Check 3: Verify OAuth Scopes**
- Go to OAuth & Permissions
- Ensure all required scopes are added
- If you added scopes after installation, reinstall the app

**Check 4: Check event subscriptions**
- Go to Event Subscriptions
- Verify `app_mention` and `message.im` are subscribed

### Slash commands don't work

**Check 1: Verify commands are created**
- Go to Slash Commands in your app settings
- Ensure all commands are listed

**Check 2: Check command permissions**
- The bot needs `commands` scope in OAuth & Permissions

**Check 3: Reinstall the app**
- After making changes, you often need to reinstall
- Go to Install App → Reinstall to Workspace

### "Invalid token" errors

**Check 1: Verify token format**
- Bot Token must start with `xoxb-`
- App Token must start with `xapp-`
- No spaces or quotes in `.env` file

**Check 2: Regenerate tokens if needed**
- Go to OAuth & Permissions
- Click "Reinstall to Workspace"
- Copy the new bot token

### Socket Mode connection fails

**Check 1: App-level token scope**
- Go to Basic Information → App-Level Tokens
- Ensure token has `connections:write` scope

**Check 2: Network/firewall issues**
- Socket Mode requires outbound WebSocket connections
- Check if your firewall blocks WebSocket traffic
- Try disabling VPN temporarily

### Database errors

**Check 1: File permissions**
```bash
# Check if database file is writable
ls -la scrum_master.db
```

**Check 2: Reinitialize database**
```bash
# Backup existing database
cp scrum_master.db scrum_master.db.backup

# Remove and recreate
rm scrum_master.db
python main.py  # Will create fresh database
```

### Anthropic API errors

**Check 1: Verify API key**
```bash
# Test API key (requires anthropic package)
python -c "
from anthropic import Anthropic
client = Anthropic()  # Uses ANTHROPIC_API_KEY from environment
print('API key is valid!')
"
```

**Check 2: Check rate limits**
- Free tier has limited requests per day
- Check usage at [console.anthropic.com](https://console.anthropic.com)

**Check 3: Verify model name**
- Ensure `MODEL_NAME` in `.env` is correct
- Current recommended model: `claude-sonnet-4-5-20250929`

### App mentions don't work in channels

**Check 1: Invite bot to channel**
```
/invite @YourBotName
```

**Check 2: Check event subscriptions**
- Verify `app_mention` is subscribed
- For channel messages: subscribe to `message.channels`

**Check 3: Verify scopes**
- Need `app_mentions:read` scope
- Need `channels:history` for reading channel messages

### Modal/Interactive components don't work

**Check 1: Verify Interactivity is enabled**
- Go to Interactivity & Shortcuts
- Ensure toggle is ON

**Check 2: For HTTP mode**
- Verify Request URL is correct
- Ensure endpoint is responding with 200 OK

---

## Advanced Configuration

### Production Deployment

When deploying to production:

1. **Use HTTP Mode instead of Socket Mode**
   - Socket Mode is for development only
   - HTTP mode is more reliable for production

2. **Set up a proper web server**
   - Use gunicorn or uvicorn
   - Configure HTTPS with SSL certificate
   - Set up reverse proxy (nginx)

3. **Environment variables**
   - Don't commit `.env` file
   - Use proper secrets management
   - Consider using environment-specific configs

4. **Monitoring**
   - Set up logging to files or log service
   - Monitor API rate limits
   - Track error rates

### Security Best Practices

1. **Token Security**
   ```bash
   # Never commit tokens
   echo ".env" >> .gitignore

   # Use restrictive permissions
   chmod 600 .env
   ```

2. **Signing Secret Verification**
   - Always verify Slack requests using signing secret
   - This is handled automatically by the Slack SDK

3. **Scope Minimization**
   - Only request scopes you actually need
   - Review and audit scopes regularly

4. **Regular Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Rotate tokens periodically

### Multi-Workspace Installation

To make your app installable in multiple workspaces:

1. **Enable Distribution**
   - Go to Manage Distribution
   - Fill in required information
   - Submit for App Directory (optional)

2. **OAuth Redirect URLs**
   - Set up proper OAuth flow
   - Handle token storage per workspace

3. **Database per Workspace**
   - Store data separately per workspace
   - Use workspace ID as key

---

## Additional Resources

### Slack Documentation
- [Slack API Documentation](https://api.slack.com/)
- [Bolt for Python](https://slack.dev/bolt-python/)
- [Socket Mode Guide](https://api.slack.com/apis/connections/socket)

### Anthropic Documentation
- [Claude API Documentation](https://docs.anthropic.com/)
- [API Reference](https://docs.anthropic.com/claude/reference/)

### Support
- **Slack API Support**: [api.slack.com/community](https://api.slack.com/community)
- **Project Issues**: [GitHub Issues](https://github.com/your-repo/issues)

---

## Appendix: Quick Reference

### Required Slack Tokens Checklist

- [ ] Bot User OAuth Token (`xoxb-...`)
- [ ] App-Level Token (`xapp-...`)
- [ ] Signing Secret (32-character hex)

### Required OAuth Scopes Checklist

- [ ] `app_mentions:read`
- [ ] `chat:write`
- [ ] `commands`
- [ ] `im:history`
- [ ] `im:read`
- [ ] `im:write`
- [ ] `users:read`
- [ ] `channels:read`
- [ ] `groups:read`

### Required Event Subscriptions Checklist

- [ ] `app_mention`
- [ ] `message.im`

### Required Slash Commands Checklist

- [ ] `/standup`
- [ ] `/sprint-planning`
- [ ] `/retrospective`
- [ ] `/estimate`

### Configuration Checklist

- [ ] Socket Mode enabled
- [ ] Interactivity enabled
- [ ] App installed to workspace
- [ ] `.env` file configured with all tokens
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] Bot successfully responds to test message

---

**Last Updated**: 2025-01-14
**Version**: 1.0
**Maintained by**: Scrum Master AI Agent Team
