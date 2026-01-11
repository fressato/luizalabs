import requests

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    # 1. Create User
    user_data = {
        "username": "11122233344",
        "nome": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "data_nascimento": "01-01-1990"
    }
    
    print(f"Attempting to create user with: {user_data}")
    try:
        resp = requests.post(f"{BASE_URL}/usuarios", json=user_data)
        if resp.status_code == 201:
            print("User created successfully!")
        elif resp.status_code == 400 and "CPF já cadastrado" in resp.text:
            print("User already exists, proceeding to login...")
        else:
            print(f"Failed to create user. Status: {resp.status_code}, Body: {resp.text}")
            return
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 2. Login (Get Token)
    # OAuth2PasswordRequestForm expects form-data, not JSON
    login_data = {
        "username": "11122233344",
        "password": "password123"
    }
    
    print(f"Attempting login with: {login_data}")
    resp = requests.post(f"{BASE_URL}/token", data=login_data) # Note: data= means form-encoded, json= means json
    
    if resp.status_code == 200:
        token_info = resp.json()
        print("Login successful!")
        print(f"Token: {token_info}")
    else:
        print(f"Login failed. Status: {resp.status_code}, Body: {resp.text}")
        
    # 3. Test Invalid Login (JSON) - what the user might be doing
    print("Testing INVALID login with JSON...")
    resp = requests.post(f"{BASE_URL}/token", json=login_data)
    print(f"Invalid JSON login status: {resp.status_code} (Expected 422 or similar)")

if __name__ == "__main__":
    test_flow()
