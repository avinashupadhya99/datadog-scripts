"""
Get all monitor details returns "OK" response
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType
import csv
import re

insensitive_hotfix = re.compile(re.escape('Dev'), re.IGNORECASE)
header = ['Monitor Name', 'Metric', 'Critical Threshold', 'Warning Threshold', 'Monitor Link', 'Monitor Edit Link']

with open('apm-monitors.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(query="type:apm tag:(\"env:pc-dev\" AND \"component:manufacturing\")")

    for monitor in response.monitors:
        # Since the search monitor API does not provide the message of the monitor, we need to call the get monitor API for each monitor
        monitor_response = api_instance.get_monitor(
            monitor_id=int(monitor.id),
        )
        for i, tag in enumerate(monitor.tags):
            monitor.tags[i] = str(insensitive_hotfix.sub('prod', tag))
        create_body = Monitor(
            name=str(insensitive_hotfix.sub('Prod', monitor.name)),
            type=MonitorType('query alert'),
            query=str(insensitive_hotfix.sub('prod', monitor.query)),
            message=str(insensitive_hotfix.sub('Prod', monitor_response.message)).replace('@avinashupadhya99@gmail.com', '@avinashupadhya12@gmail.com @avinash@defhacks.co'),
            tags=monitor.tags
        )

        create_monitors_response = api_instance.create_monitor(body=create_body)

        print(create_monitors_response)
        row = [create_monitors_response['name'], '', '', '', 'https://app.datadoghq.com/monitors/'+str(create_monitors_response['id']), 'https://app.datadoghq.com/monitors/'+str(create_monitors_response['id'])+'/edit']
        with open('apm-monitors.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    print(response.monitors)