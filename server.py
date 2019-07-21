import os
import requests
from flask import Flask, render_template, redirect, flash, session, request, jsonify
import jinja2
from flask_debugtoolbar import DebugToolbarExtension
from nrel import *
from pprint import pprint
import smartcar
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.secret_key = 'xb2@<4*axd3x7fxb9x9bxdcD&x88x01xe0xd2x9dxdcxcc4nxf3v'



access = None
range_left = None
percentRemaining = None


client = smartcar.AuthClient(
    client_id=os.environ.get("CLIENT_ID"),
    client_secret=os.environ.get("CLIENT_SECRET"),
    redirect_uri="http://localhost:5000/exchange",
    scope=['required:read_vehicle_info','required:read_battery'],
    test_mode=True,
)

@app.route('/login', methods=['GET'])
def login():
   
    auth_url = client.get_auth_url()
    return redirect(auth_url)




@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')
    print(code)

    # access our global variable and store our access tokens
    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    print(access)
    # print("ACCESS " + access)
    return '', 200

@app.route('/vehicle', methods=['GET'])
def vehicle():
    # access our global variable to retrieve our access tokens
    global access, range_left, percentRemaining
    print(access)
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']
        
    # instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])
    print("VEHICLE!!")
    print(vehicle)

    # TODO: Request Step 4: Make a request to Smartcar API
    info = vehicle.info()
    battery = vehicle.battery()
    range_left = battery['data']['range']
    percentRemaining = battery['data']['percentRemaining']
    print(range_left)
    print(percentRemaining)
    # print(dir(vehicle.battery))
    # print(vehicle.battery)  
     # for k in battery.keys():
    #     print(k)
    # print(battery['range'])
    # print(vehicle.battery.percentRemaining)
    # print(info)
    '''
    {
        "id": "36ab27d0-fd9d-4455-823a-ce30af709ffc",
        "make": "TESLA",
        "model": "Model S",
        "year": 2014
    }
    '''

    return '', 200


@app.route("/")
def homepage():
    """Show homepage"""
    print("HOMEPAGE")
    print(range_left)

    return render_template("homepage.html", range_left=range_left, percentRemaining=percentRemaining)

@app.route("/charging", methods=["GET", "POST"])
def charging():
    """Show homepage"""

    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    print(type(latitude))
    print((latitude,longitude))
    response = get_chargers_by_location(float(latitude),float(longitude))
    print(response["fuel_stations"][0]["latitude"])
    pprint(response)
    
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



