# Library System API Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Mobile Application                        │
│                   (iOS / Android / Web)                      │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/HTTPS Requests
                     │ JSON Responses
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   REST API Layer                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  POST /api/login     - Student Authentication        │   │
│  │  GET  /api/books     - List All Books                │   │
│  │  GET  /api/book/:id  - Book Details                  │   │
│  │  POST /api/reserve   - Reserve Book                  │   │
│  │  GET  /api/mybooks/:id - Student's Books             │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │ SQLAlchemy ORM
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 Business Logic Layer                         │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐              │
│  │  Student   │  │   Book   │  │ Reservation│              │
│  │  Service   │  │ Service  │  │  Service   │              │
│  └────────────┘  └──────────┘  └────────────┘              │
└────────────────────┬────────────────────────────────────────┘
                     │ Database Operations
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  SQLite Database                             │
│  ┌──────────┐  ┌───────┐  ┌────────────┐  ┌──────────┐     │
│  │ Students │  │ Books │  │Reservations│  │IssuedBooks│    │
│  └──────────┘  └───────┘  └────────────┘  └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## API Request Flow

### Example: Book Reservation Flow

```
Mobile App → POST /api/reserve
    ↓
API Endpoint Validates Request
    ↓
Check if Student Exists → 404 if Not Found
    ↓
Check if Book Exists → 404 if Not Found
    ↓
Check for Duplicate Reservation → 400 if Exists
    ↓
Check if Book Already Issued → 400 if Issued
    ↓
Create Reservation Record
    ↓
Return Success (201 Created)
    ↓
Mobile App Receives Confirmation
```

---

## Data Models

### Student Model
```json
{
  "id": 1,
  "full_name": "John Doe",
  "branch": "Computer Science",
  "register_number": "CS2024001",
  "phone_number": "1234567890",
  "password": "hashed_password"
}
```

### Book Model
```json
{
  "id": 1,
  "title": "Introduction to Algorithms",
  "author": "Thomas H. Cormen",
  "author_born_year": 1944,
  "author_died_year": null,
  "book_published_year": 2009,
  "author_description": "American mathematician...",
  "isbn": "978-0262033848",
  "branch_category": "Computer Science",
  "cover_image": "978-0262033848_algo.jpg",
  "total_copies": 5,
  "available_copies": 3
}
```

### Reservation Model
```json
{
  "id": 12,
  "student_id": 1,
  "book_id": 5,
  "status": "pending",  // pending, approved, rejected
  "request_date": "2024-03-07T11:00:00",
  "processed_date": null
}
```

### IssuedBook Model
```json
{
  "id": 8,
  "student_id": 1,
  "book_id": 3,
  "issue_date": "2024-03-06T10:00:00",
  "due_date": "2024-03-13T10:00:00",
  "return_date": null,
  "returned": false
}
```

---

## Authentication Flow

### Current Implementation (Session-Based)
```
Student Login via Web → Session Created → Cookie Stored
                              ↓
                    Web Pages Access
```

### Mobile Implementation (Recommended JWT)
```
POST /api/login
      ↓
Validate Credentials
      ↓
Generate JWT Token
      ↓
Return Token to Mobile
      ↓
Mobile Stores Token
      ↓
Include Token in Headers for Future Requests
      ↓
Server Validates Token on Each Request
```

---

## Security Layers

```
┌─────────────────────────────────────┐
│   Input Validation                  │
│   - Check required fields           │
│   - Validate data types             │
│   - Sanitize inputs                 │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│   Authentication                    │
│   - Password hashing (Werkzeug)     │
│   - Session/JWT verification        │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│   Authorization                     │
│   - Student can only reserve        │
│   - Verify ownership of records     │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│   Database Protection               │
│   - SQLAlchemy ORM (SQL injection)  │
│   - Foreign key constraints         │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│   Error Handling                    │
│   - Consistent error responses      │
│   - No sensitive data in errors     │
└─────────────────────────────────────┘
```

---

## Response Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET requests |
| 201 | Created | Successful reservation creation |
| 400 | Bad Request | Invalid input, duplicate request |
| 401 | Unauthorized | Invalid login credentials |
| 404 | Not Found | Student/Book not found |
| 500 | Internal Server Error | Database errors, exceptions |

---

## Rate Limiting Strategy (Recommended)

```python
from flask_limiter import Limiter

limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")  # Prevent brute force
def api_login():
    ...

@app.route('/api/reserve', methods=['POST'])
@limiter.limit("10 per hour")  # Prevent spam reservations
def api_reserve_book():
    ...
```

---

## CORS Configuration (For Web/Mobile)

```python
from flask_cors import CORS

# Allow specific origins
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-mobile-app.com",
            "https://your-admin-panel.com"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## API Versioning Strategy

For future updates, consider versioning:

```
/api/v1/login
/api/v1/books
/api/v2/login  (with new features)
```

Implementation:
```python
@api_v1.route('/login')
def login_v1():
    ...

@api_v2.route('/login')
def login_v2():
    ...  # Enhanced version
```

---

## Monitoring & Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.before_request
def log_request():
    app.logger.info(f'{request.method} {request.path}')

@app.after_request
def log_response(response):
    app.logger.info(f'{response.status_code}')
    return response
```

---

## Performance Optimization

### Database Queries
- Use eager loading for relationships
- Add indexes on frequently queried columns
- Implement pagination for large datasets

### Caching Strategy
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/api/books')
@cache.cached(timeout=300)  # Cache for 5 minutes
def api_get_books():
    ...
```

---

## Testing Strategy

### Unit Tests
```python
def test_api_login_success():
    response = client.post('/api/login', json={
        'register_number': 'CS001',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert response.json['success'] == True
```

### Integration Tests
```python
def test_full_reservation_flow():
    # Login
    login_resp = client.post('/api/login', json=login_data)
    student_id = login_resp.json['student']['id']
    
    # Reserve book
    reserve_resp = client.post('/api/reserve', json={
        'student_id': student_id,
        'book_id': 1
    })
    assert reserve_resp.status_code == 201
```

---

## Deployment Checklist

- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Add monitoring/logging
- [ ] Configure database backups
- [ ] Set up error tracking (Sentry)
- [ ] Load testing
- [ ] Security audit
- [ ] API documentation published
- [ ] Version control strategy

---

This architecture supports both the existing web application and new mobile clients simultaneously!
