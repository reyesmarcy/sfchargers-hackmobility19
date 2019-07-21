import os
import requests
from flask import Flask, render_template, redirect, flash, session, request, jsonify
import jinja2
from flask_debugtoolbar import DebugToolbarExtension
from nrel import *

app = Flask(__name__)

app.secret_key = 'xb2@<4*axd3x7fxb9x9bxdcD&x88x01xe0xd2x9dxdcxcc4nxf3v'


@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("homepage.html")

@app.route("/charging", methods=["GET", "POST"])
def charging():
    """Show homepage"""

    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    print(type(latitude))
    print((latitude,longitude))
    response = get_chargers_by_location(float(latitude),float(longitude))
    print(response["fuel_stations"][0]["latitude"])
    station_list = response["fuel_stations"]
    station_dict = {}
    for station in station_list:
        station_latitude = station['latitude']
        station_longitude = station['longitude']
        station_dict[station_latitude] = station_longitude
        print(station_latitude, station_longitude)
    print(station_dict)
    return jsonify(station_dict)

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host="0.0.0.0")



