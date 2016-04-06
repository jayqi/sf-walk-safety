from flask import Flask, render_template, request, redirect
from application import app
from df_to_geojson import *
import pandas as pd
import re

import os
# __file__ refers to the file settings.py
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_DATA = os.path.join(APP_ROOT, 'data')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/robbery_markers")
def robbery_markers_map():
    # Get data from pickle
    df = pd.read_pickle(os.path.join(APP_DATA, 'robbery-street.p'))
    # Apply filters

    # Convert date and time columns to strings
    df['date'] = df['date'].apply(lambda x: x.isoformat())
    df['time'] = df['time'].apply(lambda x: x.strftime("%H:%M"))

    # Columns to pass
    #cols = ['date','time','descript']
    cols = ['address', 'date', 'dayofweek', 'descript', 'time',
            'nhood', 'tractce10', 'police_district', 'hist_police_district']

    # Convert dataframe to geojson js variable
    geojson = df_to_geojson(df, cols, lat='y', lon='x')

    return render_template('map.html',
        title='Robberies &ndash; Individual Incidents',
        maptype='markers',
        data=geojson
        )

@app.route("/robbery_choropleth")
def robbery_choropleth_map():
    # Get data from pickle
    df = pd.read_pickle(os.path.join(APP_DATA, 'robbery-street.p'))

    # Apply filters

    # Groupby and count

    # Columns to pass

    # Convert to geojson js variable
    geojson = geojson_js_var(df_to_geojson(df, cols, lat='y', lon='x'))

    return render_template('map.html',maptype='choropleth',data=geojson)

@app.route("/theft_markers")
def robbery_markers_map():
    # Get data from pickle
    df = pd.read_pickle(os.path.join(APP_DATA, 'robbery-street.p'))
    # Apply filters

    # Convert date and time columns to strings
    df['date'] = df['date'].apply(lambda x: x.isoformat())
    df['time'] = df['time'].apply(lambda x: x.strftime("%H:%M"))

    # Columns to pass
    #cols = ['date','time','descript']
    cols = ['address', 'date', 'dayofweek', 'descript', 'time',
            'nhood', 'tractce10', 'police_district', 'hist_police_district']

    # Convert dataframe to geojson js variable
    geojson = df_to_geojson(df, cols, lat='y', lon='x')

    #geojson = re.sub(r" / ",r" \/ ",geojson)

    return render_template('map.html',
        title='Robberies &ndash; Individual Incidents',
        maptype='markers',
        data=geojson
        )

@app.route("/theft_choropleth")
def robbery_choropleth_map():
    # Get data from pickle
    df = pd.read_pickle(os.path.join(APP_DATA, 'robbery-street.p'))

    # Apply filters

    # Groupby and count

    # Columns to pass

    # Convert to geojson js variable
    geojson = geojson_js_var(df_to_geojson(df, cols, lat='y', lon='x'))

    return render_template('map.html',maptype='choropleth',data=geojson)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
