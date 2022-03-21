import requests
import json

query = "Mocktails"
preprod_url = "http://localhost:8080/api/v3/search?maxCount=100&pageOffset=0&str=%s&entityType=RESTAURANT" % query
prod_url = "http://localhost:8081/api/v3/search?maxCount=100&pageOffset=0&str=%s&entityType=RESTAURANT" % query

payload = json.dumps({
    "latLong": "12.990565740022038, 77.69421425124344",
    "submitAction": "DEFAULT_SUGGESTION",
    "trackingId": "1234590123",
    "trySpellCorrection": "false",
    "isAdsEnabled": "false",
    "context": {
        "filters": {},
        "isSemanticSearchEnabled": True
    }
})
headers_test = {
    'Content-Type': 'application/json',
    'swuid': 'test',
    'explain': 'true'
}

headers_control = {
    'Content-Type': 'application/json',
    'explain': 'true'
}

control_list = []
test_list = []


def method_name(url, addition_list, headers):
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    # debug_response = response_json['debugResponse']['entities']
    # debug_response_dict = {}
    # for entity in debug_response:
    #     debug_response_dict[entity['id']] = entity
    for rest in response_json['data']['searchResult']['RESTAURANT']:
        addition_list.append(rest['name'])
        print(rest['name'])

method_name(preprod_url, control_list, headers_control)
method_name(preprod_url, test_list, headers_test)

with open('control.txt', 'w') as f:
    for item in control_list:
        f.write("%s\n" % item)

with open('test.txt', 'w') as f:
    for item in test_list:
        f.write("%s\n" % item)