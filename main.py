# from todoist_api_python.api import TodoistAPI
#
# api = TodoistAPI("")
#
# try:
#     projects = api.get_projects()
#     print(projects)
# except Exception as error:
#     print(error)

import requests
import os
from dotenv import load_dotenv

load_dotenv('//home/ni_whale/Documents/projects/Python/storage.env')

TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
TODOIST_API_URL = "https://api.todoist.com/sync/v9/sync"

headers = {'Authorization': f'Bearer {TODOIST_API_TOKEN}'}
params = {
    'sync_token': "*",
    'resource_types': '["projects"]'
}


try:
    response = requests.get(TODOIST_API_URL, params=params, headers=headers)
    response.raise_for_status()
    todoist_data = response.json()
    print(todoist_data)
except Exception as error:
    print(error)
