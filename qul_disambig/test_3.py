import json

import requests
from sshtunnel import SSHTunnelForwarder


queries = ["Chinese", "Pizza", "Pizza Hut", "Pizza H", "Adrak"]
headers = {
  'Content-Type': 'application/json',
  'swuid': 'test_swuid',
  'user-agent': 'Swiggy-Android',
  'requestId': 'afwgfasgasgg'
}

def ordered(obj):
  if isinstance(obj, dict):
    return sorted((k, ordered(v)) for k, v in obj.items())
  if isinstance(obj, list):
    return sorted(ordered(x) for x in obj)
  else:
    return obj

def connect():
    preprod_server = SSHTunnelForwarder(
         ('bastion-prod', 4242),
         ssh_username="raghunandan.j",
         local_bind_address=('127.0.0.1', 8081),
         remote_bind_address=('172.31.34.210', 8081))
    preprod_server.start()

    prod_server = SSHTunnelForwarder(
         ('bastion-prod', 4242),
         ssh_username="raghunandan.j",
         local_bind_address=('127.0.0.1', 8082),
         remote_bind_address=('172.31.34.210', 8080))
    prod_server.start()
    print("servers connected")

    for query in queries:
         payload_mumbai = json.dumps({
             "query": ("%s" % query),
             "cityId": 5,
             "latlong": "18.9982, 72.8270",
             "searchAction": "ENTER",
             "trackingId": "gjgkjhk",
             "intentRequired": True
         })
         control_response = requests.request("POST", "http://127.0.0.1:8081/v1/predict/query-intent", headers=headers, data=payload_mumbai)
         test_response = requests.request("POST", "http://127.0.0.1:8082/v1/predict/query-intent", headers=headers,
                                             data=payload_mumbai)
         json_compare_response = ordered(json.loads(control_response.text)) == ordered(json.loads(test_response.text))
         if json_compare_response:
             print(query + " => " + str(json_compare_response))
         else:
             print("Failed for query: " + query)
             print("control: " + control_response.text)
             print("test: " + test_response.text)


connect()