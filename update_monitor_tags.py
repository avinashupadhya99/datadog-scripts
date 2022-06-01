"""
Script to update the tags of monitors
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest


configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(per_page=160, query="tag:(\"oldkey:oldvalue\")")
    count=0
    for monitor in response.monitors:
        for i, tag in enumerate(monitor.tags):
            if tag=="oldkey:oldvalue":
                monitor.tags[i]="newkey:newvalue"
        edit_body = MonitorUpdateRequest(
            tags=monitor.tags
        )

        edit_monitors_response = api_instance.update_monitor(monitor_id=int(monitor.id), body=edit_body)
        count+=1
        print(edit_monitors_response)

    # print(response.metadata)
    print("Updated monitor count - "+str(count))