import os
import requests
from flask import Flask, render_template, redirect, flash, session, request, jsonify
import jinja2
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.secret_key = 'xb2@<4*axd3x7fxb9x9bxdcD&x88x01xe0xd2x9dxdcxcc4nxf3v'


@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("homepage.html")

@app.route("/charging", methods=["GET", "POST"])
def charging():
    """Show homepage"""
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    print((latitude,longitude))

    return jsonify(latitude)


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.run(host="0.0.0.0")



