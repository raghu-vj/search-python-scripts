from sshtunnel import SSHTunnelForwarder
import requests
import json

remote_user = 'raghunandan.j'
remote_host = 'sp.swiggy.co'
remote_port = 4242
local_host = '127.0.0.1'
local_port = 5000

queries = ["Chinese"]
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


server = SSHTunnelForwarder(
   (remote_host, remote_port),
   ssh_username=remote_user,
   remote_bind_address=(local_host, local_port),
   local_bind_address=(local_host, local_port),
   )
server.start()
print("server started")
for query in queries:
    payload_mumbai = json.dumps({
      "query": ("%s" % query),
      "cityId": 5,
      "latlong": "18.9982, 72.8270",
      "searchAction": "ENTER",
      "trackingId": "gjgkjhk",
      "intentRequired": True
    })
    control_url = "http://query-understanding-layer.swiggy.prod/v1/predict/query-intent"
    test_url = "172.31.35.135:8081/v1/predict/query-intent"
    control_response = requests.request("POST", control_url, headers=headers, data=payload_mumbai)
    test_response = requests.request("POST", test_url, headers=headers, data=payload_mumbai)
    json_compare_response = ordered(json.loads(control_response.text)) == ordered(json.loads(test_response.text))
    if json_compare_response:
        print(query + " => " + str(json_compare_response))
    else:
        print("Failed for query: " + query)


