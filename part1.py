import urllib.request
import json
from pprint import pprint

MAPQUEST_API_KEY = "9UevApDckPiKd1cnvkVJL2ZvZcQZNH6z"
MBTA_API_KEY = "c8640baae96c4213b1fd130df032069c"
MAPQUEST_BASE_URL = "http://open.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

### Write a function (maybe two) to extract the latitude and longitude from the JSON response.###
def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode("utf-8")
    response_data = json.loads(response_text)
    return response_data


##### still need to extract lat and long for all data in json?

### Write a function that takes an address or place name as input and returns a properly encoded URL to make a MapQuest geocode request.###
def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    place_name = place_name.replace(" ", "%20")  #gotta find explanation for this
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name}"
    response_data = get_json(url)
    response_latlng = response_data["results"][0]["locations"][0]["displayLatLng"]
    lat = response_latlng["lat"]
    lng = response_latlng["lng"]
    return lat, lng


### Write a function that takes a latitude and longitude and returns the name of the closest MBTA stop and whether it is wheelchair accessible. ###
def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    url_MBTA = f"{MBTA_BASE_URL}?api_key={MBTA_API_KEY}&filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance"
    response_data_MBTA = get_json(url_MBTA)

    try:
        station = response_data_MBTA["data"][0]["attributes"]["name"]
        wheelchair = response_data_MBTA["data"][0]["attributes"]["wheelchair_boarding"]
        return f"Nearest station: {station}, Wheelchair Accessible{wheelchair}"
    except:
        return f"Nearest station: {None}, Wheelchair Accessible{None}"
        #### tbh i dont think this works

### Combine all functions to create a tool that takes a place name or address as input, finds its latitude and longitude, and returns the nearest MBTA stop and whether it is wheelchair accessible
def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    lat, lng = get_lat_long(place_name)
    stop, station_accessible = get_nearest_station(lat, lng)
    if station_accessible == 1:
        station_accessible = "accessible"

    elif station_accessible == 2:
        station_accessible = "inaccessible"

    else:
        station_accessible = "accessibility data unavailable"

    return stop, station_accessible


def main():
    ### for 1 doesnt work idk why print(get_json("http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}"))
    print(get_lat_long("Babson College"))
    print(get_nearest_station(42.29822, -71.2654)) # babson college
    print(find_stop_near("Babson College"))


if __name__ == "__main__":
    main()
