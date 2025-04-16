import requests
import time

# Replace with your FastAPI server URL
API_URL = "http://localhost:8000/proxy/"
ADMIN_URL = "http://localhost:8000/admin/"

# Example: Token generation via Admin route
def create_token(tier="free", rate_limit=60):
    response = requests.post(f"{ADMIN_URL}token/", json={"tier": tier, "rate_limit": rate_limit})
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print("Error creating token:", response.json())
        return None

# Test the /proxy/ endpoint with a token
def test_proxy(token):
    headers = {"Authorization": token}
    data = {
        "messages": [
            {"role": "user", "content": "What is AI?"}
        ]
    }
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        print("Response from LLM:", response.json())
    else:
        print("Error:", response.status_code, response.json())

# Simulate a client request
if __name__ == "__main__":
    # Create a token first
    token = create_token(tier="free", rate_limit=5)
    if token:
        print(f"Generated Token: {token}")

        # Test the /proxy/ endpoint
        test_proxy(token)

        # Simulate multiple requests to test rate limiting
        print("\nTesting rate limiting...")
        for _ in range(7):  # Attempt 7 requests (to test rate limiting)
            test_proxy(token)
            time.sleep(1)  # Wait 1 second between requests