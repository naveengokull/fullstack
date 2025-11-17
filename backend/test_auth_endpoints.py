import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration():
    print("Testing Registration...")
    url = f"{BASE_URL}/auth/register"
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("Registration successful!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login(username, password):
    print(f"\nTesting Login with username: {username}...")
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("Login successful!")
            print(f"Token received: {result['access_token'][:50]}...")
            return result['access_token']
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("  Authentication Endpoint Tester")
    print("=" * 50)
    print("\nMake sure the backend server is running on http://localhost:8000")
    print()
    
    if test_registration():
        token = test_login("testuser", "test123")
        if token:
            print("\nAll tests passed!")
        else:
            print("\nLogin test failed")
    else:
        print("\nRegistration test failed")
        print("\nTrying to login with existing user...")
        username = input("Enter username: ")
        password = input("Enter password: ")
        test_login(username, password)

