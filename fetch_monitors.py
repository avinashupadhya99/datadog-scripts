"""
Get all monitor details with a certain tag and document in a csv
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
import csv

header = ['Monitor Name', 'Metric', 'Critical Threshold', 'Warning Threshold', 'Monitor Link']

with open('monitors.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.list_monitors(monitor_tags="env:prod")

    for monitor in response:
        row = [monitor['name'], monitor['options']['aggregation']['metric'], monitor['options']['thresholds']['critical'], monitor['options']['thresholds']['warning'], 'https://app.datadoghq.com/monitors/'+str(monitor['id'])]
        with open('monitors.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(row)

    print(response)