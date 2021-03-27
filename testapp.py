  
from flask import Flask, render_template, request

from mbta_helper import find_stop_near

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["POST"])
def find():
    # modify this function so it renders different templates for POST and GET method.
    # aka. it displays the form when the method is 'GET'; it displays the results when
    # the method is 'POST' and the data is correctly processed.
    if request.method == "POST":
        requestedplace = str(request.form["place"])
        requestedstop = find_stop_near(requestedplace)
        if requestedstop:
            return render_template(
                "testfound.html", requestedstop=requestedstop, requestedplace=requestedplace
            )
        else:
            return render_template("testfind.html", error=True)
    return render_template("testfind.html", error=None)