"""
Simple test script to demonstrate API functionality
Run this after starting the Django server
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("=== Django REST API Test ===\n")
    
    # Test API Overview
    print("1. Testing API Overview:")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    
    # Test Categories
    print("2. Testing Categories List:")
    response = requests.get(f"{BASE_URL}/categories/")
    print(f"Status: {response.status_code}")
    categories = response.json()
    print(f"Found {len(categories)} categories")
    for cat in categories[:2]:  # Show first 2
        print(f"  - {cat['name']}: {cat['products_count']} products")
    print()
    
    # Test Products
    print("3. Testing Products List:")
    response = requests.get(f"{BASE_URL}/products/")
    print(f"Status: {response.status_code}")
    products = response.json()
    print(f"Found {len(products)} products")
    for prod in products[:3]:  # Show first 3
        print(f"  - {prod['name']}: ${prod['price']} ({prod['category_name']})")
    print()
    
    # Test Product Filtering
    if categories:
        electronics_id = next((cat['id'] for cat in categories if cat['name'] == 'Electronics'), None)
        if electronics_id:
            print("4. Testing Product Filtering (Electronics only):")
            response = requests.get(f"{BASE_URL}/products/?category={electronics_id}")
            print(f"Status: {response.status_code}")
            electronics_products = response.json()
            print(f"Found {len(electronics_products)} electronics products")
            for prod in electronics_products:
                print(f"  - {prod['name']}: ${prod['price']}")
            print()
    
    # Test Statistics
    print("5. Testing Statistics:")
    response = requests.get(f"{BASE_URL}/stats/")
    print(f"Status: {response.status_code}")
    stats = response.json()
    print(f"Statistics: {json.dumps(stats, indent=2)}\n")
    
    # Test Creating a New Category
    print("6. Testing Category Creation:")
    new_category = {
        "name": "Test Category",
        "description": "A test category created via API"
    }
    response = requests.post(f"{BASE_URL}/categories/", json=new_category)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        created_category = response.json()
        print(f"Created category: {created_category['name']} (ID: {created_category['id']})")
        
        # Test Creating a Product in the new category
        print("\n7. Testing Product Creation:")
        new_product = {
            "name": "Test Product",
            "description": "A test product created via API",
            "price": "99.99",
            "category": created_category['id'],
            "is_active": True,
            "stock_quantity": 5
        }
        response = requests.post(f"{BASE_URL}/products/", json=new_product)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            created_product = response.json()
            print(f"Created product: {created_product['name']} (ID: {created_product['id']})")
    
    print("\n=== API Test Complete ===")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Django server is running at http://127.0.0.1:8000/")
    except Exception as e:
        print(f"Error: {e}")
