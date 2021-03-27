
from flask import Flask, render_template, request

from mbta_helper import find_stop_near

app = Flask(__name__, template_folder="templates")

# Upon visiting the index page at http://127.0.0.1:5000/, the user will be greeted by a page that says hello, and includes an input form that requests a place name.
@app.route("/")
def index():
    return render_template("index.html")

# Upon clicking the 'Submit' button, the data from the form will be sent via a POST request to the Flask backend at the route POST /nearest
# The Flask backend will handle the request to POST /nearest_mbta. Then your app will render a mbta_station page for the user - presenting nearest MBTA stop and whether it is wheelchair accessible. In this step, you need to use the code from Part 1.
# If something is wrong, the app will render a simple error page, which will include some indication that the search did not work, in addition to a button (or link) that will redirect the user back to the home page.

@app.route("/POST/nearest", methods=["POST","GET"])
def find():
    if request.method == "POST":
        requestedplace = str(request.form["location"])
        requestedstop = find_stop_near(requestedplace)
        if requestedstop != (None, None):
            return render_template(
                "found.html", 
                requestedstop=requestedstop[0], requestedplace=requestedplace,
                wheelchair=requestedstop[1]
            )
        elif requestedstop == (None, None):
            return render_template("notfound.html")
        else:
            return render_template("index.html", error=True)
    return render_template("index.html", error=None)


if __name__ == "__main__":
    app.run(debug=True)
