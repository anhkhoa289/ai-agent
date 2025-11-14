# Trello API Documentation

## Overview

The Trello API allows you to programmatically interact with Trello boards, lists, cards, and other resources. This documentation covers the essential endpoints for building a Scrum Master AI Agent integration with Trello.

## Authentication

### Getting API Credentials

1. **API Key**: Get your API key from https://trello.com/app-key

2. **Token**: Generate a token by visiting:
   ```
   https://trello.com/1/authorize?expiration=never&scope=read,write&response_type=token&name=YourAppName&key=YOUR_API_KEY
   ```

### Making Authenticated Requests

```python
import requests

API_KEY = 'your-api-key'
TOKEN = 'your-token'

url = "https://api.trello.com/1/boards/{boardId}"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
```

## Base URL

```
https://api.trello.com/1/
```

## Core Endpoints for Scrum Master Agent

### 1. Boards

#### Get Board

```python
GET /1/boards/{id}

# Example
url = "https://api.trello.com/1/boards/abc123"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
board = response.json()
```

#### Get User's Boards

```python
GET /1/members/me/boards

# Example
url = "https://api.trello.com/1/members/me/boards"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
boards = response.json()
```

#### Create Board

```python
POST /1/boards

# Example
url = "https://api.trello.com/1/boards/"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'name': 'Sprint 15 Board',
    'defaultLists': 'false'  # Don't create default lists
}

response = requests.post(url, params=query)
new_board = response.json()
```

#### Update Board

```python
PUT /1/boards/{id}

# Example
url = "https://api.trello.com/1/boards/abc123"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'name': 'Updated Board Name',
    'desc': 'Sprint 15: Complete authentication feature'
}

response = requests.put(url, params=query)
```

#### Get Board Lists

```python
GET /1/boards/{id}/lists

# Example
url = "https://api.trello.com/1/boards/abc123/lists"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
lists = response.json()
```

#### Get Board Cards

```python
GET /1/boards/{id}/cards

# Example
url = "https://api.trello.com/1/boards/abc123/cards"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
cards = response.json()
```

### 2. Lists

#### Get List

```python
GET /1/lists/{id}

# Example
url = "https://api.trello.com/1/lists/def456"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
list_data = response.json()
```

#### Create List

```python
POST /1/lists

# Example: Create sprint lists
url = "https://api.trello.com/1/lists"

lists_to_create = ['Backlog', 'To Do', 'In Progress', 'Review', 'Done']

for list_name in lists_to_create:
    query = {
        'key': API_KEY,
        'token': TOKEN,
        'name': list_name,
        'idBoard': 'abc123'
    }
    response = requests.post(url, params=query)
```

#### Update List

```python
PUT /1/lists/{id}

# Example
url = "https://api.trello.com/1/lists/def456"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'name': 'Current Sprint',
    'closed': 'false'
}

response = requests.put(url, params=query)
```

#### Archive/Unarchive List

```python
PUT /1/lists/{id}/closed

# Example: Archive list
url = "https://api.trello.com/1/lists/def456/closed"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'value': 'true'
}

response = requests.put(url, params=query)
```

#### Get Cards in List

```python
GET /1/lists/{id}/cards

# Example
url = "https://api.trello.com/1/lists/def456/cards"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
cards = response.json()
```

### 3. Cards

#### Get Card

```python
GET /1/cards/{id}

# Example
url = "https://api.trello.com/1/cards/ghi789"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
card = response.json()
```

#### Create Card

```python
POST /1/cards

# Example: Create user story
url = "https://api.trello.com/1/cards"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'idList': 'def456',
    'name': 'As a user, I want to login with OAuth',
    'desc': 'Implement OAuth2 authentication flow',
    'pos': 'bottom'  # Position: top, bottom, or a positive number
}

response = requests.post(url, params=query)
new_card = response.json()
```

#### Update Card

```python
PUT /1/cards/{id}

# Example
url = "https://api.trello.com/1/cards/ghi789"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'name': 'Updated card name',
    'desc': 'Updated description'
}

response = requests.put(url, params=query)
```

#### Move Card to Another List

```python
PUT /1/cards/{id}

# Example: Move to "In Progress"
url = "https://api.trello.com/1/cards/ghi789"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'idList': 'new-list-id'
}

response = requests.put(url, params=query)
```

