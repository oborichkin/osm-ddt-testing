'''
Без слез не взглянешь

Набор данных прямомого и обратного геокодирования:
    * forward_data.xls
    * reverse_data.xls
'''

import random
import urllib, json
import itertools
import threading

import pandas as pd
import requests

from threading import Thread

# T H X R K N
proxies = {
    "https": "89.236.17.106:3128"
}

# Номер текущей строки для записи в *.xls
w_current = 1

print_lock = threading.Lock()
write_lock = threading.Lock()

def reverse_mine(writer, region=(59.8944444, 30.2641667, 1), buffer=25, amount=2**1000, proxies=None):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2"

    b = buffer
    list_of_places = []
    global w_current
    w_rows = 0

    for i in range(amount):
        random.seed()
        lat = region[0] + (random.random() * region[2] - region[2]*2)
        lon = region[0] + (random.random() * region[2] - region[2]*2)

        data_url = url + "&lat=" + str(lat) + "&lon=" + str(lon)
        with print_lock:
            print(str(i+1) + '(rev): ' + data_url)

        try:
            r = requests.get(url=data_url, proxies=proxies)
            j = r.json()
            list_of_places.append((j['place_id'], lat, lon, j['category'],
                j['type'], j['addresstype'], j['display_name'], j['address']))
            w_rows += 1
        except:
            pass
        
        b -= 1
        if b < 1:
            b = buffer
            with write_lock:
                pd.DataFrame.from_records(list_of_places, columns=df_header).to_excel(writer, index=False, startrow=w_current, header=None)
                w_current += w_rows
                writer.save()
            w_rows = 0
            list_of_places = []

def forward_mine(filename='forward_data', buffer=25, proxies=None):
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2"

    b = buffer
    list_of_places = []

    w_current = 1
    w_rows = 0
    writer = pd.ExcelWriter(filename + '.xls', engine='openpyxl')

    # Записываем заголовки для столбцов
    df_header = ['count', 'name', 'places']
    pd.DataFrame(columns=df_header).to_excel(writer, index=False)

    # Набор заранее подготовленных адресов
    df = pd.read_excel('names.xls')

    for i in range(df.shape[0]):
        # Разбиваем полный адрес на части
        # При помощи itertools.combination получаем новый адрес из частей полного
        # Производим преобразование
        names = df.loc[i]['display_name'].split(',')
        for j in range(1, len(names)+1):
            for name in itertools.combinations(names, j):
                data_url = url + "&q=" + ', '.join(name).replace(' ', '+')
                with print_lock:
                    print(str(i+1) + '(forward): ' + data_url)

                try:
                    r = requests.get(url=data_url, proxies=proxies)
                    j = r.json()
                    list_of_places.append((len(j), name, [(x['lon'], x['lat'], x['category'], x['type'], x['display_name']) for x in j]))
                    w_rows += 1
                except:
                    pass
                
                b -= 1
                if b < 1:
                    b = buffer
                    pd.DataFrame.from_records(list_of_places, columns=df_header).to_excel(writer, index=False, startrow=w_current, header=None)
                    w_current += w_rows
                    w_rows = 0
                    list_of_places = []
                    writer.save()

if __name__ == '__main__':
    # writer для обратного преобразования
    writer = pd.ExcelWriter('reverse_data.xls', engine='openpyxl')

    # Записываем заголовки для столбцов
    df_header = ['place_id', 'lat', 'lon', 'category', 'type', 'addresstype', 'display_name', 'address']
    pd.DataFrame(columns=df_header).to_excel(writer, index=False)

    Thread(target=reverse_mine, args=(writer, (59.8944444, 30.2641667, 1), 25, 2**1000, proxies)).start()
    Thread(target=reverse_mine, args=(writer, (55.7494733, 37.3523210, 1), 25, 2**1000, proxies)).start()
    Thread(target=reverse_mine, args=(writer, (33.8688914, -118.5496523, 1), 25, 2**1000, proxies)).start()
    Thread(target=forward_mine, args=('forward_data', 25, proxies)).start()
