# API Documentation

This document describes the API endpoints available in the Study Resource Recommender system. This is useful for advanced users who want to build custom applications or integrate with other systems.

## Base URL

```
http://localhost:5000/api
```

## Authentication

The system uses session-based authentication. You must create a user first before accessing most endpoints.

## Endpoints

### User Management

#### Create/Load User
**Endpoint:** `POST /api/user/create`

**Request:**
```json
{
    "user_id": "student1"
}
```

**Response:**
```json
{
    "success": true,
    "user_id": "student1",
    "preferences": {
        "subject": "programming",
        "difficulty": "beginner",
        "format": "mixed",
        "tags": []
    }
}
```

---

### Recommendations

#### Get Personalized Recommendations
**Endpoint:** `GET /api/recommendations`

**Requirements:** User must be logged in

**Response:**
```json
[
    {
        "resource": {
            "id": "res_001",
            "title": "Python Crash Course",
            "type": "book",
            "subject": "programming",
            "difficulty": "beginner",
            "format": "text",
            "duration_hours": 20,
            "url": "https://nostarch.com/pythoncrashcourse2e",
            "tags": ["python", "coding", "basics"]
        },
        "score": 85.5
    }
]
```

---

### Resources

#### Get All Resources
**Endpoint:** `GET /api/resources`

**Response:**
```json
[
    {
        "id": "res_001",
        "title": "Python Crash Course",
        "type": "book",
        "subject": "programming",
        "difficulty": "beginner",
        "format": "text",
        "duration_hours": 20,
        "url": "https://nostarch.com/pythoncrashcourse2e",
        "tags": ["python", "coding", "basics"]
    }
]
```

#### Get Specific Resource
**Endpoint:** `GET /api/resources/<resource_id>`

**Example:** `GET /api/resources/res_001`

**Response:**
```json
{
    "id": "res_001",
    "title": "Python Crash Course",
    "type": "book",
    "subject": "programming",
    "difficulty": "beginner",
    "format": "text",
    "duration_hours": 20,
    "url": "https://nostarch.com/pythoncrashcourse2e",
    "tags": ["python", "coding", "basics"]
}
```

#### Add New Resource
**Endpoint:** `POST /api/resources/add`

**Request:**
```json
{
    "id": "res_009",
    "title": "New Course",
    "type": "course",
    "subject": "programming",
    "difficulty": "intermediate",
    "format": "video",
    "duration_hours": 30,
    "url": "https://example.com/course",
    "tags": ["programming", "web"]
}
```

**Response:**
```json
{
    "success": true,
    "resource": {
        "id": "res_009",
        "title": "New Course",
        ...
    }
}
```

---

### User Preferences

#### Get User Preferences
**Endpoint:** `GET /api/user/preferences`

**Requirements:** User must be logged in

**Response:**
```json
{
    "subject": "programming",
    "difficulty": "beginner",
    "format": "mixed",
    "tags": ["python", "ai"]
}
```

#### Update User Preferences
**Endpoint:** `POST /api/user/preferences`

**Requirements:** User must be logged in

**Request:**
```json
{
    "subject": "mathematics",
    "difficulty": "intermediate",
    "format": "video",
    "tags": ["calculus", "linear-algebra"]
}
```

**Response:**
```json
{
    "success": true,
    "preferences": {
        "subject": "mathematics",
        "difficulty": "intermediate",
        "format": "video",
        "tags": ["calculus", "linear-algebra"]
    }
}
```

---

### Bookmarks

#### Get User Bookmarks
**Endpoint:** `GET /api/user/bookmarks`

**Requirements:** User must be logged in

**Response:**
```json
[
    {
        "id": "res_001",
        "title": "Python Crash Course",
        ...
    }
]
```

#### Add Bookmark
**Endpoint:** `POST /api/user/bookmarks`

**Requirements:** User must be logged in

**Request:**
```json
{
    "resource_id": "res_001"
}
```

**Response:**
```json
{
    "success": true
}
```

