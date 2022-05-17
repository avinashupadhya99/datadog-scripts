"""

"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi


configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.list_monitors(monitor_tags="env:sit,component:abc")

    for monitor in response:
        new_name = ''
        if "APM" in monitor.name: 
            continue
        for idx, key in enumerate(monitor.name.split(' - ')):
            if idx == 3:
                new_name += key
                break
            if idx == 2:
                new_name += 'APM' + ' - '
            new_name += key + ' - '
        print(new_name)
        update_response = api_instance.update_monitor(monitor.id, {'name': new_name})
        print(update_response)

    # print(response)