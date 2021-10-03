import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def create_blocks(block_id: str):
    # This is just an example, take a look at the documentation to see what kind of blocks you can create
    # https://developers.notion.com/reference/block
    payload = {
        'children': [
            {

                'object': 'block',
                'type': 'heading_2',
                'heading_2': {
                    'text': [{'type': 'text', 'text': {'content': 'This is a Heading!'}}]
                }
            },
            {
                'object': 'block',

                'type': 'paragraph',
                'paragraph': {
                    'text': [{
                        'type': 'text',
                        'text': {
                            'content': 'Some simple',
                        }
                    },
                        {
                        'type': 'text',
                        'text': {
                            'content': ' bold text!',
                        },
                        'annotations': {
                            'bold': True
                        }
                    }],
                }
            },
            {
                'type': 'to_do',
                'to_do': {
                    'text': [{
                        'type': 'text',
                        'text': {
                            'content': 'Do this!',
                        }
                    }],
                    'checked': False,
                }
            },
            {
                'type': 'image',
                'image': {
                    'type': 'external',
                    'external': {
                        'url': 'https://images.unsplash.com/photo-1633074320366-365b5e382fb5'
                    }
                }
            }
        ]

    }

    # The actual API request
    response = requests.patch('https://api.notion.com/v1/blocks/{}/children'.format(block_id), json=payload, headers={
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

    # Id of your Block. Looks like this: f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc
    # A Page (or Database Row) is also a Block
    # Blocks get appendend to the end of a page
    block_id = 'TODO'

    # Create a row in database
    data = create_blocks(block_id)
    if data is not None:
        print(json.dumps(data, indent=4))
