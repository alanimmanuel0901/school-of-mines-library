import requests
import json

print("Testing GET /api/books endpoint...\n")

try:
    response = requests.get('http://127.0.0.1:5000/api/books')
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        books = response.json()
        print(f"✅ Success! Found {len(books)} book(s)\n")
        
        if books:
            # Show first book as sample
            print("Sample response (first book):")
            print("=" * 80)
            print(json.dumps(books[0], indent=2))
            print("=" * 80)
            
            # Verify all required fields
            required_fields = [
                'id', 'title', 'author', 'author_born_year', 'author_died_year',
                'book_published_year', 'author_description', 'isbn', 'branch_category',
                'cover_image', 'total_copies', 'available_copies', 'created_at'
            ]
            
            print(f"\nField verification:")
            missing = []
            for field in required_fields:
                if field in books[0]:
                    print(f"  ✅ {field}")
                else:
                    print(f"  ❌ {field} - MISSING")
                    missing.append(field)
            
            if not missing:
                print(f"\n✅ All {len(required_fields)} required fields present!")
            else:
                print(f"\n❌ Missing fields: {missing}")
        else:
            print("No books in database. Add some books via admin panel.")
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure Flask server is running: python app.py")
