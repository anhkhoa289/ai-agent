# Jira API Documentation

## Overview

The Jira REST API allows you to interact with Jira programmatically to manage projects, issues, sprints, and other agile resources. This documentation covers the most relevant endpoints for a Scrum Master AI Agent.

## Authentication

### API Token Authentication

1. Generate an API token from your Atlassian account:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Copy and securely store the token

2. Use Basic Authentication with email and API token:

```python
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://your-domain.atlassian.net/rest/api/3/issue/{issueKey}"

auth = HTTPBasicAuth("your-email@example.com", "your-api-token")

headers = {
   "Accept": "application/json"
}

response = requests.get(url, headers=headers, auth=auth)
```

### OAuth 2.0 Authentication

For more secure, user-delegated access:

```python
from requests_oauthlib import OAuth2Session

client_id = 'your-client-id'
client_secret = 'your-client-secret'
authorization_base_url = 'https://auth.atlassian.com/authorize'
token_url = 'https://auth.atlassian.com/oauth/token'

oauth = OAuth2Session(client_id, redirect_uri='your-redirect-uri')
```

## Base URL Structure

```
https://your-domain.atlassian.net/rest/api/3/
```

For Jira Cloud, use API version 3. For Jira Server/Data Center, use version 2.

## Core Endpoints for Scrum Master Agent

### 1. Projects

#### Get All Projects

```python
GET /rest/api/3/project

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/api/3/project",
    headers=headers,
    auth=auth
)
projects = response.json()
```

#### Get Project Details

```python
GET /rest/api/3/project/{projectIdOrKey}

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/api/3/project/PROJ",
    headers=headers,
    auth=auth
)
```

### 2. Issues

#### Create Issue

```python
POST /rest/api/3/issue

# Example
issue_data = {
    "fields": {
        "project": {
            "key": "PROJ"
        },
        "summary": "Implement user authentication",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Add OAuth2 authentication to the API"
                        }
                    ]
                }
            ]
        },
        "issuetype": {
            "name": "Story"
        },
        "priority": {
            "name": "High"
        },
        "customfield_10016": 8  # Story points
    }
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/api/3/issue",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(issue_data)
)
```

#### Get Issue

```python
GET /rest/api/3/issue/{issueIdOrKey}

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123",
    headers=headers,
    auth=auth
)
issue = response.json()
```

#### Update Issue

```python
PUT /rest/api/3/issue/{issueIdOrKey}

# Example: Update story points
update_data = {
    "fields": {
        "customfield_10016": 5  # Story points
    }
}

response = requests.put(
    "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(update_data)
)
```

#### Search Issues (JQL)

```python
POST /rest/api/3/search

# Example: Find all stories in current sprint
jql_query = {
    "jql": "project = PROJ AND sprint in openSprints() AND type = Story",
    "maxResults": 100,
    "fields": ["summary", "status", "assignee", "customfield_10016"]
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/api/3/search",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(jql_query)
)
issues = response.json()['issues']
```

### 3. Sprints (Agile API)

#### Get All Sprints for Board

```python
GET /rest/agile/1.0/board/{boardId}/sprint

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/agile/1.0/board/123/sprint",
    headers=headers,
    auth=auth
)
sprints = response.json()['values']
```

#### Get Sprint Details

```python
GET /rest/agile/1.0/sprint/{sprintId}

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/agile/1.0/sprint/456",
    headers=headers,
    auth=auth
)
sprint = response.json()
```

#### Create Sprint

```python
POST /rest/agile/1.0/sprint

# Example
sprint_data = {
    "name": "Sprint 15",
    "startDate": "2024-01-15T09:00:00.000Z",
    "endDate": "2024-01-29T17:00:00.000Z",
    "originBoardId": 123,
    "goal": "Complete user authentication and API endpoints"
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/agile/1.0/sprint",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(sprint_data)
)
```

#### Update Sprint

```python
POST /rest/agile/1.0/sprint/{sprintId}

# Example: Start a sprint
update_data = {
    "state": "active"
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/agile/1.0/sprint/456",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(update_data)
)
```

#### Get Sprint Issues

```python
GET /rest/agile/1.0/sprint/{sprintId}/issue

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/agile/1.0/sprint/456/issue",
    headers=headers,
    auth=auth
)
issues = response.json()['issues']
```

#### Move Issues to Sprint

```python
POST /rest/agile/1.0/sprint/{sprintId}/issue

# Example
issue_data = {
    "issues": ["PROJ-123", "PROJ-124", "PROJ-125"]
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/agile/1.0/sprint/456/issue",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(issue_data)
)
```

### 4. Boards

#### Get All Boards

```python
GET /rest/agile/1.0/board

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/agile/1.0/board",
    headers=headers,
    auth=auth
)
boards = response.json()['values']
```

#### Get Board Configuration

```python
GET /rest/agile/1.0/board/{boardId}/configuration

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/agile/1.0/board/123/configuration",
    headers=headers,
    auth=auth
)
```

### 5. Backlog

#### Get Backlog Issues

```python
GET /rest/agile/1.0/board/{boardId}/backlog

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/agile/1.0/board/123/backlog",
    headers=headers,
    auth=auth
)
backlog_issues = response.json()['issues']
```

#### Move Issues to Backlog

```python
POST /rest/agile/1.0/backlog/issue

# Example
issue_data = {
    "issues": ["PROJ-126", "PROJ-127"]
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/agile/1.0/backlog/issue",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(issue_data)
)
```

### 6. Comments

#### Add Comment to Issue

```python
POST /rest/api/3/issue/{issueIdOrKey}/comment

# Example
comment_data = {
    "body": {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "This issue is blocked by PROJ-100"
                    }
                ]
            }
        ]
    }
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/comment",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(comment_data)
)
```

