import requests
import json
from decouple import config


def get_request(url, params=None):
    '''
    '''
    if params != None:
        page = requests.get(url, params)
    else:
        page = requests.get(url)

    if page.status_code >= 200 and page.status_code < 300: # successful
        return json.loads(page.text)
    else:
        print("Exception!")
        return None
    

def get_air_quality(cityBounds):
    '''
    '''
    AIR_API_KEY = config("AIR_API_KEY")
    EMAIL = "alvaradx@umich.edu"
    
    url = "https://aqs.epa.gov/data/api/annualData/byBox"
    params = {"apiKey": AIR_API_KEY,
              "email": EMAIL,
              "param": 44201,
              "bdate": 20230101,
              "edate": 20230201,
              "minlat": cityBounds["minlat"],
              "maxlat": cityBounds["maxlat"],
              "minlon": cityBounds["minlon"],
              "maxlon": cityBounds["maxlon"],
              }
    
    result = get_request(url, params)
    

def get_route_number(cityBounds):
    '''
    '''
    TRANSIT_API_KEY = config("TRANSIT_API_KEY")

    url = "https://external.transitapp.com/v3/public/available_networks"
    params = {"apiKey": TRANSIT_API_KEY,
              "minlat": cityBounds["minlat"],
              "maxlat": cityBounds["maxlat"],
              "minlon": cityBounds["minlon"],
              "maxlon": cityBounds["maxlon"],}

    return None


def main():
    cities = {
        "chicago": {
            "minlat": 10,
            "maxlat": 10,
            "minlon": 10,
            "maxlon": 10
        },
        "new-york": {
            "min-lat": 10,
            "max-lat": 10,
            "min-long": 10,
            "max-long": 10
        },
        "detroit": {
            "min-lat": 10,
            "max-lat": 10,
            "min-long": 10,
            "max-long": 10
        },
        "ann arbor": {
            "min-lat": 10,
            "max-lat": 10,
            "min-long": 10,
            "max-long": 10
        },
    }
    get_air_quality()
    get_route_number()

main()









