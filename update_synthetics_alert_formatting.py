"""
Get the list of all tests returns "OK - Returns the list of all Synthetic tests." response
"""

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.synthetics_api import SyntheticsApi
from datadog_api_client.v1.model.synthetics_api_test import SyntheticsAPITest
from datadog_api_client.v1.model.synthetics_test_options import SyntheticsTestOptions
from datadog_api_client.v1.model.synthetics_api_test_config import SyntheticsAPITestConfig
from datadog_api_client.v1.model.synthetics_api_test_type import SyntheticsAPITestType
from datadog_api_client.v1.model.monitor_update_request import MonitorUpdateRequest
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor

alert_message = """{{{{#is_alert}}}}The health check for the {0} service of Commission in Prod environment has failed.{{{{/is_alert}}}}
{{{{#is_recovery}}}}{0} service of Commission in Prod environment has recovered and is responding to health checks.{{{{/is_recovery}}}} 
"""

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = SyntheticsApi(api_client)
    monitors_api_instance = MonitorsApi(api_client)
    response = api_instance.list_tests()
    # print(response.tests)
    apiTests = []
    for test in response.tests:
        if 'api' == str(test.type) and 'env:prod' in test.tags and 'API Health Check' in test.name and'{{#is_alert}}{{/is_alert}}' in test.message:
            service = test.name.split(' - ')[3]
            # print(test)
            print('---')
            print(test.name)
            print("https://app.datadoghq.com/synthetics/edit/{}".format(test.public_id))
            print(alert_message.format(service))
            confirmation = input("Enter Y to update and N to skip")
            if 'Y' in confirmation:
                body = SyntheticsAPITest(
                    config=SyntheticsAPITestConfig(assertions=test.config.assertions, request=test.config.request),
                    locations=test.locations,
                    name=test.name,
                    options=test.options,
                    type=SyntheticsAPITestType("api")
                )
                print(body)
                edit_synthetic_response = api_instance.update_api_test(public_id=test.public_id, body=body)
                print(edit_synthetic_response)
            else:
                print("Did not update synthetic test - https://app.datadoghq.com/synthetics/edit/{}".format(test.public_id))
                # row = [test.name, "https://app.datadoghq.com/synthetics/edit/{}".format(test.public_id)]
                # with open('unupdated-synthetics.csv', 'a', encoding='UTF8') as f:
                #     writer = csv.writer(f)
                #     writer.writerow(row)
            break
    # print(apiTests)
    print(len(apiTests))