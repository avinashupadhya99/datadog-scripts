"""
For specific use cases only
Used to update the name and message of an anomaly alert
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest
import re

def get_alert_message(query):


configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(query="type:apm tag:\"env:dev\"")

    for monitor in response.monitors:
        service=''
        component_tag=False
        for i, tag in enumerate(monitor.tags):
            if monitor.tags[i].split(':')[0] == 'service':
                service = monitor.tags[i].split(':')[1]
            if tag == 'component:commission':
                component_tag=True
        if not component_tag:        
            monitor.tags.append('component:commission')

        message = get_alert_message(monitor.query).format(service)
        print(message)
        print(monitor.tags)
        # print(monitor)
        confirmation = input("Enter Y to update and N to skip - ")
        if 'Y' in confirmation:
            edit_body = MonitorUpdateRequest(
                message=message,
                tags=monitor.tags
            )

            edit_monitors_response = api_instance.update_monitor(monitor_id=int(monitor.id), body=edit_body)

            print(edit_monitors_response)
        else:
            print("Did not update monitor - https://app.datadoghq.com/monitors/{}/edit".format(monitor.id))

