import requests

def fetch_all_projects(base_url, api_key):
    all_projects = []
    page = 1
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    while True:
        url = f"{base_url}?page={page}&order=desc&orderBy=id&width=100%25&height=auto"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch data:", response.text)
            break
        
        data = response.json()['data']
        projects = data['data']
        if not projects:
            break  # Exit the loop if no projects are found on the current page

        for project in projects:
            project_info = {'id': project['id'], 'project_name': project['project_name']}
            all_projects.append(project_info)

        if data['next_page_url'] is None:
            break  # Exit the loop if there is no next page

        page += 1  # Increment to fetch the next page

    return all_projects

# Ask the user for the API key
api_key = input("Please enter your API key: ")

# URL setup
url = "https://app.customgpt.ai/api/v1/projects"

# Fetch all projects
projects = fetch_all_projects(url, api_key)
print(projects)