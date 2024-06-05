import requests
import json
from sseclient import SSEClient
import re

def calculate_similarity(question, answer):
    # Normalize and split the strings to compare
    question_words = set(re.findall(r'\w+', question.lower()))
    answer_words = set(re.findall(r'\w+', answer.lower()))
    common_words = question_words.intersection(answer_words)
    return len(common_words), common_words

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
        questions_input = input("Enter your list of questions separated by a comma ',' (or type 'exit' to end): ")
        if questions_input.lower() == 'exit':
            print("Exiting conversation.")
            break
        
        questions = questions_input.split(',')
        for question in questions:
            question = question.strip()
            payload = json.dumps({
                "prompt": question,
                "stream": 1
            })

            url = f"{api_endpoint}projects/{project_id}/conversations/{session_id}/messages"
            stream_response = requests.post(url, headers=headers, data=payload, stream=True)
            client = SSEClient(stream_response)
            print(f"Question: {question}")
            answer = ""
            for event in client.events():
                data = json.loads(event.data)
                print(data.get("message", ""))
                answer += data.get("message", "")
                if data.get("status") == "finish":
                    client.close()
                    break
            
            similarity_score, common_words = calculate_similarity(question, answer)
            print(f"Answer: {answer}")
            print(f"Similarity score (count of common words): {similarity_score}")
            print(f"Common words: {common_words}")

if __name__ == "__main__":
    main()
