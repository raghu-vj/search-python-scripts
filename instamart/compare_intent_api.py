import os

import requests
import json

from util.io_helper import write_to_file

payload = json.dumps({
  "latLong": "12.9731335,77.6073478",
  "cityId": 1,
  "trackingId": "1234590123",
  "supportedTypes" : []
})
headers = {
  'Content-Type': 'application/json'
}

queries = ["Pizza", "Chai", "Chai Point", "Chinese", "Instamart", "Genie"]

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


for query in queries:
    control_url = "http://localhost:8189/api/v1/search/intent?q=%s" % query
    test_url = "http://localhost:8188/api/v1/search/intent?q=%s" % query
    control_response = requests.request("POST", control_url, headers=headers, data=payload)
    test_response = requests.request("POST", test_url, headers=headers, data=payload)
    json_compare_response = ordered(json.loads(control_response.text)) == ordered(json.loads(test_response.text))
    if json_compare_response:
        print(query + " => " + str(json_compare_response))
    else:
        print("Failed for query: " + query)
        control_file = "control"
        write_to_file(control_response.text, control_file)
        test_file = "test"
        write_to_file(test_response.text, test_file)
        os.system("diffchecker /Users/raghunandan.j/PycharmProjects/pythonProject/instamart/control.json /Users/raghunandan.j/PycharmProjects/pythonProject/instamart/test.json")
        break
