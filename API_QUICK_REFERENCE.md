# 📱 Quick API Reference Card

## Base URL
```
http://localhost:5000/api
```

---

## Endpoints at a Glance

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | Student login | ❌ No |
| GET | `/books` | Get all books | ❌ No |
| GET | `/book/<id>` | Get book details | ❌ No |
| POST | `/reserve` | Reserve a book | ❌ No* |
| GET | `/mybooks/<id>` | Get student's books | ❌ No* |

*Note: Authentication recommended for production

---

## Quick Examples

### 🔐 Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"register_number":"CS001","password":"pass123"}'
```

**Response:**
```json
{
  "success": true,
  "student": {
    "id": 1,
    "full_name": "John Doe",
    "branch": "Computer Science"
  }
}
```

---

### 📚 Get All Books
```bash
curl http://localhost:5000/api/books
```

**Response:**
```json
{
  "success": true,
  "books": [
    {
      "id": 1,
      "title": "Algorithm Design",
      "author": "Kleinberg",
      "category": "Computer Science",
      "availability": "Available"
    }
  ]
}
```

---

### 📖 Get Book Details
```bash
curl http://localhost:5000/api/book/1
```

**Response:**
```json
{
  "success": true,
  "book": {
    "id": 1,
    "title": "Algorithm Design",
    "author": "Kleinberg & Tardos",
    "isbn": "978-0321295354",
    "category": "Computer Science",
    "available_copies": 3,
    "total_copies": 5
  }
}
```

---

### 📝 Reserve Book
```bash
curl -X POST http://localhost:5000/api/reserve \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"book_id":5}'
```

**Response:**
```json
{
  "success": true,
  "message": "Book reservation request submitted successfully",
  "reservation_id": 12
}
```

---

### 📋 Get Student's Books
```bash
curl http://localhost:5000/api/mybooks/1
```

**Response:**
```json
{
  "success": true,
  "reservations": [...],
  "issued_books": [...],
  "total_books": 5
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| ✅ 200 | Success |
| ✅ 201 | Created |
| ❌ 400 | Bad Request |
| ❌ 401 | Unauthorized |
| ❌ 404 | Not Found |
| ❌ 500 | Server Error |

---

## Common Errors

### Invalid Login
```json
{
  "success": false,
  "message": "Invalid register number or password"
}
```

### Duplicate Reservation
```json
{
  "success": false,
  "message": "You already have a pending reservation for this book"
}
```

### Student Not Found
```json
{
  "success": false,
  "message": "Student not found"
}
```

---

## Testing Tools

### Postman Collection
Import these endpoints into Postman for easy testing.

### Python Test
```python
import requests

# Login
r = requests.post('http://localhost:5000/api/login', 
    json={'register_number': 'CS001', 'password': 'pass123'})
print(r.json())

# Get books
r = requests.get('http://localhost:5000/api/books')
print(r.json())
```

### JavaScript Fetch
```javascript
// Login
const response = await fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    register_number: 'CS001',
    password: 'pass123'
  })
});
const data = await response.json();
```

---

## Production Checklist

- [ ] Enable HTTPS
- [ ] Add JWT authentication
- [ ] Configure CORS
- [ ] Set up rate limiting
- [ ] Add request logging
- [ ] Monitor API usage
- [ ] Implement error tracking

---

## Need Help?

📖 **Full Documentation**: `API_DOCUMENTATION.md`  
🏗️ **Architecture Details**: `API_ARCHITECTURE.md`  
📊 **Integration Summary**: `API_INTEGRATION_SUMMARY.md`  
🧪 **Test Script**: `test_api.py`

---

**Happy Coding! 🚀**
