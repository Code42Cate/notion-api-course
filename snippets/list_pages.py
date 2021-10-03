import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def list_pages():
    has_more = True
    pages = []
    next_cursor = None

    # This is the filter for the query, you can also use value: database if you want to get all databases instead!
    payload = {
        'filter': {
            'value': 'page',
            'property': 'object'
        }
    }

    # Notion uses "Pagination", which is a technique to split large amounts of data into smaller chunks.
    # Each requests has a has_more attribute which indicates if there are more pages to be fetched.
    # The next_cursor variable is the cursor for the next page.
    # More information about pagination: https://developers.notion.com/reference/pagination
    while has_more:

        # In the first iteration we don't have a cursor, so we don't pass it as a parameter
        if next_cursor is not None:
            params = {'start_cursor': next_cursor}
        else:
            params = {}

        # The actual API request
        response = requests.post('https://api.notion.com/v1/search', params, json=payload, headers={
            'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

        # If the request was not successful, we print the error and return the page array
        if not response.ok:
            print('Error:', response.status_code)
            print('Error:', response.content)
            return pages

        # Parse the response as JSON
        data = response.json()
        # Extract has_more and next_cursor attributes
        has_more = data['has_more']
        next_cursor = data['next_cursor']

        # Extend our user array with the new results
        pages.extend(data['results'])

        # If you want to see the complete response, uncomment the following line
        # print(json.dumps(data, indent=4))

    return pages


if __name__ == "__main__":

    # Call function to get pages
    pages = list_pages()

    # Pretty print
    # print(json.dumps(databases, indent=2))

    # Example iteration over page array
    for page in pages:
        print(page['url'], page['id'], page['object'])
