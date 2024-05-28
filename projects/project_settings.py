import requests
import json

def update_settings():
    # Prompt user for their API key and project ID
    api_key = input("Enter your API key: ")
    project_id = input("Enter your project ID: ")

    # Set the API endpoint for the project settings
    url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/settings"

    # Set the headers with your API key
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    # Fetch and display current settings
    print("Fetching current project settings...")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Current Settings:", response.json())
    else:
        print("Failed to fetch settings:", response.text)
        return

    # Ask user what settings they want to update
    updates = {}
    while True:
        key = input("Enter the setting key to update (or type 'done' to finish): ")
        if key.lower() == 'done':
            break
        if key:
            value = input(f"Enter new value for {key}: ")
            if key == "example_questions":
                updates[key] = value.split(",")  # Assume input is comma-separated
            else:
                updates[key] = value

    if not updates:
        print("No updates made.")
        return

    # Convert the updates dictionary to JSON format
    data = json.dumps(updates)

    # Set additional headers for JSON content-type
    update_headers = headers.copy()
    update_headers["content-type"] = "application/json"

    # Update the project settings
    print("Updating project settings...")
    update_response = requests.post(url, headers=update_headers, data=data)
    if update_response.status_code == 200:
        print("Update successful:", update_response.json())
    else:
        print("Failed to update settings:", update_response.text)

# Run the update function
update_settings()
