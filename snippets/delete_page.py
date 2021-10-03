import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def delete_page(notion_id: str):

    # The actual API request
    response = requests.delete('https://api.notion.com/v1/blocks/'+notion_id, headers={
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

    # TODO: Replace this notion_id with the ID of the page (row) that you want to delete
    # You can use the recurring_task project to generate a new page
    # And then delete the new page again with this script
    page_id = 'TODO'

    # Call function to delete page
    data = delete_page(page_id)
    print(json.dumps(data, indent=4))
