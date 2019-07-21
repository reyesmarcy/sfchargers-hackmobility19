"""National Renewal Energy Laboratory functions."""

from pprint import pprint
import requests
import os

NREL_KEY = os.environ.get("NREL_KEY")
BASE_URI = f"https://developer.nrel.gov/"


class chargeStation:
    """Charge Station Information Object."""

    def __init__(
        self,
        station_name,
        street_address,
        city,
        state,
        zip,
        ev_connector_types,
        pricing,
        latitude,
        longitude,
    ):
        """Initialize object with given values."""
        self.station_name = station_name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.ev_connector_types = ev_connector_types
        self.pricing = ev_pricing
        self.latitude = latitude
        self.longitude = longitude


def get_chargers_by_location(latitude, longitude):
    """Get EV Chargers API."""
    response = requests.get(
        (BASE_URI + "/api/alt-fuel-stations/v1/nearest.json"),
        params={
            "api_key": NREL_KEY,
            # "location": location,  # value is address, city,state, or zip
            "latitude": latitude,
            "longitude": longitude,
            "fuel-type": "ELEC",
            "ev-charging_level": ["2", "dc_fast"],
            # "ev_connector_type": ["J1772", "CHADEMO", "J1772COMBO", "TESLA"]
        },
    )
    if response:
        all_stations = response.json()
        return all_stations


def get_chargers_by_route(linestring):
    """Return chargers near route."""
    response = requests.get(
        (BASE_URI + "/api/alt-fuel-stations/v1/nearby-route.json"),
        params={
            "api_key": NREL_KEY,
            "route": linestring,
            "fuel-type": "ELEC",
            "ev-charging_level": ["2", "dc_fast"],
            # "ev_connector_type": ["J1772", "CHADEMO", "J1772COMBO", "TESLA"]
        },
    )
    if response:
        all_stations = response.json()
        return all_stations
    else:
        print(response)


# def filter_chargers(all_stations):
#     """Filter charging stations."""
#     params = {"access_code": "public", "status_code": "e"}
#     station_data = [
#         station_name,
#         street_address,
#         city,
#         state,
#         zip_code,
#         ev_connector_types,
#         pricing,
#         latitude,
#         longitude,
#     ]
#     filtered_stations = []
#     for station in all_stations:
#         for key, val in param.items():
#             if station[key] == value:
#                 filtered_station = chargeStation(
#                     station_name,
#                     street_address,
#                     city,
#                     state,
#                     zip_code,
#                     ev_connector_types,
#                     pricing,
#                     latitude,
#                     longitude,
#                 )
