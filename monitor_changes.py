"""
Query the event stream returns all changes to production monitors in the last 24 hours
"""

from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.events_api import EventsApi
import datetime
from mistletoe import Document, HTMLRenderer

def get_background_color(event_string):
    background_color='white'
    if "created" in event_string:
        background_color = '#E3FCBF'
    elif "deleted" in event_string:
        background_color = '#FFC3C3'
    elif "modified" in event_string:
        background_color = '#FEF9A7'
    return background_color

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)

output_file_name = "monitor-{}.html".format(now.strftime("%m-%d-%Y_%H-%M-%S"))

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = EventsApi(api_client)
    response = api_instance.list_events(
        start=int(yesterday.timestamp()),
        end=int(now.timestamp()),
        tags="env:(prod* OR ne-prod*),monitor,source:datadog"
    )
    print(response.events)
    f = open(output_file_name, "w")
    f.write("<center><h1>Production Datadog monitor modifications report</h1><p>The report contains the modifications for all monitor in production for the past 1 day including the creation and deletion of monitors.</p></center>")
    f.write("<h3>Summary</h3><ul><li>Date and time of the report generation - <b>{}</b></li><li>There are <b>{}</b> monitor(s) modified/created/deleted in production in the past 24 hours.</li></ul>".format(now.strftime("%m-%d-%Y %H:%M:%S"), len(response['events'])))
    f.close()

    if len(response['events']) == 0:
        print("No monitors were modified in the past 24 hours")


    for event in response['events']:
        with HTMLRenderer() as renderer:
            event_string = event.text.replace("%%%", "") # Remove %%% from the event string
            background_color = get_background_color(event_string)
            ast_doc = Document(event_string)     # parse the lines into AST
            rendered = renderer.render(ast_doc)
            formatted_rendered = rendered.replace("href=\"/monitors", "target=\"_blank\" href=\"https://app.datadoghq.com/monitors")
            formatted_rendered += "\n<hr>"
            event_date_time = datetime.datetime.fromtimestamp(event.date_happened)
            f = open(output_file_name, "a")
            f.write("<div style=\"background-color:{}\">".format(background_color))
            f.write("Date and time - {}\n".format(event_date_time))
            f.write(formatted_rendered)
            f.write('</div>')
            f.close()
