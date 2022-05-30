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

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.search_monitors(query="type:anomaly tag:\"env:dev\"")

    for monitor in response.monitors:
        service=''
        for i, tag in enumerate(monitor.tags):
            if monitor.tags[i].split(':')[0] == 'service':
                service = monitor.tags[i].split(':')[1]
        monitor.tags.append('component:commission')

        hit_type = re.findall(r'[a-z]*.hits$', monitor.metrics[0])[0].split('.')[0]
        name = "Commission - Dev - {0} - East - abnormal change in throughput".format(service)
        message = """{{{{#is_alert}}}}The number of {0} hits to `{1}` is {{{{value}}}} and has too much from its usual value for Commission Dev East environment.
{{{{action}}}}
@avinashupadhya99@gmail.com needs to take a look{{{{/is_alert}}}} 
{{{{#is_recovery}}}}
The number of {0} hits to `{1}` is {{{{value}}}} and has recovered for Commission Dev East environment. @avinashupadhya99@gmail.com{{{{/is_recovery}}}}
        """.format(hit_type, service)
        # print(name)
        # print(message)
        # print(monitor.tags)
        # print(monitor)
        edit_body = MonitorUpdateRequest(
            name=name,
            message=message,
            tags=monitor.tags
        )

        edit_monitors_response = api_instance.update_monitor(monitor_id=int(monitor.id), body=edit_body)

        print(edit_monitors_response)