#### Archive/Delete Card

```python
# Archive (soft delete)
PUT /1/cards/{id}

url = "https://api.trello.com/1/cards/ghi789"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'closed': 'true'
}

response = requests.put(url, params=query)

# Permanently delete
DELETE /1/cards/{id}

url = "https://api.trello.com/1/cards/ghi789"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.delete(url, params=query)
```

### 4. Checklists

#### Add Checklist to Card

```python
POST /1/cards/{id}/checklists

# Example: Add acceptance criteria
url = "https://api.trello.com/1/cards/ghi789/checklists"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'name': 'Acceptance Criteria'
}

response = requests.post(url, params=query)
checklist = response.json()
```

#### Add Checklist Item

```python
POST /1/checklists/{id}/checkItems

# Example
url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'name': 'User can login with Google',
    'pos': 'bottom'
}

response = requests.post(url, params=query)
```

#### Update Checklist Item

```python
PUT /1/cards/{cardId}/checkItem/{checkItemId}

# Example: Mark item as complete
url = f"https://api.trello.com/1/cards/ghi789/checkItem/item123"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'state': 'complete'  # or 'incomplete'
}

response = requests.put(url, params=query)
```

#### Get Card Checklists

```python
GET /1/cards/{id}/checklists

# Example
url = "https://api.trello.com/1/cards/ghi789/checklists"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
checklists = response.json()
```

### 5. Labels

#### Create Label

```python
POST /1/labels

# Example
url = "https://api.trello.com/1/labels"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'name': 'High Priority',
    'color': 'red',
    'idBoard': 'abc123'
}

response = requests.post(url, params=query)
```

#### Add Label to Card

```python
POST /1/cards/{id}/idLabels

# Example
url = "https://api.trello.com/1/cards/ghi789/idLabels"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'value': 'label-id'
}

response = requests.post(url, params=query)
```

#### Get Board Labels

```python
GET /1/boards/{id}/labels

# Example
url = "https://api.trello.com/1/boards/abc123/labels"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
labels = response.json()
```

### 6. Members

#### Add Member to Card

```python
POST /1/cards/{id}/idMembers

# Example: Assign card
url = "https://api.trello.com/1/cards/ghi789/idMembers"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'value': 'member-id'
}

response = requests.post(url, params=query)
```

#### Get Board Members

```python
GET /1/boards/{id}/members

# Example
url = "https://api.trello.com/1/boards/abc123/members"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
members = response.json()
```

#### Get Current User

```python
GET /1/members/me

# Example
url = "https://api.trello.com/1/members/me"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
user = response.json()
```

### 7. Comments (Actions)

#### Add Comment to Card

```python
POST /1/cards/{id}/actions/comments

# Example
url = "https://api.trello.com/1/cards/ghi789/actions/comments"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'text': 'This card is blocked by authentication issues'
}

response = requests.post(url, params=query)
```

#### Get Card Comments

```python
GET /1/cards/{id}/actions

# Example: Get comments only
url = "https://api.trello.com/1/cards/ghi789/actions"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'filter': 'commentCard'
}

response = requests.get(url, params=query)
comments = response.json()
```

#### Update Comment

```python
PUT /1/actions/{id}

# Example
url = "https://api.trello.com/1/actions/action123"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'text': 'Updated comment text'
}

response = requests.put(url, params=query)
```

#### Delete Comment

```python
DELETE /1/actions/{id}

# Example
url = "https://api.trello.com/1/actions/action123"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.delete(url, params=query)
```

### 8. Custom Fields

#### Get Custom Fields on Board

```python
GET /1/boards/{id}/customFields

# Example
url = "https://api.trello.com/1/boards/abc123/customFields"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
custom_fields = response.json()
```

#### Set Custom Field Value on Card

```python
PUT /1/cards/{cardId}/customField/{customFieldId}/item

# Example: Set story points
url = "https://api.trello.com/1/cards/ghi789/customField/field123/item"

headers = {
    'Content-Type': 'application/json'
}

query = {
    'key': API_KEY,
    'token': TOKEN
}

data = {
    'value': {
        'number': '5'  # 5 story points
    }
}

response = requests.put(url, params=query, headers=headers, json=data)
```

