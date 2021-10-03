import requests
import json
import os
import time
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# TODO: Make sure that you have a UNSPLASH_ACCESS_KEY environment variable set
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY', '')
# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')

# This is the image that we use when the Unsplash API does not find a suitable image
DEFAULT_URL = 'https://cataas.com/cat/says/hello%20world!.png'

COLUMN_NAME = 'Category'  # Your column name

# This is where we keep the category of each page
# We use this to see if the category of a page has changed
page_id_category_map = {}


def get_rows(database_id: str):
    has_more = True
    rows = []
    next_cursor = None

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
        response = requests.post('https://api.notion.com/v1/databases/{}/query'.format(database_id), params, headers={
            'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

        # If the request was not successful, we print the error and return the row array
        if not response.ok:
            print('Error:', response.status_code)
            print('Error:', response.content)
            return rows

        # Parse the response as JSON
        data = response.json()
        # Extract has_more and next_cursor attributes
        has_more = data['has_more']
        next_cursor = data['next_cursor']

        # Extend our row array with the new results
        rows.extend(data['results'])

        # If you want to see the complete response, uncomment the following line
        # print(json.dumps(data, indent=4))

    return rows


def get_unsplash_url(topic: str):

    # Add topic to query and only return 1 image
    params = {'query': topic, 'per_page': 1}
    # Authorize the request
    headers = {
        'Authorization': 'Client-ID {}'.format(UNSPLASH_ACCESS_KEY)}

    r = requests.get(
        'https://api.unsplash.com/search/photos/', params=params, headers=headers)

    # Request failed, return default url
    if not r.ok:
        return DEFAULT_URL

    data = r.json()
    # No results, return default url
    if len(data['results']) == 0:
        return DEFAULT_URL

    # Return 'regular' image url of first (and only) result
    return data['results'][0]['urls']['regular']


def map_page_to_category(database_id: str):
    rows = get_rows(database_id)
    for row in rows:
        # If you change the column type, you need to update this line
        select_value = row['properties'][COLUMN_NAME]['select']['name']
        page_id_category_map[row['id']] = select_value


def get_new_rows(database_id: str):
    rows = get_rows(database_id)
    new_rows = []
    # Iterate over all rows
    for row in rows:
        page_id = row['id']
        # If you change the column type, you need to update this line
        value = row['properties'][COLUMN_NAME]['select']['name']
        # Check if the page is completely new
        is_new = page_id not in page_id_category_map
        # If the page is not new, check if the category has changed
        is_edited = not is_new and page_id_category_map[page_id] != value
        # If it changed or is completely new, add it to our new_rows array
        if is_new or is_edited:
            new_rows.append(row)
    # Return all rows that are new or where the Category column changed
    return new_rows


def update_cover(page_id: str, cover_url: str):
    # Payload for the API request
    payload = {
        'cover': {
            'type': 'external',
            'external': {
                    'url': cover_url
            },
        },
    }
    # The actual API request
    # Read more about updating pages: https://developers.notion.com/reference/patch-page
    response = requests.patch('https://api.notion.com/v1/pages/{}'.format(page_id), json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

    # Something failed:(
    # You could try to handle the error better
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)


if __name__ == '__main__':
    # Id of your Database. Looks like this: f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc
    # Use list_databases.py to get the id of your database
    # Your database should look like this: https://safelyy.notion.site/f1f5071d8d2a47aa9ddc02b8aad3f6bc
    # You can duplicate it, create one manually or try to create one with the API. See create_database.py for an example!

    database_id = 'TODO'

    # The initial mapping of page_id to category, we don't update the cover here
    map_page_to_category(database_id)

    # Do the thing every 5 seconds!
    while(True):
        time.sleep(5)
        # Get all rows where the category column has changed
        changed_rows = get_new_rows(database_id)
        # Iterate over new rows
        for row in changed_rows:
            # Get page_id
            page_id = row['id']
            # Get value of select
            # If you change the column type, you need to update this line
            category = row['properties'][COLUMN_NAME]['select']['name']
            # Update the page_id_category_map
            page_id_category_map[page_id] = category
            # Get new cover image with the category
            cover_image = get_unsplash_url(category)
            # Update cover of page
            update_cover(page_id, cover_image)
