import requests
import json

url = "https://search-search-perf-public-sfhpf2qga7guxicrs322krkrl4.ap-southeast-1.es.amazonaws.com/legacy_search_index_2021-07-11-010000/_search"
headers = {
  'Content-Type': 'application/json'
}

write_url = "https://search-search-perf-v7-ud3v5wpdc3j3o7jhgb2joqnygy.ap-southeast-1.es.amazonaws.com/_bulk"
write_dict = { 'create' : { '_id': '0', '_index': 'embeddings_test_index', 'retry_on_conflict': 2} }
offset = 0
while True:
    try:
        payload = json.dumps({
          "from": offset,
          "size": 1000,
          "query": {
            "term": {
              "cityId": {
                "value": 2
              }
            }
          }
        })
        print(payload)
        response = requests.request("POST", url, headers=headers, data=payload)
        request_body = ''
        hits_ = json.loads(response.text)['hits']['hits']
        if len(hits_) == 0:
            break
        for hit in hits_:
            write_dict['create']['_id'] = hit['_id']
            request_body = request_body + json.dumps(write_dict) + "\n"
            request_body = request_body + json.dumps(hit['_source']) + "\n"
        response = requests.request("POST", write_url, headers=headers, data=request_body)
        print(response.status_code)
    except Exception as e:
        print(e)
    offset = offset + 1000
