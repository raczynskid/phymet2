import pandas as pd
from geopy.geocoders import Nominatim
from geotext import GeoText
import requests

db_url = 'http://phymet2.biotech.uni.wroc.pl/index.php?ind=all_cvs'

def get_database(url):
    r = requests.get(url, allow_redirects=True)
    open('database.csv', 'wb').write(r.content)
    return pd.read_csv('database.csv')

def find_loc(description):
    words = description.split(' ')
    desc = ' '.join([w.capitalize() for w in words])
    city = GeoText(description).cities
    country = GeoText(desc).country_mentions
    if city and country:
        return city[0], list(country.keys())[0]
    elif city and not country:
        return city[0], None, desc
    elif country and not city:
        return None, list(country.keys())[0]
    else:
        return None, None , desc

def get_coordinates(city, ctry):
    geolocator = Nominatim(timeout=2)
    geolocator = Nominatim()
    if city:
        location = geolocator.geocode(city)
        if location:
            return (location.latitude, location.longitude)
    elif ctry:
        location = geolocator.geocode(city)
        if location:
            return (location.latitude, location.longitude)
    else:
        return None, None

def coords_to_frame(data):
    d = {}
    d["latitude"] = []
    d["longitude"] = []
    for desc in data['Description']:
        city = find_loc(desc)[0]
        ctry_code = find_loc(desc)[1]
        lat, long = (get_coordinates(city, ctry_code))
        d["latitude"].append(lat)
        d["longitude"].append(long)
    geodata = pd.DataFrame.from_dict(d)
    return geodata

if __name__ == "__main__":
    data = pd.concat([get_database(db_url), coords_to_frame(get_database(db_url))], axis=1)