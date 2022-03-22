import sys

import requests
import json

from util import io_helper
import datetime as dt

HOST = "http://localhost:8080"
PROD_HOST = "http://voyager-search-service.swiggy.prod"

location_data = io_helper.read_from_file("data/location_data.csv")
queries_data = io_helper.read_from_file("data/low_mrr_queries.txt").split("\n")


if __name__ == '__main__':
    base_url = HOST
    if len(sys.argv) > 0:
        base_url = PROD_HOST
    hour_of_day = str(dt.datetime.now().hour)
    file_name = "generated/" + str(dt.datetime.now()) + "_Hour_" + hour_of_day + ".csv"
    file = open(file_name, "a")
    for query in queries_data:
        io_helper.append_to_file(file, "#### Query: " + query)
        for query_data in location_data.split("\n"):
            try:
                location_data_split = query_data.split(",")
                city_id = location_data_split[0].strip()
                lat = location_data_split[1].strip()
                long = location_data_split[2].strip()
                location_within_city = location_data_split[3].strip()
                city = location_data_split[4].strip()
                url = (base_url + "/api/v3/search?maxCount=100&pageOffset=0&str=%s&entityType=RESTAURANT") % query
                payload = json.dumps({
                    "latLong": ("%s, %s" % (lat, long)),
                    "submitAction": "DEFAULT_SUGGESTION",
                    "trackingId": "1234590123",
                    "trySpellCorrection": "false",
                    "isAdsEnabled": "true",
                    "context": {
                        "isRadialCutEnabled": True,
                        "filters": {}
                    }
                })
                headers = {
                    'swuid': '42705fa442b74c24',
                    'X-GRID': 'raghunandan',
                    'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                json_data = json.loads(response.text)
                io_helper.append_to_file(file, "#### Location: " + location_within_city + " City: " + city_id + "(" + city + ")" + ", Hour of day: " + hour_of_day)
                io_helper.append_to_file(file, "" + "," + "Restaurant ID, Parent ID, Restaurant Name, Relevance")
                for index, rest in enumerate(json_data['data']['searchResult']['RESTAURANT']):
                    if index > 19:
                        break
                    io_helper.append_to_file(file, "" + "," + str(rest['id']) + "," + str(rest.get("parentId", "")) + "," + rest['name'])
            except:
                print
    file.close()