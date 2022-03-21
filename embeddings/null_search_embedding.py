import json
import re

import requests
from sshtunnel import SSHTunnelForwarder

from util import io_helper

def ordered(obj):
  if isinstance(obj, dict):
    return sorted((k, ordered(v)) for k, v in obj.items())
  if isinstance(obj, list):
    return sorted(ordered(x) for x in obj)
  else:
    return obj

def is_null_search(response):
    json_data = json.loads(response.text)
    return 'data' in json_data and "searchResult" in json_data['data'] \
           and "RESTAURANT_ITEM" in json_data['data']['searchResult'] and len(json_data['data']['searchResult']['RESTAURANT_ITEM']) == 0

def connect_and_test():
    preprod_server = SSHTunnelForwarder(
         ('bastion-prod', 4242),
         ssh_username="raghunandan.j",
         local_bind_address=('127.0.0.1', 8081),
         remote_bind_address=('172.31.4.61', 8080))
    preprod_server.start()
    print("servers connected")
    data = io_helper.read_from_file("/Users/raghunandan.j/PycharmProjects/pythonProject/embeddings/data/results.csv").split("\n")
    for line in data:
         if line == "":
             continue
         elements = line.split()
         payload = json.dumps({
                "latLong": ("%s" % (elements[0])),
                "submitAction": "DEFAULT_SUGGESTION",
                "trackingId": "1234590123",
                "isAdsEnabled": "true",
                "context": {
                    "filters": {
                    }
                }
            })
         url = "http://127.0.0.1:8081/api/v3/search?maxCount=100&pageOffset=0&str=%s&entityType=RESTAURANT_ITEM" % elements[1]
         headers = {
             'Content-Type': 'application/json',
             'user-agent': 'Swiggy-Android',
             'requestId': 'raghunandan',
             'swuid' : ('%s' % elements[2])
         }
         control_headers = {
             'Content-Type': 'application/json',
             'user-agent': 'Swiggy-Android',
             'requestId': 'raghunandan',
             'swuid' : 'scout_test'
         }
         control_response = requests.request("POST", url=url, headers=control_headers, data=payload)
         test_response = requests.request("POST", url=url, headers=headers, data=payload)
         if not is_null_search(control_response) and is_null_search(test_response):
             print("different response for: " + line)

connect_and_test()