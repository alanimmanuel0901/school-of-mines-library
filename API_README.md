# 📚 Library Management System - REST API Update

## Overview

Your Flask Library Management System has been successfully updated with REST API endpoints for mobile application integration. The system now supports both web and mobile clients simultaneously.

---

## ✅ What's New

### 5 REST API Endpoints Added

1. **POST /api/login** - Student authentication
2. **GET /api/books** - List all books
3. **GET /api/book/<id>** - Get book details
4. **POST /api/reserve** - Reserve a book
5. **GET /api/mybooks/<student_id>** - Get student's books

All responses are in JSON format, ready for mobile app consumption.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

The server will start at `http://localhost:5000`

### 3. Test the API
```bash
# Option 1: Use the test script
python test_api.py

# Option 2: Test manually with cURL
curl http://localhost:5000/api/books

# Option 3: Use Postman
# Import endpoints and test interactively
```

---

## 📱 API Usage Examples

### Student Login
```javascript
// JavaScript (React Native)
const login = async (registerNumber, password) => {
  const response = await fetch('http://localhost:5000/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      register_number: registerNumber,
      password: password
    })
  });
  
  const data = await response.json();
  if (data.success) {
    console.log('Logged in:', data.student);
  }
  return data;
};
```

### Get All Books
```python
# Python
import requests

response = requests.get('http://localhost:5000/api/books')
books = response.json()['books']

for book in books:
    print(f"{book['title']} by {book['author']}")
```

### Reserve a Book
```java
// Java (Android)
JSONObject requestBody = new JSONObject();
requestBody.put("student_id", 1);
requestBody.put("book_id", 5);

JsonObjectRequest request = new JsonObjectRequest(
    Request.Method.POST,
    "http://localhost:5000/api/reserve",
    requestBody,
    response -> {
        if (response.getBoolean("success")) {
            Toast.makeText(context, "Book reserved!", Toast.LENGTH_SHORT).show();
        }
    },
    error -> Log.e("API", "Error: " + error.getMessage())
);

MySingleton.getInstance(context).addToRequestQueue(request);
```

---

## 📋 Documentation Files

| File | Description |
|------|-------------|
| `API_DOCUMENTATION.md` | Complete API reference with examples |
| `API_QUICK_REFERENCE.md` | Quick lookup card for developers |
| `API_ARCHITECTURE.md` | Architecture diagrams and patterns |
| `API_INTEGRATION_SUMMARY.md` | Implementation summary |
| `test_api.py` | Automated test script |

---

## 🔒 Security Features

- ✅ Password hashing (Werkzeug)
- ✅ Input validation
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Proper error handling
- ⚠️ Session-based auth (consider JWT for production)

---

## 🎯 Existing Features Preserved

All website functionality remains intact:

- ✅ Admin Dashboard
- ✅ Book Management (Add/Delete/Edit)
- ✅ Student Registration & Login
- ✅ Book Search & Browse
- ✅ Reservation System
- ✅ Admin Approval Workflow
- ✅ Book Issue Tracking
- ✅ Renewal Requests
- ✅ Fine Calculation

---

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "message": "Optional message",
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description"
}
```

---

## 🧪 Testing

### Using the Test Script
```bash
# Make sure Flask is running first
python test_api.py
```

### Using Postman
1. Create a new collection called "Library API"
2. Add requests for each endpoint
3. Set headers: `Content-Type: application/json`
4. Send requests and verify responses

### Using cURL
```bash
# Get all books
curl http://localhost:5000/api/books

# Get specific book
curl http://localhost:5000/api/book/1

# Login
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"register_number":"CS001","password":"password"}'

# Reserve book
curl -X POST http://localhost:5000/api/reserve \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"book_id":5}'
```

---

## 🏗️ Architecture

```
Mobile App → REST API → Business Logic → Database
     ↓           ↓
Web Browser → Flask Routes → Same Backend
```

Both web and mobile clients share the same backend logic and database.

---

## 📈 Production Recommendations

1. **Authentication**: Implement JWT tokens for mobile apps
2. **HTTPS**: Enable SSL/TLS encryption
3. **Rate Limiting**: Prevent abuse with flask-limiter
4. **CORS**: Configure properly for your domains
5. **Monitoring**: Add logging and error tracking (Sentry)
6. **Caching**: Use Redis or Memcached for frequently accessed data
7. **Database**: Consider PostgreSQL for production
8. **Backups**: Implement automated database backups

---

## 🔧 Configuration

### Environment Variables (Recommended for Production)
```python
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'
```

### CORS Setup
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-app.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def api_login():
    ...
```

---

## 🐛 Troubleshooting

### API Not Responding
- Check if Flask server is running
- Verify port 5000 is not blocked
- Check firewall settings

### CORS Errors
- Enable CORS in Flask
- Add your mobile app's domain to allowed origins

### Authentication Issues
- Verify credentials are correct
- Check password hashing implementation
- Ensure session is properly configured

### Database Errors
- Run `python app.py` to initialize database
- Check if `instance/library.db` exists
- Verify write permissions

---

## 📞 Support

For detailed information:
- 📖 Full API Docs: `API_DOCUMENTATION.md`
- 🏗️ Architecture: `API_ARCHITECTURE.md`
- ⚡ Quick Reference: `API_QUICK_REFERENCE.md`
- 🧪 Tests: `test_api.py`

---

## 🎉 Next Steps

1. **Design Mobile UI**
   - Create wireframes
   - Design screens (Login, Browse, Details, Profile)
   - Implement navigation

2. **Develop Mobile App**
   - Choose framework (React Native, Flutter, Native)
   - Implement API calls
   - Add offline support

3. **Test Thoroughly**
   - Unit tests
   - Integration tests
   - User acceptance testing

4. **Deploy**
   - Set up production server
   - Configure HTTPS
   - Monitor performance

---

## 📝 Version History

**v2.0 - March 2026**
- ✅ Added REST API endpoints
- ✅ Mobile app integration ready
- ✅ Comprehensive documentation
- ✅ Test scripts included

**v1.0 - Original**
- ✅ Web-based library management
- ✅ Admin dashboard
- ✅ Student portal
- ✅ Book management

---

## 📄 License

This project is for educational purposes.

---

**Built with ❤️ using Flask, SQLite, and modern web technologies**

**Ready for mobile integration! 🚀📱**
