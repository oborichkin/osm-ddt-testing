import random
import urllib, json
import threading

import pandas as pd
import requests

proxies = {
    "https": "77.52.188.230:3128"
}

print_lock = threading.Lock()

def reverse_main(filename='names', buffer=25, amount=2**1000, proxies=None):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2"

    b = buffer
    list_of_places = []

    w_current = 0
    w_rows = 0
    writer = pd.ExcelWriter(filename + '.xls', engine='openpyxl')

    df_header = ['display_name', 'address']

    pd.DataFrame(columns=df_header).to_excel(writer, index=False)

    for i in range(amount):
        lat = (random.random() * 180 - 90)
        lon = (random.random() * 360 - 180)

        data_url = url + "&lat=" + str(lat) + "&lon=" + str(lon)
        with print_lock:
            print(str(i+1) + ': ' + data_url)

        try:
            r = requests.get(url=data_url, proxies=proxies)
            j = r.json()
            list_of_places.append((j['display_name'], j['address']))
            w_rows += 1
            b -= 1
        except:
            pass
        
        if b < 1:
            b = buffer
            pd.DataFrame.from_records(list_of_places, columns=df_header).to_excel(writer, index=False, startrow=w_current, header=None)
            w_current += w_rows
            w_rows = 0
            list_of_places = []
            writer.save()

if __name__ == '__main__':
    reverse_main(proxies=proxies)
