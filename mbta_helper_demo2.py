
import json
import urllib.request
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "3Jf1vAlPW2aUKudf7Qq8AbXuBYatwVEy"
MBTA_API_KEY = "f80c2ca258714f04a7b7072cb81d4656"


# A little bit of scaffolding if you want to use it
def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    We did similar thing in the previous assignment.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding API URL formatting requirements.
    """
    place = place_name.replace(' ', '%20')
    url = f'{MAPQUEST_BASE_URL}?key={MAPQUEST_API_KEY}&location={place}'
    #print(url) # uncomment to test the url in browser
    place_json = get_json(url)
    lat = place_json['results'][0]['locations'][0]['latLng']['lat'] # modify this so you get the correct latitude
    lon = place_json['results'][0]['locations'][0]['latLng']['lng'] # modify this so you get the correct longitude
  
    return lat, lon


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """

    url = f'{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance'
    # print(url) # uncomment to test the url in browser
    station_json = get_json(url)
    #pprint(station_json) # uncomment to see the json data
    station_name = station_json['data'][0]['attributes']['name'] # modify this so you get the correct station name
    #print(station_name) # uncomment to check it

    # try to find out where the wheelchair_boarding information is
    wheelchair_boarding = station_json['data'][0]['attributes']['wheelchair_boarding']
    if wheelchair_boarding == 1:
        wheelchair_boarding = 'Accessible'
    elif wheelchair_boarding == 0:
        wheelchair_boarding = 'No Information'
    else:
        wheelchair_boarding = 'Inaccessible'
    return station_name, wheelchair_boarding


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    You don't need to modify this function
    """
    return get_nearest_station(*get_lat_long(place_name))


def main():
    # final test here
    place = input('Enter a place name in Boston such as "Fenway Park": ')
    #lat, lon = get_lat_long(place)
    #print(lat, lon)
    #print(get_nearest_station(lat, lon))

    # final wrap-up
    print(find_stop_near(place))


if __name__ == '__main__':
    main()
   