#### Remove Bookmark
**Endpoint:** `DELETE /api/user/bookmarks`

**Requirements:** User must be logged in

**Request:**
```json
{
    "resource_id": "res_001"
}
```

**Response:**
```json
{
    "success": true
}
```

---

### Learning History

#### Get Learning History
**Endpoint:** `GET /api/user/history`

**Requirements:** User must be logged in

**Response:**
```json
[
    {
        "resource": {
            "id": "res_001",
            "title": "Python Crash Course",
            ...
        },
        "action": "viewed",
        "timestamp": "2024-01-15T10:30:00"
    }
]
```

#### Mark Resource as Completed
**Endpoint:** `POST /api/user/complete`

**Requirements:** User must be logged in

**Request:**
```json
{
    "resource_id": "res_001"
}
```

**Response:**
```json
{
    "success": true
}
```

---

### System Information

#### Get Available Subjects
**Endpoint:** `GET /api/subjects`

**Response:**
```json
[
    "programming",
    "mathematics",
    "science",
    "computer science",
    "artificial intelligence"
]
```

#### Get Available Formats
**Endpoint:** `GET /api/formats`

**Response:**
```json
[
    "text",
    "video",
    "mixed"
]
```

#### Get System Statistics
**Endpoint:** `GET /api/stats`

**Response:**
```json
{
    "total_resources": 8,
    "by_type": {
        "book": 3,
        "course": 3,
        "video": 2
    },
    "by_subject": {
        "programming": 3,
        "mathematics": 2,
        "science": 1,
        "computer science": 1,
        "artificial intelligence": 1
    },
    "by_difficulty": {
        "beginner": 4,
        "intermediate": 2,
        "advanced": 2
    }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "success": false,
    "error": "Invalid resource or duplicate ID"
}
```

### 401 Unauthorized
```json
{
    "error": "User not logged in"
}
```

### 404 Not Found
```json
{
    "error": "Not found"
}
```

### 500 Server Error
```json
{
    "error": "Server error"
}
```

---

## Example: Using the API with Python

```python
import requests
import json

BASE_URL = "http://localhost:5000/api"
session = requests.Session()

# 1. Create/load user
response = session.post(f"{BASE_URL}/user/create", 
    json={"user_id": "student1"})
print(response.json())

# 2. Update preferences
response = session.post(f"{BASE_URL}/user/preferences",
    json={
        "subject": "programming",
        "difficulty": "beginner",
        "format": "mixed",
        "tags": ["python"]
    })
print(response.json())

# 3. Get recommendations
response = session.get(f"{BASE_URL}/recommendations")
recommendations = response.json()
for rec in recommendations:
    print(f"{rec['resource']['title']}: {rec['score']}/100")

# 4. Bookmark a resource
response = session.post(f"{BASE_URL}/user/bookmarks",
    json={"resource_id": "res_001"})
print(response.json())

# 5. Get bookmarks
response = session.get(f"{BASE_URL}/user/bookmarks")
bookmarks = response.json()
print(f"You have {len(bookmarks)} bookmarks")
```

---

## Example: Using the API with JavaScript

```javascript
const BASE_URL = "http://localhost:5000/api";

// 1. Create/load user
fetch(`${BASE_URL}/user/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 'student1' })
})
.then(r => r.json())
.then(data => console.log(data));

// 2. Get recommendations
fetch(`${BASE_URL}/recommendations`)
    .then(r => r.json())
    .then(recs => {
        recs.forEach(rec => {
            console.log(`${rec.resource.title}: ${rec.score}/100`);
        });
    });

// 3. Bookmark a resource
fetch(`${BASE_URL}/user/bookmarks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resource_id: 'res_001' })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## Rate Limiting

Currently, there is no rate limiting. In a production environment, you should implement rate limiting to prevent abuse.

## CORS

The API does not have CORS enabled by default. To enable CORS for cross-origin requests, install Flask-CORS:

```bash
pip install flask-cors
```

Then modify `src/app.py`:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```
