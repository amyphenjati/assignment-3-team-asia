import urllib.request
import json
from pprint import pprint

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
MAPQUEST_API_KEY = "9UevApDckPiKd1cnvkVJL2ZvZcQZNH6z"
MBTA_API_KEY = "043b2649493e4aa08ceaf24ad0743cf4"  # c8640baae96c4213b1fd130df032069c


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode("utf-8")
    response_data = json.loads(response_text)
    return response_data


### Write a function (maybe two) to extract the latitude and longitude from the JSON response.###
### Write a function that takes place name as input and returns a properly encoded URL to make a MapQuest geocode request.###
def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    place = place_name.replace(" ", "%20")  # replace space with %20
    place = place + "," + "MA"
    url = f"{MAPQUEST_BASE_URL}?key={MAPQUEST_API_KEY}&location={place}"
    # print(url) # print ecoded URL with the location inputed

    place_data = get_json(url)  # get data from mapquest api
    # print(place_data)
    data_latlng = place_data["results"][0]["locations"][0]["displayLatLng"]
    # print(data_latlng)
    lat = data_latlng["lat"]
    lng = data_latlng["lng"]
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
        name, wheel_chair = (
            response_data_MBTA["data"][0]["attributes"]["name"],
            response_data_MBTA["data"][0]["attributes"]["wheelchair_boarding"],
        )
    except:
        return None, None
    if wheel_chair == 2:
        wheel_chair = "Inaccessible"
    elif wheel_chair == 1:
        wheel_chair = "Accessible"
    else:
        wheel_chair = "No Information"
    return name, wheel_chair


### Combine all functions to create a tool that takes a place name or address as input, finds its latitude and longitude, and returns the nearest MBTA stop and whether it is wheelchair accessible ###
def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    lat_long_data = get_lat_long(place_name)
    return get_nearest_station(*lat_long_data)


def main():
    """
    You can test all the functions here
    """
    # url = f"{MAPQUEST_BASE_URL}?key={MAPQUEST_API_KEY}&location=Babson%20College"
    # pprint(get_json(url))

    location = input("Please enter a place:")
    # print(get_lat_long(location))
    # pprint(get_nearest_station(42.34461, -71.10411)) # fenway park

    print(find_stop_near(location))
    # print(find_stop_near("Boston Common"))


if __name__ == "__main__":
    main()
