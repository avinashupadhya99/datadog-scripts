"""
Script to update the average latency monitor from sum(trace.servlet.request.duration)/sum(trace.servlet.request.hits)
to avg(trace.servlet.request)
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest
import re

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(query="type:(apm OR trace-analytics) tag:(\"env:pc-dev\" AND \"component:manufacturing\") metric:\"trace.servlet.request.duration\"")

    for monitor in response.monitors:
        service=''
        for i, tag in enumerate(monitor.tags):
            if monitor.tags[i].split(':')[0] == 'service':
                service=tag
        aggregation_time = re.findall(r'\(.*?\)', monitor.query)[0]
        aggregation_by_reg = re.findall(r'by \{.*?\}', monitor.query)
        aggregation_by = aggregation_by_reg[0] if len(aggregation_by_reg) > 0 else ''
        threshold = re.findall(r'> [0-9]*.[0-9]*$', monitor.query)[0]
        query="avg{0}:avg:trace.servlet.request{{env:dev,{1}}} {2} {3}".format(aggregation_time, service, aggregation_by, threshold)
        edit_body = MonitorUpdateRequest(
            query=query,
        )
        print(query)

        edit_monitors_response = api_instance.update_monitor(monitor_id=int(monitor.id), body=edit_body)

        print(edit_monitors_response)
