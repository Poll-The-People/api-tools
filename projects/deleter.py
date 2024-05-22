import requests
import time

def get_all_projects(api_key):
    """ Fetch all projects with pagination and return their IDs. """
    api_endpoint = 'https://app.customgpt.ai/api/v1/projects'
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    project_ids = []
    page = 1
    while True:
        response = requests.get(api_endpoint, headers=headers, params={"page": page})
        if response.status_code == 200:
            data = response.json()
            projects = data['data']['data']
            if projects:
                project_ids.extend([project['id'] for project in projects])
                page += 1  # move to the next page if the current page is not empty
                if not data['data']['next_page_url']:  # check if there is no next page
                    break
            else:
                break
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break
    return project_ids


def delete_selected_projects(api_key, exclude_ids):
    """ Delete all projects except those with IDs listed in exclude_ids. """
    project_ids = get_all_projects(api_key)
    api_endpoint = 'https://app.customgpt.ai/api/v1/projects/'
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    for project_id in project_ids:
        if project_id not in exclude_ids:
            response = requests.delete(f"{api_endpoint}{project_id}", headers=headers)
            time.sleep(1)
            # Sleep for 1 second between each deletion. Adjust as needed for subscription tier.
            #Customer Tier Rate Limits:
            #Basic: 60 per minute
            #Standard: 90 per minute
            #Premium: 120 per minute
            if response.status_code == 200:
                print(f"Project ID {project_id} deleted successfully.")
            else:
                print(f"Failed to delete project ID {project_id}: {response.text}")
        else:
            print(f"Skipping deletion for project ID {project_id} as it is in the exclude list.")

def main(api_key):
    # IDs to exclude from deletion
    exclude_ids = [] #Add the project IDs you want to keep, separated by commas
    delete_selected_projects(api_key, exclude_ids)

if __name__ == "__main__":
    api_key = input("Enter your API Key:")
    main(api_key)