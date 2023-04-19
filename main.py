from todoistapi import TodoistApi
from visualization import Charts

todoist_api = TodoistApi()
visual_data = Charts()

# todoist_api.todoist_api_call()
print(todoist_api.projects_get())
visual_data.test()