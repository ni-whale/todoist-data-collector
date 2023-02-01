import requests
import os
from dotenv import load_dotenv
import json
from datetime import date, datetime, timedelta

load_dotenv('//home/ni_whale/Documents/projects/Python/storage.env')


class TodoistApi:
    def __init__(self):
        self.TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
        self.TODOIST_API_URL = "https://api.todoist.com/sync/v9/completed/get_all"
        # self.TODOIST_API_URL = "https://api.todoist.com/sync/v9/sync"
        self.headers = {'Authorization': f'Bearer {self.TODOIST_API_TOKEN}'}

    def get_previous_month(self):
        dt = date.today()
        first_day_of_the_current_month = (datetime.combine(dt, datetime.min.time())).replace(day=1)  # get the first
        # day of the month + reset time to 00:00:00
        last_day_of_the_previous_month = first_day_of_the_current_month - timedelta(days=1)
        first_day_of_the_previous_month = (last_day_of_the_previous_month.replace(day=1)).isoformat()  # getting the
        # last day of the previous month and replacing it with the first one + converting it to the ISO format
        previous_month = [first_day_of_the_previous_month, last_day_of_the_previous_month.replace(hour=23, minute=59, second=59).isoformat()]
        return previous_month[1]

    def todoist_auth(self, date_since, date_until):
        params = {
            'since': date_since,
            'until': date_until,
            'limit': 200
        }
        # params = {
        #     'since': '2022-12-1T00:00:00',
        #     'until': '2022-12-07T18:48:36.000000Z',
        #     'limit': 200
        # }

        # params = {
        #     'sync_token': "*",
        #     'resource_types': '["completed/get_all "]'
        # }
        ...

# try:
#     response = requests.get(TODOIST_API_URL, params=params, headers=headers)
#     response.raise_for_status()
#     todoist_data = response.json()
#     # print(todoist_data)
# except Exception as error:
#     print(error)
#
# with open('date.json', 'w') as f:
#     json.dump(todoist_data, f, ensure_ascii=False, indent=4)

# last_item = list(todoist_data['items'])[-1::]
# # print(last_item)
#
# for date in last_item:
#     the_last_date = date['completed_at']
