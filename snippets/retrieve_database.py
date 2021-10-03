import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def retrieve_database(notion_id: str):

    # The actual API request
    response = requests.get('https://api.notion.com/v1/databases/'+notion_id, headers={
                            'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

    # If the request was not successful, we print the error and return the user array
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)

    # Parse the response as JSON
    data = response.json()

    # If you want to see the complete response, uncomment the following line
    # print(json.dumps(data, indent=4))

    return data


if __name__ == "__main__":

    # Your database notion id, example format: 0428ef5b-c030-4b4f-b3c5-4bf0a0e370b3
    database_id = 'TODO'

    # Call function to get database
    database = retrieve_database(database_id)

    # Pretty print
    print(json.dumps(database, indent=4))
