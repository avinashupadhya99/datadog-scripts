"""
Script to add/remove a word from the title of a monitor.
For specific use cases only.
Add word -
ABC - XYZ - service - metric   =>    ABC - XYZ - APM - service - metric
Remove word -
ABC - XYZ - APM - service - metric    =>      ABC - XYZ - service - metric
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
import os

def add_word_to_title(monitors):
    for monitor in monitors:
        new_name = ''
        if "APM" in monitor.name: 
            continue
        for idx, key in enumerate(monitor.name.split(' - ')):
            if idx == 3: # Final word
                new_name += key
                break
            if idx == 2:
                new_name += 'APM' + ' - '
            new_name += key + ' - '
        print(new_name)
        update_response = api_instance.update_monitor(monitor.id, {'name': new_name})
        print(update_response)

def remove_word_from_title(monitors):
    for monitor in monitors:
        new_name = ''
        if "APM" not in monitor.name: 
            continue
        for idx, key in enumerate(monitor.name.split(' - ')):
            if idx == 4: # Final word
                new_name += key
                break
            if key == "APM":
                continue
            new_name += key + ' - '
        print(new_name)
        update_response = api_instance.update_monitor(monitor.id, {'name': new_name})
        print(update_response)

action = os.getenv('MON_TITLE_ACTION', 'remove')

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(query="type:metric tag:(\"env:sit\" AND \"component:abc\")")

    if action == "add":
        add_word_to_title(response['monitors'])
    elif action == "remove":
        remove_word_from_title(response['monitors'])

    # print(response)

