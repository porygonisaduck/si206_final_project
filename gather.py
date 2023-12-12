import requests
import sqlite3
import json
import time
from bs4 import BeautifulSoup
from decouple import config
from requests.auth import HTTPBasicAuth

def setup_up_database(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    # create air table
    cur.execute("CREATE TABLE IF NOT EXISTS air (air_id INTEGER PRIMARY KEY AUTOINCREMENT, city_id INTEGER, PM25 INTEGER)")

    # create transportation table
    cur.execute("CREATE TABLE IF NOT EXISTS transportation (route_name TEXT PRIMARY KEY, city_id INTEGER, transportation_id INTEGER)")

    # create city table
    cur.execute("CREATE TABLE IF NOT EXISTS cities (city_id INTEGER PRIMARY KEY, city_name TEXT, population INTEGER)")

    # create types of transportation table
    cur.execute("CREATE TABLE IF NOT EXISTS typeOfTrans (transportation_id INTEGER PRIMARY KEY AUTOINCREMENT, transportation_type TEXT)")

    conn.commit()
    return cur, conn


def populate_city_database(cur, conn, cities):
    # insert cities into table with id, name, and population (web-scraped)
    counter = 1
    # wikipedia article for population data
    soup = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population').text, 'html.parser')
    for city in cities:
        # scrape population
        population = get_population(soup, city)
        cur.execute("INSERT OR IGNORE INTO cities (city_id, city_name, population) VALUES (?, ?, ?)", (counter, city, population))
        counter += 1

    conn.commit()

def get_population(soup, city):
    # find a city's current population estimate with given soup object
    table = soup.find('table', class_='wikitable sortable')
    rows = table.find_all('tr')
    for row in rows:
        info = row.text.split('\n')
        if city in info[3]:
            return int(info[7].replace(',', ''))

def get_request(url, headers=None, params=None):
    '''
    '''
    if headers == None:
        page = requests.get(url, params)
    else:
        page = requests.get(url, headers=headers, params=params)

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
              "param": "88101,88502",
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
    counter = 0
    while True:

        if counter%24 == 0:
            result = get_request(url, params=params)
            data = result["Data"]

        if len(data) == 0: # some cities don't have data (ex: Detroit)
            break

        # add data to database 25 at a time
        cur.execute("INSERT OR IGNORE INTO air (city_id, PM25) VALUES (?, ?)", (city_id, data[counter]["arithmetic_mean"]))
        conn.commit()

        counter += 1

        if counter == len(data): # if all data has been read then exit
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
    
    # get networks for a city
    networks = get_request(url, headers=headers, params=params)
    for network in networks["networks"]:
        network_id = network["network_id"]
        network_location = network["network_location"]
        # network_name = network["network_name"]

        if network_location == "NYC":
            network_location = "New York"

        # get city id
        cur.execute("SELECT city_id FROM cities WHERE city_name = ?", (network_location,))

        temp = cur.fetchone()
        if temp == None: # if we get a different city
            continue

        city_id = temp[0]

        url = "https://external.transitapp.com/v3/public/routes_for_network"
        params = {"network_id": network_id}

        # get the transportation data
        counter = 0
        while True:

            if counter%24 == 0:
                # sleep to avoid going over api requests per minutes
                time.sleep(13)

                # get number of routes for a network
                result = get_request(url, headers=headers, params=params)
                data = result["routes"]

            mode_name = data[counter]["mode_name"]

            # insert transportation mode
            cur.execute("INSERT OR IGNORE INTO typeOfTrans (transportation_type) VALUES (?)", (mode_name,))
            conn.commit()
            
            # get transportation mode id
            cur.execute("SELECT transportation_id FROM typeOfTrans WHERE transportation_type = ?", (mode_name,))
            
            trans_id = cur.fetchone()[0]

            # add data to database 25 at a time
            cur.execute("INSERT OR IGNORE INTO transportation (route_name, city_id, transportation_id) VALUES (?, ?, ?)", (data[counter]["route_long_name"], city_id, trans_id))
            conn.commit()

            counter += 1

            if counter > (len(data)-1): # if all data has been read than exit
                break


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
        get_route_number(city, cities[city], cur, conn)
        time.sleep(13) # transit only allows 5 calls per minute (12 seconds)

if __name__ == "__main__":
    main()
