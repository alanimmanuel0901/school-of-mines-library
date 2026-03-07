import requests

try:
    # Test the /api/books endpoint
    response = requests.get('http://127.0.0.1:5000/api/books')
    
    print(f"Status Code: {response.status_code}")
    print(f"\nResponse from GET /api/books:\n")
    
    if response.status_code == 200:
        books = response.json()
        print(f"✅ Success! Found {len(books)} books\n")
        
        if books:
            print("Books in library:")
            print("-" * 80)
            for book in books:
                print(f"ID: {book['id']}")
                print(f"Title: {book['title']}")
                print(f"Author: {book['author']}")
                print(f"Category: {book['branch_category']}")
                print("-" * 80)
        else:
            print("No books found in the database.")
            print("\nTo add books:")
            print("1. Go to http://127.0.0.1:5000/admin/login")
            print("2. Login with admin/admin123")
            print("3. Navigate to Add Book section")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error!")
    print("\nMake sure Flask server is running at http://127.0.0.1:5000")
    print("Run: python app.py")
except Exception as e:
    print(f"❌ Error: {e}")
