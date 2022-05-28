"""
Script to update the alerting channels from monitors
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest


configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(per_page=130, query="tag:(\"env:ne-proddr\" AND \"component:apollone\")")
    count=0
    for monitor in response.monitors:
        monitor_response = api_instance.get_monitor(
            monitor_id=int(monitor.id),
        )
        edit_body = MonitorUpdateRequest(
            message=monitor_response.message.replace("@old-channel", "@new-channel"),
        )

        edit_monitors_response = api_instance.update_monitor(monitor_id=int(monitor.id), body=edit_body)
        count+=1
        print(edit_monitors_response)

    # print(response)
    print("Updated monitor count - "+str(count))