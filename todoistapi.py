import requests
import os
from dotenv import load_dotenv
import json
from datetime import date, datetime, timedelta
from dateutil import parser
from operator import itemgetter
from todoist_api_python.api import TodoistAPI

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


def request_params(date_range):
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
        self.rest_api = TodoistAPI(self.TODOIST_API_TOKEN)

    def tasks_collection(self, todoist_data):
        # with open('date.json', 'w') as f:
        for key, value in todoist_data.items():
            if key == "items":
                self.tasks.append(value)
                date_of_the_last_task_from_the_query = list(map(itemgetter('completed_at'), value[-1::]))
                # print(f'The last task from the query: {date_of_the_last_task_from_the_query[0]}')
                return date_of_the_last_task_from_the_query[0]

    def request_get(self, params):
        response = requests.get(self.TODOIST_API_URL, params=params, headers=self.headers)
        response.raise_for_status()
        todoist_data = response.json()
        return todoist_data

    def todoist_api_call(self):
        get_to_the_end = False  # It will have a False while till we get tasks for the whole month
        getting_json_data = self.request_get(
            request_params(get_previous_month()))  # I'm making a first call to API and getting all tasks
        # with the limit of 200 items;
        try:
            while not get_to_the_end:
                until_date_for_the_next_query = (
                    parser.parse(self.tasks_collection(getting_json_data)).replace(hour=00, minute=00,
                                                                                   second=00).isoformat()).replace(
                    "+00:00", "")
                date_range_for_the_next_request = [get_previous_month()[0],
                                                   until_date_for_the_next_query]  # we are
                # getting the list of 'since' date from the previous month and 'until' from the date of the last task

                if until_date_for_the_next_query == get_previous_month()[0]:  # compare the date I got from the last
                    # task of the query and date of the 1st day of the previous month
                    print(f'Dates are identical = {True}')
                    get_to_the_end = True
                else:
                    print(f'Dates are identical = {False}')
                    getting_json_data = self.request_get(request_params(date_range_for_the_next_request))

            print(self.tasks)
            print(f'{len(self.tasks[0])}, {len(self.tasks[1])}')
        except Exception as error:
            print(error)

    def labels_get(self):
        try:
            labels = self.rest_api.get_shared_labels()
            print(labels)
        except Exception as error:
            print(error)

    def projects_get(self):
        try:
            projects = self.rest_api.get_projects()
            print(projects)
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
