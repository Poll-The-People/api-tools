import requests
import time

def get_files(api_key, project_id):
    """ Fetch all files listed in the uploads section of the given project. """
    all_files = []
    url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/sources"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        all_files.extend(data['data']['uploads']['pages'])  # Correct path to fetch files
    else:
        print(f"Failed to list files: {response.status_code}, {response.text}")
    return all_files

def delete_file(api_key, project_id, file_id):
    """ Delete a specific page by page ID within a project. """
    url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/sources/{file_id}" 
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Deleted page with ID {file_id} successfully.")
    elif response.status_code == 429:
        print(f"Failed to delete page with ID {file_id} due to rate limits. Retrying...")
        time.sleep(10)  # Adjust the sleep time if necessary
        delete_file(api_key, project_id, file_id)  # Retry deleting the same page
    else:
        print(f"Failed to delete file with ID {file_id}: {response.status_code}, {response.text}")

def delete_files_containing_string(api_key, project_id, search_string):
    """ Delete all files that contain a specified string in their filename. """
    files = get_files(api_key, project_id)
    for file in files:
        if search_string.lower() in file['filename'].lower():
            delete_file(api_key, project_id, file['id'])
            time.sleep(1) # Sleep for 1 second between each deletion. Adjust as needed for subscription tier.
            #Customer Tier Rate Limits:
            #Basic: 60 per minute
            #Standard: 90 per minute
            #Premium: 120 per minute

def main():
    api_key = input('Enter your API key: ')
    project_id = input("Enter the project ID: ")
    search_string = input("Delete all pages containing the following string: ")
    delete_files_containing_string(api_key, project_id, search_string)

if __name__ == "__main__":
    main()
