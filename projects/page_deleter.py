import requests
import time

def delete_page(api_key, project_id, page_id):
    """ Delete a specific page by page ID within a project. """
    url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/pages/{page_id}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Deleted page with ID {page_id} successfully.")
    elif response.status_code == 429:
        print(f"Failed to delete page with ID {page_id} due to rate limits. Retrying...")
        time.sleep(10)  # Adjust the sleep time if necessary
        delete_page(api_key, project_id, page_id)  # Retry deleting the same page
    else:
        print(f"Failed to delete page with ID {page_id}: {response.status_code}, {response.text}")

def delete_pages_containing_string(api_key, project_id, search_string):
    """ Delete all pages that contain a specified string in their page URL. """
    page_ids = list_pages(api_key, project_id)  # This should ideally return page details, not just IDs
    for page in page_ids:
        # Assuming the function now returns detailed data for each page
        if search_string.lower() in page['page_url'].lower():
            delete_page(api_key, project_id, page['id'])
            time.sleep(1)  # Sleep to respect rate limits

def list_pages(api_key, project_id):
    """ Fetch all pages for a given project ID and return detailed information across all pages. """
    page_number = 1
    all_pages = []
    while True:
        url = f"https://app.customgpt.ai/api/v1/projects/{project_id}/pages?page={page_number}&duration=90&order=desc"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {api_key}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            pages = data['data']['pages']['data']
            all_pages.extend(pages)  # Now stores the entire page data
            # Check if there's a next page
            if data['data']['pages']['next_page_url'] is None:
                break
            else:
                page_number += 1
        else:
            print(f"Failed to list pages: {response.status_code}, {response.text}")
            break
    return all_pages

def main():
    api_key = input("Input your API key here: ")
    project_id = input("Enter the project ID: ")
    search_string = input("Delete all pages containing the following string: ")
    delete_pages_containing_string(api_key, project_id, search_string)

if __name__ == "__main__":
    main()
