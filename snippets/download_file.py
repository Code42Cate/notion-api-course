import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def download_file(notion_id: str, property_name: str):

    # The actual API request
    response = requests.get('https://api.notion.com/v1/pages/'+notion_id, headers={
                            'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

    # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse the response as JSON
    data = response.json()

    # If the property does not exist we returns
    if property_name not in data['properties']:
        print('Error: {} is not a valid property name'.format(property_name))
        return

    # Get the property
    property = data['properties'][property_name]

    # If the property does not have the correct type we return
    if property['type'] != 'files':
        print('Error: {} does not have files as type'.format(property_name))
        return

    # Iterate over all files in the property
    for file in property['files']:
        print('Downloading {}'.format(file['name']))
        # Request the file from the URL where it is saved
        r = requests.get(file['file']['url'])
        # Save it with the same name as it has in notion
        with open(file['name'], 'wb') as f:
            f.write(r.content)

    # If you want to see the complete response, uncomment the following line
    # print(json.dumps(data, indent=4))


if __name__ == "__main__":

    # ID of the notion row/page
    # You can get the ID by querying the database first and extracting the ID for the row that you want
    row_notion_id = 'TODO'

    # The name of the column in your database. Same as in the app! You can also get the properties by retrieving the database (retrieve_database.py)
    property_name = 'TODO'

    # Call function to download file
    users = download_file(row_notion_id, property_name)

    # File(s) should now be saved in the same directory where you executed this script
