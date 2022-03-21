from sshtunnel import SSHTunnelForwarder

def connect():

     payload_mumbai = json.dumps({
      "query": ("%s" % query),
      "cityId": 5,
      "latlong": "18.9982, 72.8270",
      "searchAction": "ENTER",
      "trackingId": "gjgkjhk",
      "intentRequired": True
    })
    try:
        with SSHTunnelForwarder(
             ('bastion-prod', 4242),
             ssh_username="raghunandan.j",
             local_bind_address=('127.0.0.1', 8081),
             remote_bind_address=('172.31.35.135', 8081)) as server:
             server.start()
             print ("server connected")
             control_response = requests.request("GET", "127.0.0.1:88081/health-check", headers=headers)
    except:
        print ("Connection Failed")

connect()