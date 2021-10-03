import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def update_page(notion_id: str):

    # This example uses the database from the recurring_tasks project.
    # Read more about updating pages: https://developers.notion.com/reference/patch-page
    # If you want to update blocks, not properties, take a look at update_block.py
    payload = {
        'properties': {
            'Fact': {
                'title': [
                    {
                        'text': {'content': 'Hehe, the funnest fun fact of all fun facts'}
                    }
                ]
            }
        }
    }

    # The actual API request
    response = requests.patch('https://api.notion.com/v1/pages/'+notion_id, json=payload, headers={
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

    # TODO: Replace this notion_id with the ID of the page (row) you want to update
    # You can use the recurring_task project to generate a new page
    # And then update the new page with this script
    page_id = 'TODO'

    # Call function to update page
    data = update_page(page_id)
    print(json.dumps(data, indent=4))
