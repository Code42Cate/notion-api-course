import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def create_row(parent_id: str):
    """Create a page (row) in a database

    Args:
        parent_id (str): ID of parent database
    """
    # The payload is for the same database format as in recurring_task. Make sure that you have the same columns, otherwise this will fail
    payload = {
        # This specifies in which database our row gets added
        'parent': {'database_id': parent_id},
        'properties': {  # These are our columns
            # Read the documentation to see what values you can use, I can't explain it better:)
            # https://developers.notion.com/reference/page#property-value-object
            'Fact': {
                'title': [
                    {
                        'text': {'content': 'Test123'}
                    }
                ]
            },
            'Category': {
                'select': {'name': 'test-category'}
            },
            'Hits': {
                'number': 42
            },
            'ID': {
                'number': 42
            }
        }
    }

    # The actual API request
    response = requests.post('https://api.notion.com/v1/pages/', json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

   # If the request was not successful, we print the error and return
    if response.status_code != 200:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse response as JSON and return
    data = response.json()
    return data


def create_page(parent_id: str):
    """Create a new page

    Args:
        parent_id (str): ID of parent page
    """
    payload = {
        # This specifies to which parent page our new page gets added
        'parent': {'page_id': parent_id},
        'icon': {
            'type': 'emoji',
            'emoji': '🎉'
        },
        'cover': {
            'type': 'external',
            'external': {
                    'url': 'https://cataas.com/cat/says/hello%20world!.png'
            },
        },
        'properties': {  # These are our columns
            # The only valid property is title when creating a normal page
            'title': {
                'title': [
                    {
                        'text': {'content': 'Test123'}
                    },
                ]
            },
        }
    }

    # The actual API request
    response = requests.post('https://api.notion.com/v1/pages/', json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

   # If the request was not successful, we print the error and return
    if response.status_code != 200:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse response as JSON and return
    data = response.json()
    return data


if __name__ == "__main__":

    # Id of your Database. Looks like this: f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc
    # Use list_databases.py to get the id of your database
    # Your database should look like this: https://safelyy.notion.site/f1f5071d8d2a47aa9ddc02b8aad3f6bc
    # You can duplicate it, create one manually or try to create one with the API. See create_database.py for an example!
    database_id = 'TODO'

    # Create a row in database
    data = create_row(database_id)
    if data is not None:
        # print(json.dumps(data, indent=4))
        print('New row available here: {}'.format(data['url']))

    page_parent_id = 'TODO'

    # Create a normal page

    page_data = create_page(page_parent_id)
    if page_data is not None:
        # print(json.dumps(data, indent=4))
        print('New page available here: {}'.format(page_data['url']))
