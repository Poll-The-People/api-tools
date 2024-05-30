import requests

def fetch_project_stats(api_key, project_id):
    url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/stats"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    return response.text

def main():
    api_key = input("Please enter your API key: ")
    project_id = input("Please enter your project ID: ")
    result = fetch_project_stats(api_key, project_id)
    print("Response from API:")
    print(result)

if __name__ == "__main__":
    main()
