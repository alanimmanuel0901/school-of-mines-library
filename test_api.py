"""
Test script for Library Management System REST API
Run this after starting the Flask server with: python app.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(title, response):
    """Helper function to print API responses nicely"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print()

# Test 1: Get All Books
print("\n📚 TEST 1: Getting all books...")
try:
    response = requests.get(f"{BASE_URL}/api/books")
    print_response("GET /api/books", response)
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get Specific Book (ID=1)
print("\n📖 TEST 2: Getting book details for ID=1...")
try:
    response = requests.get(f"{BASE_URL}/api/book/1")
    print_response("GET /api/book/1", response)
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Student Login
print("\n🔐 TEST 3: Testing student login...")
print("💡 Note: You need to register a student first via the web interface")
login_data = {
    "register_number": "TEST001",  # Replace with actual register number
    "password": "test123"           # Replace with actual password
}
try:
    response = requests.post(f"{BASE_URL}/api/login", json=login_data)
    print_response("POST /api/login", response)
    
    if response.status_code == 200:
        student_id = response.json()['student']['id']
        print(f"✅ Login successful! Student ID: {student_id}")
        
        # Test 4: Get Student's Books
        print(f"\n📚 TEST 4: Getting books for student ID={student_id}...")
        response = requests.get(f"{BASE_URL}/api/mybooks/{student_id}")
        print_response(f"GET /api/mybooks/{student_id}", response)
        
        # Test 5: Reserve a Book
        print("\n📝 TEST 5: Testing book reservation...")
        reserve_data = {
            "student_id": student_id,
            "book_id": 1  # Try to reserve book with ID=1
        }
        response = requests.post(f"{BASE_URL}/api/reserve", json=reserve_data)
        print_response("POST /api/reserve", response)
        
    else:
        print("❌ Login failed. Please check the credentials or register a student first.")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("✅ API Testing Complete!")
print("="*60)
print("\n💡 Tips:")
print("1. Make sure the Flask server is running (python app.py)")
print("2. Register a student via /student/register if login fails")
print("3. Add some books via admin panel before testing")
print("4. Use Postman for more interactive testing")
print("\n📱 All API endpoints are ready for mobile app integration!")
print()
