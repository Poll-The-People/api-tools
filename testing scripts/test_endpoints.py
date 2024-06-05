import pytest
import requests

# Constants for API
BASE_URL = "https://app.customgpt.ai/api/v1/projects"
API_TOKEN = "" #Input your API token here
project = "" #Input a projectID
session = "" #Input a sessionID


# Headers template
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Tests for GET endpoint
def test_get_project_details():
    project_id = project  # Can Replace with your actual project ID
    response = requests.get(f"{BASE_URL}/{project_id}?width=100%25&height=auto", headers=headers)
    assert response.status_code == 200
    assert "data" in response.json(), "Response should contain 'data' key"
    assert response.json()['status'] == 'success', "API call did not succeed"

# Tests for POST endpoint to create conversations
def test_create_conversation():
    project_id = project  # Can Replace with your actual project ID
    payload = {"name": "test_conversation"}
    response = requests.post(f"{BASE_URL}/{project_id}/conversations", json=payload, headers=headers)
    session = response.json()['data']['session_id']
    assert response.status_code == 201
    assert "id" in response.json()['data'], "Response should contain 'id' of the conversation"

# Tests for POST endpoint to send messages
def test_send_message():
    project_id = project
    session_id = session
    payload = {"response_source": "default", "prompt": "hello"}
    response = requests.post(f"{BASE_URL}/{project_id}/conversations/{session_id}/messages?stream=false&lang=en", json=payload, headers=headers)
    assert response.status_code == 200, f"Failed with status {response.status_code}: {response.json()}"
    assert "data" in response.json(), "Response should contain 'data' key"
    assert "id" in response.json()['data'], "Response should contain 'id' in 'data'"
    assert response.json()['status'] == 'success', "API call did not succeed"

# Running the tests
if __name__ == "__main__":
    pytest.main()
