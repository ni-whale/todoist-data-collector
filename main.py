import requests
import os
from dotenv import load_dotenv
import json


load_dotenv('//home/ni_whale/Documents/projects/Python/storage.env')

TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
# TODOIST_API_URL = "https://api.todoist.com/sync/v9/sync"
TODOIST_API_URL = "https://api.todoist.com/sync/v9/completed/get_all"

headers = {'Authorization': f'Bearer {TODOIST_API_TOKEN}'}
# params = {
#     'sync_token': "*",
#     'resource_types': '["completed/get_all "]'
# }
# params = {
#     'since': '2022-12-1T00:00:00',
#     'until': '2022-12-31T23:59:59',
#     'limit': 200
# }
params = {
    'since': '2022-12-1T00:00:00',
    'until': '2022-12-07T18:48:36.000000Z',
    'limit': 200
}


try:
    response = requests.get(TODOIST_API_URL, params=params, headers=headers)
    response.raise_for_status()
    todoist_data = response.json()
    # print(todoist_data)
except Exception as error:
    print(error)

with open('date.json', 'w') as f:
    json.dump(todoist_data, f, ensure_ascii=False, indent=4)

# last_item = list(todoist_data['items'])[-1::]
# # print(last_item)
#
# for date in last_item:
#     the_last_date = date['completed_at']

