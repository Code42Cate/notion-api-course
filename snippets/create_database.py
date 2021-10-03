import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def create_database(parent_id: str):
    """Create a page (row) in a database

    Args:
        parent_id (str): ID of parent database
    """
    payload = {
        # This specifies where our new database gets created
        'parent': {'page_id': parent_id},
        'title': [
            {
                'type': 'text',
                'text': {
                    'content': 'Movie Database',
                }
            }
        ],
        'properties': {  # These are our columns
            # Read the documentation to see what values you can use, I can't explain it better:)
            # https://developers.notion.com/reference/create-a-database
            'Name': {
                'title': {}
            },
            'Category': {
                'select': {}
            },
            'Rating': {
                'number': {}
            },
        }
    }

    # The actual API request
    response = requests.post('https://api.notion.com/v1/databases/', json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

   # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse response as JSON and return
    data = response.json()
    return data


if __name__ == "__main__":

    # Id of your parent page. Looks like this: f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc
    # Use list_page.py to get the id of your page
    page_parent_id = 'TODO'

    # Create a new database
    data = create_database(page_parent_id)
    if data is not None:
        # print(json.dumps(data, indent=4))
        print('New database available here: {}'.format(data['url']))
