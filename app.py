
# Upon visiting the index page at http://127.0.0.1:5000/, the user will be greeted by a page that says hello, and includes an input form that requests a place name.
# Upon clicking the 'Submit' button, the data from the form will be sent via a POST request to the Flask backend at the route POST /nearest
# (Optional) Perform some simple validation on the user input. See wtforms.
# The Flask backend will handle the request to POST /nearest_mbta. Then your app will render a mbta_station page for the user - presenting nearest MBTA stop and whether it is wheelchair accessible. In this step, you need to use the code from Part 1.
# If something is wrong, the app will render a simple error page, which will include some indication that the search did not work, in addition to a button (or link) that will redirect the user back to the home page.


from flask import Flask, render_template, request

from mbta_helper import find_stop_near

app = Flask(__name__, template_folder="templates")

# Upon visiting the index page at http://127.0.0.1:5000/, the user will be greeted by a page that says hello, and includes an input form that requests a place name.
@app.route("/")
def index():
    return render_template("index.html")
    

# @app.route("/find/", methods=["GET","POST"])
# def find():
#     # modify this function so it renders different templates for POST and GET method.
#     # aka. it displays the form when the method is 'GET'; it displays the results when
#     # the method is 'POST' and the data is correctly processed.
#     if request.method == "POST":
#         requestedplace = str(request.form["place"])
#         requestedstop = find_stop_near(requestedplace)
#         if requestedstop:
#             return render_template(
#                 "found.html", requestedstop=requestedstop, requestedplace=requestedplace
#             )
#         else:
#             return render_template("find.html", error=True)
#     return render_template("find.html", error=None)

