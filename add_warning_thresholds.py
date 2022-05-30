"""
Script to add warning thresholds from one environment to another
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_options import MonitorOptions
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest
import re

insensitive_prod = re.compile(re.escape('Prod'), re.IGNORECASE)
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(query="tag:(\"env:pc-prod\")")
    count=0
    missing=[]
    for monitor in response.monitors:
        monitor_response = api_instance.list_monitors(
            name=str(insensitive_prod.sub('Dev', monitor.name)),
        )
        if len(monitor_response)>0:
            count+=1
            edit_body = MonitorUpdateRequest(
                options = MonitorOptions(
                    thresholds = MonitorThresholds(
                        critical = monitor_response[0].options.thresholds.critical,
                        warning = monitor_response[0].options.thresholds.warning
                    )
                )
            )

            edit_monitors_response = api_instance.update_monitor(monitor_id=int(monitor.id), body=edit_body)

            print(edit_monitors_response)
        else:
            print(str(insensitive_prod.sub('Dev', monitor.name)))
            missing.append('https://app.datadoghq.com/monitors/'+str(monitor['id']))
    # print(response.monitors)
    print(count)
    print(missing)