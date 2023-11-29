import requests
import json

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
    

def get_air_quality():
    '''
    '''

    return None


def get_route_number():
    '''
    '''

    return None









