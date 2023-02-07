import requests
import os
from dotenv import load_dotenv
import json
from datetime import date, datetime, timedelta
from operator import itemgetter

load_dotenv('//home/ni_whale/Documents/projects/Python/storage.env')


def get_previous_month():
    dt = date.today()
    first_day_of_the_current_month = (datetime.combine(dt, datetime.min.time())).replace(day=1)  # get the first
    # day of the month + reset time to 00:00:00
    last_day_of_the_previous_month = first_day_of_the_current_month - timedelta(days=1)
    first_day_of_the_previous_month = (last_day_of_the_previous_month.replace(day=1)).isoformat()  # getting the
    # last day of the previous month and replacing it with the first one + converting it to the ISO format
    previous_month = [first_day_of_the_previous_month,
                      last_day_of_the_previous_month.replace(hour=23, minute=59, second=59).isoformat()]
    return previous_month  # returns [1st day of the month, last day of the month] in format yyyy-mm-ddThh:mm:ss


# def write_to_file_first_quety(todoist_data):
#     with open('date.json', 'w') as f:
#         for key, value in todoist_data.items():
#             if key == "items":
#                 json.dump(value, f, ensure_ascii=False, indent=4)
#                 date_for_the_second_query = list(map(itemgetter('completed_at'), value[-1::]))
#                 print(f'The last task from the 1st query: {date_for_the_second_query}')
#     return date_for_the_second_query



def request_params():
    # TODO: Change it to have a possibility to call the func with different parameters for use it in the second request to API
    date_range = get_previous_month()
    params = {
        'since': date_range[0],
        'until': date_range[1],
        'limit': 200
    }
    return params


class TodoistApi:
    def __init__(self):
        self.TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
        self.TODOIST_API_URL = "https://api.todoist.com/sync/v9/completed/get_all"
        # self.TODOIST_API_URL = "https://api.todoist.com/sync/v9/sync"
        self.headers = {'Authorization': f'Bearer {self.TODOIST_API_TOKEN}'}
        self.tasks = []

    def tasks_collection(self, todoist_data, request_iteration):  # In general, I need only 2 iterations for getting
        # information in API. For the second iteration, I don't need to get the date of the last task, so I'm limiting
        # the return of this value
        for key, value in todoist_data.items():
            if key == "items":
                self.tasks.append(value)
                if request_iteration == 0:
                    date_for_the_second_query = list(map(itemgetter('completed_at'), value[-1::]))
                    print(f'The last task from the 1st query: {date_for_the_second_query[0]}')
                    return date_for_the_second_query[0]

                # print(f"tasks = {tasks[0]}")

    def todoist_data_collector(self):
        try:
            response = requests.get(self.TODOIST_API_URL, params=request_params(), headers=self.headers)
            response.raise_for_status()
            todoist_data = response.json()
            print(self.tasks_collection(todoist_data, 0))
            print(get_previous_month())
            # print(todoist_data)
        except Exception as error:
            print(error)

# last_item = list(todoist_data['items'])[-1::]
# # print(last_item)
#
# for date in last_item:
#     the_last_date = date['completed_at']


# params = {
#     'since': '2022-12-1T00:00:00',
#     'until': '2022-12-07T18:48:36.000000Z',
#     'limit': 200
# }

# params = {
#     'sync_token': "*",
#     'resource_types': '["completed/get_all "]'
# }
