import requests
import sqlite3
import json
import time
from decouple import config
from requests.auth import HTTPBasicAuth

def setup_up_database(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # create air table
    cur.execute("CREATE TABLE IF NOT EXISTS air (air_id INTEGER AUTO_INCREMENT PRIMARY KEY, city_id INTEGER, observation_count INTEGER, observation_percent INTEGER)")

    # create transportation table
    cur.execute("CREATE TABLE IF NOT EXISTS transportation (transportation_id INTEGER)")

    # create city table
    cur.execute("CREATE TABLE IF NOT EXISTS cities (city_id INTEGER PRIMARY KEY, city_name TEXT)")

    return cur, conn

def populate_city_database(cur, conn, cities):

    counter = 1
    for city in cities:
        cur.execute("INSERT OR IGNORE INTO cities (city_id, city_name) VALUES (?, ?)", (counter, city))
        counter += 1

    conn.commit()


def get_request(url, headers=None, params=None):
    '''
    '''
    if headers == None:
        page = requests.get(url, params)
    else:
        page = requests.get(url, headers=headers, params=params)

    print(page.url)

    if page.status_code >= 200 and page.status_code < 300: # successful
        return json.loads(page.text)
    else:
        print("Exception!")
        return None
    

def get_air_quality(city, cityBounds, cur, conn):
    '''
    '''
    AIR_API_KEY = config("AIR_API_KEY")
    EMAIL = "alvaradx@umich.edu"
    
    url = "https://aqs.epa.gov/data/api/annualData/byBox"
    params = {"email": EMAIL,
              "key": AIR_API_KEY,
              "param": 44201,
              "bdate": 20230101,
              "edate": 20230201,
              "minlat": round(cityBounds["minlat"], 1),
              "maxlat": round(cityBounds["maxlat"], 1),
              "minlon": round(cityBounds["minlon"], 1),
              "maxlon": round(cityBounds["maxlon"], 1),
              }
    
    # get city id
    cur.execute("SELECT city_id FROM cities WHERE city_name = ?", (city,))
    city_id = cur.fetchone()[0]

    # get the air data
    while True:
        counter = 0

        if counter%24 == 0:
            result = get_request(url, params=params)
            data = result["Data"]

        # add data to database 25 at a time
        cur.execute("INSERT OR IGNORE INTO air (city_id, observation_count, observation_percent) VALUES (?, ?, ?)", (city_id, data[counter]["observation_count"], data[counter]["observation_percent"]))
        conn.commit()

        counter += 1

        if counter > (len(data)-1): # if all data has been read than exit
            break
    

def get_route_number(city, cityBounds, cur, conn):
    '''
    '''
    TRANSIT_API_KEY = config("TRANSIT_API_KEY")

    url = "https://external.transitapp.com/v3/public/available_networks"
    headers = {'apiKey': TRANSIT_API_KEY}
    params = {"lat": cityBounds["lat"],
              "lon": cityBounds["lon"],
              }
    
    result = get_request(url, headers=headers, params=params)
    print(result)

def main():

    cur, conn = setup_up_database("final_database.db")

    cities = {
        "Chicago": {
            "minlat": 41.645059,
            "maxlat": 42.019615,
            "minlon": -87.800851,
            "maxlon": -87.524780,
            "lat": 41.881832,
            "lon": -87.623177,
        },
        "New York": {
            "minlat": 40.492591,
            "maxlat": 40.915684,
            "minlon": -74.199838,
            "maxlon": -73.702724,
            "lat": 40.730610,
            "lon": -73.935242,
        },
        "Detroit": {
            "minlat": 42.289426,
            "maxlat": 42.445439,
            "minlon": -83.284953,
            "maxlon": -82.910909,
            "lat": 42.331429,
            "lon": -83.045753,
        },
        "Ann Arbor": {
            "minlat": 42.222929,
            "maxlat": 42.322936,
            "minlon": -83.799241,
            "maxlon": -83.676243,
            "lat": 42.279594,
            "lon": -83.732124,
        },
        "Dallas": {
            "minlat": 32.633870,
            "maxlat": 33.009849,
            "minlon": -96.992379,
            "maxlon": -96.561180,
            "lat": 32.779167,
            "lon": -96.808891,
        },
    }

    populate_city_database(cur, conn, cities)

    for city in cities:
        get_air_quality(city, cities[city], cur, conn)
        # get_route_number(city, cities[city], cur, conn)
        time.sleep(13) # transit only allows 5 calls per minute (12 seconds)

if __name__ == "__main__":
    main()









