# Library Management System - REST API Documentation

This document describes the REST API endpoints added for mobile application integration.

## Base URL
```
http://localhost:5000
```

---

## API Endpoints

### 1. Student Login
**POST** `/api/login`

Allow students to log in using register number and password.

**Request Body (JSON):**
```json
{
  "register_number": "CS2024001",
  "password": "student_password"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "student": {
    "id": 1,
    "full_name": "John Doe",
    "branch": "Computer Science",
    "register_number": "CS2024001",
    "phone_number": "1234567890"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid or missing data
- `401 Unauthorized` - Invalid credentials

---

### 2. Get All Books
**GET** `/api/books`

Return a JSON list of all books with basic information.

**Success Response (200 OK):**
```json
{
  "success": true,
  "books": [
    {
      "id": 1,
      "title": "Introduction to Algorithms",
      "author": "Thomas H. Cormen",
      "category": "Computer Science",
      "availability": "Available",
      "available_copies": 3,
      "total_copies": 5
    },
    {
      "id": 2,
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "category": "Computer Science",
      "availability": "Not Available",
      "available_copies": 0,
      "total_copies": 2
    }
  ]
}
```

---

### 3. Get Book Details
**GET** `/api/book/<id>`

Return details of a specific book including author information.

**Example:**
```
GET /api/book/1
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "book": {
    "id": 1,
    "title": "Introduction to Algorithms",
    "author": "Thomas H. Cormen",
    "author_born_year": 1944,
    "author_died_year": null,
    "book_published_year": 2009,
    "author_description": "American mathematician and computer scientist",
    "isbn": "978-0262033848",
    "category": "Computer Science",
    "cover_image": "978-0262033848_algo.jpg",
    "availability": "Available",
    "available_copies": 3,
    "total_copies": 5,
    "created_at": "2024-03-07T10:30:00"
  }
}
```

**Error Responses:**
- `404 Not Found` - Book not found

---

### 4. Reserve Book
**POST** `/api/reserve`

Allow a student to reserve a book using student_id and book_id.

**Request Body (JSON):**
```json
{
  "student_id": 1,
  "book_id": 5
}
```

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "Book reservation request submitted successfully",
  "reservation_id": 12
}
```

**Error Responses:**
- `400 Bad Request` - Missing data or duplicate reservation
- `404 Not Found` - Student or book not found

---

### 5. Get Student's Books
**GET** `/api/mybooks/<student_id>`

Return all books reserved or borrowed by a student.

**Example:**
```
GET /api/mybooks/1
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "student_id": 1,
  "reservations": [
    {
      "type": "reservation",
      "reservation_id": 12,
      "book_id": 5,
      "book_title": "Database Systems",
      "status": "pending",
      "request_date": "2024-03-07T11:00:00",
      "processed_date": null
    },
    {
      "type": "reservation",
      "reservation_id": 10,
      "book_id": 3,
      "book_title": "Operating Systems",
      "status": "approved",
      "request_date": "2024-03-05T09:00:00",
      "processed_date": "2024-03-06T10:00:00"
    }
  ],
  "issued_books": [
    {
      "type": "issued",
      "issue_id": 8,
      "book_id": 3,
      "book_title": "Operating Systems",
      "issue_date": "2024-03-06T10:00:00",
      "due_date": "2024-03-13T10:00:00",
      "return_date": null,
      "returned": false,
      "is_overdue": false,
      "days_overdue": 0,
      "fine_amount": 0
    },
    {
      "type": "issued",
      "issue_id": 5,
      "book_id": 1,
      "book_title": "Introduction to Algorithms",
      "issue_date": "2024-02-20T08:00:00",
      "due_date": "2024-02-27T08:00:00",
      "return_date": "2024-02-26T15:00:00",
      "returned": true,
      "is_overdue": false,
      "days_overdue": 0,
      "fine_amount": 0
    }
  ],
  "total_books": 4
}
```

**Error Responses:**
- `404 Not Found` - Student not found

---

## Testing the API

### Using cURL

**1. Student Login:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d "{\"register_number\":\"CS2024001\",\"password\":\"student123\"}"
```

**2. Get All Books:**
```bash
curl http://localhost:5000/api/books
```

**3. Get Book Details:**
```bash
curl http://localhost:5000/api/book/1
```

**4. Reserve Book:**
```bash
curl -X POST http://localhost:5000/api/reserve \
  -H "Content-Type: application/json" \
  -d "{\"student_id\":1,\"book_id\":5}"
```

**5. Get Student's Books:**
```bash
curl http://localhost:5000/api/mybooks/1
```

### Using Postman

1. Open Postman
2. Create a new request with the appropriate HTTP method
3. Enter the endpoint URL (e.g., `http://localhost:5000/api/books`)
4. For POST requests:
   - Set Headers: `Content-Type: application/json`
   - In Body tab, select "raw" and enter JSON data
5. Click "Send"

### Using Python Requests

```python
import requests

# Login
login_data = {
    'register_number': 'CS2024001',
    'password': 'student123'
}
response = requests.post('http://localhost:5000/api/login', json=login_data)
print(response.json())

# Get all books
response = requests.get('http://localhost:5000/api/books')
print(response.json())

# Get specific book
response = requests.get('http://localhost:5000/api/book/1')
print(response.json())

# Reserve book
reserve_data = {
    'student_id': 1,
    'book_id': 5
}
response = requests.post('http://localhost:5000/api/reserve', json=reserve_data)
print(response.json())

# Get student's books
response = requests.get('http://localhost:5000/api/mybooks/1')
print(response.json())
```

---

## Integration Notes

### For Mobile Developers

1. **Authentication**: Currently, the API uses session-based authentication from the web system. For mobile apps, consider implementing token-based authentication (JWT).

2. **CORS**: If your mobile app communicates from a different origin, enable CORS in Flask:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

3. **HTTPS**: In production, always use HTTPS to secure data transmission.

4. **Rate Limiting**: Consider implementing rate limiting to prevent abuse:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/api/login', methods=['POST'])
   @limiter.limit("5 per minute")
   def api_login():
       # ...
   ```

5. **Error Handling**: All endpoints return consistent JSON responses with:
   - `success`: boolean indicating success/failure
   - `message`: descriptive error message (on failure)
   - Data payload: on success

---

## Database Schema

The API uses the same database models as the web interface:

- **Student**: id, full_name, branch, register_number, phone_number, password
- **Book**: id, title, author, isbn, branch_category, cover_image, total_copies, available_copies
- **Reservation**: id, student_id, book_id, status, request_date, processed_date
- **IssuedBook**: id, student_id, book_id, issue_date, return_date, due_date, returned

---

## Existing Website Features

All existing website features remain unchanged:
- ✅ Admin Dashboard
- ✅ Book Management (Add/Delete/Edit)
- ✅ Student Registration/Login
- ✅ Book Search & Browse
- ✅ Reservation System
- ✅ Admin Approval Workflow
- ✅ Book Issue Tracking
- ✅ Renewal Requests
- ✅ Fine Calculation

The new API endpoints work alongside the existing web interface without any conflicts.

---

## Running the Application

1. Make sure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask application:
   ```bash
   python app.py
   ```

3. The API will be available at `http://localhost:5000/api/...`

4. Test the endpoints using the examples above.

---

## Support

For issues or questions about the API, please refer to the main application documentation or contact the development team.
