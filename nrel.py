"""National Renewal Energy Laboratory functions."""

import requests
import os

NREL_KEY = os.environ.get("NREL_KEY")
BASE_URI = f"https://developer.nrel.gov/"


def get_nearby_ev_chargers():
    """Test API."""
    response = requests.get(
        (BASE_URI + "/api/alt-fuel-stations/v1/nearest.json"),
        params={
            "api_key": NREL_KEY,
            "location": "94597",  # value is address, city,state, or zip
            # "latitude" : latitude
            # "longitude" : longitude
            "fuel-type": "ELEC",
            "ev-charging_level": ["2", "dc_fast"],
            # "ev_connector_type": ["J1772", "CHADEMO", "J1772COMBO", "TESLA"]
        },
    )
    if response:
        info = response.json()
        return info


# during filtering of location data, filter to find "access_code" : "public"
