#!/usr/bin/env python3

from flask import Flask
from flask import render_template, redirect, url_for, request
from flask import session
from dataclasses import dataclass

app = Flask(__name__)

@dataclass
class County:
    name: str
    href: str

@dataclass
class City:
    name: str
    county: str
    href: str

# Read from file
IRELAND_COUNTIES = ['Clare', 'Cork', 'Dublin', 'Galway', 'Kerry']

# Read from file (and rest of the towns)
CORK_TOWNS = '''
Allihies
Ballincollig
Blarney
Cobh
Cork City
Crosshaven
Mallow
Youghal
'''.strip().split('\n')


COUNTIES = [County(name.title(), f'/ireland/{name.lower()}') for name in IRELAND_COUNTIES]

TOWNS = {}
for county in IRELAND_COUNTIES:
    TOWNS[county.lower()] = []

TOWNS['cork'] = CORK_TOWNS

@app.route("/")
def index():
    return render_template('index.html', counties=COUNTIES)

@app.post("/ireland/")
@app.get("/ireland/<county>")
def show_county(county=None):
    if request.method == 'POST':
        county = request.form['selected_county'].split("/")[-1]

    if county in TOWNS:
        cities = [City(city.title(), county.title(), f'/ireland/{county}/{city.lower().replace(" ", "%20")}') for cnty, cities in TOWNS.items() if county == cnty for city in cities]
        return render_template('show_county.html', cities=cities)
    else:
        return redirect(url_for('index'))

@app.get("/ireland/<county>/<city>")
def show_city(county=None, city=None):
    return f"Welcome to {county.title()}'s city {city.title()}"
