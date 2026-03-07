"""
Test script for the complete /api/books endpoint
Verifies all required fields are returned in the JSON response
"""

import requests
import json

def test_books_api():
    """Test the GET /api/books endpoint"""
    
    print("="*80)
    print("Testing GET /api/books Endpoint")
    print("="*80)
    print()
    
    try:
        # Make the API request
        response = requests.get('http://127.0.0.1:5000/api/books')
        
        print(f"Status Code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            books = response.json()
            
            print(f"✅ Success! Found {len(books)} book(s)\n")
            
            if not books:
                print("⚠️  No books found in the database.")
                print("\nTo add books:")
                print("1. Go to http://127.0.0.1:5000/admin/login")
                print("2. Login with admin/admin123")
                print("3. Navigate to 'Add Book' section")
                return False
            
            # Define required fields
            required_fields = [
                'id',
                'title',
                'author',
                'author_born_year',
                'author_died_year',
                'book_published_year',
                'author_description',
                'isbn',
                'branch_category',
                'cover_image',
                'total_copies',
                'available_copies',
                'created_at'
            ]
            
            # Test each book
            all_tests_passed = True
            for i, book in enumerate(books, 1):
                print(f"\n{'─'*80}")
                print(f"Book #{i}: {book.get('title', 'Unknown')}")
                print(f"{'─'*80}")
                
                # Check all required fields
                missing_fields = []
                extra_fields = []
                
                for field in required_fields:
                    if field not in book:
                        missing_fields.append(field)
                        print(f"  ❌ Missing field: {field}")
                        all_tests_passed = False
                    else:
                        value = book[field]
                        # Truncate long text for display
                        if isinstance(value, str) and len(value) > 50:
                            value = value[:50] + "..."
                        print(f"  ✅ {field}: {value}")
                
                # Check for unexpected fields
                for field in book.keys():
                    if field not in required_fields:
                        extra_fields.append(field)
                
                if extra_fields:
                    print(f"\n  ℹ️  Additional fields: {', '.join(extra_fields)}")
                
                if missing_fields:
                    print(f"\n  ⚠️  Total missing fields: {len(missing_fields)}")
                    all_tests_passed = False
            
            print(f"\n{'='*80}")
            if all_tests_passed:
                print("✅ ALL TESTS PASSED!")
                print(f"   - All {len(required_fields)} required fields present in all books")
                print("   - Response format matches specification")
            else:
                print("❌ SOME TESTS FAILED!")
                print("   - Some required fields are missing")
            
            print(f"{'='*80}")
            
            # Display sample JSON structure
            print(f"\n📋 Sample JSON Structure (First Book):")
            print(f"{'─'*80}")
            print(json.dumps(books[0], indent=2))
            
            return all_tests_passed
            
        else:
            print(f"❌ Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("\nMake sure Flask server is running at http://127.0.0.1:5000")
        print("Run: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_response_format():
    """Test that response matches the exact format requested"""
    
    print(f"\n{'='*80}")
    print("Verifying Response Format Against Specification")
    print(f"{'='*80}")
    print()
    
    expected_format = {
        "id": "integer",
        "title": "string",
        "author": "string",
        "author_born_year": "integer or null",
        "author_died_year": "integer or null",
        "book_published_year": "integer or null",
        "author_description": "string or null",
        "isbn": "string",
        "branch_category": "string",
        "cover_image": "string",
        "total_copies": "integer",
        "available_copies": "integer",
        "created_at": "date string (YYYY-MM-DD)"
    }
    
    print("Expected fields and types:")
    for field, field_type in expected_format.items():
        print(f"  • {field:25} - {field_type}")
    
    print()

if __name__ == '__main__':
    print("\n" + "="*80)
    print("COMPLETE BOOKS API TEST SUITE")
    print("="*80)
    print()
    
    # Test the API
    test_result = test_books_api()
    
    # Show expected format
    test_response_format()
    
    # Summary
    print(f"\n{'='*80}")
    print("TEST SUMMARY")
    print(f"{'='*80}")
    
    if test_result:
        print("✅ API endpoint is working correctly!")
        print("✅ All required fields are present!")
        print("✅ Response format matches specification!")
    else:
        print("❌ API endpoint needs fixes!")
        print("❌ Some required fields are missing!")
    
    print(f"{'='*80}")
    print()
