  import urllib.request
import json
from pprint import pprint

MAPQUEST_API_KEY = '9UevApDckPiKd1cnvkVJL2ZvZcQZNH6z'

url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location=Babson%20College'
f = urllib.request.urlopen(url)
response_text = f.read().decode('utf-8')
response_data = json.loads(response_text)
pprint(response_data)

##########

from flask import Flask, render_template, request

from mbta_helper import find_stop_near


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mbta_helper/", methods=["GET", "POST"])

def get_stop():
    if request.method == "POST":
        place_name = str(request.form["location"])
        stop, is_accessible = find_stop_near(place_name)
        accessibility = ""
        if stop:
            if is_accessible == "accessible":
                accessibility = "The station is accessible to wheelchairs"
            elif is_accessible == "inaccessible":
                accessibility = "The station is not accessible to wheelchairs"
            else:
                accessibility = "The station does not have accessibility data available"
            return render_template("mbta_results.html", place_name=place_name, stop=stop, accessibility=accessibility)
        else:
            return render_template("mbta_helper.html", error=True)
    return render_template("mbta_helper.html", error=None)