from flask import Flask, render_template, request, redirect
from application import app
import models

#from bokeh.embed import components

@app.route("/")
def index():
    return render_template('index.html')

##############################################
################### THEFTS ###################
##############################################

@app.route("/thefts/")
def theft_main():
    return render_template('thefts.html')

@app.route("/thefts/mapmarkers/")
def theft_markers_map():
    return render_template('map.html',
        title='Theft &ndash; Individual Incidents Map',
        maptype='markers',
        data=models.markers_geojson(app.df_thefts)
        )

@app.route("/thefts/mapchoropleth/")
def theft_choropleth_map():
    region_type = 'nhood'
    return render_template('map.html',
        title='Theft &ndash; Choropleth Map',
        maptype='choropleth',
        region_type=region_type,
        data=models.choropleth_geojson(app.df_thefts,region_type)
        )


###############################################
################## ROBBERIES ##################
###############################################
@app.route("/robberies/")
def robbery_main():
    return render_template('robberies.html')

@app.route("/robberies/mapmarkers/")
def robbery_markers_map():
    return render_template('map.html',
        title='Robberies &ndash; Individual Incidents Map',
        maptype='markers',
        data=models.markers_geojson(app.df_robberies)
        )

@app.route("/robberies/mapchoropleth/")
def robbery_choropleth_map():
    region_type = 'nhood'
    return render_template('map.html',
        title='Robberies &ndash; Choropleth Map',
        maptype='choropleth',
        region_type=region_type,
        data=models.choropleth_geojson(app.df_robberies,region_type)
        )

########################################################
################## TRAFFIC COLLISIONS ##################
########################################################

@app.route("/trafficcollisions/")
def traffic_collision_main():
    return render_template('trafficcollisions.html')




###############################################
#################### OTHER ####################
###############################################

@app.route("/highlights/")
def highlights():
    return render_template('highlights.html')

@app.route("/aboutdata/")
def aboutdata():
    return render_template('aboutdata.html')

@app.route("/resources/")
def resources():
    return render_template('resources.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