#### Get Comments

```python
GET /rest/api/3/issue/{issueIdOrKey}/comment

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/comment",
    headers=headers,
    auth=auth
)
comments = response.json()['comments']
```

### 7. Transitions

#### Get Available Transitions

```python
GET /rest/api/3/issue/{issueIdOrKey}/transitions

# Example
response = requests.get(
    "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/transitions",
    headers=headers,
    auth=auth
)
transitions = response.json()['transitions']
```

#### Transition Issue

```python
POST /rest/api/3/issue/{issueIdOrKey}/transitions

# Example: Move to "In Progress"
transition_data = {
    "transition": {
        "id": "21"  # Transition ID from get transitions
    }
}

response = requests.post(
    "https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123/transitions",
    headers={"Content-Type": "application/json"},
    auth=auth,
    data=json.dumps(transition_data)
)
```

## JQL (Jira Query Language)

### Common Queries for Scrum Master

```python
# Get current sprint issues
"sprint in openSprints() AND project = PROJ"

# Get completed issues in sprint
"sprint in openSprints() AND status = Done AND project = PROJ"

# Get blocked issues
"status = Blocked AND project = PROJ"

# Get unassigned high priority issues
"assignee is EMPTY AND priority = High AND project = PROJ"

# Get overdue issues
"due < now() AND status != Done AND project = PROJ"

# Get issues updated today
"updated >= startOfDay() AND project = PROJ"

# Get issues by story points
"'Story Points' > 5 AND project = PROJ"

# Get bugs in current sprint
"type = Bug AND sprint in openSprints() AND project = PROJ"
```

## Python Client Library

### Installation

```bash
pip install jira
```

### Basic Usage

```python
from jira import JIRA

# Connect to Jira
jira = JIRA(
    server='https://your-domain.atlassian.net',
    basic_auth=('your-email@example.com', 'your-api-token')
)

# Get current user
user = jira.current_user()

# Search issues
issues = jira.search_issues('project=PROJ AND sprint in openSprints()')

# Create issue
new_issue = jira.create_issue(
    project='PROJ',
    summary='New feature request',
    description='Detailed description',
    issuetype={'name': 'Story'}
)

# Update issue
issue = jira.issue('PROJ-123')
issue.update(fields={'customfield_10016': 5})  # Update story points

# Add comment
jira.add_comment(issue, 'This is a comment')

# Transition issue
jira.transition_issue(issue, '21')  # Transition to "In Progress"

# Get sprints
board_id = 123
sprints = jira.sprints(board_id)

# Get active sprint
active_sprints = [s for s in sprints if s.state == 'active']
```

## Rate Limiting

Jira Cloud has rate limits:
- Standard: 10 requests per second per user
- Premium: Higher limits available

Handle rate limiting:

```python
import time
from requests.exceptions import HTTPError

def jira_request_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                retry_after = int(e.response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
            else:
                raise
    raise Exception("Max retries exceeded")
```

## Best Practices

### 1. Pagination

Always handle pagination for large result sets:

```python
start_at = 0
max_results = 50
all_issues = []

while True:
    response = jira.search_issues(
        'project=PROJ',
        startAt=start_at,
        maxResults=max_results
    )
    all_issues.extend(response)
    if len(response) < max_results:
        break
    start_at += max_results
```

### 2. Field Selection

Request only needed fields to improve performance:

```python
issues = jira.search_issues(
    'project=PROJ',
    fields='summary,status,assignee,customfield_10016'
)
```

### 3. Error Handling

```python
try:
    issue = jira.issue('PROJ-123')
except JIRAError as e:
    if e.status_code == 404:
        print("Issue not found")
    elif e.status_code == 401:
        print("Authentication failed")
    else:
        print(f"Error: {e.text}")
```

### 4. Batch Operations

Use bulk operations when possible:

```python
# Bulk create issues
issues_to_create = [
    {"fields": {"project": {"key": "PROJ"}, "summary": f"Task {i}", "issuetype": {"name": "Task"}}}
    for i in range(10)
]

for issue_data in issues_to_create:
    jira.create_issue(fields=issue_data['fields'])
```

## Useful Custom Fields

Common custom field IDs (may vary by instance):
- `customfield_10016`: Story Points
- `customfield_10014`: Sprint
- `customfield_10015`: Epic Link
- `customfield_10018`: Epic Name

Find custom field IDs:

```python
# Get all fields
fields = jira.fields()
for field in fields:
    print(f"{field['name']}: {field['id']}")
```

## Webhooks

Set up webhooks to receive real-time updates:

```python
# Webhook payload example
{
    "timestamp": 1635789012345,
    "webhookEvent": "jira:issue_updated",
    "issue": {
        "key": "PROJ-123",
        "fields": {
            "summary": "Updated summary",
            "status": {"name": "In Progress"}
        }
    },
    "changelog": {
        "items": [
            {
                "field": "status",
                "fromString": "To Do",
                "toString": "In Progress"
            }
        ]
    }
}
```

## Resources

- **Official API Documentation**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **Agile API Documentation**: https://developer.atlassian.com/cloud/jira/software/rest/
- **Python JIRA Library**: https://jira.readthedocs.io/
- **API Reference**: https://docs.atlassian.com/software/jira/docs/api/REST/

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
- Verify API token is correct
- Check email address is correct
- Ensure user has necessary permissions

**Issue: 404 Not Found**
- Verify the issue key or ID exists
- Check project permissions
- Ensure correct API version

**Issue: 400 Bad Request**
- Validate JSON payload structure
- Check required fields are provided
- Verify field IDs are correct for your instance

**Issue: Custom field not updating**
- Find correct custom field ID using fields endpoint
- Ensure field is editable for the issue type
- Check field configuration in Jira admin
