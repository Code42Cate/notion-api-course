import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def delete_block(notion_id: str):

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

    # TODO: Replace this notion_id with the ID of the block that you want to delete
    # You can use create_block.py to create a block and get its ID
    # And then delete the block again
    block_id = 'TODO'

    # Call function to delete page
    data = delete_block(block_id)
    print(json.dumps(data, indent=4))
