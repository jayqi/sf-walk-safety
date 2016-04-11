from flask import Flask, render_template, request, redirect
from application import app
import models

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/robberies/")
def robbery_main():
    return render_template('robberies.html')

@app.route("/robberies/mapmarkers/")
def robbery_markers_map():
    return render_template('map.html',
        title='Robberies &ndash; Individual Incidents',
        maptype='markers',
        data=models.robbery_markers_geojson()
        )

@app.route("/robberies/mapchoropleth/")
def robbery_choropleth_map():
    region_type = 'nhood'
    return render_template('map.html',
        title='Robberies &ndash; Choropleth',
        maptype='choropleth',
        region_type=region_type,
        data=models.robbery_choropleth_geojson(region_type)
        )

@app.route("/theft_markers/")
def theft_markers_map():
    return render_template('map.html',
        title='Theft &ndash; Individual Incidents',
        maptype='markers',
        data=models.robbery_markers_geojson()
        )

@app.route("/theft_choropleth/")
def theft_choropleth_map():
    return render_template('map.html',
        title='Theft &ndash; Choropleth',
        maptype='choropleth',
        data=models.robbery_markers_geojson()
        )



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
