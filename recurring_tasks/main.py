import requests
import os
from dotenv import load_dotenv
import json
import time
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def post_task(database_id: str):
    """
        Gets a fun fact and posts it to your database
    Args:
        database_id (str): id of your database
    """
    # Use our own function to get the data for our task
    fun_fact = get_fun_fact()

    if fun_fact is None:
        print('Could not get fun fact')
        return

    payload = {
        # This specifies in which database our row gets added
        'parent': {'database_id': database_id},
        'properties': {  # These are our columns
            # Read the documentation to see what values you can use, I can't explain it better:)
            # https://developers.notion.com/reference/page#property-value-object
            'Fact': {
                'title': [
                    {
                        'text': {'content': fun_fact['fact']}
                    }
                ]
            },
            'Category': {
                'select': {'name': fun_fact['cat']}
            },
            'Hits': {
                # We have to convert the string to an int because the fun-fact API returns strings for some reason
                'number': int(fun_fact['hits'])
            },
            'ID': {
                # We have to convert the string to an int because the fun-fact API returns strings for some reason
                'number': int(fun_fact['id'])
            }
        }
    }
    # For more information about this endpoint, visit the documentation: https://developers.notion.com/reference/post-page
    response = requests.post('https://api.notion.com/v1/pages/', json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

    # Request failed, don't try to parse and just return
    if not response.ok:
        print(response.status_code, response.content)
        return

    data = response.json()
    print(data['id'])
    print('New task available here: {}'.format(data['url']))

    # Uncomment the following line to see the complete response
    # print(json.dumps(data, indent=4))


def get_fun_fact():
    """Gets a fun-fact from an external API. 
    This is just a placeholder with a fun-fact API to get some external data.
    Check out https://github.com/public-apis/public-apis for more free & public APIs!
    """
    # Get the fun fact:)
    r = requests.get('https://asli-fun-fact-api.herokuapp.com/')
    # Request failed, don't try to parse and just return None
    if not r.ok:
        return None

    # Parse JSON
    json_data = r.json()

    # Uncomment the following line to see the complete response
    # print(json.dumps(json_data, indent=4))
    return json_data['data']


if __name__ == '__main__':
    # Id of your Database. Looks like this: f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc
    # Use list_databases.py to get the id of your database
    # Your database should look like this: https://safelyy.notion.site/f1f5071d8d2a47aa9ddc02b8aad3f6bc
    # You can duplicate it, create one manually or try to create one with the API. See create_database.py for an example!
    database_id = 'f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc'
    while True:
        post_task(database_id)
        time.sleep(5)
