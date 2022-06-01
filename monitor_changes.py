"""
Query the event stream returns all changes to production monitors in the last 24 hours
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
import datetime
from mistletoe import Document, HTMLRenderer

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=2)

output_file_name = "output-{}.html".format(now.strftime("%m-%d-%Y_%H-%M-%S"))

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = EventsApi(api_client)
    response = api_instance.list_events(
        start=int(yesterday.timestamp()),
        end=int(now.timestamp()),
        tags="env:*prod*,monitor,source:datadog"
    )

    if len(response['events']) == 0:
        print("No monitors were modified in the past 24 hours")
        f = open(output_file_name, "a")
        f.write("<h1>No monitors in the production environment were modified in the past 24 hours</h1>")
        f.close()

    for event in response['events']:
        with HTMLRenderer() as renderer:
            event_string = event.text.replace("%%%", "") # Remove %%% from the event string
            ast_doc = Document(event_string)     # parse the lines into AST
            rendered = renderer.render(ast_doc)
            f = open(output_file_name, "a")
            formatted_rendered = rendered.replace("href=\"/monitors", "target=\"_blank\" href=\"https://app.datadoghq.com/monitors")
            formatted_rendered += "\n<hr>"
            f.write(formatted_rendered)
            f.close()
