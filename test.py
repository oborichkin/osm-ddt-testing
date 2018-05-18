import random

import urllib.request, json
import pandas


SIZE = 10

list_of_places = []
list_of_errors = []

url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2"

for i in range(SIZE):
    lon = random.random() * 360 - 180
    lat = random.random() * 180 - 90

    data_url = url + "&lat=" + str(lat) + "&lon=" + str(lon)
    print(data_url)
    try:
        data = urllib.request.urlopen(data_url)
        json_data = json.loads(data.read().decode())
        list_of_places((lon, lat, json_data["display_name"], json_data["address"]))
    except urllib.error.HTTPError:
        list_of_errors.append((lon, lat))
        pass

df     = pandas.DataFrame.from_records(list_of_places, columns=['lon', 'lat', 'display_name', 'address'])
err_df = pandas.DataFrame.from_records(list_of_errors, columns=['lon', 'lat'])

df.to_excel("places.xls")
err_df.to_excel("errors.xls")
