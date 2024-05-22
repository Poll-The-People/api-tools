import requests
import time

# Fetch all conversations for a given project ID
def list_conversations(api_key, project_id):
    """ Fetch all conversations for a given project ID and return their session IDs. """
    url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/conversations"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            # Access the nested 'data' key inside the outer 'data' dictionary
            conversations = data['data']['data']  # First 'data' is for the response, second 'data' is the list
            return [conv['session_id'] for conv in conversations]
        except KeyError:
            print("KeyError: One of the expected keys is not in the response.")
            return []
        except TypeError:
            print("TypeError: There was a type issue with the response processing, check data structure.")
            return []
    else:
        print(f"Failed to list conversations: {response.status_code}, {response.text}")
        return []

# Delete a single conversation
def delete_conversation(api_key, project_id, session_id):
    """ Delete a specific conversation by session ID within a project. """
    url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/conversations/{session_id}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Deleted conversation with session ID {session_id} successfully.")
    elif response.status_code == 429:
        print(f"Failed to delete conversation with ID {session_id} due to rate limits. Retrying...")
        time.sleep(10)  # Adjust the sleep time if necessary
        delete_conversation(api_key, project_id, session_id)  # Retry deleting the same page
    else:
        print(f"Failed to delete conversation with session ID {session_id}: {response.text}")

# Loop and delete all conversations
def delete_all_conversations(api_key, project_id):
    """ Delete all conversations for a given project ID. """
    session_ids = list_conversations(api_key, project_id)
    for session_id in session_ids:
        delete_conversation(api_key, project_id, session_id)
        time.sleep(1)  # Sleep for 1 second between each deletion. Adjust as needed for subscription tier.
        #Customer Tier Rate Limits:
        #Basic: 60 per minute
        #Standard: 90 per minute
        #Premium: 120 per minute


def main():
    api_key = input("Enter your API Key:")  # Prompt user for the API key
    project_id = input("Enter the project ID: ")  # Prompt user for the project ID
    delete_all_conversations(api_key, project_id)

if __name__ == "__main__":
    main()
