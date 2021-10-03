import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def query_sort(notion_id: str):

    # You can add have multiple sort criteria in series
    # More information about sorts: https://developers.notion.com/reference/post-database-query#post-database-query-sort
    payload = {
        'sorts': [{
            # Column name in Notion, this example works with the database from the recurring_tasks project
            'property': 'Fact',
            'timestamp': 'created_time',  # Or last_edited_time
            'direction': 'descending'  # Or descending
        }]
    }

    # The actual API request
    response = requests.post('https://api.notion.com/v1/databases/{}/query'.format(notion_id), json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

    # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse the response as JSON
    data = response.json()

    # If you want to see the complete response, uncomment the following line
    # print(json.dumps(data, indent=4))

    return data['results']


if __name__ == "__main__":

    # ID of the notion row/page
    # You can get the ID by listing all databases first (list_databases.py)
    # You can not copy the id from the app!
    # I suggest using the same database as in the recurring_tasks project
    database_id = 'TODO'

    # Call function to query the database
    rows = query_sort(database_id)

    # Something failed:(
    if rows is None:
        exit(1)

    for row in rows:
        # Find the title row
        title = 'Untitled'
        # Iterate over all columns and find the title column
        for property_key in row['properties']:
            property = row['properties'][property_key]
            if property['type'] == 'title':  # If we find the title column
                # Join all title parts together and ignore the formatting
                title = ''.join([t['plain_text'] for t in property['title']])

        # Print id and title
        print(row['id'], title)

        # If you want to see the complete row, uncomment the following line
        # print(json.dumps(row, indent=4))
