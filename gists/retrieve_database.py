

import requests
import json

# TODO: Insert your notion token here
NOTION_TOKEN = 'TODO'


def retrieve_database(notion_id: str):

    # The actual API request
    response = requests.get('https://api.notion.com/v1/databases/'+notion_id, headers={
                            'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

    # If the request was not successful, we print the error and return the user array
    if response.status_code != 200:
        print('Error:', response.status_code)
        print('Error:', response.content)

    # Parse the response as JSON
    data = response.json()

    return data
    # If you want to see the complete response, uncomment the following line
    # print(json.dumps(data, indent=4))


if __name__ == "__main__":

    # your database notion id, example format: 0428ef5b-c030-4b4f-b3c5-4bf0a0e370b3
    database_id = 'TODO'

    # call function to get database
    database = retrieve_database(database_id)

    # pretty print
    print(json.dumps(database, indent=2))