### 9. Due Dates

#### Set Due Date

```python
PUT /1/cards/{id}

# Example
url = "https://api.trello.com/1/cards/ghi789"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'due': '2024-12-31T23:59:59.000Z',
    'dueComplete': 'false'
}

response = requests.put(url, params=query)
```

#### Mark Due Date Complete

```python
PUT /1/cards/{id}

# Example
url = "https://api.trello.com/1/cards/ghi789"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'dueComplete': 'true'
}

response = requests.put(url, params=query)
```

### 10. Attachments

#### Add Attachment to Card

```python
POST /1/cards/{id}/attachments

# Example: Add URL attachment
url = "https://api.trello.com/1/cards/ghi789/attachments"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'url': 'https://example.com/design-mockup.png',
    'name': 'Design Mockup'
}

response = requests.post(url, params=query)
```

#### Get Card Attachments

```python
GET /1/cards/{id}/attachments

# Example
url = "https://api.trello.com/1/cards/ghi789/attachments"

query = {
    'key': API_KEY,
    'token': TOKEN
}

response = requests.get(url, params=query)
attachments = response.json()
```

## Python Client Library

### Installation

```bash
pip install py-trello
```

### Basic Usage

```python
from trello import TrelloClient

# Initialize client
client = TrelloClient(
    api_key='your-api-key',
    token='your-token'
)

# Get all boards
boards = client.list_boards()

# Get specific board
board = client.get_board('board-id')

# Get lists on board
lists = board.list_lists()

# Get cards in list
todo_list = lists[0]
cards = todo_list.list_cards()

# Create card
new_card = todo_list.add_card(
    name='New user story',
    desc='Description here',
    labels=['High Priority']
)

# Add comment
new_card.comment('This is a comment')

# Move card
in_progress_list = lists[1]
new_card.change_list(in_progress_list.id)

# Add checklist
checklist = new_card.add_checklist('Acceptance Criteria', ['Item 1', 'Item 2'])

# Assign member
new_card.add_member(member_id)

# Set due date
from datetime import datetime, timedelta
due_date = datetime.now() + timedelta(days=7)
new_card.set_due(due_date)
```

## Webhooks

### Create Webhook

```python
POST /1/webhooks

# Example
url = "https://api.trello.com/1/webhooks/"

query = {
    'key': API_KEY,
    'token': TOKEN
}

data = {
    'callbackURL': 'https://your-server.com/webhook',
    'idModel': 'abc123',  # Board, list, or card ID
    'description': 'Sprint board webhook'
}

response = requests.post(url, params=query, json=data)
```

### Webhook Payload Example

```python
{
    "action": {
        "type": "updateCard",
        "data": {
            "card": {
                "id": "ghi789",
                "name": "User Authentication"
            },
            "listBefore": {
                "id": "def456",
                "name": "To Do"
            },
            "listAfter": {
                "id": "xyz123",
                "name": "In Progress"
            }
        },
        "memberCreator": {
            "id": "member123",
            "fullName": "John Doe"
        }
    },
    "model": {
        "id": "abc123",
        "name": "Sprint Board"
    }
}
```

## Scrum Board Setup Example

```python
import requests

def setup_scrum_board(board_name, api_key, token):
    """Create a Scrum board with standard lists"""

    # Create board
    url = "https://api.trello.com/1/boards/"
    query = {
        'key': api_key,
        'token': token,
        'name': board_name,
        'defaultLists': 'false'
    }
    board_response = requests.post(url, params=query)
    board = board_response.json()
    board_id = board['id']

    # Create lists
    lists = ['Backlog', 'To Do', 'In Progress', 'Review', 'Done']
    list_ids = {}

    for list_name in lists:
        url = "https://api.trello.com/1/lists"
        query = {
            'key': api_key,
            'token': token,
            'name': list_name,
            'idBoard': board_id
        }
        list_response = requests.post(url, params=query)
        list_data = list_response.json()
        list_ids[list_name] = list_data['id']

    # Create labels
    labels = [
        {'name': 'High Priority', 'color': 'red'},
        {'name': 'Medium Priority', 'color': 'yellow'},
        {'name': 'Low Priority', 'color': 'green'},
        {'name': 'Bug', 'color': 'orange'},
        {'name': 'Feature', 'color': 'blue'},
        {'name': 'Blocked', 'color': 'black'}
    ]

    for label in labels:
        url = "https://api.trello.com/1/labels"
        query = {
            'key': api_key,
            'token': token,
            'name': label['name'],
            'color': label['color'],
            'idBoard': board_id
        }
        requests.post(url, params=query)

    return {
        'board_id': board_id,
        'list_ids': list_ids
    }
```

