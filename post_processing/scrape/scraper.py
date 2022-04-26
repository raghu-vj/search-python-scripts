import sys

import requests
import json
import datetime as dt

from paramiko.client import SSHClient

PROD_HOST = "http://voyager-search-service.swiggy.prod"

client = SSHClient()
client.load_system_host_keys()
client.connect('sp.swiggy.co', port=4242, username="raghunandan.j")


def read_from_file(file_name):
    with open(file_name, "r") as file:
        return file.read()


def append_to_file(file, text):
    file.write(text)
    file.write("\n")


def curl_request(url,method,headers,payloads):
    # construct the curl command from request
    command = "curl -v -H {headers} {data} -X {method} {uri}"
    data = " -d '" + payloads + "'"
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    return command.format(method=method, headers=header, data=data, uri=url)

def curl_request_v2(url,method,headers,payloads):
    data = " -d '" + payloads + "'"
    command = "curl --location --request POST '%s' --header 'swuid: 42705fa442b74c24' --header 'X-GRID: raghunandan' --header 'Content-Type: application/json' {data}" % url
    return command.format(data=data, url=url)

if __name__ == '__main__':
    location_data = read_from_file("data/location_data.csv")
    queries_data = read_from_file("data/low_mrr_queries.txt").split("\n")
    base_url = PROD_HOST
    # if len(sys.argv) > 0:
    #     base_url = PROD_HOST
    hour_of_day = str(dt.datetime.now().hour)
    file_name = "generated/" + str(dt.datetime.now()) + "_Hour_" + hour_of_day + ".csv"
    file = open(file_name, "a")
    for query in queries_data:
        append_to_file(file, "#### Query: " + query)
        for query_data in location_data.split("\n"):
            try:
                location_data_split = query_data.split(",")
                city_id = location_data_split[0].strip()
                lat = location_data_split[1].strip()
                long = location_data_split[2].strip()
                location_within_city = location_data_split[3].strip()
                city = location_data_split[4].strip()
                url = (base_url + "/api/v3/search?maxCount=100&pageOffset=0&str=%s&entityType=RESTAURANT") % query
                payload = "{\"latLong\":\"%s, %s\",\"submitAction\":\"DEFAULT_SUGGESTION\",\"trackingId\":\"1234590123\",\"trySpellCorrection\":\"false\",\"isAdsEnabled\":\"true\",\"context\":{\"isRadialCutEnabled\":true,\"filters\":{}}}" % (
                lat, long)
                headers = {
                    'swuid': '42705fa442b74c24',
                    'X-GRID': 'raghunandan',
                    'Content-Type': 'application/json'
                }
                request = curl_request_v2(url, "POST", headers, payload)
                _, stdout, _ = client.exec_command(request)
                json_data = json.loads(stdout.read())
                append_to_file(file, "#### Location: " + location_within_city + " City: " + city_id + "(" + city + ")" + ", Hour of day: " + hour_of_day)
                append_to_file(file, "" + "," + "Restaurant ID, Parent ID, Restaurant Name, Relevance")
                for index, rest in enumerate(json_data['data']['searchResult']['RESTAURANT']):
                    if index > 19:
                        break
                    append_to_file(file, "" + "," + str(rest['id']) + "," + str(rest.get("parentId", "")) + "," + rest['name'])
            except Exception as e:
                print(e)
                pass
    file.close()