import json
import requests
import SnowFlake

sample_json = {
          "version": 1625956739192,
          "restId": 126569,
          "latLong": "17.711961700895145,83.31836751405149",
          "cityId": 1,
          "cuisines": [
            "Beverages"
          ],
          "popularity": 1,
          "type": "Restaurant",
          "isRestEnabled": 'false',
          "isLongDistanceEnabled": 'false'
    }

headers = {
  'Content-Type': 'application/json'
}


if __name__ == '__main__':
    es_json_list = []
    query = """
            select * from DATA_SCIENCE.DS_STOREFRONT.ITEM_EMBEDDINGS_SIAMESE_TRIPLET_64DIM_V1 limit 1000;
        """
    results = SnowFlake.SnowflakeClient().fetch_results(query)
    for result in results:
        es_json = sample_json.copy()
        embeddings = []
        es_json['embeddings_v1'] = [float(x.strip()) for x in result[2].strip('][').split(',')]
        es_json['id'] = 'I-' + result[0]
        es_json['name'] = result[1]
        es_json_list.append(es_json)
        response = requests.request("PUT", 'https://search-search-perf-v7-ud3v5wpdc3j3o7jhgb2joqnygy.ap-southeast-1.es.amazonaws.com/embeddings_test_index/_doc/' + es_json['id'],
                                    headers=headers, data=json.dumps(es_json))
        print(response.status_code)
        # print(response.text)