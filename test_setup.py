import requests
import json
import os
from dotenv import load_dotenv
import sys
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')

if NOTION_TOKEN == '':
    print('Notion Token not found? Does your .env file exist with the token filled in?')
    sys.exit(1)

print('Seems like everything works! Lets start coding:D')
