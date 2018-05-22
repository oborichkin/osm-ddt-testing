import requests
import warnings


def compare_amount(count, name):
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2&q=" + name.replace(' ', '+')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        if r.ok:
            j = r.json()
            r.close()
            if(len(j) == count):
                return True
    return False


def get_coord(name):
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2&q=" + name.replace(' ', '+')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        j = r.json()
        return (float(j[0]['lat']), float(j[0]['lon']))


def check_coordinates(name, lat, lon):
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2&q=" + name.replace(' ', '+')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        j = r.json()
        r.close()
        if(float(j[0]['lat']) == float(lat) and float(j[0]['lon']) == float(lon)):
            return True
    return False


def get_info(name):
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2&q=" + name.replace(' ', '+')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        return [x['place_id'] for x in r.json()]


def get_place_id(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lon=" + str(lon) + "&lat=" + str(lat)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        j = r.json()
        return j['place_id']

def get_category(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lon=" + str(lon) + "&lat=" + str(lat)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        j = r.json()
        return j['category']

def get_type(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lon=" + str(lon) + "&lat=" + str(lat)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        j = r.json()
        return j['type']

def get_address_type(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lon=" + str(lon) + "&lat=" + str(lat)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        j = r.json()
        return j['address_type']

def get_display_name(lat, lon):
    url = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lon=" + str(lon) + "&lat=" + str(lat)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = requests.get(url=url)
        j = r.json()
        return j['display_name']