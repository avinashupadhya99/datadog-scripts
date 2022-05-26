"""
Script to swap words at 3rd and 4th places from the title of a monitor.
For specific use cases only.
Example -
ABC - XYZ - Region - service - metric   =>    ABC - XYZ - service - Region - metric
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest
import csv


configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(query="type:apm tag:(\"env:pc-dev\" AND \"component:manufacturing\")")

    for monitor in response.monitors:
        name_arr=monitor.name.split(' - ')
        name=''
        for i, nm in enumerate(name_arr):
            if i == 2:
                name += name_arr[i+1]
            elif i==3:
                name += name_arr[i-1]
            else:
                name += nm
            if i != 4:
                name += ' - '
        edit_body = MonitorUpdateRequest(
            name=name,
        )

        edit_monitors_response = api_instance.update_monitor(monitor_id=int(monitor.id), body=edit_body)

        print(edit_monitors_response)

    print(response.monitors)