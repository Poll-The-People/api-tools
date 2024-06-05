import requests
import json
from sseclient import SSEClient

def main():
    # Setup API URL and API Token
    api_endpoint = 'https://app.customgpt.ai/api/v1/'
    api_token = input('Please enter your API token: ')
    project_id = input('Please enter the project ID: ')

    headers = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + api_token,
        'Accept': 'text/event-stream'
    }

    # Fetch project info
    url = f"{api_endpoint}projects/{project_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_token}", "accept": "application/json"})
    print("Project Information Response:")
    print(response.text)
    
    # Create a conversation
    name = input("Enter a name for the conversation: ")
    payload = json.dumps({
        "name": name
    })

    url = f"{api_endpoint}projects/{project_id}/conversations"
    response = requests.post(url, headers=headers, data=payload)
    print("Conversation Creation Response:")
    print(response.text)
    conversation_data = json.loads(response.text)["data"]
    session_id = conversation_data["session_id"]

    # Engage in a continuous conversation
    while True:
        prompt = input("Enter your prompt (or type 'exit' to end): ")
        if prompt.lower() == 'exit':
            print("Exiting conversation.")
            break
        
        stream = 1
        payload = json.dumps({
            "prompt": prompt,
            "stream": stream
        })

        url = f"{api_endpoint}projects/{project_id}/conversations/{session_id}/messages"
        stream_response = requests.post(url, headers=headers, data=payload, stream=True)
        client = SSEClient(stream_response)
        print("Streaming Responses:")
        for event in client.events():
            print(event.data)
            if json.loads(event.data).get("status") == "finish":
                client.close()
                break

if __name__ == "__main__":
    main()
