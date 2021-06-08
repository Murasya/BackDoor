# import gpsして、gps.get_location()関数を読みだすと位置情報を吐く

from subprocess import Popen, PIPE
import json
import requests
import urllib.request

def get_location():
    iwlist = Popen('iwlist wlan0 scan'.split(), stdout=PIPE)
    grep = Popen('grep Address:'.split(),
                stdin=iwlist.stdout, stdout=PIPE)
    awk = Popen(['awk', '{print $5}'],
                stdin=grep.stdout, stdout=PIPE)
    mac_address = awk.communicate()[0].splitlines()
    print(mac_address)

    query = json.dumps(
        {
            "homeMobileCountryCode": 310,
            "homeMobileNetworkCode": 410,
            "radioType": "lte",
            "considerIp": "true",
            "wifiAccessPoints": [
            {
                "macAddress": d.decode("UTF-8")
            } for d in mac_address]
        }
    ).encode("utf-8")

    print(query)

    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyDMshWDUJan7O0Zmlh5SZ_X8rCGtBFzG4o'
    headers = {"Content-Type" : "application/json"}
    method = "POST"
    request = urllib.request.Request(url, data=query, headers=headers, method=method)
    # r = requests.post('http://www.google.com/loc/json', query)
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print(response_body)
        data = json.loads(response_body)
        print(data['location']['lat'], data['location']['lng'], data['accuracy'])
    
    return data['location']['lat'], data['location']['lng'], data['accuracy']