## Sprint Metrics Calculation

```python
def calculate_sprint_metrics(board_id, done_list_id, api_key, token):
    """Calculate sprint completion metrics"""

    # Get all cards in Done list
    url = f"https://api.trello.com/1/lists/{done_list_id}/cards"
    query = {
        'key': api_key,
        'token': token
    }

    response = requests.get(url, params=query)
    done_cards = response.json()

    # Get all cards on board
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    response = requests.get(url, params=query)
    all_cards = response.json()

    # Calculate metrics
    total_cards = len(all_cards)
    completed_cards = len(done_cards)
    completion_rate = (completed_cards / total_cards * 100) if total_cards > 0 else 0

    return {
        'total_cards': total_cards,
        'completed_cards': completed_cards,
        'completion_rate': round(completion_rate, 2),
        'in_progress': total_cards - completed_cards
    }
```

## Rate Limiting

Trello API limits:
- **Free**: 100 requests per 10 seconds per token
- **Paid**: 300 requests per 10 seconds per token

Handle rate limiting:

```python
import time
from requests.exceptions import HTTPError

def trello_request_with_retry(func, max_retries=3):
    """Retry Trello API requests with exponential backoff"""
    for attempt in range(max_retries):
        try:
            response = func()
            if response.status_code == 429:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            return response
        except HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

## Best Practices

### 1. Batch Operations

Use batch endpoints when available:

```python
# Get multiple resources in single request
url = "https://api.trello.com/1/batch"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'urls': '/boards/abc123,/boards/def456,/boards/ghi789'
}

response = requests.get(url, params=query)
```

### 2. Field Filtering

Request only needed fields:

```python
url = "https://api.trello.com/1/boards/abc123/cards"

query = {
    'key': API_KEY,
    'token': TOKEN,
    'fields': 'name,idList,labels,due'  # Only get specific fields
}

response = requests.get(url, params=query)
```

### 3. Pagination

Handle large result sets:

```python
def get_all_cards(board_id, api_key, token):
    """Get all cards with pagination"""
    all_cards = []
    before = None

    while True:
        url = f"https://api.trello.com/1/boards/{board_id}/cards"
        query = {
            'key': api_key,
            'token': token,
            'limit': 1000
        }

        if before:
            query['before'] = before

        response = requests.get(url, params=query)
        cards = response.json()

        if not cards:
            break

        all_cards.extend(cards)
        before = cards[-1]['id']

    return all_cards
```

### 4. Error Handling

```python
def safe_trello_request(url, params):
    """Make Trello request with error handling"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Authentication failed. Check API key and token.")
        elif e.response.status_code == 404:
            print("Resource not found.")
        elif e.response.status_code == 429:
            print("Rate limit exceeded. Retry later.")
        else:
            print(f"HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
```

## Resources

- **Official API Documentation**: https://developer.atlassian.com/cloud/trello/rest/
- **API Introduction**: https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/
- **Python Trello Library**: https://github.com/sarumont/py-trello
- **Trello Power-Ups**: https://developer.atlassian.com/cloud/trello/power-ups/

## Troubleshooting

### Common Issues

**Issue: 401 Unauthorized**
- Verify API key and token are correct
- Check token hasn't expired
- Ensure token has necessary permissions

**Issue: Invalid ID**
- Verify board/list/card IDs are correct
- Use full IDs, not shortened versions
- Check resource hasn't been deleted

**Issue: Rate Limit Exceeded**
- Implement exponential backoff
- Reduce request frequency
- Consider upgrading to paid tier

**Issue: Webhook Not Triggering**
- Verify callback URL is accessible
- Check webhook is still active
- Ensure HTTPS is used for callback URL
